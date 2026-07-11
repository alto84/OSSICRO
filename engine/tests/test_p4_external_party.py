"""Overhaul P4 — external-party document model (the manufacturer concern).

Covers, end-to-end in the engine:
  - the LOA ledger state machine (M2): required fields filled but no
    recorded receipt -> ``awaiting-external-party``; receipt DATE alone is
    not enough; date + signatory recorded -> green with the receipt note
    (plus the optional document hash); a missing required field still wins
    as red; totals carry the fourth bucket;
  - the generic author_party rule: a non-physician-authored document can
    never be green on intake completeness alone;
  - ``submission_ready`` consults the external fact (M2): the LOA branch
    blocks until ``manufacturer.loa_received_date`` is recorded; the no-IND
    division-contact branch is the alternative; the package payload carries
    ``human_acts_outstanding`` (unsigned gates + awaiting-external-party
    docs) so readiness is never a bare boolean (ethics 9);
  - enclosure honesty: the cover letter encloses the LOA "upon receipt";
  - gen_loa_request triage completeness (M15): urgency literal, quantity /
    license / shipping / IRB-status / charging lines, 312.8 routed through
    the single-source citation table, honest MISSING markers;
  - gen_loa (m4): letterhead block from manufacturer.address; signatory /
    sections-excluded / effective-expiration terms honestly MISSING until
    the manufacturer supplies them.

Run: `cd engine && python -m unittest tests.test_p4_external_party -v`.
"""

import datetime
import json
import unittest
from pathlib import Path

from ossicro import citations, ea_generators, routes
from ossicro.assemble import assemble_submission
from ossicro.check import (
    AWAITING_EXTERNAL_PARTY,
    EXTERNAL_RECEIPT_FACTS,
    build_ledger,
    ledger_totals,
)
from ossicro.citations import cite
from ossicro.ea_generators import build_study, generate_route_documents
from ossicro.models import Document, Study
from ossicro.pipeline import run_check
from ossicro.registry import load_documents, load_gates

ENGINE_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_PATH = ENGINE_ROOT / "fixtures" / "ea_sample_case.json"

D = datetime.date
LOA = "manufacturer-letter-of-authorization"


def _sample_fields():
    data = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    return dict(data.get("fields", data))


def _build_case(fields):
    emergency = str(fields.get("submission.emergency", "")).strip().lower() in ("true", "1", "yes")
    route = routes.route_for_emergency(emergency)
    study = build_study(fields, route)
    documents = generate_route_documents(study, route, load_documents())
    return study, documents, route


def _ledger_item(fields, doc_id=LOA):
    study, documents, _route = _build_case(fields)
    result = run_check(study, documents, load_documents(), load_gates())
    return next(i for i in result.ledger if i.doc_id == doc_id)


class LoaLedgerStateMachineTests(unittest.TestCase):
    """draft -> awaiting-external-party -> green on the recorded fact."""

    def test_complete_intake_without_receipt_is_awaiting_external_party(self):
        fields = _sample_fields()
        del fields["manufacturer.loa_received_date"]
        del fields["manufacturer.loa_signatory"]
        item = _ledger_item(fields)
        self.assertEqual(item.status, AWAITING_EXTERNAL_PARTY)
        # the spec-fixed resolving question
        self.assertEqual(item.questions, [EXTERNAL_RECEIPT_FACTS[LOA]["question"]])
        self.assertIn("OSSICRO's draft for their review", item.questions[0])

    def test_receipt_date_alone_is_not_green(self):
        fields = _sample_fields()
        del fields["manufacturer.loa_signatory"]
        item = _ledger_item(fields)
        self.assertEqual(item.status, AWAITING_EXTERNAL_PARTY)

    def test_recorded_date_and_signatory_turn_green_with_receipt_note(self):
        item = _ledger_item(_sample_fields())
        self.assertEqual(item.status, "green")
        note = " ".join(item.notes)
        self.assertIn("received, signed instrument recorded", note)
        self.assertIn("Dana Q. Example", note)
        self.assertIn("2026-06-20", note)

    def test_optional_document_hash_carried_into_the_note(self):
        fields = _sample_fields()
        fields["manufacturer.loa_document_sha256"] = "a" * 64
        item = _ledger_item(fields)
        self.assertEqual(item.status, "green")
        self.assertIn("document sha256 " + "a" * 64, " ".join(item.notes))

    def test_missing_required_field_still_wins_as_red(self):
        fields = _sample_fields()
        del fields["manufacturer.ind_dmf_reference"]
        item = _ledger_item(fields)
        self.assertEqual(item.status, "red")

    def test_totals_gain_the_fourth_bucket(self):
        fields = _sample_fields()
        del fields["manufacturer.loa_received_date"]
        study, documents, _route = _build_case(fields)
        result = run_check(study, documents, load_documents(), load_gates())
        totals = ledger_totals(result.ledger)
        self.assertIn(AWAITING_EXTERNAL_PARTY, totals)
        self.assertEqual(totals[AWAITING_EXTERNAL_PARTY], 1)
        # and the bucket is present (0) even when nothing is awaiting
        study, documents, _route = _build_case(_sample_fields())
        result = run_check(study, documents, load_documents(), load_gates())
        self.assertEqual(ledger_totals(result.ledger)[AWAITING_EXTERNAL_PARTY], 0)

    def test_generic_external_doc_never_green_on_intake_alone(self):
        # An ungated document whose author_party is not the physician — and
        # which has no receipt-fact contract — parks at
        # awaiting-external-party even with every required field filled.
        study = Study.from_dict({"required_documents": ["ext-doc"]})
        doc = Document(doc_id="ext-doc", title="External Instrument",
                       fields={"a_field": "filled"}, rendered="x")
        registry = {"ext-doc": {"id": "ext-doc", "title": "External Instrument",
                                "author_party": "irb",
                                "required_fields": ["a_field"], "gate": None}}
        ledger = build_ledger(study, {"ext-doc": doc}, registry)
        self.assertEqual(ledger[0].status, AWAITING_EXTERNAL_PARTY)
        self.assertIn("authored/signed by the irb", ledger[0].questions[0])


class SubmissionReadyMatrixTests(unittest.TestCase):
    """assemble_submission consults the recorded external fact (M2)."""

    def _pkg(self, fields):
        study, documents, route = _build_case(fields)
        return assemble_submission(study, documents, route,
                                   load_documents(), load_gates())

    def test_sample_with_recorded_loa_is_ready(self):
        pkg = self._pkg(_sample_fields())
        self.assertTrue(pkg["submission_ready"])
        self.assertEqual(pkg["blocking"], [])

    def test_loa_branch_blocks_until_receipt_recorded(self):
        fields = _sample_fields()
        del fields["manufacturer.loa_received_date"]
        pkg = self._pkg(fields)
        self.assertFalse(pkg["submission_ready"])
        messages = [b["message"] for b in pkg["blocking"]]
        self.assertIn(
            "Manufacturer LOA not yet received (recorded fact required; the "
            "no-IND division-contact branch is the alternative).", messages)

    def test_division_contact_branch_is_the_alternative(self):
        fields = _sample_fields()
        del fields["manufacturer.ind_dmf_reference"]
        del fields["manufacturer.loa_received_date"]
        del fields["manufacturer.loa_signatory"]
        fields["manufacturer.ind_on_file"] = "false"
        fields["manufacturer.fda_division_contact"] = (
            "Spoke with Division of Oncology 1 on 2026-06-10; supporting "
            "information list recorded.")
        pkg = self._pkg(fields)
        titles = [b["title"] for b in pkg["blocking"]]
        self.assertNotIn("Manufacturer LOA receipt", titles)
        self.assertNotIn("Manufacturer cross-reference", titles)

    def test_human_acts_outstanding_counts_gates_and_external_docs(self):
        fields = _sample_fields()
        del fields["manufacturer.loa_received_date"]
        pkg = self._pkg(fields)
        acts = pkg["human_acts_outstanding"]
        kinds = {a["kind"] for a in acts}
        self.assertEqual(kinds, {"gate", "external-party"})
        ext = [a for a in acts if a["kind"] == "external-party"]
        self.assertEqual([a["id"] for a in ext], [LOA])
        self.assertEqual(ext[0]["who"], "manufacturer")
        gate_ids = {a["id"] for a in acts if a["kind"] == "gate"}
        self.assertIn("submission-to-fda", gate_ids)
        self.assertIn("informed-consent", gate_ids)
        # ready package still names the outstanding HUMAN acts — never a
        # bare boolean (ethics 9)
        ready = self._pkg(_sample_fields())
        self.assertTrue(ready["submission_ready"])
        self.assertTrue(ready["human_acts_outstanding"])
        self.assertTrue(all(a["kind"] == "gate"
                            for a in ready["human_acts_outstanding"]))


class EnclosureHonestyTests(unittest.TestCase):
    def test_cover_letter_encloses_loa_upon_receipt(self):
        study, documents, _route = _build_case(_sample_fields())
        rendered = documents["expanded-access-cover-letter"].rendered
        self.assertIn("Letter of Authorization (enclosed upon receipt from "
                      "the manufacturer)", rendered.replace("\n   ", " "))


class LoaRequestTriageTests(unittest.TestCase):
    """M15: the LOA request carries everything Medical Affairs triages on."""

    def _render(self, fields):
        route = routes.route_for_emergency(
            str(fields.get("submission.emergency", "")).strip().lower() in ("true", "1", "yes"))
        study = build_study(dict(fields), route)
        return ea_generators.gen_loa_request(study, load_documents(),
                                             as_of=D(2026, 7, 10))

    def test_non_emergency_urgency_literal_with_needed_by(self):
        rendered = self._render(_sample_fields()).rendered
        self.assertIn("URGENCY: Non-emergency request — drug needed by "
                      "2026-07-20 (physician-entered)", rendered)

    def test_emergency_urgency_literal(self):
        fields = _sample_fields()
        fields["submission.emergency"] = "true"
        rendered = self._render(fields).rendered
        self.assertIn("URGENCY: EMERGENCY REQUEST (21 CFR 312.310(d))", rendered)

    def test_triage_lines_render_from_intake(self):
        rendered = self._render(_sample_fields()).rendered
        self.assertIn("Quantity requested: Two 28-day cycles' supply", rendered)
        self.assertIn("Medical license: 036-114520 (IL)", rendered)
        self.assertIn("Shipping destination (treatment facility): "
                      "Fictional Oncology Associates, Rivertown, IL", rendered)
        self.assertIn("age 58", rendered)
        self.assertIn("sex Female", rendered)
        self.assertIn("IRB status: Midwest Regional IRB — chair-concurrence "
                      "pathway requested in lieu of a convened board "
                      "(21 CFR 56.105)", rendered)

    def test_charging_line_cites_312_8_via_the_table(self):
        # First appearance of 312.8 in a rendered doc — via the single-source
        # citation table (P1 discipline), never a string literal.
        self.assertEqual(cite("charging.expanded_access"), "21 CFR 312.8")
        doc = self._render(_sample_fields())
        self.assertIn("Charging / cost recovery (%s):"
                      % cite("charging.expanded_access"), doc.rendered)
        self.assertIn("no cost recovery under 21 CFR 312.8 is requested",
                      doc.rendered)
        by_span = {p.span: p.citation for p in doc.provenance}
        self.assertEqual(by_span["cost_recovery_statement"],
                         cite("charging.expanded_access"))

    def test_missing_triage_values_render_missing_markers(self):
        fields = _sample_fields()
        del fields["drug.quantity_requested"]
        del fields["submission.needed_by_date"]
        del fields["submission.cost_recovery_statement"]
        rendered = self._render(fields).rendered
        self.assertIn("[[MISSING: quantity_requested]]", rendered)
        self.assertIn("[[MISSING: cost_recovery_statement]]", rendered)
        # urgency literal is computed, never MISSING; no needed-by suffix
        self.assertIn("URGENCY: Non-emergency request\n", rendered)
        self.assertNotIn("drug needed by", rendered)


class LoaDraftStructureTests(unittest.TestCase):
    """m4: the reference template's structure, honestly MISSING where only
    the manufacturer can supply the value."""

    def _render(self, fields):
        route = routes.route_for_emergency(False)
        study = build_study(dict(fields), route)
        return ea_generators.gen_loa(study, load_documents(),
                                     as_of=D(2026, 7, 10)).rendered

    def test_letterhead_block_uses_manufacturer_address(self):
        rendered = self._render(_sample_fields())
        self.assertIn("[LETTERHEAD]", rendered)
        self.assertIn("One Discovery Way, Cambridge, MA 02100", rendered)

    def test_manufacturer_only_terms_render_missing(self):
        rendered = self._render(_sample_fields())
        self.assertIn("[[MISSING: sections_expressly_excluded]]", rendered)
        self.assertIn("[[MISSING: loa_effective_date]]", rendered)
        self.assertIn("[[MISSING: loa_expiration_or_revocation_terms]]", rendered)

    def test_signatory_fills_only_from_the_recorded_received_loa(self):
        rendered = self._render(_sample_fields())
        self.assertIn("Dana Q. Example, VP Regulatory Affairs", rendered)
        fields = _sample_fields()
        del fields["manufacturer.loa_signatory"]
        rendered = self._render(fields)
        self.assertIn("[[MISSING: loa_signatory]]", rendered)

    def test_external_party_marker_names_the_recorded_facts(self):
        rendered = self._render(_sample_fields())
        self.assertIn("EXTERNAL-PARTY ACT", rendered)
        self.assertIn("manufacturer.loa_received_date", rendered)


if __name__ == "__main__":
    unittest.main(verbosity=2)
