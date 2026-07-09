"""Registry loading: documents.json, gates.json, and fixtures.

Paths are resolved relative to this package's parent (the engine root),
so the engine works from any current working directory.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .models import Gate

ENGINE_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_DIR = ENGINE_ROOT / "registry"
FIXTURES_DIR = ENGINE_ROOT / "fixtures"


def load_documents() -> Dict[str, Dict[str, Any]]:
    """Return the document registry keyed by document id."""
    with open(REGISTRY_DIR / "documents.json", encoding="utf-8") as f:
        entries = json.load(f)
    return {e["id"]: e for e in entries}


def load_gates() -> Dict[str, Gate]:
    """Return the non-delegable gate registry keyed by gate id."""
    with open(REGISTRY_DIR / "gates.json", encoding="utf-8") as f:
        entries = json.load(f)
    return {e["id"]: Gate(**e) for e in entries}


def load_fixture(name: str = "sample_study.json") -> Dict[str, Any]:
    """Load a study fixture from engine/fixtures/."""
    with open(FIXTURES_DIR / name, encoding="utf-8") as f:
        return json.load(f)
