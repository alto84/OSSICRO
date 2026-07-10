"""Matching-engine tests (Wave 2, feature C): a registry-search ORGANIZER.

Covers the Non-Device CDS design constraints (Fable BLOCKER 1):
- candidates carry matched / unmatched / unverifiable CRITERIA — no score,
  no confidence, no ranking key anywhere in the output;
- absence renders the exact "no candidates found in the queried registries
  as of <date>" framing, never "no options exist";
- v1 scope = trials + expanded-access records ONLY (a drug_listing record in
  the fixture is structurally dropped);
- age / sex / drug are compared LOCALLY against structured eligibility
  (unmatched criteria are SHOWN, not silently filtered — the physician
  reviews the basis);
- unstructured eligibility text is honestly unverifiable;
- the mini eval harness (GAP-6): recall AND precision 1.0 against the
  labeled fixture cases — no unbenchmarked quality claims;
- every registry query lands one 'egress_query' audit record.
"""

import json
import unittest
from pathlib import Path

from ossicro import audit as audit_mod
from ossicro.egress import DeidentifiedPredicates
from ossicro.matching import (
    ABSENCE_MESSAGE_TEMPLATE,
    MockRegistryAdapter,
    match,
)

ENGINE_ROOT = Path(__file__).resolve().parent.parent
EVAL_PATH = ENGINE_ROOT / "fixtures" / "match_eval.json"

AS_OF = "2026-07-10"


def _predicates(**overrides):
    base = dict(condition_codes=("70179006", "C22.1"), drug_name="Cytoravir",
                age_band="55-59", sex="female", route_code="26643006")
    base.update(overrides)
    return DeidentifiedPredicates(**base)


def _match(predicates, trail=None):
    return match(predicates, MockRegistryAdapter(),
                 trail=trail if trail is not None else [], as_of=AS_OF)


class TestOrganizerNotRecommender(unittest.TestCase):

    def setUp(self):
        self.result = _match(_predicates())
        self.by_id = {c["id"]: c for c in self.result["candidates"]}

    def test_contract_shape(self):
        self.assertEqual(set(self.result),
                         {"candidates", "absence", "absence_message",
                          "queried_registries", "predicates_used", "as_of"})
        for c in self.result["candidates"]:
            self.assertEqual(set(c), {"kind", "id", "title", "source_registry",
                                      "source_url", "matched_criteria",
                                      "unmatched_criteria",
                                      "unverifiable_criteria"})
            self.assertIn(c["kind"], ("trial", "ea_record"))
        self.assertEqual(self.result["as_of"], AS_OF)
        self.assertEqual(self.result["queried_registries"],
                         ["api.fda.gov", "clinicaltrials.gov"])

    def test_no_score_or_confidence_anywhere(self):
        serialized = json.dumps(self.result).lower()
        for banned in ("score", "confidence", "ranking", "probability",
                       "percent_match"):
            self.assertNotIn(banned, serialized)

    def test_criteria_not_scores(self):
        c = self.by_id["NCT90000001"]
        self.assertIn("condition code 70179006, C22.1",
                      c["matched_criteria"][0])
        self.assertTrue(any("age" in m for m in c["matched_criteria"]))
        self.assertIn("sex: all", c["matched_criteria"])
        self.assertEqual(c["unmatched_criteria"], [])
        # ECOG / organ function cannot be verified from structured predicates.
        self.assertTrue(any("ECOG" in u for u in c["unverifiable_criteria"]))
        self.assertTrue(all(u.startswith("not verifiable from structured data")
                            for u in c["unverifiable_criteria"]))

    def test_unmatched_criterion_shown_not_silently_filtered(self):
        # The male-only trial still appears — with its unmatched sex criterion
        # visible. The organizer shows the basis; the physician decides.
        c = self.by_id["NCT90000004"]
        self.assertTrue(any(u.startswith("sex: male")
                            for u in c["unmatched_criteria"]))

    def test_ea_records_drug_identity_compared_locally(self):
        cyto = self.by_id["EA-90000001"]
        self.assertIn("drug: Cytoravir", cyto["matched_criteria"])
        other = self.by_id["EA-90000002"]
        self.assertTrue(any(u.startswith("drug: Helixamab")
                            for u in other["unmatched_criteria"]))

    def test_missing_predicate_is_unverifiable_never_guessed(self):
        result = _match(_predicates(age_band=None, sex=None))
        by = {x["id"]: x for x in result["candidates"]}
        # Age rule with no age band -> unverifiable (never matched/unmatched).
        c = by["NCT90000002"]
        self.assertTrue(any("no age band" in u
                            for u in c["unverifiable_criteria"]))
        self.assertEqual(c["unmatched_criteria"], [])
        # A sex-restricted candidate with no sex predicate -> unverifiable.
        c4 = by["NCT90000004"]
        self.assertTrue(any("no sex" in u for u in c4["unverifiable_criteria"]))
        self.assertEqual(c4["unmatched_criteria"], [])

    def test_age_band_straddling_limit_is_unverifiable(self):
        # Band 75-79 straddles NCT90000002's age_max 75: not verifiable from
        # a 5-year band — never called matched OR unmatched.
        result = _match(_predicates(age_band="75-79"))
        c = {x["id"]: x for x in result["candidates"]}["NCT90000002"]
        self.assertTrue(any("straddles" in u
                            for u in c["unverifiable_criteria"]))


class TestV1Scope(unittest.TestCase):
    """v1 = open trials + expanded-access records ONLY (defer drug ranking)."""

    def test_drug_listing_record_structurally_dropped(self):
        adapter = MockRegistryAdapter()
        # The fixture record exists and the adapter WOULD return it...
        raw = adapter.search("api.fda.gov",
                             condition_codes=["70179006", "C22"])
        self.assertIn("DRUG-90000001", [r["id"] for r in raw])
        # ...but the organizer never surfaces a non-v1 kind.
        result = _match(_predicates())
        ids = [c["id"] for c in result["candidates"]]
        self.assertNotIn("DRUG-90000001", ids)
        self.assertTrue(all(c["kind"] in ("trial", "ea_record")
                            for c in result["candidates"]))


class TestAbsenceFraming(unittest.TestCase):

    def test_absence_message_exact_never_no_options_exist(self):
        result = _match(DeidentifiedPredicates(condition_codes=("E10.9",),
                                               age_band="20-24", sex="female"))
        self.assertEqual(result["candidates"], [])
        self.assertTrue(result["absence"])
        self.assertEqual(result["absence_message"],
                         ABSENCE_MESSAGE_TEMPLATE % AS_OF)
        self.assertEqual(
            result["absence_message"],
            "no candidates found in the queried registries as of 2026-07-10")
        self.assertNotIn("no options", json.dumps(result))

    def test_non_absence_has_empty_message(self):
        result = _match(_predicates())
        self.assertFalse(result["absence"])
        self.assertEqual(result["absence_message"], "")


class TestMatchAuditTrail(unittest.TestCase):

    def test_one_egress_record_per_registry(self):
        trail = []
        result = _match(_predicates(), trail=trail)
        self.assertEqual([r["action"] for r in trail],
                         ["egress_query", "egress_query"])
        self.assertEqual(sorted(r["target"] for r in trail),
                         result["queried_registries"])
        self.assertEqual(audit_mod.verify_chain(trail), [])


class TestMiniEvalHarness(unittest.TestCase):
    """GAP-6: labeled predicate -> expected-candidate cases. The claim this
    benchmark licenses is exactly this and no more: on the synthetic fixture,
    retrieval recall and precision are both 1.0."""

    def test_recall_and_precision_on_labeled_cases(self):
        cases = json.loads(EVAL_PATH.read_text(encoding="utf-8"))["cases"]
        self.assertGreaterEqual(len(cases), 3)
        total_expected = total_returned = total_hit = 0
        for case in cases:
            preds = dict(case["predicates"])
            preds["condition_codes"] = tuple(preds["condition_codes"])
            result = _match(DeidentifiedPredicates(**preds))
            returned = {c["id"] for c in result["candidates"]}
            expected = set(case["expected_ids"])
            total_expected += len(expected)
            total_returned += len(returned)
            total_hit += len(returned & expected)
            self.assertEqual(returned, expected, case["name"])
            for banned_id in case.get("must_not_return", []):
                self.assertNotIn(banned_id, returned, case["name"])
            if not expected:
                self.assertTrue(result["absence"], case["name"])
        recall = total_hit / total_expected if total_expected else 1.0
        precision = total_hit / total_returned if total_returned else 1.0
        self.assertEqual(recall, 1.0)
        self.assertEqual(precision, 1.0)


class _StubAdapter:
    """Returns one candidate carrying eligibility keys the comparator does not
    evaluate (route, pregnancy) — to prove they surface as unverifiable."""

    registries = ("clinicaltrials.gov",)

    def search(self, destination, condition_codes, drug_name=None, drug_rxnorm=None):
        return [{
            "kind": "trial", "id": "NCT-STUB", "title": "Stub",
            "source_registry": "clinicaltrials.gov",
            "source_url": "https://clinicaltrials.gov/NCT-STUB",
            "eligibility": {"condition_codes": list(condition_codes),
                            "route": "oral", "pregnancy_excluded": True},
        }]


class TestUnrecognizedEligibilityKeysSurfaced(unittest.TestCase):
    """MINOR-4: a structured eligibility key OSSICRO does not compare must show
    as unverifiable, never be silently ignored."""

    def test_unevaluated_keys_are_unverifiable(self):
        res = match(_predicates(), _StubAdapter(), trail=[], as_of=AS_OF)
        c = res["candidates"][0]
        uv = " ".join(c["unverifiable_criteria"])
        self.assertIn("not evaluated from structured data: route", uv)
        self.assertIn("not evaluated from structured data: pregnancy_excluded", uv)


if __name__ == "__main__":
    unittest.main(verbosity=2)
