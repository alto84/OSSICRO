"""Registry loading: documents.json, gates.json, claims.json, and fixtures.

Paths are resolved relative to this package's parent (the engine root),
so the engine works from any current working directory.

PT-4 (Overhaul P2): every document entry carries ``author_party`` — who
authors/signs the real-world instrument the draft stands in for. The value
is a registry FACT, never an inference, and the loader fails closed on a
missing or unknown value. Buckets (exactly four, a P2 contract later
packages consume): ``physician`` (the treating physician / sponsor-
investigator's own hand), ``manufacturer`` (the commercial sponsor /
manufacturer side, including CRO functions acting for the sponsor), ``irb``
(independent oversight bodies — the IRB, and the DSMB by analogy), ``fda``.

PT-3 (Overhaul P2): ``load_claims`` loads the single-source registry of
cross-cutting user-facing claims (engine/registry/claims.json). Each claim
has exactly one authored copy — the app renders from this registry and a
tripwire test fails if a claim's distinctive text reappears hardcoded.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .models import Gate

ENGINE_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_DIR = ENGINE_ROOT / "registry"
FIXTURES_DIR = ENGINE_ROOT / "fixtures"

# The PT-4 author/signer enum — a declared contract (Overhaul P2 spec item 3).
AUTHOR_PARTIES = ("physician", "manufacturer", "irb", "fda")

# Keys every claims.json entry must carry, each non-empty (PT-3).
_CLAIM_REQUIRED_KEYS = ("id", "text", "true_when", "tripwire")


class RegistryError(ValueError):
    """A registry file failed validation — the loader fails closed."""


def _require_author_party(entry: Dict[str, Any]) -> None:
    """Fail closed unless the entry carries a valid ``author_party`` (PT-4)."""
    party = entry.get("author_party")
    if party not in AUTHOR_PARTIES:
        raise RegistryError(
            "documents.json entry %r: author_party %r is missing or not one of "
            "%s. Who authors/signs the real-world instrument is a registry "
            "fact (PT-4) — the loader refuses to guess it."
            % (entry.get("id"), party, "/".join(AUTHOR_PARTIES))
        )


def load_documents() -> Dict[str, Dict[str, Any]]:
    """Return the document registry keyed by document id.

    Validates the PT-4 ``author_party`` enum on every entry and fails closed
    (RegistryError) on a missing or unknown value.
    """
    with open(REGISTRY_DIR / "documents.json", encoding="utf-8") as f:
        entries = json.load(f)
    for entry in entries:
        _require_author_party(entry)
    return {e["id"]: e for e in entries}


def load_gates() -> Dict[str, Gate]:
    """Return the non-delegable gate registry keyed by gate id."""
    with open(REGISTRY_DIR / "gates.json", encoding="utf-8") as f:
        entries = json.load(f)
    return {e["id"]: Gate(**e) for e in entries}


def _validate_claim_entry(entry: Dict[str, Any]) -> None:
    """Fail closed unless the claim entry carries every required key (PT-3)."""
    for key in _CLAIM_REQUIRED_KEYS:
        if not str(entry.get(key, "") or "").strip():
            raise RegistryError(
                "claims.json entry %r: %r is missing or blank — every "
                "registered claim carries id, canonical text, its truth "
                "conditions, and the duplication-tripwire literal (PT-3)."
                % (entry.get("id"), key)
            )


def load_claims() -> Dict[str, Dict[str, Any]]:
    """Return the PT-3 claim registry keyed by claim id (fails closed)."""
    with open(REGISTRY_DIR / "claims.json", encoding="utf-8") as f:
        data = json.load(f)
    claims: Dict[str, Dict[str, Any]] = {}
    for entry in data.get("claims", []):
        _validate_claim_entry(entry)
        if entry["id"] in claims:
            raise RegistryError("claims.json: duplicate claim id %r" % entry["id"])
        claims[entry["id"]] = entry
    if not claims:
        raise RegistryError("claims.json carries no claims — refusing an "
                            "empty claim registry (PT-3).")
    return claims


def load_fixture(name: str = "sample_study.json") -> Dict[str, Any]:
    """Load a study fixture from engine/fixtures/."""
    with open(FIXTURES_DIR / name, encoding="utf-8") as f:
        return json.load(f)
