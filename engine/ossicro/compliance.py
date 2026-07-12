"""COMPLIANCE MAP: artifact -> governing authority -> validation -> gate.

The compliance map is the citation-carrying manifest (strategy item 6): for
every required document it records the governing citations, the validation
rules that touched it and whether they passed, and the non-delegable human
gate (and responsible role) that guards it. It asserts what authority governs
each artifact and which human is accountable -- never that software made an
accountable decision.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .models import Document, Gate, Study


@dataclass
class ComplianceEntry:
    doc_id: str
    title: str
    present: bool
    citations: List[str] = field(default_factory=list)
    gate_id: Optional[str] = None
    gate_name: Optional[str] = None
    gate_role: Optional[str] = None
    gate_citation: Optional[str] = None
    rules: List[dict] = field(default_factory=list)  # {rule_id, passed, citation}


@dataclass
class ComplianceMap:
    entries: List[ComplianceEntry]
    study_level_rules: List[dict]  # {rule_id, passed, citation, message}


def build_compliance_map(
    study: Study,
    documents: Dict[str, Document],
    doc_registry: Dict[str, dict],
    gate_registry: Dict[str, Gate],
    rule_results: list,
) -> ComplianceMap:
    by_doc: Dict[str, list] = {}
    study_level: List[dict] = []
    for r in rule_results:
        if r.doc_id:
            by_doc.setdefault(r.doc_id, []).append(r)
        else:
            study_level.append(
                {"rule_id": r.rule_id, "passed": r.passed, "citation": r.citation, "message": r.message}
            )

    entries: List[ComplianceEntry] = []
    for doc_id in study.required_documents:
        entry = doc_registry.get(doc_id, {})
        gate_id = entry.get("gate")
        if gate_id and gate_id not in gate_registry:
            raise KeyError(
                "document %r references gate %r not in the gate registry "
                "(typo or stale entry)." % (doc_id, gate_id))
        gate = gate_registry.get(gate_id) if gate_id else None
        entries.append(
            ComplianceEntry(
                doc_id=doc_id,
                title=entry.get("title", doc_id),
                present=doc_id in documents,
                citations=list(entry.get("governing_citations", [])),
                gate_id=gate_id,
                gate_name=gate.name if gate else None,
                gate_role=gate.responsible_role if gate else None,
                gate_citation=gate.citation if gate else None,
                rules=[
                    {"rule_id": r.rule_id, "passed": r.passed, "citation": r.citation}
                    for r in by_doc.get(doc_id, [])
                ],
            )
        )
    return ComplianceMap(entries=entries, study_level_rules=study_level)
