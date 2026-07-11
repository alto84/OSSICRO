"""Wave-3 engine tests: the hand-written Form-3926 PDF / FDF export.

Covers:
  - render_3926_pdf returns structurally valid PDF bytes (%PDF header, xref,
    trailer, %%EOF) with the DRAFT watermark on EVERY page and the
    human-review footer;
  - a committed sample's intake values appear in the output, value-faithful;
  - a missing field renders BLANK — never a fabricated value, never the
    engine's [[MISSING: ...]] marker leaking into a print artifact;
  - fdf_3926 emits a standard FDF whose field map covers ONLY route-schema
    intake ids, omits absent values, and carries the DRAFT marker;
  - no signature is ever filled (the signature is a non-delegable human act).

Pure stdlib; no rendering library is (or may be) involved.
"""

import json
import os
import sys
import unittest

ENGINE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

from ossicro import ea_generators                            # noqa: E402
from ossicro import pdf_3926                                  # noqa: E402
from ossicro import routes as routes_mod                     # noqa: E402
from ossicro.pdf_3926 import (                               # noqa: E402
    FDF_3926_FIELD_MAP,
    FORM_3926_ITEMS,
    ITEM_UNRESOLVED,
    PENDING_NUMBERING_NOTE,
    fdf_3926,
    render_3926_pdf,
)

FIXTURES = os.path.join(ENGINE_DIR, "fixtures")


def _sample_intake():
    with open(os.path.join(FIXTURES, "ea_sample_case.json"), encoding="utf-8") as f:
        return dict(json.load(f)["fields"])


def _doc_registry():
    from ossicro.registry import load_documents
    return load_documents()


def _pdf_escape(text: str) -> bytes:
    """The same WinAnsi literal-string encoding the PDF writer uses, so a
    heading with non-ASCII (e.g. the em dash) is searchable in the bytes."""
    from ossicro.pdf_3926 import _pdf_escape as esc
    return esc(text)


def _page_count(pdf: bytes) -> int:
    return pdf.count(b"/Type /Page ")   # page objects (the Pages node has no trailing space match)


class TestRender3926Pdf(unittest.TestCase):

    def setUp(self):
        self.intake = _sample_intake()
        self.pdf = render_3926_pdf(self.intake)

    def test_valid_pdf_structure(self):
        self.assertTrue(self.pdf.startswith(b"%PDF-"))
        self.assertIn(b"xref", self.pdf)
        self.assertIn(b"trailer", self.pdf)
        self.assertIn(b"startxref", self.pdf)
        self.assertTrue(self.pdf.rstrip().endswith(b"%%EOF"))
        self.assertGreaterEqual(_page_count(self.pdf), 1)

    def test_draft_watermark_on_every_page(self):
        pages = _page_count(self.pdf)
        # One watermark op per page: the op string is unique to the watermark
        # (42pt bold, rotated). "NOT FOR SUBMISSION" is ASCII and byte-visible.
        self.assertEqual(self.pdf.count(b"NOT FOR SUBMISSION"), pages)
        self.assertGreaterEqual(self.pdf.count(b"DRAFT"), pages)

    def test_footer_names_human_review_on_every_page(self):
        pages = _page_count(self.pdf)
        self.assertEqual(self.pdf.count(b"DRAFT for qualified human review"),
                         pages)

    def test_committed_sample_values_appear(self):
        for token in (b"PT-3926-014", b"Cytoravir", b"Helix Therapeutics, Inc.",
                      b"240 mg orally twice daily", b"Midwest Regional IRB",
                      b"IND 178452", b"036-114520"):
            self.assertIn(token, self.pdf,
                          "expected intake value %r in the PDF" % token)

    def test_missing_field_renders_blank_not_fabricated(self):
        intake = _sample_intake()
        del intake["patient.age"]
        del intake["drug.duration"]
        pdf = render_3926_pdf(intake)
        # The label line survives with an EMPTY value...
        self.assertIn(b"(Age: ) Tj", pdf)
        # ...and nothing is invented in its place.
        self.assertNotIn(b"[[MISSING", pdf)
        self.assertNotIn(b"58", pdf.partition(b"(Age: ")[2][:8])

    def test_no_wall_clock_and_no_filled_signature(self):
        # The signature block is a notice, never a filled signature; there is
        # no fabricated date (the layout carries no engine-supplied dates).
        self.assertIn(b"NON-DELEGABLE HUMAN ACT", self.pdf)
        self.assertIn(b"DATE: __________", self.pdf)

    def test_accepts_study_too(self):
        route = routes_mod.route_for_emergency(False)
        from ossicro.ea_generators import build_study
        study = build_study(self.intake, route)
        pdf = render_3926_pdf(study)
        self.assertTrue(pdf.startswith(b"%PDF-"))
        self.assertIn(b"Cytoravir", pdf)


class TestFdf3926(unittest.TestCase):

    def test_fdf_maps_only_schema_fields(self):
        schema_ids = {f["id"] for f in routes_mod.intake_fields()}
        unknown = set(FDF_3926_FIELD_MAP) - schema_ids
        self.assertEqual(unknown, set(),
                         "FDF map carries non-schema intake ids: %s" % unknown)

    def test_fdf_structure_and_values(self):
        fdf = fdf_3926(_sample_intake())
        self.assertTrue(fdf.startswith(b"%FDF-1.2"))
        self.assertIn(b"/FDF", fdf)
        self.assertIn(b"/Fields", fdf)
        self.assertTrue(fdf.rstrip().endswith(b"%%EOF"))
        self.assertIn(b"/T (3926_04_drug_name) /V (Cytoravir)", fdf)
        self.assertIn(b"/T (3926_03_patient_identifier) /V (PT-3926-014)", fdf)

    def test_fdf_omits_absent_values_and_stays_draft_marked(self):
        intake = _sample_intake()
        intake.pop("submission.ind_number", None)  # absent in the fixture too
        del intake["patient.age"]                  # honestly absent
        intake["drug.dose"] = "   "                # blank == absent
        fdf = fdf_3926(intake)
        self.assertNotIn(b"3926_02_ind_number", fdf)
        self.assertNotIn(b"3926_03_age", fdf)
        self.assertNotIn(b"3926_05_dose", fdf)
        # DRAFT travels in the DATA (a marker field), not only in comments.
        self.assertIn(b"ossicro_draft_notice", fdf)
        self.assertIn(b"NOT FOR SUBMISSION", fdf)
        self.assertIn(b"HUMAN-VERIFY", fdf)

    def test_fdf_never_carries_unmapped_intake(self):
        # Consent narratives etc. are NOT part of the 3926 form fill.
        fdf = fdf_3926(_sample_intake())
        self.assertNotIn(b"consent.purpose", fdf)
        self.assertNotIn(b"kept confidential", fdf)


class TestForm3926ItemMap(unittest.TestCase):
    """Overhaul P8 (M6): the ONE item map — text template, PDF layout, and
    FDF field map are all derived from FORM_3926_ITEMS, so they cannot
    disagree, and the pending-numbering marker stands until a human initials
    the map."""

    def setUp(self):
        self.intake = _sample_intake()

    def test_item_numbers_are_contiguous_1_to_11(self):
        numbers = [item.number for item in FORM_3926_ITEMS]
        self.assertEqual(numbers, [str(n) for n in range(1, 12)])

    def test_item_9_is_explicit_unresolved(self):
        by_num = {item.number: item for item in FORM_3926_ITEMS}
        self.assertEqual(by_num["9"].status, ITEM_UNRESOLVED)

    def test_pdf_layout_headings_match_the_item_map(self):
        # Every item heading (number + label) appears verbatim in the PDF.
        pdf = render_3926_pdf(self.intake)
        for item in FORM_3926_ITEMS:
            heading = "%s. %s" % (item.number, item.label)
            self.assertIn(_pdf_escape(heading), pdf, heading)

    def test_text_template_headings_match_the_item_map(self):
        # The ea_generators text render carries the same numbered headings —
        # the two renders consume the same table.
        route = routes_mod.route_for_emergency(False)
        study = ea_generators.build_study(self.intake, route)
        rendered = ea_generators.gen_form_3926(
            study, _doc_registry()).rendered
        for item in FORM_3926_ITEMS:
            heading = "%s. %s" % (item.number, item.label)
            self.assertIn(heading, rendered, heading)

    def test_fdf_map_is_derived_from_the_item_map(self):
        derived = {intake_id: fdf_name
                   for item in FORM_3926_ITEMS
                   for (_l, intake_id, fdf_name) in item.fields
                   if fdf_name}
        self.assertEqual(dict(FDF_3926_FIELD_MAP), derived)

    def test_pending_marker_present_until_a_human_initials_the_map(self):
        # Default state: no verifier -> the pending marker is on the PDF, the
        # FDF, and the text template.
        self.assertIsNone(pdf_3926.FORM_3926_MAP_VERIFIED_BY,
                          "the shipped map must be unverified (HITL)")
        self.assertEqual(pdf_3926.pending_item_numbering_note(),
                         PENDING_NUMBERING_NOTE)
        pdf = render_3926_pdf(self.intake)
        self.assertIn(b"Item numbering pending verification", pdf)
        fdf = fdf_3926(self.intake)
        self.assertIn(b"item numbering unverified", fdf)
        route = routes_mod.route_for_emergency(False)
        study = ea_generators.build_study(self.intake, route)
        rendered = ea_generators.gen_form_3926(
            study, _doc_registry()).rendered
        self.assertIn("PENDING-HUMAN-VERIFICATION", rendered)
        self.assertIn("Item numbering pending verification", rendered)

    def test_marker_removed_only_by_the_verifier_edit(self):
        # Simulate the human pass (the one edit that removes the marker) and
        # prove nothing else does.
        orig = pdf_3926.FORM_3926_MAP_VERIFIED_BY
        try:
            pdf_3926.FORM_3926_MAP_VERIFIED_BY = "Dr. Verifier, 2026-07-15"
            self.assertEqual(pdf_3926.pending_item_numbering_note(), "")
            pdf = render_3926_pdf(self.intake)
            self.assertNotIn(b"Item numbering pending verification", pdf)
            # The DRAFT watermark is untouched by the numbering verification.
            self.assertIn(b"NOT FOR SUBMISSION", pdf)
            fdf = fdf_3926(self.intake)
            self.assertIn(b"map verified by Dr. Verifier", fdf)
            self.assertNotIn(b"item numbering unverified", fdf)
        finally:
            pdf_3926.FORM_3926_MAP_VERIFIED_BY = orig

    def test_heading_softened_to_draft_layout(self):
        pdf = render_3926_pdf(self.intake)
        self.assertIn(b"DRAFT LAYOUT", pdf)


if __name__ == "__main__":
    unittest.main()
