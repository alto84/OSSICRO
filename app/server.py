"""OSSICRO MVP backend — Route-3926 single-patient expanded access.

Pure Python 3 stdlib (http.server). Starts with:

    python app/server.py

and listens on 127.0.0.1:8765. Disk-backed case store at app/data/cases/{id}.json
(no real PHI; coded identifiers only). Serves the frontend at ``/`` and the
SHARED API CONTRACT:

    GET  /api/route/3926/schema
    POST /api/case
    GET  /api/case/{id}                 -> {intake, signoffs, intake_rev, generated_rev, profile, audit}
    POST /api/case/{id}/intake          -> {ok, intake_rev, stale, profile}
                                           (rejects any key not in the route schema)
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
    POST /api/case/{id}/match           -> {candidates, absence, absence_message,
                                           queried_registries, predicates_used, as_of}
                                           (INV-3 gate: 409 unless committed; INV-4:
                                           de-identified predicates via the egress
                                           gateway to the MOCK registry adapter —
                                           live egress disabled; a registry-search
                                           ORGANIZER: criteria, never scores)
    GET  /api/case/{id}/package         -> manifest over ALL route documents + package digest
    GET  /api/case/{id}/form3926.pdf    -> DRAFT-watermarked filled Form-3926 PDF
                                           (INV-3 gate: 409 unless committed — a
                                           draft PDF of an unconfirmed input
                                           must not exist; watermark stays
                                           until the gates clear)
    GET  /api/case/{id}/form3926.fdf    -> DRAFT-marked FDF fill data (same gate;
                                           field-name map UNVERIFIED — see
                                           ossicro.pdf_3926.FDF_3926_FIELD_MAP)
    POST /api/case/{id}/release         -> {actor, to:'manufacturer'}: the
                                           NAMED-HUMAN cross-persona release act
                                           (Wave 3 E). Requires committed profile
                                           + documents generated from it; writes
                                           one audit 'release' record; refused
                                           otherwise. Cross-persona visibility
                                           is a SEND — never a default.
    GET  /api/manufacturer/inbox        -> RELEASED cases only, release-time
                                           snapshot view (LOA request +
                                           drug/indication + coded id). The
                                           supply/authorize decision and the LOA
                                           signature stay the manufacturer's
                                           alone (FDCA 561A) — OSSICRO models
                                           neither as an action it takes.
    POST /api/case/{id}/patient-link    -> {actor}: a NAMED human mints/shares
                                           the patient's OPAQUE status token
                                           (Wave 4 F; audit 'patient_link').
                                           The token — never the case_id — is
                                           the only way to reach the patient
                                           view (no case enumeration).
    GET  /api/patient/{token}           -> READ-ONLY plain-language status view
                                           (21 CFR Part 50 "understandable to
                                           the subject"): stage, what remains,
                                           and the standing draft notice. NO
                                           case_id, NO clinical detail beyond
                                           coded id + drug name. Unknown token
                                           -> 404, indistinguishable from any
                                           other not-found.
    POST /api/case/{id}/promote         -> {actor, legal_basis}: INV-5 — the
                                           preparatory-review -> ENROLLMENT
                                           legal transition (the HIPAA
                                           disclosure basis changes here).
                                           Requires committed profile + named
                                           actor + a recorded legal_basis;
                                           arms the post-enrollment sponsor-
                                           investigator obligation clocks
                                           (21 CFR 312.32 / 312.310(d) /
                                           312.33 — HC3: computed or honestly
                                           UNARMED, never fabricated) and
                                           returns the obligations checklist.
                                           Audit-logged 'promote'; a repeat
                                           promote is refused (409).
    GET  /api/cro/board                 -> Micro-CRO READ-ONLY status board
                                           (Wave 4 G): every case's stage
                                           summary. No action affordance —
                                           this is the physician's own
                                           coordinating view (persona auth
                                           INV-7-deferred).

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

from ossicro import audit as audit_mod                       # noqa: E402
from ossicro import routes as routes_mod                     # noqa: E402
from ossicro.assemble import assemble_submission             # noqa: E402
from ossicro.clocks import (                                     # noqa: E402
    expanded_access_emergency_deadlines,
    ind_30_day_deadline,
    working_days_between,
)
from ossicro.ea_generators import (                              # noqa: E402
    TriggerDateError,
    build_study,
    compute_clocks,
    generate_route_documents,
)
from ossicro.egress import DeidentifiedPredicates               # noqa: E402
from ossicro.matching import MockRegistryAdapter                 # noqa: E402
from ossicro.matching import match as run_registry_match         # noqa: E402
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
from ossicro.pdf_3926 import fdf_3926, render_3926_pdf       # noqa: E402
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

# INV-4 / Wave 2: the /match flow runs against the fixture-backed MOCK
# registry adapter only — live egress is DISABLED in the engine gateway
# (ossicro.egress raises EgressDisabled on any live=True call; flipping the
# greenlight flag is an explicit human act, never a server default).
REGISTRY_ADAPTER = MockRegistryAdapter()

# Intake schema, indexed by dotted field id.
SCHEMA_FIELDS = {f["id"]: f for f in routes_mod.intake_fields()}

# ---------------------------------------------------------------------------
# Display-string table (BUILD-PLAN Wave 3: "All UI strings move into a single
# display-string table from this wave on"). NEW user-facing strings land HERE
# so the Wave-5 jargon pass (K) is a data pass over one object. Existing
# strings are deliberately NOT refactored into it in this wave.
# ---------------------------------------------------------------------------
STRINGS = {
    "release_actor_required": (
        "actor is required — a release is an explicit act by a named human "
        "(BUILD-PLAN Wave 3 / HC1); OSSICRO never releases on its own."),
    "release_target_invalid": (
        "unsupported release target — the only release destination in this "
        "wave is 'manufacturer'."),
    "release_requires_generated_loa": (
        "release refused: no generated LOA request exists for the committed "
        "profile — generate the route documents (which include the "
        "manufacturer LOA request) from the committed input first."),
    "release_already_released": (
        "already released to the manufacturer for this committed profile — "
        "a re-release only applies after the profile is re-committed with "
        "changes (a new named release act over the new input-of-record)."),
    "inbox_note": (
        "DRAFT — synthetic-only pilot. Only cases a named human explicitly "
        "released appear here. The decision to supply the drug and the "
        "Letter of Authorization signature are the manufacturer's alone "
        "(FDCA 561A) — OSSICRO records facts; it never decides, signs, or "
        "sends on the manufacturer's behalf."),
    "pdf_filename": "form-fda-3926-%s-DRAFT.pdf",
    "fdf_filename": "form-fda-3926-%s-DRAFT.fdf",

    # -- Wave 4 F: patient persona (PLAIN LANGUAGE, authored at build time —
    # "understandable to the subject" is a 21 CFR Part 50 requirement, not a
    # Wave-5 polish item). The patient view shows ONLY these strings plus the
    # coded id and the drug name the patient already holds.
    "patient_link_actor_required": (
        "actor is required — sharing the patient status link is an explicit "
        "act by a named human (HC1); OSSICRO never sends anything to a "
        "patient on its own."),
    "patient_link_note": (
        "Share this link with the patient only. It opens a read-only, "
        "plain-language status page: no case number, no chart details — "
        "only the request's stage, what remains, and the standing "
        "nothing-has-been-submitted notice."),
    "patient_notice": (
        "This page only shows status. Everything described here is a DRAFT "
        "that your doctor is preparing. Nothing has been submitted to the "
        "FDA, and no decision has been made. If you have questions, ask "
        "your doctor."),
    # MAJOR-2: at the enrolled stage the request is no longer a draft, so the
    # "nothing submitted / no decision" notice would be false. The enrolled
    # notice makes no claim about submission and points to the doctor's office.
    "patient_notice_enrolled": (
        "This page only shows status. For anything about your treatment or "
        "where things stand, your doctor's office is the right place to ask. "
        "They have the full picture."),
    "patient_stage_draft": (
        "Your doctor is preparing a request to ask the FDA for permission "
        "to treat you with a medicine that is not yet approved for your "
        "condition. The request is still being written."),
    "patient_remaining_draft": [
        "Your doctor is still filling in and double-checking the details.",
        "The company that makes the medicine must agree to provide it.",
        "The FDA must allow the treatment to go ahead.",
        "An ethics review board (called an IRB) must agree.",
        "Before any treatment, you will be asked for your written "
        "permission (informed consent).",
    ],
    "patient_stage_committed": (
        "Your doctor has confirmed the details of the request. The "
        "paperwork is drafted, but it has not been sent anywhere yet."),
    "patient_remaining_committed": [
        "The company that makes the medicine must agree to provide it.",
        "The FDA must allow the treatment to go ahead.",
        "An ethics review board (called an IRB) must agree.",
        "Before any treatment, you will be asked for your written "
        "permission (informed consent).",
    ],
    "patient_stage_released": (
        "Your doctor has shared a draft of the request with the company "
        "that makes the medicine, asking for their support. The company "
        "has not decided yet."),
    "patient_remaining_released": [
        "The company that makes the medicine must decide whether to "
        "provide it.",
        "The FDA must allow the treatment to go ahead.",
        "An ethics review board (called an IRB) must agree.",
        "Before any treatment, you will be asked for your written "
        "permission (informed consent).",
    ],
    "patient_stage_enrolled": (
        "Your doctor has recorded that you are enrolled in this treatment "
        "plan. From now on your doctor is responsible for watching your "
        "safety and sending required reports."),
    "patient_remaining_enrolled": [
        "Your doctor must report certain side effects to the FDA within "
        "fixed deadlines.",
        "Your doctor must send the FDA the required follow-up and yearly "
        "reports.",
        "Tell your doctor about anything you notice — new symptoms, side "
        "effects, or questions.",
    ],

    # -- Wave 4 H: INV-5 promote() — the preparatory-review -> enrollment
    # legal transition and the obligations it arms.
    "promote_actor_required": (
        "actor is required — enrollment is recorded by a named human "
        "(INV-5 / HC1); OSSICRO never enrolls a patient on its own."),
    "promote_legal_basis_required": (
        "legal_basis is required and must be one of: authorization-164.508 "
        "(the patient's written HIPAA authorization, 45 CFR 164.508), "
        "waiver-164.512 (IRB/Privacy Board waiver of authorization, 45 CFR "
        "164.512(i)(1)(i)), or treatment-disclosure (use/disclosure for "
        "treatment, 45 CFR 164.506(c)). Enrollment is the moment the HIPAA "
        "disclosure basis changes — preparatory review (45 CFR "
        "164.512(i)(1)(ii)) ends here — so the new basis must be recorded, "
        "never assumed."),
    "promote_already_enrolled": (
        "already enrolled — the enrollment record stands and is neither "
        "silently re-recorded nor undone (the audit trail is append-only). "
        "If the record is wrong, the correction is itself a recorded human "
        "act outside this endpoint; OSSICRO never rewrites its history."),
    "promote_note": (
        "Enrollment recorded. The post-enrollment sponsor-investigator "
        "obligations below now attach to you, the physician-sponsor. "
        "OSSICRO computes the statutory deadlines (HC3) and keeps this "
        "checklist in view; it never files, sends, or decides anything "
        "for you."),
    "obligation_safety_15": (
        "IND safety report: any suspected adverse reaction that is both "
        "serious and unexpected must be reported to FDA no later than 15 "
        "calendar days after you determine the information qualifies."),
    "obligation_safety_15_q": (
        "No deadline is computed because no qualifying event has been "
        "recorded — this clock runs per event, from the date you determine "
        "a suspected adverse reaction is both serious and unexpected "
        "(21 CFR 312.32(c)(1)), never from enrollment and never from a "
        "date OSSICRO invents. Record that determination date to arm it."),
    "obligation_safety_7": (
        "Fatal or life-threatening unexpected suspected adverse reaction: "
        "notify FDA no later than 7 calendar days after your initial "
        "receipt of the information."),
    "obligation_safety_7_q": (
        "No deadline is computed because no qualifying event has been "
        "recorded — this clock runs per event, from your initial receipt "
        "of the information (21 CFR 312.32(c)(2)). Record that receipt "
        "date to arm it."),
    "obligation_followup": (
        "Emergency-use follow-up: when FDA authorized the emergency use by "
        "telephone, the written expanded-access submission (Form 3926) is "
        "due within 15 working days of that authorization."),
    "obligation_followup_q": (
        "Applies when FDA authorized emergency use by telephone (21 CFR "
        "312.310(d)). Enter the FDA telephone-authorization date "
        "(submission.emergency_auth_datetime) to arm the 15-working-day "
        "deadline; OSSICRO assumes no date."),
    "obligation_irb_notify": (
        "Emergency-use IRB notification: when a patient is treated before IRB "
        "review under the emergency provision, the IRB must be notified within "
        "5 working days of the treatment."),
    "obligation_irb_notify_q": (
        "Applies on the emergency path (21 CFR 56.104(c)). Enter the FDA "
        "telephone-authorization date (submission.emergency_auth_datetime) to "
        "arm the 5-working-day IRB-notification deadline; OSSICRO assumes no date."),
    "obligation_annual": (
        "IND annual report: due within 60 days of each anniversary of the "
        "date the IND went into effect."),
    "obligation_annual_q": (
        "Enter the FDA receipt date of the 3926 "
        "(submission.fda_receipt_date) so OSSICRO can compute the "
        "IND-effective date (30 calendar days after receipt, 21 CFR "
        "312.40(b)(1)) and the annual-report window (within 60 days of "
        "its anniversary, 21 CFR 312.33); OSSICRO assumes no date."),
    "obligation_date_unreadable": (
        "The recorded %s could not be read as a date (YYYY-MM-DD) — "
        "correct it to arm this deadline; OSSICRO computes clocks only "
        "from readable recorded dates (HC3), never from guesses."),

    # -- Wave 4 G: Micro-CRO read-only status board.
    "cro_board_note": (
        "READ-ONLY coordinating status board over the requesting "
        "physician's own cases. It offers no actions: every act (commit, "
        "sign-off, release, promote) happens on the case itself, by a "
        "named human. Persona-level authentication is deferred (INV-7) — "
        "this board must not be exposed beyond the physician pilot."),
}

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
            "committed_profile": None, "generated_hash": None,
            # I-AUDIT (Wave 1): the append-only audit trail — field ids,
            # actions, actors, timestamps, input hashes; NEVER chart values
            # (INV-8). Written via ossicro.audit.append only; later waves
            # (INV-4 egress, INV-5 enrollment, release acts) write here too.
            "audit": [],
            # Wave 3 (E): the cross-persona RELEASE record. None = never
            # released — the case is INVISIBLE to every non-physician persona.
            # Set only by the explicit named-human release act (POST /release,
            # audit-logged); the manufacturer-facing view is snapshotted at
            # release time so later intake edits never leak un-released text.
            "released": None,
            # Wave 4 (F): the OPAQUE patient-view token. None = never minted —
            # the patient view is unreachable. Minted lazily by the named
            # POST /patient-link act (like the Wave-3 release_id, it is the
            # ONLY capability that reaches the patient view; the case_id
            # never is).
            "patient_token": None,
            # Wave 4 (H) / INV-5: the enrollment record. None = the case is
            # in PREPARATORY_REVIEW (45 CFR 164.512(i)(1)(ii)); set only by
            # the named POST /promote act, which records the NEW HIPAA
            # disclosure basis (the legal moment preparatory review ends).
            "enrollment": None,
            "mode": "PREPARATORY_REVIEW"}


def _normalize_case(case: dict) -> dict:
    """Backfill missing keys on a loaded case. Idempotent.

    Raises ValueError on a shape that cannot be a case (non-dict JSON, or an
    audit trail that is not a list) — the loader SKIPS such a file with a
    warning rather than crashing startup or silently discarding an audit
    trail (append-only means we never replace a corrupt trail with []).
    """
    if not isinstance(case, dict):
        raise ValueError("case JSON must be an object, got %s"
                         % type(case).__name__)
    base = _new_case()
    for key, default in base.items():
        case.setdefault(key, default)
    if not isinstance(case["audit"], list):
        raise ValueError("case audit trail is corrupt (not a list) — "
                         "refusing to load rather than discard it")
    if not all(isinstance(entry, dict) for entry in case["audit"]):
        raise ValueError("case audit trail has a non-dict entry — refusing to "
                         "load rather than serve a corrupt trail")
    return case


def _case_path(case_id: str) -> str:
    return os.path.join(CASES_DIR, case_id + ".json")


def _save_case(case_id: str) -> None:
    """Atomic write: tmp file + fsync + os.replace.

    A crash mid-write never truncates a case (the good file is replaced only
    by a fully-flushed tmp), and a failed dump never clobbers it — on any
    error the tmp is removed and the previous on-disk case stands.
    """
    os.makedirs(CASES_DIR, exist_ok=True)
    path = _case_path(case_id)
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(CASES[case_id], f, indent=1, sort_keys=True)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


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


def _match_payload(case: dict) -> dict:
    """POST /api/case/{id}/match — the registry-search ORGANIZER (Wave 2 C).

    INV-3 hard gate first: same fail-closed rule as /generate — matching
    consumes the COMMITTED profile's de-identified predicates or nothing
    (raises ProfileNotCommitted -> 409). The predicates are derived from a
    B1 snapshot of the committed intake through the closed
    ``DeidentifiedPredicates.from_profile`` builder (codes / band / sex /
    route token only — no names, dates, or free text), and every registry
    query writes an ``egress_query`` audit record through the INV-4 gateway.
    Live egress is off: the mock adapter answers. The endpoint organizes
    candidates with matched/unmatched/unverifiable CRITERIA — never a score,
    never a recommendation, and it never mutates intake. Every candidate is
    a physician-confirmed proposal.
    """
    intake = dict(case["intake"])   # B1: one snapshot for gate + predicates
    require_committed(intake, case.get("committed_profile"))
    predicates = DeidentifiedPredicates.from_profile(intake)
    return run_registry_match(
        predicates, REGISTRY_ADAPTER,
        trail=case.setdefault("audit", []),
        as_of=datetime.date.today().isoformat())


def _form3926_pdf_bytes(case: dict) -> bytes:
    """GET /api/case/{id}/form3926.pdf — the DRAFT-watermarked filled 3926.

    Gated behind the SAME require_committed as /generate: a draft PDF of an
    unconfirmed input must not exist (raises ProfileNotCommitted -> 409).
    The render is value-faithful to the committed intake snapshot; every
    page carries the DRAFT watermark (the engine offers no other render).
    """
    intake = dict(case["intake"])   # B1: one snapshot for gate + render
    require_committed(intake, case.get("committed_profile"))
    return render_3926_pdf(intake)


def _form3926_fdf_bytes(case: dict) -> bytes:
    """GET /api/case/{id}/form3926.fdf — DRAFT-marked FDF fill data.

    Same INV-3 gate as the PDF. Field-name map is UNVERIFIED (see
    ossicro.pdf_3926.FDF_3926_FIELD_MAP) — synthetic-only until the human
    verification pass against the official AcroForm.
    """
    intake = dict(case["intake"])
    require_committed(intake, case.get("committed_profile"))
    return fdf_3926(intake)


# ---------------------------------------------------------------------------
# Wave 3 (E): the Pharma persona — release act + manufacturer inbox.
#
# Cross-persona visibility is a SEND (BUILD-PLAN BLOCKER 2): nothing the
# physician produced appears in the manufacturer persona without the explicit
# NAMED-HUMAN release act below, audit-logged as 'release'. The manufacturer's
# supply/authorize decision and the LOA signature are the manufacturer's alone
# (FDCA 561A) — no endpoint here models OSSICRO taking either act.
# ---------------------------------------------------------------------------

def _actor_str(payload: dict) -> str:
    """The named-actor string, or "" for a missing/non-string value.

    MINOR-1: a dict/list actor must never be str()-baked into an immutable
    audit record. A non-string value returns "" here and is then rejected by
    each handler's existing 'actor required' 400 check.
    """
    a = payload.get("actor")
    return a.strip() if isinstance(a, str) else ""


def _release(case: dict, payload: dict):
    """POST /api/case/{id}/release {actor, to:'manufacturer'} -> (body, status).

    Requires a committed profile AND documents generated from that committed
    input (the LOA request among them). Refuses a repeat release for the same
    committed hash; a re-release becomes possible only after a re-commit
    (new input-of-record, new named act). Caller holds _LOCK and persists.
    """
    actor = _actor_str(payload)
    if not actor:
        return {"error": STRINGS["release_actor_required"]}, 400
    to = str(payload.get("to", "")).strip().lower()
    if to != "manufacturer":
        return {"error": STRINGS["release_target_invalid"]}, 400
    intake = dict(case["intake"])   # B1: one snapshot for gate + view build
    try:
        committed_hash = require_committed(intake, case.get("committed_profile"))
    except ProfileNotCommitted as exc:
        return {"error": "profile not committed", "pending": exc.pending,
                "state": exc.state}, 409
    # The release covers a generated artifact, not a hypothetical one: the
    # last /generate must have consumed exactly this committed input.
    if case.get("generated_hash") != committed_hash:
        return {"error": STRINGS["release_requires_generated_loa"]}, 409
    rel = case.get("released")
    if isinstance(rel, dict) and rel.get("released_hash") == committed_hash:
        return {"error": STRINGS["release_already_released"],
                "released": {k: rel.get(k) for k in
                             ("to", "actor", "at", "released_hash")}}, 409
    _route, _study, documents = _study_and_docs(case, intake)
    loa_request = documents.get("manufacturer-loa-request")
    if loa_request is None:
        return {"error": STRINGS["release_requires_generated_loa"]}, 409
    # The manufacturer-facing view is SNAPSHOTTED at release time: exactly
    # what the named human released, immune to later intake drift. Coded id
    # only — no other patient identifiers (the schema itself is coded-only,
    # and the view narrows further to LOA request + drug/indication summary).
    view = {
        "patient_coded_id": str(intake.get("patient.coded_id", "") or ""),
        "drug": str(intake.get("drug.name", "") or ""),
        "indication": str(intake.get("patient.diagnosis", "") or ""),
        "physician": str(intake.get("investigator.name", "") or ""),
        "loa_request": loa_request.rendered,
    }
    # MAJOR-1: the manufacturer is handed an OPAQUE release_id, never the
    # case_id — the case_id is a full-access capability on the unauthenticated
    # GET /api/case/{id} (persona auth is INV-7-deferred), so leaking it would
    # void the release view's minimization. The inbox keys on release_id only.
    prior_rid = rel.get("release_id") if isinstance(rel, dict) else None
    case["released"] = {"to": "manufacturer", "actor": actor,
                        "at": _utcnow_z(), "released_hash": committed_hash,
                        "release_id": prior_rid or uuid.uuid4().hex[:16],
                        "view": view}
    # I-AUDIT: exactly one immutable 'release' record per release act — the
    # named human, the released artifact, the committed hash. No content.
    audit_mod.append(case.setdefault("audit", []), actor=actor,
                     action="release", target="manufacturer-loa-request",
                     input_hash=committed_hash,
                     detail={"to": "manufacturer"})
    return {"ok": True,
            "released": {k: case["released"][k] for k in
                         ("to", "actor", "at", "released_hash")}}, 200


def _manufacturer_inbox() -> dict:
    """GET /api/manufacturer/inbox — RELEASED cases only, manufacturer view.

    A case with no release record simply does not exist here. Each item is
    the release-time snapshot: LOA request + drug/indication summary + the
    coded patient id — never intake at large, never a later edit.
    """
    with _LOCK:                       # MINOR-5: snapshot ids without racing a POST
        case_ids = set(CASES)
    if os.path.isdir(CASES_DIR):
        for name in os.listdir(CASES_DIR):
            if name.endswith(".json") and _CASE_ID_RE.match(name[:-len(".json")]):
                case_ids.add(name[:-len(".json")])
    items = []
    for case_id in sorted(case_ids):
        case = _get_case(case_id)
        if case is None:
            continue
        rel = case.get("released")
        if not isinstance(rel, dict) or rel.get("to") != "manufacturer":
            continue   # un-released = invisible, unconditionally
        view = rel.get("view") if isinstance(rel.get("view"), dict) else {}
        items.append({
            # MAJOR-1: opaque release_id, NOT case_id (no capability leak).
            "release_id": rel.get("release_id", ""),
            "released_by": rel.get("actor", ""),
            "released_at": rel.get("at", ""),
            "released_hash": rel.get("released_hash", ""),
            "patient_coded_id": view.get("patient_coded_id", ""),
            "drug": view.get("drug", ""),
            "indication": view.get("indication", ""),
            "physician": view.get("physician", ""),
            "loa_request": view.get("loa_request", ""),
            "draft": True,
        })
    return {"inbox": items, "count": len(items), "note": STRINGS["inbox_note"]}


# ---------------------------------------------------------------------------
# Wave 4 (F): the Patient persona — tokenized, read-only, plain-language.
#
# The patient view is reachable ONLY through the opaque per-case token (a
# uuid, like the Wave-3 release_id) — never through the case_id, and there is
# no enumeration surface. An unknown token is a plain 404, indistinguishable
# from any other not-found (no not-found vs not-authorized distinction to
# probe). The view carries NO case_id and no clinical PHI the patient would
# not already hold: the coded id, the drug name, a plain-language stage, what
# remains, and the standing draft notice (21 CFR Part 50: "understandable to
# the subject" — vocabulary authored at build time in STRINGS).
# ---------------------------------------------------------------------------

def _all_case_ids() -> list:
    """Every known case id (memory + disk), snapshotted under _LOCK."""
    with _LOCK:
        case_ids = set(CASES)
    if os.path.isdir(CASES_DIR):
        for name in os.listdir(CASES_DIR):
            if name.endswith(".json") and _CASE_ID_RE.match(name[:-len(".json")]):
                case_ids.add(name[:-len(".json")])
    return sorted(case_ids)


def _case_for_patient_token(token: str):
    """The case whose minted patient_token equals ``token``, else None.

    Lookup by token value only — the URL path never doubles as a case
    locator, so there is nothing to enumerate.
    """
    if not token or not isinstance(token, str):
        return None
    for case_id in _all_case_ids():
        case = _get_case(case_id)
        if case is not None and case.get("patient_token") == token:
            return case
    return None


def _case_stage(case: dict) -> str:
    """The coarse lifecycle stage: draft / committed / released / enrolled."""
    if isinstance(case.get("enrollment"), dict):
        return "enrolled"
    if isinstance(case.get("released"), dict):
        return "released"
    if _profile_block(case)["state"] == "COMMITTED":
        return "committed"
    return "draft"


def _patient_link(case: dict, payload: dict):
    """POST /api/case/{id}/patient-link {actor} -> (body, status).

    A NAMED act (HC1): a human decides to hand the patient a status link.
    The token is minted lazily on first use and reused thereafter (one
    stable link per case); EVERY invocation is audit-logged 'patient_link'
    — re-sharing an existing link is still an act. Caller holds _LOCK and
    persists.
    """
    actor = _actor_str(payload)
    if not actor:
        return {"error": STRINGS["patient_link_actor_required"]}, 400
    minted = not case.get("patient_token")
    if minted:
        case["patient_token"] = uuid.uuid4().hex
    cp = case.get("committed_profile")
    audit_mod.append(case.setdefault("audit", []), actor=actor,
                     action="patient_link", target="patient-view",
                     input_hash=(cp or {}).get("profile_hash") or "",
                     detail={"minted": minted})
    return {"ok": True,
            "patient_token": case["patient_token"],
            "link": "/api/patient/%s" % case["patient_token"],
            "note": STRINGS["patient_link_note"]}, 200


def _patient_view(case: dict) -> dict:
    """The read-only plain-language status view. NO case_id, NO clinical
    detail beyond the coded id + drug name the patient already holds."""
    stage = _case_stage(case)
    intake = case["intake"]
    return {
        "stage": stage,
        "status": STRINGS["patient_stage_" + stage],
        "what_remains": list(STRINGS["patient_remaining_" + stage]),
        # Stage-conditional (MAJOR-2): the "nothing submitted" notice is true
        # in draft/committed/released, false once enrolled.
        "notice": STRINGS.get("patient_notice_" + stage, STRINGS["patient_notice"]),
        "patient_coded_id": str(intake.get("patient.coded_id", "") or ""),
        "drug": str(intake.get("drug.name", "") or ""),
        "draft": True,
    }


# ---------------------------------------------------------------------------
# Wave 4 (H): INV-5 promote() — preparatory review -> ENROLLMENT.
#
# The legal moment the HIPAA disclosure basis changes: preparatory review
# (45 CFR 164.512(i)(1)(ii)) ends and the recorded legal_basis takes over.
# Requires a committed profile (the input-of-record the enrollment is FROM),
# a named actor, and one of the three recognized bases. Arms the
# post-enrollment sponsor-investigator obligation clocks via the canonical
# ossicro.clocks (HC3: computed from recorded anchor dates or honestly
# UNARMED with the resolving question — never a fabricated date) and emits
# the obligations checklist: the system must not walk a physician into
# duties it then ignores.
# ---------------------------------------------------------------------------

_LEGAL_BASES = {
    "authorization-164.508": "45 CFR 164.508 (patient's written HIPAA authorization)",
    "waiver-164.512": "45 CFR 164.512(i)(1)(i) (IRB/Privacy Board waiver of authorization)",
    "treatment-disclosure": "45 CFR 164.506(c) (use/disclosure for treatment)",
}


def _parse_intake_date(value):
    """(date | None, present: bool). Honest failure: unreadable -> None."""
    raw = str(value or "").strip()
    if not raw:
        return None, False
    for candidate in (raw, raw[:10]):
        try:
            return datetime.datetime.strptime(candidate, "%Y-%m-%d").date(), True
        except ValueError:
            continue
    return None, True


def _obligation(obligation: str, citation: str, basis: str, days: int,
                armed: bool, due, trigger_field, resolving_question) -> dict:
    return {"obligation": obligation, "citation": citation, "basis": basis,
            "days": days, "armed": armed,
            "due": due.isoformat() if due is not None else None,
            "owner": "physician-sponsor",
            "trigger_field": trigger_field,
            "resolving_question": resolving_question}


def _enrollment_obligations(case: dict) -> list:
    """The post-enrollment sponsor-investigator obligations checklist.

    Computed live from the case (not snapshotted) so a later-recorded anchor
    date arms its clock honestly. Empty until enrollment — the duties attach
    at the INV-5 transition, not before. Day-counts and citations:

    - 15 calendar days, 21 CFR 312.32(c)(1): IND safety report of a serious
      and unexpected suspected adverse reaction, from the sponsor's
      determination that the information qualifies. Per-event anchor — it
      cannot exist at enrollment, so this clock is ALWAYS emitted unarmed
      here (HC3: the resolving question, never an invented date).
    - 7 calendar days, 21 CFR 312.32(c)(2): fatal / life-threatening
      unexpected suspected adverse reaction, from initial receipt of the
      information. Same per-event honesty.
    - 15 working days, 21 CFR 312.310(d)(2): the written expanded-access
      submission after FDA's emergency telephone authorization — armed from
      the recorded authorization date via
      clocks.expanded_access_emergency_deadlines.
    - within 60 days of the IND-effective anniversary, 21 CFR 312.33: the
      annual report — effective date = FDA receipt + 30 calendar days
      (21 CFR 312.40(b)(1), via clocks.ind_30_day_deadline), first window
      closes 60 days after its first anniversary.
    """
    if not isinstance(case.get("enrollment"), dict):
        return []
    intake = case["intake"]
    items = [
        _obligation(STRINGS["obligation_safety_15"], "21 CFR 312.32(c)(1)",
                    "calendar-day", 15, False, None, None,
                    STRINGS["obligation_safety_15_q"]),
        _obligation(STRINGS["obligation_safety_7"], "21 CFR 312.32(c)(2)",
                    "calendar-day", 7, False, None, None,
                    STRINGS["obligation_safety_7_q"]),
    ]
    # BOTH clocks an emergency phone authorization arms: the 15-working-day
    # written 3926 (312.310(d)(2)) AND the 5-working-day IRB notification
    # (56.104(c)) — the shortest deadline of all. MAJOR-1: the checklist must
    # not drop the IRB notice just because the canonical function returns it
    # second. Both come from expanded_access_emergency_deadlines().
    auth_field = "submission.emergency_auth_datetime"
    auth_date, auth_present = _parse_intake_date(intake.get(auth_field))
    _emergency_labels = {
        "21 CFR 312.310(d)(2)": STRINGS["obligation_followup"],
        "21 CFR 56.104(c)": STRINGS["obligation_irb_notify"],
    }
    if auth_date is not None:
        for dl in expanded_access_emergency_deadlines(auth_date):
            items.append(_obligation(
                _emergency_labels.get(dl.citation, dl.name), dl.citation,
                dl.basis, dl.n, True, dl.due, auth_field, None))
    else:
        for citation, n, label, qkey in (
                ("21 CFR 312.310(d)(2)", 15, STRINGS["obligation_followup"],
                 "obligation_followup_q"),
                ("21 CFR 56.104(c)", 5, STRINGS["obligation_irb_notify"],
                 "obligation_irb_notify_q")):
            q = (STRINGS["obligation_date_unreadable"] % auth_field
                 if auth_present else STRINGS[qkey])
            items.append(_obligation(
                label, citation, "working-day", n, False, None, auth_field, q))
    # 312.33 — annual report, anchored on the IND-effective anniversary.
    receipt_field = "submission.fda_receipt_date"
    receipt, receipt_present = _parse_intake_date(intake.get(receipt_field))
    if receipt is not None:
        effective = ind_30_day_deadline(receipt).due   # 312.40(b)(1)
        try:
            anniversary = effective.replace(year=effective.year + 1)
        except ValueError:            # Feb 29 -> Feb 28 of the next year
            anniversary = datetime.date(effective.year + 1, 2, 28)
        items.append(_obligation(
            STRINGS["obligation_annual"], "21 CFR 312.33",
            "calendar-day", 60, True,
            anniversary + datetime.timedelta(days=60), receipt_field, None))
    else:
        q = (STRINGS["obligation_date_unreadable"] % receipt_field
             if receipt_present else STRINGS["obligation_annual_q"])
        items.append(_obligation(
            STRINGS["obligation_annual"], "21 CFR 312.33",
            "calendar-day", 60, False, None, receipt_field, q))
    return items


def _promote(case: dict, payload: dict):
    """POST /api/case/{id}/promote {actor, legal_basis} -> (body, status).

    Caller holds _LOCK and persists. Refusals mutate nothing. A repeat
    promote is refused with the standing record (the honest alternative to
    silent re-recording); there is no demotion endpoint — the enrollment
    record, like the audit trail it lives beside, is append-only history.
    """
    actor = _actor_str(payload)
    if not actor:
        return {"error": STRINGS["promote_actor_required"]}, 400
    legal_basis = str(payload.get("legal_basis", "")).strip()
    if legal_basis not in _LEGAL_BASES:
        return {"error": STRINGS["promote_legal_basis_required"],
                "allowed": sorted(_LEGAL_BASES)}, 400
    intake = dict(case["intake"])   # B1: one snapshot for the gate
    try:
        committed_hash = require_committed(intake, case.get("committed_profile"))
    except ProfileNotCommitted as exc:
        return {"error": "profile not committed", "pending": exc.pending,
                "state": exc.state}, 409
    prior = case.get("enrollment")
    if isinstance(prior, dict):
        return {"error": STRINGS["promote_already_enrolled"],
                "enrollment": dict(prior)}, 409
    from_mode = str(case.get("mode") or "PREPARATORY_REVIEW")
    case["enrollment"] = {"actor": actor, "at": _utcnow_z(),
                          "legal_basis": legal_basis,
                          "from_hash": committed_hash}
    case["mode"] = "ENROLLMENT"
    # I-AUDIT: exactly one immutable 'promote' record per enrollment — the
    # named human, the recorded legal basis, the input-of-record hash, and
    # the mode transition. No chart values (INV-8).
    audit_mod.append(case.setdefault("audit", []), actor=actor,
                     action="promote", target="enrollment",
                     input_hash=committed_hash,
                     detail={"legal_basis": legal_basis,
                             "legal_basis_citation": _LEGAL_BASES[legal_basis],
                             "from_mode": from_mode, "to_mode": "ENROLLMENT"})
    return {"ok": True, "mode": "ENROLLMENT",
            "enrollment": dict(case["enrollment"]),
            "obligations_checklist": _enrollment_obligations(case),
            "note": STRINGS["promote_note"]}, 200


# ---------------------------------------------------------------------------
# Wave 4 (G): the Micro-CRO READ-ONLY status board.
#
# The physician's own coordinating view over every case (case-level
# visibility is appropriate for the physician persona; persona auth is
# INV-7-deferred — see STRINGS["cro_board_note"]). GET only; no action
# affordance exists here, honoring the documented deferral (no real
# counterparty exists yet — an acting coordinator would be the eschaton
# pattern this build explicitly refused).
# ---------------------------------------------------------------------------

def _cro_board() -> dict:
    items = []
    for case_id in _all_case_ids():
        case = _get_case(case_id)
        if case is None:
            continue
        intake = dict(case["intake"])
        profile = _profile_block(case)
        route = _route_for(case)
        route_gates = set(route.get("gates", []))
        signed = {s.get("gate_id") for s in case.get("signoffs", [])}
        # Best-effort ledger/clock rollup: a STATUS COUNT, never the
        # authoritative check (that is GET /check). Runs the offline stub
        # reviewer — a board sweep must not fan out live model calls — and
        # a case whose data cannot render reports the failure honestly
        # instead of vanishing from its own coordinator's view.
        totals = None
        clocks = None
        rollup_error = None
        try:
            r, study, documents = _study_and_docs(case, intake)
            result = run_check(study, documents, DOC_REGISTRY, GATE_REGISTRY,
                               reviewer=DeterministicStubReviewer())
            counted = {"green": 0, "amber": 0, "red": 0}
            for item in result.ledger:
                counted[item.status] = counted.get(item.status, 0) + 1
            entries = _clock_entries(study, r)
            totals = counted
            clocks = {"armed": sum(1 for c in entries if c["armed"]),
                      "total": len(entries)}
        except Exception as exc:   # no chart content in the rollup error
            totals = None          # all-or-nothing: a partial rollup would
            clocks = None          # read as a complete one
            rollup_error = type(exc).__name__
        obligations = _enrollment_obligations(case)
        items.append({
            "case_id": case_id,   # the physician's own capability (INV-7 note)
            "patient_coded_id": str(intake.get("patient.coded_id", "") or ""),
            "drug": str(intake.get("drug.name", "") or ""),
            "route_id": route["route_id"],
            "stage": _case_stage(case),
            "mode": str(case.get("mode") or "PREPARATORY_REVIEW"),
            "profile_state": profile["state"],
            "pending_fields": len(profile["pending"]),
            "gates": {"required": len(route_gates),
                      "signed": len(signed & route_gates)},
            "ledger": totals,
            "clocks": clocks,
            "rollup_error": rollup_error,
            "obligations": {"total": len(obligations),
                            "armed": sum(1 for o in obligations if o["armed"])},
            "released": isinstance(case.get("released"), dict),
            "enrolled": isinstance(case.get("enrollment"), dict),
            "patient_link_minted": bool(case.get("patient_token")),
        })
    return {"board": items, "count": len(items),
            "note": STRINGS["cro_board_note"]}


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
    # I-AUDIT: one record per recorded sign-off — the named signer, the gate
    # and document ids, and the committed-profile hash in force at the time
    # ("" = honest absence, pre-commit). No document or chart content.
    audit_mod.append(case.setdefault("audit", []), actor=signer,
                     action="signoff", target=doc_id,
                     input_hash=record["input_hash"],
                     detail={"gate_id": gate_id, "doc_id": doc_id,
                             "role": role, "date": date})
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
    actor = _actor_str(payload)
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
    # I-AUDIT: exactly one immutable record per commit — field ids and the
    # committed hash, never values (INV-8).
    audit_mod.append(case.setdefault("audit", []), actor=actor,
                     action="commit", target="committed-profile",
                     input_hash=new_cp["profile_hash"],
                     detail={"field_ids": sorted(new_cp["field_hashes"])})
    return {"ok": True, "profile": _profile_block(case)}, 200


def _profile_confirm(case: dict, payload: dict):
    """POST /api/case/{id}/profile/confirm {actor, field_ids} -> (body, status)."""
    actor = _actor_str(payload)
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
    # I-AUDIT: one record per re-confirmation. input_hash is the commit
    # object's CURRENT hash — the new hash when the pending set drained and
    # confirm_fields auto-recommitted, the still-standing prior hash when
    # fields remain staged (honest either way).
    audit_mod.append(case.setdefault("audit", []), actor=actor,
                     action="reconfirm", target="committed-profile",
                     input_hash=new_cp.get("profile_hash") or "",
                     detail={"field_ids": sorted(field_ids)})
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
_CASE_AUDIT = re.compile(r"^/api/case/([^/]+)/audit$")
_CASE_FHIR_IMPORT = re.compile(r"^/api/case/([^/]+)/fhir/import$")
_CASE_MATCH = re.compile(r"^/api/case/([^/]+)/match$")
_CASE_PROFILE_COMMIT = re.compile(r"^/api/case/([^/]+)/profile/commit$")
_CASE_PROFILE_CONFIRM = re.compile(r"^/api/case/([^/]+)/profile/confirm$")
_CASE_FORM3926_PDF = re.compile(r"^/api/case/([^/]+)/form3926\.pdf$")
_CASE_FORM3926_FDF = re.compile(r"^/api/case/([^/]+)/form3926\.fdf$")
_CASE_RELEASE = re.compile(r"^/api/case/([^/]+)/release$")
_CASE_PATIENT_LINK = re.compile(r"^/api/case/([^/]+)/patient-link$")
_CASE_PROMOTE = re.compile(r"^/api/case/([^/]+)/promote$")
_PATIENT_VIEW = re.compile(r"^/api/patient/([^/]+)$")


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
    bundle_hash = bundle_sha256(bundle)
    with _LOCK:
        case.setdefault("privacy_log", []).append({
            "event": "fhir_bundle_loaded",
            "state": "MAPPED",
            "mode": "PREPARATORY_REVIEW",
            "source_kind": source_kind,
            "bundle_sha256": bundle_hash,
            "proposals": result["summary"]["auto"],
            "at": datetime.datetime.now(datetime.timezone.utc)
                  .strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
        # I-AUDIT: one record per bundle load. No named human performs this
        # act (import MAPS only; confirmation happens later via /intake and
        # /profile/confirm), so actor is honestly blank — never synthesized.
        audit_mod.append(case.setdefault("audit", []), actor="",
                         action="bundle_loaded", target="fhir-bundle",
                         input_hash="sha256:" + bundle_hash,
                         detail={"source_kind": source_kind,
                                 "proposals": result["summary"]["auto"]})
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

    def _send_bytes(self, data, content_type, filename, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Disposition",
                         'attachment; filename="%s"' % filename)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

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

        if path == "/api/cro/board":
            # Micro-CRO persona (Wave 4 G): READ-ONLY status board — no
            # POST route exists for it; nothing on it acts on a case.
            try:
                return self._send_json(_cro_board())
            except Exception as exc:  # no chart content in error payloads
                return self._send_json({"error": type(exc).__name__}, 500)

        m = _PATIENT_VIEW.match(path)
        if m:
            # Patient persona (Wave 4 F): the OPAQUE token is the only key.
            # Unknown token -> the same bare 404 as any other miss — no
            # enumeration, no not-found vs not-authorized distinction, and
            # the token is never echoed back.
            try:
                case = _case_for_patient_token(m.group(1))
                if case is None:
                    return self._send_json({"error": "not found"}, 404)
                return self._send_json(_patient_view(case))
            except Exception as exc:  # no chart content in error payloads
                return self._send_json({"error": type(exc).__name__}, 500)

        if path == "/api/manufacturer/inbox":
            # Pharma persona: RELEASED cases only (a SEND happened); nothing
            # else exists in this view. Read-only — the supply/authorize
            # decision is never modeled as an action OSSICRO takes.
            try:
                return self._send_json(_manufacturer_inbox())
            except Exception as exc:  # no chart content in error payloads
                return self._send_json({"error": type(exc).__name__}, 500)

        m = _CASE_FORM3926_PDF.match(path)
        if m:
            case_id = m.group(1)
            case = self._case(case_id)
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            try:
                pdf = _form3926_pdf_bytes(case)
            except ProfileNotCommitted as exc:  # INV-3 hard gate: a draft PDF
                # of an unconfirmed input must not exist — fail closed.
                return self._send_json({"error": "profile not committed",
                                        "pending": exc.pending,
                                        "state": exc.state}, 409)
            except Exception as exc:
                return self._send_json({"error": type(exc).__name__,
                                        "detail": str(exc)}, 500)
            return self._send_bytes(pdf, "application/pdf",
                                    STRINGS["pdf_filename"] % case_id)

        m = _CASE_FORM3926_FDF.match(path)
        if m:
            case_id = m.group(1)
            case = self._case(case_id)
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            try:
                fdf = _form3926_fdf_bytes(case)
            except ProfileNotCommitted as exc:  # same fail-closed gate
                return self._send_json({"error": "profile not committed",
                                        "pending": exc.pending,
                                        "state": exc.state}, 409)
            except Exception as exc:
                return self._send_json({"error": type(exc).__name__,
                                        "detail": str(exc)}, 500)
            return self._send_bytes(fdf, "application/vnd.fdf",
                                    STRINGS["fdf_filename"] % case_id)

        m = _CASE_AUDIT.match(path)
        if m:
            case = self._case(m.group(1))
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            # I-AUDIT read: copies of the immutable records, in order, plus the
            # tamper-evidence verdict from the hash chain. The trail is
            # identifier-free (INV-8): field ids, hashes, actors, timestamps,
            # and — for egress records — the de-identified outbound facts
            # (codes, bands, tokens), never raw chart text. Safe to return.
            try:
                trail = case.get("audit", [])
                broken = audit_mod.verify_chain(trail)
                return self._send_json({
                    "audit": [dict(r) for r in trail],
                    "chain_ok": not broken,
                    "chain_broken_at": broken,
                })
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
                # Wave 4: privacy mode + INV-5 enrollment record + the live
                # obligations checklist ([] until enrolled — the duties
                # attach at the transition). patient_token is the
                # physician's own capability to hand the patient (the case
                # view already grants strictly more than the patient view).
                "mode": str(case.get("mode") or "PREPARATORY_REVIEW"),
                "enrollment": case.get("enrollment"),
                "obligations": _enrollment_obligations(case),
                "patient_token": case.get("patient_token"),
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
            # MAJOR-1: intake accepts ONLY schema field ids. An unknown key is a
            # client bug or a key/value swap; without this it would flow into the
            # commit's field_ids and thence into the append-only audit trail — a
            # durable INV-8 leak in the one structure that can never be edited.
            unknown = [k for k in payload["fields"] if k not in SCHEMA_FIELDS]
            if unknown:
                return self._send_json(
                    {"error": "unknown intake field id(s): %s — intake accepts only "
                     "the route's schema fields" % ", ".join(sorted(unknown)[:5]),
                     "unknown": sorted(unknown)}, 400)
            actor = _actor_str(payload)
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
                # MINOR-4: compute the response state INSIDE the lock so it can't
                # reflect a concurrent write. m6: carry the profile block so the
                # client's res.profile branch works without a follow-up GET.
                resp = {"ok": True, "intake_rev": case["intake_rev"],
                        "stale": _is_stale(case), "profile": _profile_block(case)}
            return self._send_json(resp)

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

        m = _CASE_MATCH.match(path)
        if m:
            case_id = m.group(1)
            case = self._case(case_id)
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            try:
                with _LOCK:
                    body = _match_payload(case)
                    _save_case(case_id)   # persists the egress_query audit records
                return self._send_json(body)
            except ProfileNotCommitted as exc:  # INV-3 hard gate: fail closed —
                # matching never runs on an unconfirmed input.
                return self._send_json({"error": "profile not committed",
                                        "pending": exc.pending,
                                        "state": exc.state}, 409)
            except Exception as exc:  # no chart content in error payloads
                return self._send_json({"error": type(exc).__name__}, 500)

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

        m = _CASE_RELEASE.match(path)
        if m:
            case_id = m.group(1)
            case = self._case(case_id)
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            payload = self._read_json()
            if payload is None or not isinstance(payload, dict):
                return self._send_json({"error": "expected a JSON object"}, 400)
            try:
                with _LOCK:
                    body, status = _release(case, payload)
                    if status == 200:
                        _save_case(case_id)
            except Exception as exc:  # no chart content in error payloads
                return self._send_json({"error": type(exc).__name__}, 500)
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

        m = _CASE_PATIENT_LINK.match(path)
        if m:
            case_id = m.group(1)
            case = self._case(case_id)
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            payload = self._read_json()
            if payload is None or not isinstance(payload, dict):
                return self._send_json({"error": "expected a JSON object"}, 400)
            try:
                with _LOCK:
                    body, status = _patient_link(case, payload)
                    if status == 200:
                        _save_case(case_id)
            except Exception as exc:  # no chart content in error payloads
                return self._send_json({"error": type(exc).__name__}, 500)
            return self._send_json(body, status)

        m = _CASE_PROMOTE.match(path)
        if m:
            case_id = m.group(1)
            case = self._case(case_id)
            if case is None:
                return self._send_json({"error": "unknown case"}, 404)
            payload = self._read_json()
            if payload is None or not isinstance(payload, dict):
                return self._send_json({"error": "expected a JSON object"}, 400)
            try:
                with _LOCK:
                    body, status = _promote(case, payload)
                    if status == 200:
                        _save_case(case_id)
            except Exception as exc:  # no chart content in error payloads
                return self._send_json({"error": type(exc).__name__}, 500)
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
