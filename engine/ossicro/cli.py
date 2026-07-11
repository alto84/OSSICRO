"""OSSICRO engine command-line demo.

    cd engine && python -m ossicro.cli demo

Loads the sample study fixture, GENERATES the built-in draft documents,
CHECKS them (completeness ledger + cross-document consistency), VALIDATES
them (rule engine), builds the compliance map, and demonstrates that
non-delegable gates cannot be crossed programmatically. Everything printed
is a DRAFT for qualified human review.
"""

from __future__ import annotations

import sys

from . import gates as gate_ops
from .check import build_ledger, check_consistency, ledger_totals
from .compliance import build_compliance_map
from .generate import generate_builtin_documents, import_existing_documents
from .models import GateViolation, Study
from .registry import load_documents, load_fixture, load_gates
from .validate import run_rules

STATUS_TAG = {"green": "[ GREEN ]", "amber": "[ AMBER ]", "red": "[  RED  ]",
              "awaiting-external-party": "[AWAIT-EXT]"}


def _hr(title: str) -> None:
    print("\n" + "=" * 74)
    print(title)
    print("=" * 74)


def run_demo() -> int:
    raw = load_fixture()
    study = Study.from_dict(raw)
    doc_registry = load_documents()
    gate_registry = load_gates()

    documents = generate_builtin_documents(study, doc_registry)
    documents.update(import_existing_documents(study, doc_registry))

    rule_results = run_rules(study, documents)
    inconsistencies = check_consistency(study, documents)
    ledger = build_ledger(study, documents, doc_registry, rule_results, inconsistencies)
    totals = ledger_totals(ledger)
    cmap = build_compliance_map(study, documents, doc_registry, gate_registry, rule_results)

    _hr("OSSICRO ENGINE - GENERATE / CHECK / VALIDATE  (DRAFT for human review)")
    print("Study:      %s" % study.title)
    print("Study ID:   %s   Phase: %s   IND: %s" % (study.study_id, study.phase, study.ind_number))
    print("Protocol:   %s v%s" % (study.protocol_number, study.protocol_version))
    print("Investigator (sponsor-investigator): %s" % study.investigator.name)
    print("Documents generated/imported: %d of %d required"
          % (len(documents), len(study.required_documents)))

    _hr("COMPLETENESS LEDGER  (green=validated  amber=awaiting human gate  "
        "await-ext=awaiting external party  red=action needed)")
    print("  GREEN %d   AMBER %d   AWAIT-EXT %d   RED %d\n"
          % (totals["green"], totals["amber"],
             totals["awaiting-external-party"], totals["red"]))
    for item in ledger:
        print("%s  %s" % (STATUS_TAG.get(item.status, item.status), item.title))
        if item.gate_id and item.status == "amber":
            print("            gate: %s (a qualified human must execute this)" % item.gate_id)
        for q in item.questions:
            print("            - %s" % q)

    _hr("CROSS-DOCUMENT CONSISTENCY")
    if not inconsistencies:
        print("  No identity-critical inconsistencies detected.")
    for f in inconsistencies:
        print("  ! %s" % f.question)
        print("    implicated: %s" % ", ".join(f.implicated_docs()))

    _hr("VALIDATION RULES")
    for r in rule_results:
        mark = "PASS" if r.passed else "FAIL"
        scope = r.doc_id or "(study-level)"
        print("  [%s] %-14s %s  <%s>" % (mark, r.rule_id, r.message, r.citation))
        if not r.passed and r.resolving_question:
            print("         -> %s" % r.resolving_question)

    _hr("COMPLIANCE MAP  (artifact -> authority -> validation -> accountable human)")
    for e in cmap.entries:
        pres = "present" if e.present else "MISSING"
        print("  %s  [%s]" % (e.title, pres))
        if e.citations:
            print("      authority: %s" % "; ".join(e.citations))
        if e.gate_id:
            print("      non-delegable gate: %s -> %s (%s)"
                  % (e.gate_name, e.gate_role, e.gate_citation))
        for rr in e.rules:
            print("      rule %s: %s" % (rr["rule_id"], "PASS" if rr["passed"] else "FAIL"))
    if cmap.study_level_rules:
        print("  study-level:")
        for rr in cmap.study_level_rules:
            print("      rule %s: %s  <%s>"
                  % (rr["rule_id"], "PASS" if rr["passed"] else "FAIL", rr["citation"]))

    _hr("HARD LINE - GATE ENFORCEMENT DEMONSTRATION (Form FDA 1572)")
    doc = documents["form-fda-1572-statement-of-investigator"]
    doc.advance("in_review")
    doc.advance("approved")
    print("  Document is complete and approved for signature; attempting to finalize")
    print("  it programmatically (i.e., software signs the 1572)...")
    try:
        gate_ops.finalize(doc, gate_registry)
        print("  !! ERROR: finalized without a human sign-off - this must never happen.")
        return 1
    except GateViolation as exc:
        print("  REFUSED (correct):")
        for line in str(exc).split(". "):
            print("      %s" % line.strip())
    print("\n  Recording the named investigator's sign-off (a human act), then finalizing:")
    gate_ops.record_signoff(
        doc, gate_registry,
        person=study.investigator.name, role="investigator",
        statement=("I agree to conduct the study per the protocol, 21 CFR Part 50, "
                   "and 21 CFR Part 56, and I sign this Statement of Investigator."),
    )
    gate_ops.finalize(doc, gate_registry)
    print("      Form 1572 state -> %s (signed by %s)" % (doc.state, study.investigator.name))

    _hr("SUMMARY")
    print("  Every document above is a DRAFT prepared for qualified human review.")
    print("  OSSICRO drafts, checks, validates, times, and version-controls the")
    print("  documentation. It NEVER performs a non-delegable act: informed consent,")
    print("  IRB approval, SAE causality, statistical sign-off, or the 1571/1572")
    print("  signatures. Those remain with the accountable humans, by law.")
    return 0


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "demo"
    if cmd == "demo":
        return run_demo()
    print("usage: python -m ossicro.cli demo")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
