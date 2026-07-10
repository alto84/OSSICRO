"""Tests for the four ENGINE improvements (time discipline, manifest
completeness, sign-off read-time validation, concept integrity).

Run: `cd engine && python -m unittest tests.test_engine_improvements -v`.
"""

import datetime
import hashlib
import json
import re
import unittest
from pathlib import Path

from ossicro import clocks, gates, routes
from ossicro import ea_generators as ea
from ossicro.assemble import assemble_submission
from ossicro.ea_generators import (
    TriggerDateError,
    build_study,
    compute_clocks,
    derive_as_of,
    generate_route_documents,
)
from ossicro.models import HumanSignoff
from ossicro.pipeline import run_check
from ossicro.registry import load_documents, load_gates
from ossicro.review_port import ConceptReviewer, ReviewReport

ENGINE_ROOT = Path(__file__).resolve().parent.parent
OSSICRO_DIR = ENGINE_ROOT / "ossicro"
SAMPLE_PATH = ENGINE_ROOT / "fixtures" / "ea_sample_case.json"

D = datetime.date


def _sample_fields():
    data = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    return dict(data.get("fields", data))


def _build_case(fields):
    emergency = str(fields.get("submission.emergency", "")).strip().lower() in ("true", "1", "yes")
    route = routes.route_for_emergency(emergency)
    study = build_study(fields, route)
    documents = generate_route_documents(study, route, load_documents())
    return study, documents, route


# ---------------------------------------------------------------------------
# 1. TIME DISCIPLINE (HC2)
# ---------------------------------------------------------------------------

class NoWallClockTests(unittest.TestCase):
    def test_no_module_calls_date_today(self):
        # Grep-style proof: no module under engine/ossicro/ calls date.today()
        # (a CLI entrypoint would be the only allowed exception).
        pattern = re.compile(r"\.today\(")
        offenders = []
        for path in sorted(OSSICRO_DIR.glob("*.py")):
            if path.name == "cli.py":
                continue  # CLI entrypoint exemption (none needed today)
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                code = line.split("#", 1)[0]  # ignore comments
                if pattern.search(code):
                    offenders.append("%s:%d: %s" % (path.name, lineno, line.strip()))
        self.assertEqual(offenders, [],
                         "date.today()-style wall-clock calls found:\n" + "\n".join(offenders))


class UnarmedClockTests(unittest.TestCase):
    def test_absent_trigger_yields_unarmed_clock_never_today(self):
        route = routes.get_route("route-3926")
        fields = _sample_fields()
        del fields["submission.fda_receipt_date"]  # no trigger anywhere
        study = build_study(fields, route)
        (clock,) = compute_clocks(study, route)
        self.assertFalse(clock["armed"])
        self.assertIsNone(clock["deadline"])
        self.assertIsNone(clock["days_remaining"])
        self.assertIn("Enter the trigger date", clock["resolving_question"])
        self.assertIn("submission.fda_receipt_date", clock["resolving_question"])

    def test_emergency_clocks_unarmed_without_triggers(self):
        route = routes.get_route("route-3926-emergency")
        fields = _sample_fields()
        fields["submission.emergency"] = "true"
        del fields["submission.fda_receipt_date"]
        study = build_study(fields, route)
        for clock in compute_clocks(study, route):
            self.assertFalse(clock["armed"], clock["id"])
            self.assertIsNone(clock["deadline"], clock["id"])
            self.assertTrue(clock["resolving_question"], clock["id"])

    def test_armed_clock_days_remaining_from_as_of(self):
        route = routes.get_route("route-3926")
        study = build_study(_sample_fields(), route)  # receipt 2026-06-15
        (clock,) = compute_clocks(study, route, as_of=D(2026, 6, 15))
        self.assertTrue(clock["armed"])
        self.assertEqual(clock["deadline"], "2026-07-15")
        self.assertEqual(clock["days_remaining"], 30)
        self.assertIsNone(clock["resolving_question"])

    def test_unparseable_trigger_is_an_error_not_silent_absence(self):
        route = routes.get_route("route-3926")
        fields = _sample_fields()
        fields["submission.fda_receipt_date"] = "June 15th, 2026"
        study = build_study(fields, route)
        with self.assertRaises(TriggerDateError) as ctx:
            compute_clocks(study, route)
        self.assertIn("submission.fda_receipt_date", str(ctx.exception))

    def test_parse_trigger_date_contract(self):
        self.assertIsNone(ea.parse_trigger_date(None, "f"))
        self.assertIsNone(ea.parse_trigger_date("  ", "f"))
        self.assertEqual(ea.parse_trigger_date("2026-07-01", "f"), D(2026, 7, 1))
        with self.assertRaises(TriggerDateError):
            ea.parse_trigger_date("garbage", "f")


class AsOfThreadingTests(unittest.TestCase):
    def test_dated_spans_anchor_on_physician_entered_date(self):
        study, documents, _route = _build_case(_sample_fields())
        # anchor derives from submission.fda_receipt_date = 2026-06-15
        self.assertEqual(derive_as_of(study), D(2026, 6, 15))
        cover = documents["expanded-access-cover-letter"]
        self.assertEqual(cover.fields.get("cover_date"), "2026-06-15")
        form = documents["form-fda-3926-individual-patient-expanded-access"]
        self.assertEqual(form.fields.get("submission_date"), "2026-06-15")

    def test_no_anchor_renders_missing_marker_not_a_date(self):
        fields = _sample_fields()
        del fields["submission.fda_receipt_date"]
        study, documents, _route = _build_case(fields)
        self.assertIsNone(derive_as_of(study))
        cover = documents["expanded-access-cover-letter"]
        self.assertIn("[[MISSING: cover_date]]", cover.rendered)
        self.assertNotIn("cover_date", cover.fields)
        # the clock statement asks for the receipt date instead of fabricating one
        self.assertIn("Enter the FDA receipt date", cover.rendered)

    def test_explicit_as_of_wins(self):
        route = routes.get_route("route-3926")
        study = build_study(_sample_fields(), route)
        documents = generate_route_documents(study, route, load_documents(),
                                             as_of=D(2026, 7, 2))
        cover = documents["expanded-access-cover-letter"]
        self.assertEqual(cover.fields.get("cover_date"), "2026-07-02")


class CrossYearNewYearTests(unittest.TestCase):
    def test_new_year_2028_observed_on_2027_12_31(self):
        # 2028-01-01 is a Saturday -> observed Friday 2027-12-31, attributed
        # to 2027's holiday table.
        self.assertEqual(D(2028, 1, 1).weekday(), 5)
        h2027 = clocks.federal_holidays(2027)
        self.assertIn(D(2027, 12, 31), h2027)
        self.assertEqual(h2027[D(2027, 12, 31)], "New Year's Day")
        self.assertFalse(clocks.is_working_day(D(2027, 12, 31)))
        # 2028's own table contains no entry dated outside 2028
        for d in clocks.federal_holidays(2028):
            self.assertEqual(d.year, 2028)

    def test_sunday_new_year_observed_monday_same_year(self):
        # 2034-01-01 is a Sunday -> observed Monday 2034-01-02, same year.
        self.assertEqual(D(2034, 1, 1).weekday(), 6)
        self.assertIn(D(2034, 1, 2), clocks.federal_holidays(2034))
        self.assertFalse(clocks.is_working_day(D(2034, 1, 2)))

    def test_working_day_arithmetic_crosses_the_year_boundary(self):
        # Thu 2027-12-30 + 2 working days: Fri 12-31 is the observed New Year
        # holiday, Sat/Sun skipped -> Mon 2028-01-03, Tue 2028-01-04.
        self.assertEqual(clocks.add_working_days(D(2027, 12, 30), 2), D(2028, 1, 4))


# ---------------------------------------------------------------------------
# 2. MANIFEST COMPLETENESS
# ---------------------------------------------------------------------------

class ManifestCompletenessTests(unittest.TestCase):
    def test_manifest_covers_all_route_documents(self):
        study, documents, route = _build_case(_sample_fields())
        pkg = assemble_submission(study, documents, route, load_documents(), load_gates())
        manifest_ids = [m["doc_id"] for m in pkg["manifest"]]
        self.assertEqual(manifest_ids, route["documents"])  # all 8, route order
        self.assertEqual(len(manifest_ids), 8)
        for entry in pkg["manifest"]:
            self.assertFalse(entry["absent"], entry["doc_id"])
            self.assertTrue(entry["sha256"], entry["doc_id"])
        # every manifest entry has a bundled rendered document that re-hashes
        rendered = {d["doc_id"]: d["rendered"] for d in pkg["documents"]}
        for entry in pkg["manifest"]:
            self.assertEqual(
                hashlib.sha256(rendered[entry["doc_id"]].encode("utf-8")).hexdigest(),
                entry["sha256"], entry["doc_id"])

    def test_missing_document_gets_absent_entry(self):
        study, documents, route = _build_case(_sample_fields())
        del documents["drug-accountability-log"]
        pkg = assemble_submission(study, documents, route, load_documents(), load_gates())
        by_id = {m["doc_id"]: m for m in pkg["manifest"]}
        entry = by_id["drug-accountability-log"]
        self.assertTrue(entry["absent"])
        self.assertIsNone(entry["sha256"])
        self.assertEqual(len(pkg["manifest"]), 8)      # still the full set
        self.assertEqual(len(pkg["documents"]), 7)     # only present docs bundle

    def test_package_digest_is_sha256_over_sorted_doc_hashes(self):
        study, documents, route = _build_case(_sample_fields())
        pkg = assemble_submission(study, documents, route, load_documents(), load_gates())
        hashes = sorted(m["sha256"] for m in pkg["manifest"] if not m["absent"])
        expected = hashlib.sha256("\n".join(hashes).encode("utf-8")).hexdigest()
        self.assertEqual(pkg["package_sha256"], expected)


# ---------------------------------------------------------------------------
# 3. SIGN-OFF READ-TIME VALIDATION
# ---------------------------------------------------------------------------

class SignoffReadTimeValidationTests(unittest.TestCase):
    def setUp(self):
        self.study, self.documents, self.route = _build_case(_sample_fields())
        self.docreg = load_documents()
        self.gatereg = load_gates()
        self.cover = self.documents["expanded-access-cover-letter"]

    def test_valid_reapplied_signoff_flows_amber_to_green(self):
        # A persisted sign-off re-applied to the regenerated Document (the app
        # flow) with the gate's responsible role clears the amber.
        self.cover.signoffs.append(HumanSignoff(
            gate_id="submission-to-fda", person="Jordan A. Rivera, MD",
            role="sponsor-investigator",
            statement="I have reviewed this letter and adopt it as my submission."))
        result = run_check(self.study, self.documents, self.docreg, self.gatereg)
        item = next(i for i in result.ledger if i.doc_id == "expanded-access-cover-letter")
        self.assertEqual(item.status, "green")
        pending = {pg.gate_id: pg for pg in result.gate_packet}
        self.assertNotIn("expanded-access-cover-letter",
                         pending.get("submission-to-fda").doc_ids
                         if "submission-to-fda" in pending else [])

    def test_wrong_role_signoff_does_not_clear_the_gate(self):
        self.cover.signoffs.append(HumanSignoff(
            gate_id="submission-to-fda", person="Someone Else",
            role="study-coordinator", statement="signed"))
        result = run_check(self.study, self.documents, self.docreg, self.gatereg)
        item = next(i for i in result.ledger if i.doc_id == "expanded-access-cover-letter")
        self.assertEqual(item.status, "amber")
        pending = {pg.gate_id for pg in result.gate_packet}
        self.assertIn("submission-to-fda", pending)

    def test_missing_attribution_signoff_does_not_clear_the_gate(self):
        self.cover.signoffs.append(HumanSignoff(
            gate_id="submission-to-fda", person="   ",
            role="sponsor-investigator", statement=""))
        result = run_check(self.study, self.documents, self.docreg, self.gatereg)
        item = next(i for i in result.ledger if i.doc_id == "expanded-access-cover-letter")
        self.assertEqual(item.status, "amber")
        self.assertTrue(any("INVALID" in q for q in item.questions), item.questions)

    def test_finalize_rejects_invalid_signoff(self):
        self.cover.signoffs.append(HumanSignoff(
            gate_id="submission-to-fda", person="Someone Else",
            role="study-coordinator", statement="signed"))
        self.cover.advance("in_review")
        self.cover.advance("approved")
        with self.assertRaises(gates.GateViolation):
            gates.finalize(self.cover, self.gatereg)

    def test_signoff_problems_lists_each_defect(self):
        gate = self.gatereg["submission-to-fda"]
        bad = HumanSignoff(gate_id="submission-to-fda", person="", role="irb", statement="")
        problems = gates.signoff_problems(bad, gate)
        self.assertEqual(len(problems), 3)  # person, role, statement
        good = HumanSignoff(gate_id="submission-to-fda", person="J. Rivera, MD",
                            role="sponsor-investigator", statement="I adopt this filing.")
        self.assertEqual(gates.signoff_problems(good, gate), [])


# ---------------------------------------------------------------------------
# 4. CONCEPT INTEGRITY
# ---------------------------------------------------------------------------

class _ExplodingReviewer(ConceptReviewer):
    model = "exploding-reviewer-v1"

    def review(self, text, doc, principles):
        raise RuntimeError("simulated transport failure")


class _CleanReviewer(ConceptReviewer):
    model = "clean-reviewer-v1"

    def review(self, text, doc, principles):
        return ReviewReport(model=self.model)


class ConceptIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.study, self.documents, self.route = _build_case(_sample_fields())
        self.docreg = load_documents()
        self.gatereg = load_gates()

    def test_reviewer_exception_escalates_instead_of_aborting(self):
        pkg = assemble_submission(self.study, self.documents, self.route,
                                  self.docreg, self.gatereg,
                                  reviewer=_ExplodingReviewer())
        self.assertFalse(pkg["submission_ready"])
        self.assertTrue(pkg["blocking"])
        self.assertTrue(any("FAILED" in b["message"] for b in pkg["blocking"]))
        self.assertEqual(pkg["reviewer_model"], "exploding-reviewer-v1")

    def test_reviewer_model_recorded_on_package(self):
        pkg = assemble_submission(self.study, self.documents, self.route,
                                  self.docreg, self.gatereg,
                                  reviewer=_CleanReviewer())
        self.assertEqual(pkg["reviewer_model"], "clean-reviewer-v1")

    def test_precomputed_check_is_the_review_the_package_reflects(self):
        check = run_check(self.study, self.documents, self.docreg, self.gatereg,
                          reviewer=_CleanReviewer())
        pkg = assemble_submission(self.study, self.documents, self.route,
                                  self.docreg, self.gatereg, check=check)
        self.assertEqual(pkg["reviewer_model"], "clean-reviewer-v1")
        self.assertEqual(pkg["totals"], {"green": sum(1 for i in check.ledger if i.status == "green"),
                                         "amber": sum(1 for i in check.ledger if i.status == "amber"),
                                         "red": sum(1 for i in check.ledger if i.status == "red")})

    def test_reviewer_failure_never_clears_a_gate(self):
        result = run_check(self.study, self.documents, self.docreg, self.gatereg,
                           reviewer=_ExplodingReviewer())
        gate_ids = {pg.gate_id for pg in result.gate_packet}
        self.assertIn("submission-to-fda", gate_ids)
        self.assertIn("informed-consent", gate_ids)


if __name__ == "__main__":
    unittest.main(verbosity=2)
