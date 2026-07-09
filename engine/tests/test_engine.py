"""Engine tests. Run: `cd engine && python -m unittest tests.test_engine -v`."""

import unittest

from ossicro import gates as gate_ops
from ossicro.check import build_ledger, check_consistency
from ossicro.generate import generate_builtin_documents, import_existing_documents
from ossicro.models import GateViolation, Study
from ossicro.registry import load_documents, load_fixture, load_gates
from ossicro.validate import run_rules


def build(raw=None):
    raw = raw if raw is not None else load_fixture()
    study = Study.from_dict(raw)
    doc_registry = load_documents()
    gate_registry = load_gates()
    documents = generate_builtin_documents(study, doc_registry)
    documents.update(import_existing_documents(study, doc_registry))
    rules = run_rules(study, documents)
    incon = check_consistency(study, documents)
    ledger = build_ledger(study, documents, doc_registry, rules, incon)
    return study, documents, doc_registry, gate_registry, rules, incon, ledger


def item(ledger, doc_id):
    return next(i for i in ledger if i.doc_id == doc_id)


class LedgerTests(unittest.TestCase):
    def test_amber_for_gated_complete_document(self):
        *_, ledger = build()
        it = item(ledger, "form-fda-1572-statement-of-investigator")
        self.assertEqual(it.status, "amber")
        self.assertEqual(it.gate_id, "1572-signature")

    def test_green_for_complete_ungated_document(self):
        *_, ledger = build()
        self.assertEqual(item(ledger, "delegation-of-authority-log").status, "green")

    def test_red_for_missing_required_field_with_question(self):
        *_, ledger = build()  # fixture omits contacts.monitor_phone
        it = item(ledger, "form-fda-1571-ind-cover")
        self.assertEqual(it.status, "red")
        self.assertTrue(any("contact_phone" in q for q in it.questions))

    def test_red_for_missing_document(self):
        *_, ledger = build()
        self.assertEqual(item(ledger, "investigators-brochure").status, "red")


class GateTests(unittest.TestCase):
    def test_gate_blocks_then_allows_finalize(self):
        _, documents, _, gate_registry, *_ = build()
        doc = documents["form-fda-1572-statement-of-investigator"]
        doc.advance("in_review")
        doc.advance("approved")
        with self.assertRaises(GateViolation):
            gate_ops.finalize(doc, gate_registry)
        gate_ops.record_signoff(
            doc, gate_registry, person="Jordan A. Rivera, MD", role="investigator",
            statement="I sign the Statement of Investigator.",
        )
        gate_ops.finalize(doc, gate_registry)
        self.assertEqual(doc.state, "final")

    def test_wrong_role_signoff_refused(self):
        _, documents, _, gate_registry, *_ = build()
        doc = documents["form-fda-1572-statement-of-investigator"]
        with self.assertRaises(GateViolation):
            gate_ops.record_signoff(
                doc, gate_registry, person="Coordinator", role="coordinator",
                statement="attempting on behalf of PI",
            )


class ValidationTests(unittest.TestCase):
    def test_rule_fails_when_1572_lacks_irb(self):
        raw = load_fixture()
        raw["irb"]["name"] = ""
        _, _, _, _, rules, *_ = build(raw)
        r = next(x for x in rules if x.rule_id == "R-1572-IRB")
        self.assertFalse(r.passed)
        self.assertIn("IRB", r.resolving_question)

    def test_sae_causality_rule_is_never_auto_resolved(self):
        _, _, _, _, rules, *_ = build()
        r = next(x for x in rules if x.rule_id == "R-SAE-CAUSALITY")
        self.assertFalse(r.passed)  # a serious SAE with no human determination


class ConsistencyTests(unittest.TestCase):
    def test_protocol_version_mismatch_caught(self):
        study, documents, *_ = build()
        incon = check_consistency(study, documents)
        fields = {f.field_name for f in incon}
        self.assertIn("protocol_version", fields)


if __name__ == "__main__":
    unittest.main(verbosity=2)
