"""I-AUDIT: the append-only audit log (BUILD-PLAN Wave 1).

Pure stdlib (dataclasses / datetime / types). No I/O, no network — this
module extends the ``TestEngineEgressBoundary`` surface.

The audit log records WHAT happened, WHO did it (a named human where the
act has one — HC1/HC5), WHEN, and the input fingerprint. It records field
ids, actions, actors, timestamps, and input hashes — **NEVER chart values**
(INV-8). The caller owns that contract at the call site; this module
enforces the shape (flat detail of primitives / lists of strings, no nested
objects) so an accidental value-bearing blob is refused loudly.

The trail itself is a plain list of JSON-serializable dicts — it persists
inside the case JSON as ``case["audit"]``. The API surface is APPEND and
READ only: there is no update, no delete. Immutability is enforced at that
surface — ``append`` never touches existing entries and deep-copies what it
stores (a caller's later mutation of its own detail dict cannot reach the
trail), and ``read`` returns frozen ``AuditRecord`` views (frozen dataclass,
mappingproxy detail, lists frozen to tuples) so nothing handed out can
mutate the trail.

``append`` takes an ARBITRARY action string on purpose: later waves write
to this same trail (INV-4 egress ``egress_query``, INV-5 enrollment
``promote``, the cross-persona ``release`` act) without touching this
module.
"""

from __future__ import annotations

import copy
import datetime
import hashlib
import json
from dataclasses import dataclass
from types import MappingProxyType
from typing import Dict, List, Mapping, Optional

__all__ = ["AuditRecord", "append", "read", "last_seq", "verify_chain"]

# Tamper-evidence: each record binds the previous record's hash (MINOR-7).
# The API is append-only by construction; the chain makes that *checkable* —
# altering or removing any record breaks every hash after it, so a direct file
# edit or an in-process bug that rewrites history is detectable, not silent.
# (This is the Part-11 substrate the wiki anticipates; cheap now, costly to
# retrofit once real trails exist.)
_CHAIN_PREFIX = "ossicro-audit-v1\n"

# Detail values may be primitives or flat lists of strings (field ids,
# doc ids). Nested dicts / lists-of-objects are refused: a flat shape keeps
# the INV-8 surface reviewable at every call site.
_DETAIL_SCALARS = (str, int, float, bool, type(None))


@dataclass(frozen=True)
class AuditRecord:
    """One immutable audit event. Ids / hashes / names / times — no values."""

    seq: int          # 1-based, strictly increasing within a trail
    at: str           # UTC timestamp, YYYY-MM-DDTHH:MM:SSZ
    actor: str        # named human where the act has one; "" = honest absence
    action: str       # arbitrary verb: commit / reconfirm / signoff / bundle_loaded / ...
    target: str       # what the act touched (a doc id, "committed-profile", ...)
    input_hash: str   # the input fingerprint where one exists, else ""
    detail: Mapping[str, object]   # flat, value-free metadata (field ids, counts)
    prev_hash: str = ""            # rec_hash of the preceding record ("" for the first)
    rec_hash: str = ""             # sha256 over this record's content + prev_hash


def _utcnow() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _check_detail(detail: Dict[str, object]) -> None:
    for key, value in detail.items():
        if not isinstance(key, str):
            raise ValueError("audit detail keys must be strings, got %r" % (key,))
        if isinstance(value, _DETAIL_SCALARS):
            continue
        if isinstance(value, (list, tuple)) and all(isinstance(v, str) for v in value):
            continue
        raise ValueError(
            "audit detail %r must be a primitive or a flat list of strings "
            "(INV-8: ids and counts only, never structured chart content)" % key
        )


def _record_hash(prev_hash: str, seq: int, at: str, actor: str, action: str,
                 target: str, input_hash: str, detail: Dict[str, object]) -> str:
    preimage = _CHAIN_PREFIX + json.dumps(
        {"seq": seq, "at": at, "actor": actor, "action": action, "target": target,
         "input_hash": input_hash, "detail": detail, "prev_hash": prev_hash},
        sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)
    return "sha256:" + hashlib.sha256(preimage.encode("utf-8")).hexdigest()


def verify_chain(trail: List[dict]) -> List[int]:
    """Return the seqs of records whose hash chain is broken (empty = intact).

    Recomputes each record's ``rec_hash`` from its content + the prior record's
    stored ``rec_hash``; any record that was altered, reordered, or inserted, or
    whose predecessor was, shows up here. A pure verification — no mutation.
    """
    broken, prev = [], ""
    for rec in trail:
        if not isinstance(rec, dict):
            broken.append(rec if isinstance(rec, int) else -1)
            continue
        expect = _record_hash(prev, rec.get("seq", 0), rec.get("at", ""),
                              rec.get("actor", ""), rec.get("action", ""),
                              rec.get("target", ""), rec.get("input_hash", ""),
                              dict(rec.get("detail") or {}))
        if rec.get("rec_hash") != expect or rec.get("prev_hash", "") != prev:
            broken.append(rec.get("seq", -1))
        prev = rec.get("rec_hash", "")
    return broken


def last_seq(trail: List[dict]) -> int:
    """The highest seq in the trail (0 for an empty trail).

    Uses the last record's seq, not len(): seq stays strictly increasing
    even over a trail that lost entries to corruption elsewhere.
    """
    if not trail:
        return 0
    last = trail[-1]
    try:
        return int(last.get("seq", len(trail)))
    except (TypeError, ValueError, AttributeError):
        return len(trail)


def append(trail: List[dict], actor: str, action: str, target: str = "",
           input_hash: str = "", detail: Optional[Dict[str, object]] = None,
           at: Optional[str] = None) -> AuditRecord:
    """Append one immutable record to the trail; returns the frozen view.

    The ONLY write operation this module offers. Never reads back into,
    mutates, or removes existing entries. Raises ValueError on a blank
    action or a detail that violates the flat/value-free shape.
    """
    if not isinstance(trail, list):
        raise ValueError("audit trail must be a list (case['audit'])")
    if not (action or "").strip():
        raise ValueError("audit records require an action")
    detail = dict(detail or {})
    _check_detail(detail)
    prev_hash = str(trail[-1].get("rec_hash", "")) if trail else ""
    seq = last_seq(trail) + 1
    at = at or _utcnow()
    actor = str(actor or "")
    action = action.strip()
    target = str(target or "")
    input_hash = str(input_hash or "")
    stored_detail = copy.deepcopy(detail)  # caller's dict can never mutate the trail
    record = {
        "seq": seq, "at": at, "actor": actor, "action": action,
        "target": target, "input_hash": input_hash, "detail": stored_detail,
        "prev_hash": prev_hash,
        "rec_hash": _record_hash(prev_hash, seq, at, actor, action, target,
                                 input_hash, stored_detail),
    }
    trail.append(record)
    return _freeze(record)


def read(trail: List[dict]) -> List[AuditRecord]:
    """Frozen views of every record, in order. Mutating a view is impossible
    (frozen dataclass / mappingproxy / tuples), and the views are copies —
    nothing handed out aliases the stored trail."""
    return [_freeze(rec) for rec in trail]


def _freeze(record: dict) -> AuditRecord:
    detail = {}
    for key, value in dict(record.get("detail") or {}).items():
        detail[key] = tuple(value) if isinstance(value, list) else value
    return AuditRecord(
        seq=record.get("seq", 0),
        at=record.get("at", ""),
        actor=record.get("actor", ""),
        action=record.get("action", ""),
        target=record.get("target", ""),
        input_hash=record.get("input_hash", ""),
        detail=MappingProxyType(detail),
        prev_hash=record.get("prev_hash", ""),
        rec_hash=record.get("rec_hash", ""),
    )
