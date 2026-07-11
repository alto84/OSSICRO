"""INV-3: the committed profile — canonicalization, hashing, and the commit gate.

Pure stdlib (hashlib / json / unicodedata / datetime). No I/O, no network —
this module extends the ``TestEngineEgressBoundary`` surface.

The committed profile is the input-of-record: the flat dotted-key intake map
exactly as a named human confirmed it (HC1/HC5). This module stores VALUE
HASHES, never chart values (INV-8).

PRIVACY LIMIT — read before relying on this for real PHI. Every hashing
function here takes an optional ``key``. **Keyed mode (m14, Overhaul P9)** is
the deployment posture: the app keys every hash with HMAC-SHA256 under a
server-side secret held OUTSIDE the case JSON (``app/data/secret.key`` —
created on first run, never committed, never written into a case). A keyed
hash of an enumerable value is not recoverable by offline enumeration without
the key. **Unkeyed mode** (``key=None``, the pure-engine default used by
synthetic fixtures and engine tests) keeps the honest old claim: the hashes
are deterministic, domain-separated, and unkeyed, so a value drawn from a
low-entropy space (administrative sex, age, a date, a coded diagnosis, a name
from a finite formulary) is **recoverable by offline enumeration** against
``field_hashes`` / ``staged`` / ``history`` — a hash of an enumerable value is
not de-identification. Unkeyed committed profiles must therefore NOT be
treated as PHI-safe at rest, and keyed hashing is a stated PRECONDITION for
any non-synthetic pilot (docs/deployment/DEPLOYMENT-COMPLIANCE.md).

The two modes are mutually loud, never silently interchangeable: each commit
records its scheme tag (``hash_scheme``: "sha256-v1" unkeyed, "hmac-sha256-v1"
keyed) and the hash prefixes differ ("sha256:" vs "hmac-sha256:"), so a
profile committed under one scheme re-verified under another fails LOUD
(every field reads pending; require_committed refuses) instead of wrong.
Pending-detection and revert-equality semantics are unchanged under a key,
because only one party (the server) computes hashes with one key.

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
import hmac
import json
import unicodedata
from typing import Dict, List, Optional, Tuple

from .models import Document, GateViolation

__all__ = [
    "CANON_VERSION",
    "HASH_SCHEME_KEYED",
    "HASH_SCHEME_UNKEYED",
    "hash_scheme",
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

# m14 (Overhaul P9): the versioned hash-scheme tags. A committed profile
# records which scheme produced its hashes; the tag (and the differing hash
# prefixes) make a scheme mismatch fail loud — never a silent wrong match.
HASH_SCHEME_UNKEYED = "sha256-v1"       # pure-engine / synthetic-only default
HASH_SCHEME_KEYED = "hmac-sha256-v1"    # the m14 deployment posture


def hash_scheme(key: Optional[bytes] = None) -> str:
    """The scheme tag the given key produces (None -> unkeyed v1)."""
    return HASH_SCHEME_KEYED if key else HASH_SCHEME_UNKEYED


def _digest(preimage: str, key: Optional[bytes]) -> str:
    """One prefixed digest: HMAC-SHA256 under ``key`` when keyed (m14),
    plain SHA-256 when unkeyed. The prefixes differ so the two schemes can
    never silently compare equal."""
    data = preimage.encode("utf-8")
    if key:
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("hash key must be bytes (the server-side secret), "
                            "got %s" % type(key).__name__)
        return "hmac-sha256:" + hmac.new(bytes(key), data, hashlib.sha256).hexdigest()
    return "sha256:" + hashlib.sha256(data).hexdigest()


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


def profile_hash(flat: Dict[str, object], key: Optional[bytes] = None) -> str:
    """The profile hash: domain-separated, versioned digest over canonical
    JSON. Keyed (HMAC-SHA256, "hmac-sha256:" prefix) when ``key`` is given
    (m14); plain sha256 ("sha256:" prefix) otherwise."""
    return _digest(_PROFILE_DOMAIN + canonicalize_intake(flat), key)


def field_value_hash(value: object, key: Optional[bytes] = None) -> str:
    """Per-field value hash (pending detection + INV-8-clean storage).

    Keyed with HMAC-SHA256 under the server-side secret when ``key`` is given
    (m14 — enumeration-resistant at rest); unkeyed sha256 otherwise (the
    honest synthetic-only mode; see the module docstring's PRIVACY LIMIT).

    Raises ValueError on a value that canonicalizes to nothing — an absent
    value has no hash; absence is represented by the field's key not being
    in ``field_hashes`` at all.
    """
    canon = _canonical_value(value)
    if canon is None:
        raise ValueError("cannot hash an absent/blank value — absence is "
                         "represented by omission, not by a hash")
    return _digest(_FIELD_DOMAIN + canon, key)


# ---------------------------------------------------------------------------
# Pending-field computation (design §4) — computed on every read, never stored
# ---------------------------------------------------------------------------

def pending_fields(flat: Dict[str, object], committed: Dict[str, object],
                   key: Optional[bytes] = None) -> List[str]:
    """Field ids awaiting named re-confirmation against ``committed``.

    ``committed`` is the committed_profile dict; the caller handles None
    (UNCOMMITTED). Staged re-confirmations count toward the baseline; a
    staged _STAGED_ABSENT entry means a deletion was confirmed, so the key
    leaves the baseline.

    m14: current hashes are computed under ``key``. A profile committed
    under a DIFFERENT scheme (e.g. an old unkeyed commit re-verified by the
    keyed server) can never match — every field reads pending. That is the
    intended fail-loud behavior: the repair is a named re-confirmation /
    recommit, never a silent scheme bridge.
    """
    current = {k: field_value_hash(v, key) for k, v in canonical_items(flat)}
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
                   prior: Optional[Dict[str, object]] = None,
                   key: Optional[bytes] = None) -> Dict[str, object]:
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
    new_hash = profile_hash(flat, key)
    if prior is not None:
        still_pending = pending_fields(flat, prior, key)
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
        # m14: the versioned scheme tag — which hashing produced this commit.
        # A re-verify under a different scheme fails loud, never wrong.
        "hash_scheme": hash_scheme(key),
        "profile_hash": new_hash,
        "field_hashes": {k: field_value_hash(v, key) for k, v in items},
        "committed_by": actor.strip(),
        "committed_at": _utcnow(),
        "intake_rev_at_commit": None,
        "staged": {},
        "history": history,
    }


def confirm_fields(flat: Dict[str, object], committed: Dict[str, object],
                   actor: str, field_ids: List[str],
                   key: Optional[bytes] = None) -> Dict[str, object]:
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
    pending = pending_fields(flat, committed, key)
    current = dict(canonical_items(flat))
    staged = dict(committed.get("staged", {}))
    for field_id in field_ids:
        if field_id not in pending:
            raise ValueError(
                "field %r is not pending re-confirmation — nothing to confirm"
                % field_id
            )
        if field_id in current:
            staged[field_id] = field_value_hash(current[field_id], key)
        else:
            staged[field_id] = _STAGED_ABSENT   # named confirmation of removal
    updated = dict(committed)
    updated["staged"] = staged
    if pending_fields(flat, updated, key):
        return updated
    return commit_profile(flat, actor, prior=updated, key=key)


def require_committed(flat: Dict[str, object],
                      committed: Optional[Dict[str, object]],
                      key: Optional[bytes] = None) -> str:
    """The generate/package gate: the committed hash, or a structured refusal.

    Returns the committed profile_hash iff a commit exists AND the current
    intake's hash equals it. Otherwise raises ProfileNotCommitted carrying
    the derived state and the pending field ids — fail closed, never
    generate on refusal (state-machine guarantee 5). m14: a commit recorded
    under a different hash scheme can never match — it fails loud here
    (every field pending) and the repair is a named recommit.
    """
    if committed is None:
        raise ProfileNotCommitted(pending=[], state="UNCOMMITTED")
    if profile_hash(flat, key) != committed.get("profile_hash"):
        raise ProfileNotCommitted(
            pending=pending_fields(flat, committed, key), state="CONFIRMING"
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
