"""INV-3: the committed profile — canonicalization, hashing, and the commit gate.

Pure stdlib (hashlib / json / unicodedata / datetime). No I/O, no network —
this module extends the ``TestEngineEgressBoundary`` surface.

The committed profile is the input-of-record: the flat dotted-key intake map
exactly as a named human confirmed it (HC1/HC5). This module stores VALUE
HASHES, never chart values (INV-8).

PRIVACY LIMIT — read before relying on this for real PHI. The per-field hashes
are deterministic, domain-separated, and **unkeyed**. A value drawn from a
low-entropy space (administrative sex, age, a date, a coded diagnosis, a name
from a finite formulary) is therefore **recoverable by offline enumeration**
against ``field_hashes`` / ``staged`` / ``history`` — a hash of an enumerable
value is not de-identification. This is acceptable for the current
synthetic-only fixtures (no real PHI anywhere), but the object must NOT be
treated as PHI-safe at rest. The hardening is to key the field hashes with
HMAC-SHA256 under a server-side secret held OUTSIDE the case JSON
(``field_value_hash(value, key)``); pending-detection and revert-equality are
unchanged because only the server computes hashes. That keying rides the
authentication work (design Q3 / INV-7 tail); until then, the honest claim is
the one stated here, not "leaks nothing".

Commit is ATTRIBUTION, not a gate sign-off. It deliberately does not touch
``models.HumanSignoff`` / ``gates.record_signoff`` — those are the
non-delegable regulatory acts. A commit with a blank actor raises
``GateViolation`` (a nameless commit is software executing a human act);
an *uncommitted* profile at generate time raises ``ProfileNotCommitted``,
which is a user-fixable workflow state, NOT a GateViolation.

Per-case profile state machine (derived, never stored as a string):

    UNCOMMITTED   committed_profile is None
    COMMITTED     committed_profile set and pending_fields() == []
    CONFIRMING    committed_profile set and pending_fields() != []
"""

from __future__ import annotations

import datetime
import hashlib
import json
import unicodedata
from typing import Dict, List, Optional, Tuple

from .models import Document, GateViolation

__all__ = [
    "CANON_VERSION",
    "ProfileNotCommitted",
    "canonical_items",
    "canonicalize_intake",
    "profile_hash",
    "field_value_hash",
    "pending_fields",
    "commit_profile",
    "confirm_fields",
    "require_committed",
    "stamp_input_hash",
]

CANON_VERSION = 1

# Domain-separated, versioned preimage prefixes: a future canonicalization
# change bumps the version and can never silently collide with v1 hashes.
_PROFILE_DOMAIN = "ossicro-profile-v1\n"
_FIELD_DOMAIN = "ossicro-field-v1\n"

# Sentinel stored in ``staged`` when a named human confirms a field's REMOVAL
# (a deleted fact is a change to the input-of-record too). Empty string can
# never be a real field hash ("sha256:…"), so it is unambiguous.
_STAGED_ABSENT = ""


class ProfileNotCommitted(Exception):
    """The profile is not committed (or has drifted from its commit).

    A structured, user-fixable refusal — NOT a GateViolation. Carries the
    derived state and the pending field ids so the caller can render the
    exact repair instruction (mirrors TriggerDateError's field-carrying
    pattern).
    """

    def __init__(self, pending: Optional[List[str]] = None, state: str = "UNCOMMITTED"):
        self.pending: List[str] = sorted(pending or [])
        self.state = state
        if state == "UNCOMMITTED":
            msg = ("Profile never committed — a named human must commit the "
                   "intake profile before generation (INV-3 / HC1).")
        else:
            msg = ("Profile has changed since it was committed — a named human "
                   "must re-confirm the changed fields: %s (INV-3)."
                   % (", ".join(self.pending) or "(none listed)"))
        super().__init__(msg)


def _utcnow() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Canonicalization (design §2)
# ---------------------------------------------------------------------------

def _canonical_value(value: object) -> Optional[str]:
    """Canonical text form of one intake value, or None if it drops out.

    Mirrors the server's store rule (blanks stay honestly absent), then:
    non-string values take their JSON text form (True -> "true", 3 -> "3");
    strings are used as-is; NFC + whitespace collapse is HASH-ONLY (stored
    intake and generated documents keep the user's original text).
    """
    if value is None:
        return None
    if isinstance(value, str):
        if value.strip() == "":
            return None
        text = value
    else:
        text = json.dumps(value, sort_keys=True, ensure_ascii=True)
    text = unicodedata.normalize("NFC", text)
    text = " ".join(text.split())
    if text == "":
        return None
    return text


def canonical_items(flat: Dict[str, object]) -> List[Tuple[str, str]]:
    """Sorted (key, canonical_value) pairs; dropped entries omitted.

    Keys are taken verbatim (a wrong key is a different field — the hash
    must not paper over key typos).
    """
    items: List[Tuple[str, str]] = []
    for key, value in flat.items():
        canon = _canonical_value(value)
        if canon is None:
            continue
        items.append((str(key), canon))
    items.sort(key=lambda kv: kv[0])
    return items


def canonicalize_intake(flat: Dict[str, object]) -> str:
    """Canonical JSON text of the flat intake (design §2 step 3, sans prefix)."""
    return json.dumps(dict(canonical_items(flat)), sort_keys=True,
                      separators=(",", ":"), ensure_ascii=True)


def profile_hash(flat: Dict[str, object]) -> str:
    """The profile hash: domain-separated, versioned sha256 over canonical JSON."""
    preimage = _PROFILE_DOMAIN + canonicalize_intake(flat)
    return "sha256:" + hashlib.sha256(preimage.encode("utf-8")).hexdigest()


def field_value_hash(value: object) -> str:
    """Per-field value hash (pending detection + INV-8-clean storage).

    Raises ValueError on a value that canonicalizes to nothing — an absent
    value has no hash; absence is represented by the field's key not being
    in ``field_hashes`` at all.
    """
    canon = _canonical_value(value)
    if canon is None:
        raise ValueError("cannot hash an absent/blank value — absence is "
                         "represented by omission, not by a hash")
    preimage = _FIELD_DOMAIN + canon
    return "sha256:" + hashlib.sha256(preimage.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Pending-field computation (design §4) — computed on every read, never stored
# ---------------------------------------------------------------------------

def pending_fields(flat: Dict[str, object], committed: Dict[str, object]) -> List[str]:
    """Field ids awaiting named re-confirmation against ``committed``.

    ``committed`` is the committed_profile dict; the caller handles None
    (UNCOMMITTED). Staged re-confirmations count toward the baseline; a
    staged _STAGED_ABSENT entry means a deletion was confirmed, so the key
    leaves the baseline.
    """
    current = {k: field_value_hash(v) for k, v in canonical_items(flat)}
    baseline = dict(committed.get("field_hashes", {}))
    for key, staged_hash in committed.get("staged", {}).items():
        if staged_hash == _STAGED_ABSENT:
            baseline.pop(key, None)       # confirmed-removed
        else:
            baseline[key] = staged_hash   # confirmed new value
    changed = [k for k, h in current.items() if baseline.get(k) != h]  # added/edited
    removed = [k for k in baseline if k not in current]                # deleted fields
    return sorted(set(changed) | set(removed))


# ---------------------------------------------------------------------------
# Commit / confirm (design §§3-5)
# ---------------------------------------------------------------------------

def commit_profile(flat: Dict[str, object], actor: str,
                   prior: Optional[Dict[str, object]] = None) -> Dict[str, object]:
    """Commit the whole current intake as the input-of-record (HC1/HC5).

    Returns a NEW committed_profile dict. Raises GateViolation on a blank
    actor (a nameless commit is software executing a human act — that
    refusal is correct behavior), on an empty canonical intake (nothing to
    commit), or when ``prior`` exists with unconfirmed pending fields (those
    must go through confirm_fields — per-field ceremony on re-confirmation).

    ``intake_rev_at_commit`` is left None here (the counter lives at the app
    boundary); the caller stamps it.
    """
    if not (actor or "").strip():
        raise GateViolation(
            "Profile commit requires a named human actor — software cannot "
            "commit the input-of-record (HC1/HC5)."
        )
    items = canonical_items(flat)
    if not items:
        raise GateViolation(
            "Profile commit refused: the intake is empty — there is no "
            "input-of-record to commit."
        )
    reconfirmed: List[str] = []
    history: List[Dict[str, object]] = []
    new_hash = profile_hash(flat)
    if prior is not None:
        still_pending = pending_fields(flat, prior)
        if still_pending:
            raise GateViolation(
                "Profile commit refused: changed fields await named "
                "re-confirmation (%s) — confirm them via confirm_fields."
                % ", ".join(still_pending)
            )
        reconfirmed = sorted(prior.get("staged", {}).keys())
        history = list(prior.get("history", []))
        # m2: an idempotent recommit (same hash, nothing re-confirmed) does not
        # supersede anything — don't pile a duplicate history entry (audit noise).
        if new_hash != prior.get("profile_hash") or reconfirmed:
            history.append({
                "profile_hash": prior.get("profile_hash"),
                "committed_by": prior.get("committed_by"),
                "committed_at": prior.get("committed_at"),
                "intake_rev_at_commit": prior.get("intake_rev_at_commit"),
                "reconfirmed_fields": reconfirmed,
            })
    return {
        "canon_version": CANON_VERSION,
        "profile_hash": new_hash,
        "field_hashes": {k: field_value_hash(v) for k, v in items},
        "committed_by": actor.strip(),
        "committed_at": _utcnow(),
        "intake_rev_at_commit": None,
        "staged": {},
        "history": history,
    }


def confirm_fields(flat: Dict[str, object], committed: Dict[str, object],
                   actor: str, field_ids: List[str]) -> Dict[str, object]:
    """Stage named re-confirmations for pending fields (per-field ceremony).

    Raises GateViolation on a blank actor and ValueError on a field id that
    is not currently pending (fail loud, no silent no-op). If staging drains
    the pending set, auto-recommits: returns commit_profile(flat, actor,
    prior) — a NEW profile hash, the prior commit pushed to history with
    its reconfirmed_fields. Otherwise returns a copy of ``committed`` with
    the updated ``staged`` ledger.
    """
    if not (actor or "").strip():
        raise GateViolation(
            "Field re-confirmation requires a named human actor (HC1/HC5)."
        )
    pending = pending_fields(flat, committed)
    current = dict(canonical_items(flat))
    staged = dict(committed.get("staged", {}))
    for field_id in field_ids:
        if field_id not in pending:
            raise ValueError(
                "field %r is not pending re-confirmation — nothing to confirm"
                % field_id
            )
        if field_id in current:
            staged[field_id] = field_value_hash(current[field_id])
        else:
            staged[field_id] = _STAGED_ABSENT   # named confirmation of removal
    updated = dict(committed)
    updated["staged"] = staged
    if pending_fields(flat, updated):
        return updated
    return commit_profile(flat, actor, prior=updated)


def require_committed(flat: Dict[str, object],
                      committed: Optional[Dict[str, object]]) -> str:
    """The generate/package gate: the committed hash, or a structured refusal.

    Returns the committed profile_hash iff a commit exists AND the current
    intake's hash equals it. Otherwise raises ProfileNotCommitted carrying
    the derived state and the pending field ids — fail closed, never
    generate on refusal (state-machine guarantee 5).
    """
    if committed is None:
        raise ProfileNotCommitted(pending=[], state="UNCOMMITTED")
    if profile_hash(flat) != committed.get("profile_hash"):
        raise ProfileNotCommitted(
            pending=pending_fields(flat, committed), state="CONFIRMING"
        )
    return committed["profile_hash"]


# ---------------------------------------------------------------------------
# Provenance stamping (design §6) — one post-pass, one stamping site
# ---------------------------------------------------------------------------

def stamp_input_hash(documents: Dict[str, Document], input_hash: str) -> None:
    """Stamp ``input_hash`` on every Document and every ProvenanceRecord.

    The caller passes the hash of the intake ACTUALLY CONSUMED by this
    generation (on the gated generate/package paths that equals the
    committed hash by construction; on /check it is the true, possibly
    drifted, hash) — a provenance record never claims a committed input it
    did not have.
    """
    for doc in documents.values():
        doc.input_hash = input_hash
        for rec in doc.provenance:
            rec.input_hash = input_hash
