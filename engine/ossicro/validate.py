"""VALIDATE pass: rule execution over the rules-as-data registry.

Rules live in ``engine/registry/rules.json`` (see ossicro.rules for the
loader and the closed check-verb vocabulary), each carrying
``{citation, principle_text, strategy}``:

- ``deterministic`` rules check fact-shaped properties (field presence,
  structured-field equality against the study record, pending human
  determinations).
- ``provenance`` rules verify properties that are factual BY CONSTRUCTION
  of generation -- a verbatim-locked template span (SHA-256 + provenance
  record) or a filled field tracing to and equalling a study-record fact.
  No prose is inspected for meaning.
- ``concept`` rules are never executed here: the principle text plus its
  citation is handed to the concept reviewer (future review port).
  ``run_rules`` skips them; a skipped concept rule is deferred judgment,
  not a pass.

Rules NEVER auto-resolve a gate: a rule that touches an accountable act
fails toward the gate (with a resolving question that routes to the
responsible human), it never executes the act.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from .models import Document, Study
from .rules import RuleSpec, concept_rules, execute_rule, load_rules

__all__ = ["RuleResult", "run_rules", "load_rules", "concept_rules", "RuleSpec"]


@dataclass
class RuleResult:
    rule_id: str
    doc_id: Optional[str]
    passed: bool
    message: str
    citation: str
    resolving_question: Optional[str] = None


def run_rules(study: Study, documents: Dict[str, Document]) -> List[RuleResult]:
    """Run every applicable deterministic and provenance rule.

    Document rules only run when the target document is present (its
    absence is the ledger's red, not a rule fail). Concept-strategy rules
    are skipped: they belong to the concept reviewer, and this executor
    has no authority over them.
    """
    results: List[RuleResult] = []
    for spec in load_rules():
        if spec.strategy == "concept":
            continue  # deferred to the concept reviewer; never run as code
        if spec.doc_id is not None:
            doc = documents.get(spec.doc_id)
            if doc is None:
                continue
        else:
            doc = None
        passed, message, question = execute_rule(spec, study, doc)
        results.append(
            RuleResult(
                rule_id=spec.id,
                doc_id=spec.doc_id,
                passed=passed,
                message=message,
                citation=spec.citation,
                resolving_question=question,
            )
        )
    return results
