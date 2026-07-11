"""Rules-as-data: loader, check-verb vocabulary, and strategy executors.

Validation rules live in ``engine/registry/rules.json`` (versioned like
documents.json and gates.json), each carrying ``{citation, principle_text,
strategy}`` per the boundary doctrine in docs/VALIDATION-PHILOSOPHY.md:

- ``deterministic``  -- ``check`` names a verb in the small closed
  vocabulary below (fact-shaped properties: presence, structured-field
  equality, pending human determinations). New verbs require code review;
  new rules using existing verbs are data edits.
- ``provenance``     -- the property is factual BY CONSTRUCTION of
  generation: the named span/field carries a ProvenanceRecord tracing to
  its source (a verbatim-locked template span verified by SHA-256, or a
  study-record path the filled value must equal). No prose is inspected
  for meaning; origin and fidelity are the facts checked.
- ``concept``        -- never executed here. ``principle_text`` plus
  ``citation`` IS the check; these rules are handed to the concept
  reviewer (future review port). ``run_rules`` skips them.

The loader fails loudly at load time: a rule without a citation does not
ship (hard rule D4), and an unknown strategy or check verb is a registry
error, not a silent skip.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

from .generate import VERBATIM_SPANS
from .models import Document, Study

ENGINE_ROOT = Path(__file__).resolve().parent.parent
RULES_PATH = ENGINE_ROOT / "registry" / "rules.json"

VALID_STRATEGIES = ("deterministic", "provenance", "concept")

# Accept the execution plan's long-form names as aliases of the canonical
# short forms used in rules.json.
_STRATEGY_ALIASES = {
    "provenance-verified": "provenance",
    "concept-reviewed": "concept",
}


class RuleRegistryError(ValueError):
    """Raised when rules.json is malformed: missing citation, unknown
    strategy, or an unregistered check verb. Failing loudly at load time
    is the point -- a rule without a citation does not ship."""


@dataclass
class RuleSpec:
    """One validation rule, loaded from rules.json."""

    id: str
    description: str
    citation: str
    doc_id: Optional[str]              # None = study-level rule
    strategy: str                      # deterministic | provenance | concept
    principle_text: str = ""           # the concept the check stands in for
    check: Optional[str] = None        # verb name (deterministic/provenance)
    params: Dict = field(default_factory=dict)
    resolving_question: str = ""
    version: str = ""


# check functions return (passed, message, resolving_question_or_None)
CheckFn = Callable[[Study, Optional[Document], RuleSpec], Tuple[bool, str, Optional[str]]]


def _field_value(doc: Optional[Document], name: str) -> str:
    return (doc.fields.get(name, "") if doc else "").strip()


def _provenance_for(doc: Optional[Document], span: str):
    if doc is None:
        return None
    for record in doc.provenance:
        if record.span == span:
            return record
    return None


# ---------------------------------------------------------------------------
# Deterministic check verbs (closed vocabulary)
# ---------------------------------------------------------------------------

def _check_field_nonempty(study: Study, doc: Optional[Document], spec: RuleSpec):
    name = spec.params["field"]
    value = _field_value(doc, name)
    if value:
        pass_message = spec.params.get("pass_message", "Field '{field}' is present: {value}")
        return True, pass_message.format(field=name, value=value), None
    fail_message = spec.params.get("fail_message", "Required field '{field}' is missing or empty.")
    return False, fail_message.format(field=name), (spec.resolving_question or None)


def _check_fields_nonempty(study: Study, doc: Optional[Document], spec: RuleSpec):
    names = spec.params["fields"]
    missing = [n for n in names if not _field_value(doc, n)]
    if not missing:
        return True, spec.params.get("pass_message", "All required fields are present."), None
    fail_message = spec.params.get("fail_message", "Missing required field(s): {missing}.")
    return False, fail_message.format(missing=", ".join(missing)), (spec.resolving_question or None)


def _check_field_equals_study(study: Study, doc: Optional[Document], spec: RuleSpec):
    name = spec.params["field"]
    path = spec.params["path"]
    value = _field_value(doc, name)
    fact = study.fact(path)
    reference = fact.value if fact else None
    if value and reference is not None and value == reference:
        pass_message = spec.params.get("pass_message", "Field '{field}' matches the study record: {value}")
        return True, pass_message.format(field=name, value=value), None
    if value and reference is None:
        # The document carries a value but the study record has nothing at this
        # path to check it against — report the absence, not a None-valued
        # "mismatch" (which reads as if the study said None).
        absent_message = spec.params.get(
            "absent_message",
            "Field '{field}' is set to {value!r}, but the study record has no value "
            "at '{path}' to check it against.",
        )
        question = spec.params.get("absent_question") or spec.resolving_question or None
        return False, absent_message.format(field=name, value=value, path=path), question
    if value:
        mismatch_message = spec.params.get(
            "mismatch_message",
            "Field '{field}' ({value!r}) does not match the study record ({reference!r}).",
        )
        question = spec.params.get("mismatch_question") or spec.resolving_question or None
        return False, mismatch_message.format(field=name, value=value, reference=reference), question
    missing_message = spec.params.get("missing_message", "Field '{field}' is missing or empty.")
    question = spec.params.get("missing_question") or spec.resolving_question or None
    return False, missing_message.format(field=name), question


def _check_human_determination_pending(study: Study, doc: Optional[Document], spec: RuleSpec):
    """Every serious safety report needs a HUMAN causality determination.

    This verb never fills the determination -- it fails toward the
    'sae-causality' gate. That is the never-auto-resolve behavior.
    """
    pending = [r for r in study.safety_reports if r.serious and r.causality_determination is None]
    if not pending:
        return True, spec.params.get(
            "pass_message", "No serious safety report is awaiting a causality determination."
        ), None
    ids = ", ".join(r.report_id for r in pending)
    fail_message = spec.params.get(
        "fail_message",
        "{count} serious safety report(s) awaiting human determination: {ids}.",
    )
    question = spec.resolving_question.format(ids=ids) if spec.resolving_question else None
    return False, fail_message.format(count=len(pending), ids=ids), question


DETERMINISTIC_CHECKS: Dict[str, CheckFn] = {
    "field_nonempty": _check_field_nonempty,
    "fields_nonempty": _check_fields_nonempty,
    "field_equals_study": _check_field_equals_study,
    "human_determination_pending": _check_human_determination_pending,
}


# ---------------------------------------------------------------------------
# Provenance check verbs
# ---------------------------------------------------------------------------

def _check_verbatim_spans_present(study: Study, doc: Optional[Document], spec: RuleSpec):
    """Verify verbatim-locked template spans by provenance and hash.

    The property is factual by construction of generation: generate.py
    stamps a ProvenanceRecord for each registered verbatim span it
    rendered. This verb confirms (a) the canonical span text still
    matches its registered SHA-256 (nothing altered the lock), (b) the
    document carries the provenance record, and (c) the exact bytes are
    present in the rendered text. No proxy-word substring hunting.
    """
    span_ids = spec.params.get("spans", [])
    hashes = spec.params.get("sha256", {})
    registry = VERBATIM_SPANS.get(doc.doc_id, {}) if doc else {}
    problems: List[str] = []
    for span_id in span_ids:
        entry = registry.get(span_id)
        if entry is None:
            problems.append("%s (no canonical template span registered)" % span_id)
            continue
        text = entry[0]
        expected = hashes.get(span_id)
        if expected:
            actual = hashlib.sha256(text.encode("utf-8")).hexdigest()
            if actual != expected:
                problems.append("%s (canonical span text fails its registered SHA-256)" % span_id)
                continue
        if _provenance_for(doc, span_id) is None:
            problems.append("%s (no provenance record on the document)" % span_id)
            continue
        if doc is not None and text not in doc.rendered:
            problems.append("%s (verbatim span absent from the rendered document)" % span_id)
    if not problems:
        pass_message = spec.params.get(
            "pass_message", "All {count} verbatim span(s) verified by provenance and SHA-256."
        )
        return True, pass_message.format(count=len(span_ids)), None
    fail_message = spec.params.get("fail_message", "Verbatim span verification failed: {problems}")
    return False, fail_message.format(problems="; ".join(problems)), (spec.resolving_question or None)


def _check_field_traces_to_study(study: Study, doc: Optional[Document], spec: RuleSpec):
    """Verify a filled field traces to -- and equals -- a study-record fact.

    Origin and fidelity are the facts checked: the field carries a
    ProvenanceRecord whose source is the named study path, and the value
    equals the provenance-stamped StudyFact at that path. Whether an
    unusual value is APPROPRIATE is a human intake question, not a
    rendering-time whitelist.
    """
    name = spec.params["field"]
    source = spec.params["source"]
    value = _field_value(doc, name)
    question = spec.resolving_question or None
    if not value:
        missing_message = spec.params.get("missing_message", "Field '{field}' is missing or empty.")
        return False, missing_message.format(field=name, source=source), question
    record = _provenance_for(doc, name)
    if record is None or not record.source.startswith(source + " = "):
        untraced_message = spec.params.get(
            "untraced_message",
            "Field '{field}' does not carry a provenance record tracing to study record path '{source}'.",
        )
        return False, untraced_message.format(field=name, source=source), question
    fact = study.fact(source)
    if fact is None:
        no_fact_message = spec.params.get(
            "no_fact_message", "The study record has no value at path '{source}'."
        )
        return False, no_fact_message.format(field=name, source=source), question
    if value != fact.value:
        mismatch_message = spec.params.get(
            "mismatch_message",
            "Field '{field}' ({value!r}) does not equal the study record fact at '{source}' ({reference!r}).",
        )
        return False, mismatch_message.format(field=name, source=source, value=value, reference=fact.value), question
    pass_message = spec.params.get(
        "pass_message", "Field '{field}' ({value}) traces to and equals study record '{source}'."
    )
    return True, pass_message.format(field=name, source=source, value=value), None


PROVENANCE_CHECKS: Dict[str, CheckFn] = {
    "verbatim_spans_present": _check_verbatim_spans_present,
    "field_traces_to_study": _check_field_traces_to_study,
}


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

_CACHE: Optional[List[RuleSpec]] = None


def load_rules(path: Optional[str] = None) -> List[RuleSpec]:
    """Load and validate rules.json. Fails loudly on a malformed registry.

    Enforced at load time:
    - every rule has a nonempty ``citation`` (a rule without a citation
      does not ship);
    - ``strategy`` is one of deterministic | provenance | concept;
    - deterministic and provenance rules name a check verb registered in
      this module's closed vocabulary;
    - concept rules carry ``principle_text`` (the principle IS the check);
    - rule ids are unique.
    """
    global _CACHE
    if path is None and _CACHE is not None:
        return _CACHE

    rules_path = Path(path) if path is not None else RULES_PATH
    with open(rules_path, encoding="utf-8") as f:
        entries = json.load(f)

    specs: List[RuleSpec] = []
    seen_ids = set()
    for entry in entries:
        rule_id = entry.get("id", "").strip()
        if not rule_id:
            raise RuleRegistryError("A rule in %s has no id." % rules_path)
        if rule_id in seen_ids:
            raise RuleRegistryError("Duplicate rule id %r in %s." % (rule_id, rules_path))
        seen_ids.add(rule_id)

        citation = str(entry.get("citation", "") or "").strip()
        if not citation:
            raise RuleRegistryError(
                "Rule %r lacks a citation. A rule without a citation does not "
                "ship (VALIDATION-PHILOSOPHY hard rule: citation presence)." % rule_id
            )

        strategy = str(entry.get("strategy", "") or "").strip()
        strategy = _STRATEGY_ALIASES.get(strategy, strategy)
        if strategy not in VALID_STRATEGIES:
            raise RuleRegistryError(
                "Rule %r has unknown strategy %r (expected one of %s)."
                % (rule_id, entry.get("strategy"), ", ".join(VALID_STRATEGIES))
            )

        check = entry.get("check")
        if strategy == "deterministic":
            if check not in DETERMINISTIC_CHECKS:
                raise RuleRegistryError(
                    "Rule %r: deterministic check verb %r is not in the closed "
                    "vocabulary (%s). New verbs require code review."
                    % (rule_id, check, ", ".join(sorted(DETERMINISTIC_CHECKS)))
                )
        elif strategy == "provenance":
            if check not in PROVENANCE_CHECKS:
                raise RuleRegistryError(
                    "Rule %r: provenance check verb %r is not registered (%s)."
                    % (rule_id, check, ", ".join(sorted(PROVENANCE_CHECKS)))
                )
        else:  # concept
            if not str(entry.get("principle_text", "") or "").strip():
                raise RuleRegistryError(
                    "Rule %r is concept-strategy but has no principle_text; "
                    "the principle plus citation IS the check." % rule_id
                )

        specs.append(
            RuleSpec(
                id=rule_id,
                description=str(entry.get("description", "") or ""),
                citation=citation,
                doc_id=entry.get("doc_id"),
                strategy=strategy,
                principle_text=str(entry.get("principle_text", "") or ""),
                check=check,
                params=entry.get("params", {}) or {},
                resolving_question=str(entry.get("resolving_question", "") or ""),
                version=str(entry.get("version", "") or ""),
            )
        )

    if path is None:
        _CACHE = specs
    return specs


def concept_rules(doc_id: Optional[str] = None) -> List[RuleSpec]:
    """Concept-strategy rules for the (future) reviewer port.

    ``run_rules`` never executes these; they are deferred to concept
    review. Filter by doc_id when given.
    """
    return [
        r for r in load_rules()
        if r.strategy == "concept" and (doc_id is None or r.doc_id == doc_id)
    ]


def execute_rule(spec: RuleSpec, study: Study, doc: Optional[Document]):
    """Dispatch a deterministic or provenance rule to its check verb.

    Concept rules are not executable here by design; attempting to is a
    registry error, not a silent pass.
    """
    if spec.strategy == "deterministic":
        fn = DETERMINISTIC_CHECKS[spec.check]
    elif spec.strategy == "provenance":
        fn = PROVENANCE_CHECKS[spec.check]
    else:
        raise RuleRegistryError(
            "Rule %r is concept-strategy: it is judged by the concept "
            "reviewer against its principle text, never executed as code." % spec.id
        )
    return fn(study, doc, spec)
