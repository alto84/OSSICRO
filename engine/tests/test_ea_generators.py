"""Overhaul P1 (M8 + [PT-2]) — citation-remap and single-source-table tests.

Pins every corrected 21 CFR 312.305(b)(2) pinpoint (the regulator persona's
off-by-one remap), proves the generators/registry route every remapped
pinpoint through the single-source table in ossicro.citations, and verifies
the HITL discipline: while any citation a document uses is still
PENDING-HUMAN-VERIFICATION, the rendered artifact carries the pending footer,
and the committed CITATION-INVENTORY.md matches the table.

Run: `cd engine && python -m unittest tests.test_ea_generators -v`.
"""

import datetime
import json
import unittest
from pathlib import Path

from ossicro import citations, ea_generators, routes
from ossicro.citations import cite
from ossicro.ea_generators import build_study
from ossicro.registry import load_documents

ENGINE_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = ENGINE_ROOT.parent
SAMPLE_PATH = ENGINE_ROOT / "fixtures" / "ea_sample_case.json"
INVENTORY_PATH = REPO_ROOT / "docs" / "regulatory" / "CITATION-INVENTORY.md"

D = datetime.date

# The corrected 312.305(b)(2) map (M8). PENDING-HUMAN-VERIFICATION until a
# qualified human initials the rows in ossicro.citations against eCFR.
CORRECTED_305B2 = {
    "ea.treatment_plan.rationale": "21 CFR 312.305(b)(2)(ii)",
    "ea.treatment_plan.patient_description": "21 CFR 312.305(b)(2)(iii)",
    "ea.treatment_plan.dosing": "21 CFR 312.305(b)(2)(iv)",
    "ea.treatment_plan.facility": "21 CFR 312.305(b)(2)(v)",
    "ea.treatment_plan.cmc": "21 CFR 312.305(b)(2)(vi)",
    "ea.treatment_plan.pharmtox": "21 CFR 312.305(b)(2)(vii)",
    "ea.treatment_plan.monitoring": "21 CFR 312.305(b)(2)(viii)",
}


def _sample_fields():
    data = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    return dict(data.get("fields", data))


def _gen(gen_name, fields=None, emergency=False):
    route = routes.route_for_emergency(emergency)
    study = build_study(fields or _sample_fields(), route)
    return getattr(ea_generators, gen_name)(study, load_documents(),
                                            as_of=D(2026, 7, 10))


class CitationTableTests(unittest.TestCase):
    def test_corrected_305b2_map(self):
        for key, pinpoint in CORRECTED_305B2.items():
            self.assertEqual(cite(key), pinpoint, key)

    def test_305b2_rows_start_pending_human_verification(self):
        # HITL: the M8 remap ships pending until a qualified human flips the
        # rows (with name + date) in the table itself.
        for key in CORRECTED_305B2:
            row = citations.CITATIONS[key]
            self.assertEqual(row.status, citations.PENDING_HUMAN_VERIFICATION, key)
        # The monitoring row records the (viii)-not-(iv) judgment call for
        # the human verifier.
        self.assertIn("JUDGMENT CALL",
                      citations.CITATIONS["ea.treatment_plan.monitoring"].note)

    def test_clock_citations_in_table(self):
        self.assertEqual(cite("clock.written_3926"), "21 CFR 312.310(d)(2)")
        self.assertEqual(cite("clock.irb_emergency_notification"), "21 CFR 56.104(c)")
        self.assertEqual(cite("clock.ind_effective_30_day"), "21 CFR 312.40(b)(1)")
        self.assertEqual(cite("clock.ind_annual_report"), "21 CFR 312.33")
        self.assertEqual(cite("clock.safety_report_15"), "21 CFR 312.32(c)(1)")
        self.assertEqual(cite("clock.safety_report_7"), "21 CFR 312.32(c)(2)")

    def test_cite_fails_loud_on_unknown_key(self):
        with self.assertRaises(KeyError):
            cite("no.such.citation")

    def test_cite_range(self):
        self.assertEqual(
            citations.cite_range("ea.treatment_plan.cmc", "ea.treatment_plan.pharmtox"),
            "21 CFR 312.305(b)(2)(vi)-(vii)")

    def test_committed_inventory_doc_matches_table(self):
        # docs/regulatory/CITATION-INVENTORY.md is the rendered table; the two
        # may never drift (regenerate with `python -m ossicro.citations`).
        committed = INVENTORY_PATH.read_text(encoding="utf-8")
        self.assertEqual(committed.replace("\r\n", "\n"),
                         citations.render_inventory())

    def test_inventory_lists_every_key_and_status(self):
        text = citations.render_inventory()
        for key, row in citations.CITATIONS.items():
            self.assertIn("`%s`" % key, text)
            self.assertIn(row.pinpoint, text)
        self.assertIn(citations.PENDING_HUMAN_VERIFICATION, text)


class TreatmentPlanPinpointTests(unittest.TestCase):
    """The rendered treatment plan's section headers carry the corrected
    sub-citations — all seven remapped elements, (ii) through (viii)."""

    def setUp(self):
        self.rendered = _gen("gen_treatment_plan").rendered

    def test_section_headers_carry_corrected_pinpoints(self):
        expected = [
            "1. RATIONALE FOR TREATMENT USE — 21 CFR 312.305(b)(2)(ii)",
            "2. PATIENT DESCRIPTION AND SELECTION — 21 CFR 312.305(b)(2)(iii)",
            "3. METHOD OF ADMINISTRATION, DOSE, AND DURATION — 21 CFR 312.305(b)(2)(iv)",
            "4. FACILITY AND PERSONNEL — 21 CFR 312.305(b)(2)(v)",
            "5. CMC; PHARMACOLOGY/TOXICOLOGY — 21 CFR 312.305(b)(2)(vi)-(vii)",
            "6. MONITORING PLAN — 21 CFR 312.305(b)(2)(viii)",
        ]
        for header in expected:
            self.assertIn(header, self.rendered, header)

    def test_old_off_by_one_pinpoints_are_gone(self):
        # The pre-remap assignments must not appear anywhere in the rendered
        # plan: rationale is no longer (i), monitoring no longer (vii)-alone.
        self.assertNotIn("21 CFR 312.305(b)(2)(i)\n", self.rendered)
        self.assertNotIn("RATIONALE FOR TREATMENT USE — 21 CFR 312.305(b)(2)(i)",
                         self.rendered)
        self.assertNotIn("MONITORING PLAN — 21 CFR 312.305(b)(2)(vii)",
                         self.rendered)
        self.assertNotIn("(b)(2)(v)-(vi)", self.rendered)

    def test_provenance_citations_use_table_pinpoints(self):
        doc = _gen("gen_treatment_plan")
        by_span = {p.span: p.citation for p in doc.provenance}
        self.assertEqual(by_span["monitoring_plan"], cite("ea.treatment_plan.monitoring"))
        self.assertEqual(by_span["facility"], cite("ea.treatment_plan.facility"))
        self.assertEqual(by_span["diagnosis"], cite("ea.treatment_plan.patient_description"))
        self.assertEqual(by_span["route"], cite("ea.treatment_plan.dosing"))
        self.assertIn(cite("ea.treatment_plan.rationale"), by_span["treatment_rationale"])
        self.assertEqual(by_span["dosing_plan"], cite("ea.treatment_plan.dosing"))


class OtherGeneratorPinpointTests(unittest.TestCase):
    def test_form_3926_sources_remapped(self):
        doc = _gen("gen_form_3926")
        by_span = {p.span: p.citation for p in doc.provenance}
        for span in ("treatment_plan_summary", "dose", "route", "duration"):
            self.assertEqual(by_span[span], cite("ea.treatment_plan.dosing"), span)
        self.assertEqual(by_span["monitoring_plan"], cite("ea.treatment_plan.monitoring"))

    def test_loa_request_sources_remapped(self):
        doc = _gen("gen_loa_request")
        by_span = {p.span: p.citation for p in doc.provenance}
        for span in ("dose", "route", "duration"):
            self.assertEqual(by_span[span], cite("ea.treatment_plan.dosing"), span)


class RegistryPinpointTests(unittest.TestCase):
    """routes.json cannot call cite() — this test IS its reconciliation with
    the single-source table (a drifted registry pinpoint fails here)."""

    def test_intake_field_citations_match_table(self):
        by_id = {f["id"]: f for f in routes.intake_fields()}
        self.assertEqual(by_id["drug.dose"]["citation"], cite("ea.treatment_plan.dosing"))
        self.assertEqual(by_id["drug.route"]["citation"], cite("ea.treatment_plan.dosing"))
        self.assertEqual(by_id["drug.duration"]["citation"], cite("ea.treatment_plan.dosing"))
        self.assertEqual(by_id["treatment.monitoring_plan"]["citation"],
                         cite("ea.treatment_plan.monitoring"))
        self.assertEqual(by_id["site.name"]["citation"], cite("ea.treatment_plan.facility"))

    def test_route_clock_bases_match_table(self):
        em = routes.route_for_emergency(True)
        by_id = {c["id"]: c for c in em["clocks"]}
        self.assertEqual(by_id["written-3926-15-working-day"]["basis"],
                         cite("clock.written_3926"))
        self.assertEqual(by_id["irb-notify-5-working-day"]["basis"],
                         cite("clock.irb_emergency_notification"))
        non = routes.route_for_emergency(False)
        self.assertEqual(non["clocks"][0]["basis"], cite("clock.ind_effective_30_day"))


class Form3926ItemMapTests(unittest.TestCase):
    """Overhaul P8 (M6): the Form-3926 text render consumes the ONE item map
    (pdf_3926.FORM_3926_ITEMS) and carries the item-numbering pending marker
    until a qualified human initials the map."""

    def setUp(self):
        from ossicro import pdf_3926
        self.pdf_3926 = pdf_3926
        self.rendered = _gen("gen_form_3926").rendered

    def test_headings_come_from_the_item_map(self):
        for item in self.pdf_3926.FORM_3926_ITEMS:
            heading = "%s. %s" % (item.number, item.label)
            self.assertIn(heading, self.rendered, heading)

    def test_reconciled_item_numbers(self):
        # The pre-P8 disagreement is resolved: LOA=5, qualification=6,
        # requestor=7, IRB=8 (not the old LOA=6/qual=7/IRB=8/no-9 layout).
        self.assertIn("5. LETTER OF AUTHORIZATION (LOA)", self.rendered)
        self.assertIn("6. PHYSICIAN'S QUALIFICATION STATEMENT", self.rendered)
        self.assertIn("8. INSTITUTIONAL REVIEW BOARD (IRB) INFORMATION",
                      self.rendered)
        # Item 9 now exists as an explicit unresolved slot.
        self.assertIn("9.", self.rendered)
        self.assertIn("UNRESOLVED", self.rendered)

    def test_pending_numbering_marker_on_the_text_render(self):
        self.assertIsNone(self.pdf_3926.FORM_3926_MAP_VERIFIED_BY)
        self.assertIn("PENDING-HUMAN-VERIFICATION", self.rendered)
        self.assertIn("Item numbering pending verification", self.rendered)
        self.assertIn("(draft layout)".upper(), self.rendered)  # "DRAFT LAYOUT"

    def test_provenance_item_citations_flag_pending_numbering(self):
        doc = _gen("gen_form_3926")
        by_span = {p.span: p.citation for p in doc.provenance}
        # Item-number references route through the item map and stay honest
        # about the verification state.
        self.assertIn("item numbering PENDING-HUMAN-VERIFICATION",
                      by_span["patient_initials_coded"])
        self.assertIn("Form FDA 3926 item 3", by_span["patient_initials_coded"])


class PendingFooterTests(unittest.TestCase):
    """P1 spec item 5: while any citation a document uses is pending human
    verification, the rendered artifact says so — never silently final."""

    def test_footer_present_on_docs_using_pending_pinpoints(self):
        for gen in ("gen_treatment_plan", "gen_form_3926", "gen_loa_request",
                    "gen_cover_letter", "gen_irb_request"):
            rendered = _gen(gen).rendered
            self.assertIn(citations.PENDING_FOOTER, rendered, gen)
            self.assertIn("PENDING-HUMAN-VERIFICATION", rendered, gen)

    def test_footer_absent_when_no_pending_citation_used(self):
        # The drug-accountability shell cites only 312.62(a)/312.61 — no
        # pending pinpoint, so no pending footer (the marker is honest, not
        # a blanket stamp).
        rendered = _gen("gen_drug_accountability").rendered
        self.assertNotIn(citations.PENDING_FOOTER, rendered)

    def test_uses_pending_predicate(self):
        self.assertTrue(citations.uses_pending("… per 21 CFR 312.305(b)(2)(viii) …"))
        self.assertFalse(citations.uses_pending("… per 21 CFR 312.62(a) …"))
        self.assertTrue(citations.uses_pending("", "21 CFR 56.104(c)"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
