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

from ossicro import routes as routes_mod                     # noqa: E402
from ossicro.pdf_3926 import (                               # noqa: E402
    FDF_3926_FIELD_MAP,
    fdf_3926,
    render_3926_pdf,
)

FIXTURES = os.path.join(ENGINE_DIR, "fixtures")


def _sample_intake():
    with open(os.path.join(FIXTURES, "ea_sample_case.json"), encoding="utf-8") as f:
        return dict(json.load(f)["fields"])


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


if __name__ == "__main__":
    unittest.main()
