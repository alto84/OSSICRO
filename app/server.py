"""OSSICRO MVP backend — Route-3926 single-patient expanded access.

Pure Python 3 stdlib (http.server). Starts with:

    python app/server.py

and listens on 127.0.0.1:8765. Disk-backed case store at app/data/cases/{id}.json
(no real PHI; coded identifiers only). Serves the frontend at ``/`` and the
SHARED API CONTRACT:

    GET  /api/route/3926/schema
    POST /api/case
    GET  /api/case/{id}                 -> {intake, signoffs, intake_rev, generated_rev}
    POST /api/case/{id}/intake          -> {ok, intake_rev}
    POST /api/case/{id}/generate        -> {route_id, documents, generated_rev, intake_rev}
                                           (INV-3 hard gate: 409 {error, pending, state}
                                           unless a named human committed the profile
                                           and the intake still matches its hash;
                                           /package gated identically)
    GET  /api/case/{id}/check           -> ledger (questions as {text,field_id}), clocks, stale, ...
    POST /api/case/{id}/signoff         -> record a human gate act (role must match the gate)
    POST /api/case/{id}/profile/commit  -> {actor}: named human commits the intake profile
                                           (INV-3; hashes only, never values — INV-8)
    POST /api/case/{id}/profile/confirm -> {actor, field_ids}: named per-field re-confirmation;
                                           draining pending auto-recommits (new hash)
    POST /api/case/{id}/fhir/import     -> {proposals, never_extracted, summary}
                                           ({bundle:{...}} or {use_sample:true};
                                           MAPS ONLY — never writes intake)
    GET  /api/case/{id}/package         -> manifest over ALL route documents + package digest

The backend imports the engine (models / generate / pipeline / gates / routes /
ea_generators / assemble). It drafts, checks, and assembles; it never performs a
non-delegable act — the gates fail closed in the engine (GateViolation). A
sign-off POSTed here only RECORDS that a named human performed the act outside
OSSICRO; the engine's has_signoff path is what moves amber to green.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import sys
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# --- wire in the engine -----------------------------------------------------
APP_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(APP_DIR)
ENGINE_DIR = os.path.join(REPO_ROOT, "engine")
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

from ossicro import routes as routes_mod                     # noqa: E402
from ossicro.assemble import assemble_submission             # noqa: E402
from ossicro.clocks import working_days_between                  # noqa: E402
from ossicro.ea_generators import (                              # noqa: E402
    TriggerDateError,
    build_study,
    compute_clocks,
    generate_route_documents,
)
from ossicro.fhir_ingest import (                                # noqa: E402
    BundleError,
    bundle_sha256,
    extract_proposals,
)
from ossicro.gates import record_signoff as gates_record_signoff  # noqa: E402
from ossicro.models import GateViolation                     # noqa: E402
from ossicro.pipeline import run_check                       # noqa: E402
from ossicro.profile import (                                # noqa: E402
    ProfileNotCommitted,
    commit_profile,
    confirm_fields,
    pending_fields,
    profile_hash,
    require_committed,
    stamp_input_hash,
)
from ossicro.registry import load_documents, load_gates      # noqa: E402
from ossicro.review_port import DeterministicStubReviewer    # noqa: E402

STATIC_DIR = os.path.join(APP_DIR, "static")
FIXTURES_DIR = os.path.join(ENGINE_DIR, "fixtures")
SAMPLE_CASE_PATH = os.path.join(FIXTURES_DIR, "ea_sample_case.json")
SAMPLE_BUNDLE_PATH = os.path.join(FIXTURES_DIR, "fhir_sample_bundle.json")
CASES_DIR = os.path.join(APP_DIR, "data", "cases")
HOST, PORT = "127.0.0.1", 8765

# Registries loaded once.
DOC_REGISTRY = load_documents()
GATE_REGISTRY = load_gates()

# Intake schema, indexed by dotted field id.
SCHEMA_FIELDS = {f["id"]: f for f in routes_mod.intake_fields()}

_CASE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{4,64}$")
_LOCK = threading.Lock()

# Disk-backed case store (loaded at startup; every mutation persists).
CASES: dict = {}


# ---------------------------------------------------------------------------
# Case persistence (app/data/cases/{id}.json — no real PHI)
# ---------------------------------------------------------------------------

def _new_case() -> dict:
    return {"intake": {}, "route_id": "route-3926", "signoffs": [],
            "intake_rev": 0, "generated_rev": None,
            # Durable, named confirmation trail (review B3 / HC5): who confirmed
            # which fields, when, and whether the value came from the chart. This
            # persists in the case JSON, so a chart-confirmed value stays
            # distinguishable from a hand-typed one across a page reload.
            "confirmations": [], "field_provenance": {},
            # INV-3: the committed profile (input-of-record). None = UNCOMMITTED
            # — every legacy case loads UNCOMMITTED via _normalize_case; no
            # auto-commit, ever (a synthesized commit would be software
            # performing the named-human act). generated_hash is the committed
            # profile hash consumed by the last /generate (hash authority for
            # staleness; the rev counters stay as display metadata).
            "committed_profile": None, "generated_hash": None}


def _normalize_case(case: dict) -> dict:
    base = _new_case()
    for key, default in base.items():
        case.setdefault(key, default)
    return case


def _case_path(case_id: str) -> str:
    return os.path.join(CASES_DIR, case_id + ".json")


def _save_case(case_id: str) -> None:
    """Atomic write: tmp file + os.replace so a crash never truncates a case."""
    os.makedirs(CASES_DIR, exist_ok=True)
    path = _case_path(case_id)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(CASES[case_id], f, indent=1, sort_keys=True)
    os.replace(tmp, path)


def _load_cases() -> None:
    if not os.path.isdir(CASES_DIR):
        return
    for name in os.listdir(CASES_DIR):
        if not name.endswith(".json"):
            continue
        case_id = name[:-len(".json")]
        if not _CASE_ID_RE.match(case_id):
            continue
        try:
            with open(os.path.join(CASES_DIR, name), encoding="utf-8") as f:
                CASES[case_id] = _normalize_case(json.load(f))
        except (ValueError, OSError) as exc:
            sys.stderr.write("[ossicro] skipping unreadable case %s: %s\n" % (name, exc))


def _get_case(case_id: str):
    if not _CASE_ID_RE.match(case_id or ""):
        return None
    case = CASES.get(case_id)
    if case is None and os.path.isfile(_case_path(case_id)):
        try:
            with open(_case_path(case_id), encoding="utf-8") as f:
                case = _normalize_case(json.load(f))
            CASES[case_id] = case
        except (ValueError, OSError):
            return None
    return case


# ---------------------------------------------------------------------------
# Engine wiring per case
# ---------------------------------------------------------------------------

def _route_for(case: dict) -> dict:
    emergency = str(case["intake"].get("submission.emergency", "")).strip().lower() in ("true", "1", "yes")
    return routes_mod.route_for_emergency(emergency)


def _apply_signoffs(case: dict, documents: dict) -> None:
    """Re-apply the case's persisted human sign-offs to freshly generated docs.

    Goes through the engine's ``gates.record_signoff`` so role-vs-gate
    enforcement is never bypassed; a stored record that no longer matches its
    document's gate is skipped (it can never clear a gate it doesn't fit).
    The signoff only RECORDS the human act — the engine's existing
    ``has_signoff`` path is what turns amber to green in the ledger.
    """
    for so in case.get("signoffs", []):
        doc = documents.get(so.get("doc_id"))
        if doc is None or doc.gate_id != so.get("gate_id") or doc.has_signoff(doc.gate_id):
            continue
        statement = (
            "Recorded human act: %s (%s) performed this act outside OSSICRO on %s. "
            "OSSICRO records that it happened; it did not perform it."
            % (so.get("signer_name", ""), so.get("role", ""), so.get("date", ""))
        )
        try:
            gates_record_signoff(doc, GATE_REGISTRY, so.get("signer_name", ""),
                                 so.get("role", ""), statement,
                                 timestamp=so.get("date") or None)
        except GateViolation:
            continue


def _study_and_docs(case: dict, intake: dict | None = None):
    # B1: callers on the gated paths pass a snapshot so the gate check, the
    # build, and the hash stamp all consume the SAME input even if another
    # request mutates case["intake"] concurrently (GET /package and /check run
    # outside _LOCK). Default to the live dict for the non-gated callers.
    intake = case["intake"] if intake is None else intake
    route = _route_for(case)
    study = build_study(intake, route)
    documents = generate_route_documents(study, route, DOC_REGISTRY)
    _apply_signoffs(case, documents)
    return route, study, documents


def _schema_payload() -> dict:
    return {"fields": routes_mod.intake_fields()}


def _sample_payload() -> dict:
    """A realistic, complete synthetic EA case (no real PHI).

    Loaded from engine/fixtures/ea_sample_case.json and returned as
    ``{"fields": {<id>: <value>, ...}}``. POSTing these fields to intake yields
    a mostly-green ledger with submission_ready true — only the non-delegable
    human-gate ambers remain pending.
    """
    with open(SAMPLE_CASE_PATH, encoding="utf-8") as f:
        data = json.load(f)
    fields = data.get("fields", data)
    return {"fields": fields}


def _select_reviewer():
    """Pick the concept reviewer per the shared contract.

    Live Claude reviewer when ANTHROPIC_API_KEY is set; otherwise (or if the
    SDK is missing) the offline deterministic stub. The escalate-only coupling
    that keeps a concept finding from ever clearing a gate lives in the
    pipeline, not here — either reviewer is safe.
    """
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            from ossicro.review_claude import ClaudeConceptReviewer
            return ClaudeConceptReviewer.from_anthropic()
        except Exception:  # missing SDK / bad key -> honest offline fallback
            return DeterministicStubReviewer()
    return DeterministicStubReviewer()


# ---------------------------------------------------------------------------
# Ledger question -> intake field mapping (for the frontend fix-loop)
#
# Derived from the engine itself, not duplicated by hand: the built-in
# generators export FIELD_SOURCES, and the EA generators stamp every filled
# span with a ProvenanceRecord whose source is "<dotted.path> = <value>" —
# rendering the synthetic sample case once at startup harvests span -> path
# for every EA template placeholder.
# ---------------------------------------------------------------------------

def _build_span_to_field() -> dict:
    span_to_path: dict = {}
    # EA generators first — their spans are what Route-3926 ledger questions name.
    try:
        sample = _sample_payload()["fields"]
        for emergency in (False, True):
            route = routes_mod.route_for_emergency(emergency)
            study = build_study(dict(sample), route)
            for doc in generate_route_documents(study, route, DOC_REGISTRY).values():
                for rec in doc.provenance:
                    if " = " in rec.source:
                        span_to_path.setdefault(rec.span, rec.source.split(" = ", 1)[0].strip())
    except Exception as exc:  # sample fixture problems must not kill the server
        sys.stderr.write("[ossicro] span-map harvest incomplete: %s\n" % exc)
    # Built-in generators (ICF etc.) fill anything the EA pass didn't claim.
    try:
        from ossicro.generate import FIELD_SOURCES
        for field_map in FIELD_SOURCES.values():
            for span, (path, _citation) in field_map.items():
                span_to_path.setdefault(span, path)
    except ImportError:  # pragma: no cover
        pass
    return span_to_path


SPAN_TO_FIELD = _build_span_to_field()

_Q_PROVIDE = re.compile(r"^Provide '([^']+)'")
_Q_DIFFERS = re.compile(r"^'([^']+)' differs")


def _field_id_for_question(text: str):
    """Map a ledger question to the intake field that resolves it, or None."""
    m = _Q_PROVIDE.match(text) or _Q_DIFFERS.match(text)
    if not m:
        return None
    span = m.group(1)
    path = SPAN_TO_FIELD.get(span)
    if path in SCHEMA_FIELDS:
        return path
    if span in SCHEMA_FIELDS:
        return span
    return None


def _question_obj(text: str) -> dict:
    return {"text": text, "field_id": _field_id_for_question(text)}


# ---------------------------------------------------------------------------
# Clocks (contract shape). The engine computes them (physician-entered trigger
# dates only; absent trigger = UNARMED, never date.today(); unparseable =
# TriggerDateError surfaced to the user). This adapter maps the engine's
# clock dicts onto the contract keys and adds the DISPLAY-ONLY
# days-remaining-vs-today the CHECK screen shows.
# ---------------------------------------------------------------------------

def _clock_entries(study, route) -> list:
    today = datetime.date.today()  # display-only: how far away is the deadline NOW
    entries = []
    for c in compute_clocks(study, route):   # raises TriggerDateError on bad input
        trigger_field = c["trigger_field"]
        label = SCHEMA_FIELDS.get(trigger_field, {}).get("label", trigger_field)
        working = c["calendar"] == "working"
        basis = "working-day" if working else "calendar-day"
        days_remaining = None
        if c["armed"]:
            due = datetime.datetime.strptime(c["deadline"], "%Y-%m-%d").date()
            days_remaining = working_days_between(today, due) if working else (due - today).days
        resolving_question = None
        if not c["armed"]:
            resolving_question = (
                "Enter the %s so OSSICRO can compute the %d-%s deadline (%s)."
                % (label, c["days"], basis, c["basis"])
            )
        entries.append({
            "id": c["id"],
            "name": c["label"],
            "citation": c["basis"],
            "basis": basis,
            "days": c["days"],
            "owner": c.get("owner", ""),
            "note": c.get("note", ""),
            "trigger_field": trigger_field,
            "trigger": c["trigger_value"],
            "deadline": c["deadline"],
            "armed": c["armed"],
            "days_remaining": days_remaining,
            "resolving_question": resolving_question,
            "error": None,
        })
    return entries


def _is_stale(case: dict) -> bool:
    """Hash authority (INV-3 §6): staleness = drift from the committed hash.

    Subsumes the rev counters: every case the old counter rule called stale
    the hash rule also calls stale, plus it un-stales the revert-to-committed
    case and stales the never-committed / drifted-from-commit cases. The
    legacy fallback branch keeps pre-INV-3 cases byte-identical.
    """
    cp = case.get("committed_profile")
    if case.get("generated_hash"):                     # post-INV-3 generation
        return (cp is None
                or case["generated_hash"] != cp["profile_hash"]
                or profile_hash(case["intake"]) != cp["profile_hash"])
    return (case.get("generated_rev") is not None      # legacy fallback, verbatim
            and case["generated_rev"] != case["intake_rev"])


def _profile_block(case: dict) -> dict:
    """The derived profile state (never stored — unrepresentable drift)."""
    cp = case.get("committed_profile")
    if cp is None:
        return {"state": "UNCOMMITTED", "profile_hash": None, "pending": [],
                "committed_by": None, "committed_at": None}
    pending = pending_fields(case["intake"], cp)
    committed = (not pending
                 and profile_hash(case["intake"]) == cp.get("profile_hash"))
    # M1: a reachable state — all changed fields staged/reverted so pending is
    # empty, yet the hash still differs from the commit (a stale commit). The
    # refusal must always name a next action; here it is a plain recommit.
    recommit_needed = (not committed) and (not pending)
    return {"state": "COMMITTED" if committed else "CONFIRMING",
            "profile_hash": cp.get("profile_hash"),
            "pending": pending,
            "recommit_needed": recommit_needed,
            "committed_by": cp.get("committed_by"),
            "committed_at": cp.get("committed_at")}


# ---------------------------------------------------------------------------
# Payload builders
# ---------------------------------------------------------------------------

def _generate_payload(case: dict) -> dict:
    # INV-3 hard gate: the deliverable path never runs on an unconfirmed
    # input. require_committed raises ProfileNotCommitted (-> 409, fail
    # closed) unless the current intake's hash equals the committed hash.
    intake = dict(case["intake"])   # B1: one snapshot for gate + build + stamp
    committed_hash = require_committed(intake, case.get("committed_profile"))
    route, study, documents = _study_and_docs(case, intake)
    # On this path the consumed hash IS the committed hash (by the gate).
    stamp_input_hash(documents, committed_hash)
    case["route_id"] = route["route_id"]
    case["generated_rev"] = case["intake_rev"]
    case["generated_hash"] = committed_hash
    ordered = [d for d in route["documents"] if d in documents]
    return {
        "route_id": route["route_id"],
        "documents": [
            {"doc_id": d, "title": documents[d].title, "rendered": documents[d].rendered}
            for d in ordered
        ],
        "intake_rev": case["intake_rev"],
        "generated_rev": case["generated_rev"],
        "profile": _profile_block(case),
    }


_GATES_REGISTRY_SPEAK = "see gates registry"


def _ledger_question_objs(item) -> list:
    """Ledger questions as {text, field_id}; engine-speak replaced with the
    plain-language responsible role."""
    out = []
    for q in item.questions:
        if _GATES_REGISTRY_SPEAK in q and item.gate_id:
            gate = GATE_REGISTRY.get(item.gate_id)
            if gate is not None:
                q = (
                    "Awaiting a human act performed outside OSSICRO: %s. The %s "
                    "must perform it (%s); once done, record the sign-off here. "
                    "OSSICRO cannot and will not perform this step."
                    % (gate.name, gate.responsible_role.replace("-", " "), gate.citation)
                )
        out.append(_question_obj(q))
    return out


_PROFILE_ADVISORY = (
    "Sign-off predates a profile change — confirm it still applies or "
    "re-execute the act (INV-3 §6.1)."
)


def _check_payload(case: dict) -> dict:
    intake = dict(case["intake"])   # B1: snapshot so the stamped hash matches what was built
    route, study, documents = _study_and_docs(case, intake)
    # /check runs in EVERY profile state (it is the repair loop) and stamps
    # the TRUE consumed-input hash — recomputed from the intake actually
    # consumed, never the committed hash (INV-3 §6 honesty rule).
    consumed_hash = profile_hash(intake)
    stamp_input_hash(documents, consumed_hash)
    profile = _profile_block(case)
    cp = case.get("committed_profile")
    committed_hash_now = cp.get("profile_hash") if cp else None
    signoff_by_key = {(s.get("gate_id"), s.get("doc_id")): s
                      for s in case.get("signoffs", [])}
    reviewer = _select_reviewer()
    result = run_check(study, documents, DOC_REGISTRY, GATE_REGISTRY, reviewer=reviewer)
    totals = {"green": 0, "amber": 0, "red": 0}
    ledger = []
    for item in result.ledger:
        totals[item.status] = totals.get(item.status, 0) + 1
        notes = list(item.notes)
        # §6.1 advisory (escalate-only: a note, never a demotion or a
        # promotion): a green/amber gated item whose recorded sign-off
        # carries a committed-profile hash that differs from the CURRENT
        # committed hash predates a profile change. Legacy sign-offs with
        # no recorded hash are exempt (can't compare what was never
        # recorded — honest absence).
        if item.status in ("green", "amber") and item.gate_id:
            so = signoff_by_key.get((item.gate_id, item.doc_id))
            so_hash = (so or {}).get("input_hash") or ""
            if so_hash and committed_hash_now and so_hash != committed_hash_now:
                notes.append(_PROFILE_ADVISORY)
        ledger.append({
            "doc_id": item.doc_id,
            "title": item.title,
            "status": item.status,
            "gate_id": item.gate_id,
            "questions": _ledger_question_objs(item),
            "notes": notes,
        })
    # App-level resolving question (INV-3 §6): injected HERE, never in the
    # engine pipeline — the engine's escalate-only layers stay untouched,
    # and this can only add, never clear.
    if profile["state"] != "COMMITTED":
        if profile["state"] == "CONFIRMING":
            q = ("Profile changed since commit — a named clinician must "
                 "re-confirm before generation: %s (INV-3)."
                 % ", ".join(profile["pending"]))
        else:
            q = ("Profile not committed — a named clinician must commit the "
                 "intake profile before generation (INV-3 / HC1).")
        totals["red"] = totals.get("red", 0) + 1
        ledger.insert(0, {
            "doc_id": "committed-profile",
            "title": "Committed profile (input-of-record)",
            "status": "red",
            "gate_id": None,
            "questions": [{"text": q, "field_id": None}],
            "notes": [],
        })
    consistency = [
        {
            "field_name": f.field_name,
            "reference_value": f.reference_value,
            "observed": f.observed,
            "question": f.question,
        }
        for f in result.inconsistencies
    ]
    gate_packet = []
    for pg in result.gate_packet:
        doc_ids = pg.doc_ids or [None]
        for doc_id in doc_ids:
            gate_packet.append({
                "gate_id": pg.gate_id,
                "name": pg.name,
                "responsible_role": pg.responsible_role,
                "citation": pg.citation,
                "doc_id": doc_id,
                "questions": pg.questions,
            })
    concept_by_doc = {}
    for doc_id, report in result.concept_by_doc.items():
        concept_by_doc[doc_id] = [
            {
                "principle_id": f.principle_id,
                "severity": f.severity,
                "span": f.span,
                "message": f.message,
                "suggestion": f.suggestion,
            }
            for f in report.findings
        ]
    signed = {(s.get("gate_id"), s.get("doc_id")): s for s in case.get("signoffs", [])}
    return {
        "ledger": ledger,
        "totals": totals,
        "consistency": consistency,
        "gate_packet": gate_packet,
        "concept_by_doc": concept_by_doc,
        "reviewer": {"model": getattr(reviewer, "model", "unknown")},
        "clocks": _clock_entries(study, route),
        "stale": _is_stale(case),
        "intake_rev": case["intake_rev"],
        "generated_rev": case["generated_rev"],
        "signoffs": list(signed.values()),
        "profile": profile,
    }


def _package_payload(case: dict) -> dict:
    # INV-3 hard gate: same fail-closed rule as /generate — no package over
    # an unconfirmed input. Raises ProfileNotCommitted (-> 409).
    intake = dict(case["intake"])   # B1: snapshot — GET /package runs outside _LOCK
    committed_hash = require_committed(intake, case.get("committed_profile"))
    route, study, documents = _study_and_docs(case, intake)
    stamp_input_hash(documents, committed_hash)  # consumed == committed (gated)
    # The engine's assemble pass owns the contract manifest: every route
    # document hashed (SHA-256 over rendered utf-8, verifier-compatible),
    # explicit ABSENT entries for anything missing, plus the package-level
    # digest over the sorted per-doc hashes, and as_of-anchored clocks.
    pkg = assemble_submission(study, documents, route, DOC_REGISTRY, GATE_REGISTRY,
                              reviewer=_select_reviewer())
    pkg["stale"] = _is_stale(case)
    pkg["profile"] = _profile_block(case)
    return pkg


def _record_signoff(case: dict, payload: dict):
    """Validate and persist a human sign-off record. Returns (obj, err, status)."""
    gate_id = str(payload.get("gate_id", "")).strip()
    doc_id = str(payload.get("doc_id", "")).strip()
    signer = str(payload.get("signer_name", "")).strip()
    role = str(payload.get("role", "")).strip()
    date = str(payload.get("date", "")).strip()

    gate = GATE_REGISTRY.get(gate_id)
    if gate is None:
        return None, "unknown gate_id %r" % gate_id, 400
    entry = DOC_REGISTRY.get(doc_id)
    if entry is None:
        return None, "unknown doc_id %r" % doc_id, 400
    if entry.get("gate") != gate_id:
        return None, "document %r is not gated by %r" % (doc_id, gate_id), 400
    if not signer:
        return None, "signer_name is required — a gate is executed by a named human", 400
    if role != gate.responsible_role:
        return None, ("role %r cannot execute gate %r — it belongs to the %s (%s)"
                      % (role, gate_id, gate.responsible_role, gate.citation)), 400
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return None, "date must be YYYY-MM-DD (the date the human act was performed)", 400

    cp = case.get("committed_profile")
    record = {"gate_id": gate_id, "doc_id": doc_id, "signer_name": signer,
              "role": role, "date": date,
              # INV-3 §6.1: the committed profile hash at signoff time ("" when
              # no commit exists yet — legacy-compatible honest absence), so a
              # later profile change can surface the advisory note in /check.
              "input_hash": (cp or {}).get("profile_hash") or "",
              "recorded_at": datetime.datetime.now(datetime.timezone.utc)
              .strftime("%Y-%m-%dT%H:%M:%SZ")}
    signoffs = [s for s in case.get("signoffs", [])
                if not (s.get("gate_id") == gate_id and s.get("doc_id") == doc_id)]
    signoffs.append(record)
    case["signoffs"] = signoffs
    return record, None, 200


# ---------------------------------------------------------------------------
# INV-3 profile commit / confirm (attribution, NOT a gate sign-off — never
# routed through gates.record_signoff). Returns (body, status); callers hold
# _LOCK and persist.
# ---------------------------------------------------------------------------

def _utcnow_z() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _append_confirmation(case: dict, actor: str, action: str, field_ids: list) -> None:
    """One attribution trail, not two: commit/reconfirm land in the existing
    confirmations trail with an ``action`` key (design §5.3)."""
    case.setdefault("confirmations", []).append({
        "actor": actor,
        "action": action,
        "field_ids": sorted(field_ids),
        "from_chart": [],
        "at": _utcnow_z(),
    })


def _profile_commit(case: dict, payload: dict):
    """POST /api/case/{id}/profile/commit {actor} -> (body, status)."""
    actor = str(payload.get("actor", "")).strip()
    if not actor:
        return {"error": "actor is required — the profile is committed by a "
                         "named human (HC1/HC5)"}, 400
    cp = case.get("committed_profile")
    if cp is not None:
        pending = pending_fields(case["intake"], cp)
        if pending:
            return {"error": "pending fields must be re-confirmed via "
                             "/profile/confirm, not re-committed wholesale",
                    "pending": pending, "state": "CONFIRMING"}, 409
    try:
        new_cp = commit_profile(case["intake"], actor, prior=cp)
    except GateViolation as exc:
        return {"error": str(exc)}, 400
    new_cp["intake_rev_at_commit"] = case["intake_rev"]
    case["committed_profile"] = new_cp
    _append_confirmation(case, actor, "commit",
                         list(new_cp["field_hashes"].keys()))
    return {"ok": True, "profile": _profile_block(case)}, 200


def _profile_confirm(case: dict, payload: dict):
    """POST /api/case/{id}/profile/confirm {actor, field_ids} -> (body, status)."""
    actor = str(payload.get("actor", "")).strip()
    if not actor:
        return {"error": "actor is required — fields are re-confirmed by a "
                         "named human (HC1/HC5)"}, 400
    field_ids = payload.get("field_ids")
    if not isinstance(field_ids, list) or not field_ids:
        return {"error": "expected {field_ids:[...]} — the field ids to "
                         "re-confirm"}, 400
    field_ids = [str(f) for f in field_ids]
    cp = case.get("committed_profile")
    if cp is None:
        return {"error": "profile has never been committed — nothing is "
                         "pending; use /profile/commit"}, 400
    try:
        new_cp = confirm_fields(case["intake"], cp, actor, field_ids)
    except (ValueError, GateViolation) as exc:
        return {"error": str(exc)}, 400
    if new_cp.get("intake_rev_at_commit") is None:
        # confirm_fields auto-recommitted (pending drained -> NEW hash);
        # stamp the app-side counter bridge.
        new_cp["intake_rev_at_commit"] = case["intake_rev"]
    case["committed_profile"] = new_cp
    _append_confirmation(case, actor, "reconfirm", field_ids)
    return {"ok": True, "profile": _profile_block(case)}, 200


# ---------------------------------------------------------------------------
# HTTP handler
# ---------------------------------------------------------------------------

_CASE_GET = re.compile(r"^/api/case/([^/]+)$")
_CASE_INTAKE = re.compile(r"^/api/case/([^/]+)/intake$")
_CASE_GENERATE = re.compile(r"^/api/case/([^/]+)/generate$")
_CASE_CHECK = re.compile(r"^/api/case/([^/]+)/check$")
_CASE_PACKAGE = re.compile(r"^/api/case/([^/]+)/package$")
_CASE_SIGNOFF = re.compile(r"^/api/case/([^/]+)/signoff$")
_CASE_FHIR_IMPORT = re.compile(r"^/api/case/([^/]+)/fhir/import$")
_CASE_PROFILE_COMMIT = re.compile(r"^/api/case/([^/]+)/profile/commit$")
_CASE_PROFILE_CONFIRM = re.compile(r"^/api/case/([^/]+)/profile/confirm$")


# ---------------------------------------------------------------------------
# FHIR import (privacy-state-machine.md): BUNDLE_LOADED -> MAPPED, proposals
# only. This endpoint NEVER writes case intake — the physician-confirmed
# subset goes through the existing POST /api/case/{id}/intake (INV-2 / HC1).
# The privacy log records case_id, source kind, and the bundle SHA-256 —
# never bundle content (INV-8).
# ---------------------------------------------------------------------------

def _fhir_import(case: dict, case_id: str, payload: dict):
    """Map a bundle to proposals. Returns (body, err, status). Intake untouched."""
    if payload.get("use_sample"):
        with open(SAMPLE_BUNDLE_PATH, encoding="utf-8") as f:
            bundle = json.load(f)
        source_kind = "sample-fixture"
    elif isinstance(payload.get("bundle"), dict):
        bundle = payload["bundle"]
        source_kind = "upload"
    else:
        return None, "expected {bundle:{...FHIR Bundle...}} or {use_sample:true}", 400

    route = _route_for(case)
    try:
        # as_of = the import-time date for the age computation (mapping spec
        # §2); the wall clock lives at the app boundary, never in the engine.
        result = extract_proposals(bundle, route, as_of=datetime.date.today())
    except BundleError as exc:  # structured error; message carries no chart values
        return None, str(exc), 400

    # Privacy-state note: a bundle was loaded and mapped in PREPARATORY_REVIEW
    # mode. Hash + metadata only — the bundle itself is not retained (INV-8).
    with _LOCK:
        case.setdefault("privacy_log", []).append({
            "event": "fhir_bundle_loaded",
            "state": "MAPPED",
            "mode": "PREPARATORY_REVIEW",
            "source_kind": source_kind,
            "bundle_sha256": bundle_sha256(bundle),
            "proposals": result["summary"]["auto"],
            "at": datetime.datetime.now(datetime.timezone.utc)
                  .strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
        _save_case(case_id)
    return result, None, 200


class Handler(BaseHTTPRequestHandler):
    server_version = "OSSICRO/0.2"

    # -- helpers -------------------------------------------------------------
    def _send_json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text, status=200, content_type="text/html; charset=utf-8"):
        body = text.encode("utf-8") if isinstance(text, str) else text
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return None

    def _case(self, case_id):
        return _get_case(case_id)

    def log_message(self, fmt, *args):  # quieter console
        sys.stderr.write("[ossicro] " + (fmt % args) + "\n")

    # -- GET -----------------------------------------------------------------
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/" or path == "/index.html":
            return self._serve_static("index.html")
        if path == "/api/route/3926/schema":
            return self._send_json(_schema_payload())
        if path == "/api/route/3926/sample":
            try:
                return self._send_json(_sample_payload())
            except Exception as exc:
                return self._send_json({"error": type(exc).__name__, "detail": str(exc)}, 500)

        m = _CASE_CHECK.match(path)
        if m:
            case = self._case(m.group(1))
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            try:
                return self._send_json(_check_payload(case))
            except TriggerDateError as exc:  # bad date = user-fixable error, surfaced
                return self._send_json({"error": str(exc), "field_id": exc.field_id}, 400)
            except Exception as exc:  # surfaces GateViolation etc. honestly
                return self._send_json({"error": type(exc).__name__, "detail": str(exc)}, 500)

        m = _CASE_PACKAGE.match(path)
        if m:
            case = self._case(m.group(1))
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            try:
                return self._send_json(_package_payload(case))
            except ProfileNotCommitted as exc:  # INV-3 hard gate: fail closed
                return self._send_json({"error": "profile not committed",
                                        "pending": exc.pending,
                                        "state": exc.state}, 409)
            except TriggerDateError as exc:
                return self._send_json({"error": str(exc), "field_id": exc.field_id}, 400)
            except Exception as exc:
                return self._send_json({"error": type(exc).__name__, "detail": str(exc)}, 500)

        m = _CASE_GET.match(path)
        if m:
            case = self._case(m.group(1))
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            return self._send_json({
                "case_id": m.group(1),
                "intake": case["intake"],
                "signoffs": case.get("signoffs", []),
                "confirmations": case.get("confirmations", []),
                "field_provenance": case.get("field_provenance", {}),
                "intake_rev": case["intake_rev"],
                "generated_rev": case["generated_rev"],
                "route_id": case.get("route_id"),
                "profile": _profile_block(case),
            })

        if path.startswith("/static/"):
            return self._serve_static(path[len("/static/"):])

        return self._send_json({"error": "not found", "path": path}, 404)

    # -- POST ----------------------------------------------------------------
    def do_POST(self):
        path = self.path.split("?", 1)[0]

        if path == "/api/case":
            case_id = uuid.uuid4().hex[:12]
            with _LOCK:
                CASES[case_id] = _new_case()
                _save_case(case_id)
            return self._send_json({"case_id": case_id})

        m = _CASE_INTAKE.match(path)
        if m:
            case_id = m.group(1)
            case = self._case(case_id)
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            payload = self._read_json()
            if payload is None or not isinstance(payload.get("fields"), dict):
                return self._send_json({"error": "expected {fields:{...}}"}, 400)
            actor = str(payload.get("actor", "")).strip()
            provenance = payload.get("provenance")
            provenance = provenance if isinstance(provenance, dict) else {}
            with _LOCK:
                before = dict(case["intake"])
                written = []
                # Store only non-empty values; blanks stay honestly absent.
                for key, value in payload["fields"].items():
                    if value is None or (isinstance(value, str) and value.strip() == ""):
                        case["intake"].pop(key, None)
                        case.get("field_provenance", {}).pop(key, None)
                    else:
                        case["intake"][key] = value
                        written.append(key)
                        # Durable provenance: chart-confirmed vs hand-typed.
                        src = provenance.get(key)
                        case.setdefault("field_provenance", {})[key] = (
                            src if src in ("chart-confirmed", "manual") else "manual")
                # A named confirmation record — the input-of-record has a human
                # attached (review B3 / HC5). Values are NOT copied here; they
                # live in intake. Only recorded when an actor is named and a
                # field actually changed.
                if actor and written and case["intake"] != before:
                    case.setdefault("confirmations", []).append({
                        "actor": actor,
                        "field_ids": sorted(written),
                        "from_chart": sorted(k for k in written
                                             if provenance.get(k) == "chart-confirmed"),
                        "at": datetime.datetime.now(datetime.timezone.utc)
                              .strftime("%Y-%m-%dT%H:%M:%SZ"),
                    })
                if case["intake"] != before:
                    case["intake_rev"] += 1
                _save_case(case_id)
            return self._send_json({"ok": True, "intake_rev": case["intake_rev"],
                                    "stale": _is_stale(case)})

        m = _CASE_GENERATE.match(path)
        if m:
            case_id = m.group(1)
            case = self._case(case_id)
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            try:
                with _LOCK:
                    payload = _generate_payload(case)
                    _save_case(case_id)
                return self._send_json(payload)
            except ProfileNotCommitted as exc:  # INV-3 hard gate: fail closed,
                # nothing was generated and nothing was persisted.
                return self._send_json({"error": "profile not committed",
                                        "pending": exc.pending,
                                        "state": exc.state}, 409)
            except TriggerDateError as exc:
                return self._send_json({"error": str(exc), "field_id": exc.field_id}, 400)
            except Exception as exc:
                return self._send_json({"error": type(exc).__name__, "detail": str(exc)}, 500)

        m = _CASE_FHIR_IMPORT.match(path)
        if m:
            case_id = m.group(1)
            case = self._case(case_id)
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            payload = self._read_json()
            if payload is None or not isinstance(payload, dict):
                return self._send_json({"error": "expected a JSON object"}, 400)
            try:
                result, err, status = _fhir_import(case, case_id, payload)
            except Exception as exc:  # no chart content in error payloads
                return self._send_json({"error": type(exc).__name__}, 500)
            if err is not None:
                return self._send_json({"error": err}, status)
            return self._send_json(result)

        m = _CASE_SIGNOFF.match(path)
        if m:
            case_id = m.group(1)
            case = self._case(case_id)
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            payload = self._read_json()
            if payload is None or not isinstance(payload, dict):
                return self._send_json({"error": "expected a JSON object"}, 400)
            with _LOCK:
                record, err, status = _record_signoff(case, payload)
                if err is None:
                    _save_case(case_id)
            if err is not None:
                return self._send_json({"error": err}, status)
            return self._send_json({"ok": True, "signoff": record,
                                    "signoffs": case["signoffs"]})

        m = _CASE_PROFILE_COMMIT.match(path)
        if m:
            case_id = m.group(1)
            case = self._case(case_id)
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            payload = self._read_json()
            if payload is None or not isinstance(payload, dict):
                return self._send_json({"error": "expected a JSON object"}, 400)
            with _LOCK:
                body, status = _profile_commit(case, payload)
                if status == 200:
                    _save_case(case_id)
            return self._send_json(body, status)

        m = _CASE_PROFILE_CONFIRM.match(path)
        if m:
            case_id = m.group(1)
            case = self._case(case_id)
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            payload = self._read_json()
            if payload is None or not isinstance(payload, dict):
                return self._send_json({"error": "expected a JSON object"}, 400)
            with _LOCK:
                body, status = _profile_confirm(case, payload)
                if status == 200:
                    _save_case(case_id)
            return self._send_json(body, status)

        return self._send_json({"error": "not found", "path": path}, 404)

    # -- static --------------------------------------------------------------
    def _serve_static(self, name):
        safe = os.path.normpath(name).lstrip("/\\")
        full = os.path.join(STATIC_DIR, safe)
        if not full.startswith(STATIC_DIR) or not os.path.isfile(full):
            return self._send_text("Not found", 404, "text/plain; charset=utf-8")
        ctype = "text/html; charset=utf-8" if full.endswith(".html") else "application/octet-stream"
        with open(full, "rb") as f:
            return self._send_text(f.read(), 200, ctype)


def main():
    os.makedirs(STATIC_DIR, exist_ok=True)
    os.makedirs(CASES_DIR, exist_ok=True)
    _load_cases()
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    sys.stderr.write("OSSICRO backend on http://%s:%d  (Route-3926 MVP; %d case(s) on disk)\n"
                     % (HOST, PORT, len(CASES)))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.stderr.write("\nshutting down\n")
        httpd.shutdown()


if __name__ == "__main__":
    main()
