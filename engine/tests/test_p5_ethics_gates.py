"""Overhaul P5 — ethics-gate honesty, engine half.

Covers:
  - m8: ``Document.advance("final")`` refuses OUTRIGHT for gated documents —
    even with a recorded sign-off — so ``gates.finalize`` (which verifies a
    VALID sign-off) is the only path to 'final' by code, not convention.
    Ungated documents advance normally.
  - M13 (engine half): ``gates.record_signoff`` accepts and stores the
    ``evidence`` kwargs on the HumanSignoff record, verbatim.
  - M14: the IRB concurrence request's consent sentence is COMPUTED from
    route emergency + ``consent.timing_attestation`` (pathway-true), with
    the honest MISSING marker when the attestation was never entered, and
    is provenance-stamped like ``pathway_statement``.
  - m1: the sae-causality gate carries the display label
    "physician-sponsor / medical monitor" while its role-MATCHING key stays
    "medical-monitor" (sign-off validation is untouched).

Run: `cd engine && python -m unittest tests.test_p5_ethics_gates -v`.
"""

import json
import unittest
from pathlib import Path

from ossicro import ea_generators, gates, routes
from ossicro.ea_generators import build_study
from ossicro.models import Document, GateViolation, HumanSignoff
from ossicro.registry import load_documents, load_gates

ENGINE_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_PATH = ENGINE_ROOT / "fixtures" / "ea_sample_case.json"

GATE_REGISTRY = load_gates()
DOC_REGISTRY = load_documents()


def _sample_fields():
    data = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    return dict(data.get("fields", data))


def _irb_request(extra=None, emergency=False):
    fields = _sample_fields()
    if emergency:
        fields["submission.emergency"] = "true"
        fields.setdefault("submission.emergency_auth_datetime", "2026-06-26")
        fields.setdefault("submission.first_treatment_date", "2026-07-06")
    fields.pop("consent.timing_attestation", None)
    if extra:
        for key, value in extra.items():
            if value is None:
                fields.pop(key, None)
            else:
                fields[key] = value
    route = routes.route_for_emergency(emergency)
    study = build_study(fields, route)
    return ea_generators.gen_irb_request(study, DOC_REGISTRY)


# ---------------------------------------------------------------------------
# m8 — advance("final") refuses outright for gated documents
# ---------------------------------------------------------------------------

class AdvanceFinalRefusalTests(unittest.TestCase):

    def _gated_doc(self):
        return Document(doc_id="expanded-access-cover-letter",
                        title="Cover letter", gate_id="submission-to-fda")

    def test_advance_final_refused_without_signoff(self):
        doc = self._gated_doc()
        doc.advance("in_review")
        doc.advance("approved")
        with self.assertRaises(GateViolation):
            doc.advance("final")
        self.assertEqual(doc.state, "approved")

    def test_advance_final_refused_even_with_valid_signoff(self):
        # The m8 point: a recorded sign-off does NOT unlock advance("final").
        # finalize() is the only path, by code instead of by convention.
        doc = self._gated_doc()
        gates.record_signoff(
            doc, GATE_REGISTRY, person="Jordan A. Rivera, MD",
            role="sponsor-investigator",
            statement="I adopt this filing as my own submission to FDA.")
        doc.advance("in_review")
        doc.advance("approved")
        with self.assertRaises(GateViolation):
            doc.advance("final")
        self.assertEqual(doc.state, "approved")

    def test_finalize_remains_the_only_path(self):
        doc = self._gated_doc()
        gates.record_signoff(
            doc, GATE_REGISTRY, person="Jordan A. Rivera, MD",
            role="sponsor-investigator",
            statement="I adopt this filing as my own submission to FDA.")
        doc.advance("in_review")
        doc.advance("approved")
        gates.finalize(doc, GATE_REGISTRY)
        self.assertEqual(doc.state, "final")

    def test_finalize_still_refuses_without_valid_signoff(self):
        doc = self._gated_doc()
        doc.advance("in_review")
        doc.advance("approved")
        with self.assertRaises(GateViolation):
            gates.finalize(doc, GATE_REGISTRY)

    def test_ungated_document_advances_normally(self):
        doc = Document(doc_id="treatment-plan-notes", title="Notes")
        doc.advance("in_review")
        doc.advance("approved")
        doc.advance("final")
        self.assertEqual(doc.state, "final")


# ---------------------------------------------------------------------------
# M13 (engine half) — record_signoff stores the evidence facts
# ---------------------------------------------------------------------------

class SignoffEvidenceTests(unittest.TestCase):

    def test_evidence_stored_verbatim(self):
        doc = Document(doc_id="irb-concurrence-request",
                       title="IRB concurrence request", gate_id="irb-approval")
        signoff = gates.record_signoff(
            doc, GATE_REGISTRY, person="Alex B. Chen, MD", role="irb",
            statement="The chair concurred with this treatment use after review.",
            evidence={"concurrence_date": "2026-07-02",
                      "concurring_member": "Dr. P. Mfume (chair)",
                      "irb_reference": "MRB-2026-114"})
        self.assertEqual(signoff.evidence["concurrence_date"], "2026-07-02")
        self.assertEqual(signoff.evidence["concurring_member"],
                         "Dr. P. Mfume (chair)")
        self.assertEqual(signoff.evidence["irb_reference"], "MRB-2026-114")
        self.assertIs(doc.signoffs[-1], signoff)

    def test_evidence_defaults_to_empty_honest_absence(self):
        doc = Document(doc_id="informed-consent-form-part50",
                       title="ICF", gate_id="informed-consent")
        signoff = gates.record_signoff(
            doc, GATE_REGISTRY, person="Jordan A. Rivera, MD",
            role="investigator",
            statement="I obtained the patient's written informed consent today.")
        self.assertEqual(signoff.evidence, {})

    def test_dataclass_default_is_empty_dict(self):
        so = HumanSignoff(gate_id="informed-consent", person="A", role="investigator",
                          statement="s")
        self.assertEqual(so.evidence, {})


# ---------------------------------------------------------------------------
# M14 — the pathway-true consent sentence in the IRB request
# ---------------------------------------------------------------------------

class IrbConsentSentenceTests(unittest.TestCase):

    FIXED_LINE = ("Informed consent per 21 CFR Part 50 will be obtained "
                  "before treatment begins.")

    def test_non_emergency_future_tense(self):
        doc = _irb_request(emergency=False)
        self.assertIn(self.FIXED_LINE, doc.rendered)
        self.assertNotIn("[[MISSING: consent.timing_attestation]]", doc.rendered)

    def test_emergency_obtained_before_treatment_past_tense(self):
        doc = _irb_request(
            extra={"consent.timing_attestation": "obtained-before-treatment"},
            emergency=True)
        self.assertIn("was obtained before the emergency treatment began",
                      doc.rendered)
        self.assertIn("obtained-before-treatment", doc.rendered)
        self.assertNotIn(self.FIXED_LINE, doc.rendered)

    def test_emergency_5023_exception_statement(self):
        doc = _irb_request(
            extra={"consent.timing_attestation": "exception-50.23-documented"},
            emergency=True)
        self.assertIn("was not obtained before this emergency use", doc.rendered)
        self.assertIn("21 CFR 50.23", doc.rendered)
        self.assertNotIn(self.FIXED_LINE, doc.rendered)

    def test_emergency_not_yet_obtained_states_the_gap(self):
        doc = _irb_request(
            extra={"consent.timing_attestation": "not-yet-obtained"},
            emergency=True)
        self.assertIn("NOT yet been obtained", doc.rendered)
        self.assertNotIn(self.FIXED_LINE, doc.rendered)

    def test_emergency_absent_attestation_renders_missing_marker(self):
        # HC2: never assert what was not entered — the emergency route with
        # no attestation renders the explicit MISSING marker naming the
        # intake field, never the (possibly false) fixed sentence.
        doc = _irb_request(emergency=True)
        self.assertIn("[[MISSING: consent.timing_attestation]]", doc.rendered)
        self.assertNotIn(self.FIXED_LINE, doc.rendered)
        self.assertNotIn("consent_statement", doc.fields)

    def test_consent_statement_is_provenance_stamped(self):
        # Like pathway_statement: a computed literal with its computation
        # recorded as the source, and the citation from the single-source
        # table (50.20 / 50.23).
        doc = _irb_request(emergency=False)
        recs = [r for r in doc.provenance if r.span == "consent_statement"]
        self.assertEqual(len(recs), 1)
        self.assertIn("consent.timing_attestation", recs[0].source)
        self.assertIn("computed from", recs[0].source)
        self.assertIn("21 CFR 50.20", recs[0].citation)
        self.assertIn("21 CFR 50.23", recs[0].citation)


# ---------------------------------------------------------------------------
# m1 — sae-causality display label; role-matching key unchanged
# ---------------------------------------------------------------------------

class SaeCausalityLabelTests(unittest.TestCase):

    def test_display_label_and_unchanged_key(self):
        gate = GATE_REGISTRY["sae-causality"]
        self.assertEqual(gate.responsible_role, "medical-monitor")
        self.assertEqual(gate.responsible_role_label,
                         "physician-sponsor / medical monitor")
        self.assertEqual(gate.role_label, "physician-sponsor / medical monitor")

    def test_other_gates_fall_back_to_the_key(self):
        gate = GATE_REGISTRY["informed-consent"]
        self.assertEqual(gate.responsible_role_label, "")
        self.assertEqual(gate.role_label, gate.responsible_role)

    def test_role_matching_still_uses_the_key(self):
        # The label is display-only: causality determinations still require
        # the 'medical-monitor' role key, and the label is refused.
        from ossicro.models import SafetyReport
        report = SafetyReport(report_id="SAE-1", subject_code="PT-1",
                              event_term="event", onset_date="2026-07-01")
        with self.assertRaises(GateViolation):
            gates.record_causality_determination(
                report, GATE_REGISTRY, person="A. Doctor, MD",
                role="physician-sponsor / medical monitor",
                statement="Assessed as not related.")
        signoff = gates.record_causality_determination(
            report, GATE_REGISTRY, person="A. Doctor, MD",
            role="medical-monitor", statement="Assessed as not related.")
        self.assertEqual(signoff.role, "medical-monitor")


if __name__ == "__main__":
    unittest.main(verbosity=2)
