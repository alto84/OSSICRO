"""Pipeline composition tests.

Run: `cd engine && python -m unittest tests.test_pipeline -v`.

Covers: run_check composes every layer over the sample fixture; concept/tripwire
findings escalate but NEVER clear a gate; the stub reviewer honors
validate_report (a finding inside a verbatim-locked span is dropped).
"""

import unittest

from ossicro.generate import (
    VERBATIM_SPANS,
    generate_builtin_documents,
    generate_document,
    import_existing_documents,
)
from ossicro.models import Document, Study
from ossicro.pipeline import CheckResult, run_check
from ossicro.registry import load_documents, load_fixture, load_gates
from ossicro.review_port import (
    ConceptFinding,
    DeterministicStubReviewer,
    ReviewReport,
    load_writing_principles,
    validate_report,
)


def build():
    raw = load_fixture()
    study = Study.from_dict(raw)
    doc_registry = load_documents()
    gate_registry = load_gates()
    documents = generate_builtin_documents(study, doc_registry)
    documents.update(import_existing_documents(study, doc_registry))
    return study, documents, doc_registry, gate_registry


def item(ledger, doc_id):
    return next(i for i in ledger if i.doc_id == doc_id)


class RunCheckComposition(unittest.TestCase):
    def test_returns_all_layers(self):
        study, documents, doc_registry, gate_registry = build()
        result = run_check(study, documents, doc_registry, gate_registry)
        self.assertIsInstance(result, CheckResult)
        self.assertTrue(result.ledger)
        self.assertTrue(result.rule_results)
        # every generated document was linted and concept-reviewed
        self.assertEqual(set(result.tripwire_by_doc), set(documents))
        self.assertEqual(set(result.concept_by_doc), set(documents))

    def test_ledger_preserves_base_semantics(self):
        # The known amber/green/red items from the fixture survive composition.
        study, documents, doc_registry, gate_registry = build()
        result = run_check(study, documents, doc_registry, gate_registry)
        self.assertEqual(item(result.ledger, "delegation-of-authority-log").status, "green")
        self.assertEqual(item(result.ledger, "form-fda-1572-statement-of-investigator").status, "amber")
        self.assertEqual(item(result.ledger, "form-fda-1571-ind-cover").status, "red")

    def test_gate_packet_lists_pending_human_gates(self):
        study, documents, doc_registry, gate_registry = build()
        result = run_check(study, documents, doc_registry, gate_registry)
        gate_ids = {g.gate_id for g in result.gate_packet}
        self.assertIn("1572-signature", gate_ids)
        self.assertIn("sae-causality", gate_ids)  # serious SAE, no determination


class EscalateOnly(unittest.TestCase):
    """Concept/tripwire findings may ADD reds; they never clear a gate."""

    def test_concept_finding_never_promotes_amber_to_green(self):
        study, documents, doc_registry, gate_registry = build()
        doc_id = "form-fda-1572-statement-of-investigator"

        class AlwaysClean(DeterministicStubReviewer):
            def review(self, text, doc, principles):
                return ReviewReport(model="always-clean")

        result = run_check(study, documents, doc_registry, gate_registry, reviewer=AlwaysClean())
        it = item(result.ledger, doc_id)
        # A pristine review does not discharge the signature gate.
        self.assertEqual(it.status, "amber")
        self.assertEqual(it.gate_id, "1572-signature")
        self.assertIn("1572-signature", {g.gate_id for g in result.gate_packet})

    def test_concept_deficiency_escalates_amber_to_red_but_keeps_gate(self):
        study, documents, doc_registry, gate_registry = build()
        doc_id = "form-fda-1572-statement-of-investigator"
        target = documents[doc_id]
        # Inject a real value present in the rendered doc so validate_report keeps it.
        quote = target.fields["investigator_name"]
        self.assertIn(quote, target.rendered)

        class FlagsPI(DeterministicStubReviewer):
            def review(self, text, doc, principles):
                if getattr(doc, "doc_id", "") == doc_id:
                    return ReviewReport(
                        model="flags-pi",
                        findings=[ConceptFinding("P2", "deficient", quote,
                                                 "promotional framing", "state plainly")],
                    )
                return ReviewReport(model="flags-pi")

        result = run_check(study, documents, doc_registry, gate_registry, reviewer=FlagsPI())
        it = item(result.ledger, doc_id)
        self.assertEqual(it.status, "red")            # escalated
        self.assertEqual(it.gate_id, "1572-signature")  # gate NOT dropped
        # gate still pending in the packet: a red concept finding cannot clear it
        self.assertIn("1572-signature", {g.gate_id for g in result.gate_packet})

    def test_tripwire_hard_finding_escalates_but_gate_stays(self):
        # A chat-residue hard finding on a gated doc turns it red; gate persists.
        study, documents, doc_registry, gate_registry = build()
        doc_id = "informed-consent-form-part50"
        documents[doc_id].rendered += "\nAs an AI, I hope this helps.\n"
        result = run_check(study, documents, doc_registry, gate_registry)
        it = item(result.ledger, doc_id)
        self.assertEqual(it.status, "red")
        self.assertEqual(it.gate_id, "informed-consent")
        self.assertIn("informed-consent", {g.gate_id for g in result.gate_packet})


class ValidateReportLockedSpans(unittest.TestCase):
    def _icf(self):
        raw = load_fixture()
        study = Study.from_dict(raw)
        doc_registry = load_documents()
        return generate_document(study, "informed-consent-form-part50", doc_registry)

    def test_finding_inside_locked_span_is_dropped(self):
        doc = self._icf()
        locked_text = VERBATIM_SPANS[doc.doc_id]["icf-element-2"][0]
        self.assertIn(locked_text, doc.rendered)
        # quote a substring that lies inside the locked span
        inside = locked_text.split(" - ")[0]
        report = ReviewReport(
            model="t",
            findings=[ConceptFinding("P2", "deficient", inside, "flagged locked prose")],
        )
        kept = validate_report(report, doc)
        self.assertEqual(kept.findings, [], "a finding inside a locked span must be dropped")

    def test_finding_on_filled_field_is_kept(self):
        doc = self._icf()
        quote = doc.fields["investigator_name"]
        self.assertIn(quote, doc.rendered)
        report = ReviewReport(
            model="t",
            findings=[ConceptFinding("P2", "advisory", quote, "editorial note")],
        )
        kept = validate_report(report, doc)
        self.assertEqual(len(kept.findings), 1)

    def test_finding_quoting_absent_text_is_dropped(self):
        doc = self._icf()
        report = ReviewReport(
            model="t",
            findings=[ConceptFinding("P2", "deficient", "text that is not in the document at all",
                                     "invented evidence")],
        )
        kept = validate_report(report, doc)
        self.assertEqual(kept.findings, [])

    def test_attribution_preserved(self):
        doc = self._icf()
        report = ReviewReport(model="model-x", findings=[], reviewed_at="2026-07-09T00:00:00Z")
        kept = validate_report(report, doc)
        self.assertEqual(kept.model, "model-x")
        self.assertEqual(kept.reviewed_at, "2026-07-09T00:00:00Z")


class StubReviewerHonorsLockedSpans(unittest.TestCase):
    def test_stub_output_survives_validation_without_locked_hits(self):
        # The real stub over the sample ICF must not, after validate_report,
        # carry any finding that lies inside a locked span.
        raw = load_fixture()
        study = Study.from_dict(raw)
        doc_registry = load_documents()
        doc = generate_document(study, "informed-consent-form-part50", doc_registry)
        reviewer = DeterministicStubReviewer()
        report = validate_report(reviewer.review(doc.rendered, doc, load_writing_principles()), doc)
        # Every surviving finding is a verbatim substring outside all locked ranges.
        from ossicro.review_port import _locked_ranges
        locked = _locked_ranges(doc)
        for f in report.findings:
            idx = doc.rendered.find(f.span)
            self.assertNotEqual(idx, -1)
            end = idx + len(f.span)
            self.assertFalse(any(idx < hi and end > lo for lo, hi in locked))


if __name__ == "__main__":
    unittest.main(verbosity=2)
