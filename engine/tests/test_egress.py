"""INV-4 egress-gateway tests (BUILD-PLAN Wave 2, feature B).

Covers the walls in order:
- the closed DeidentifiedPredicates struct: unknown fields are a TypeError
  at construction; date-shaped / free-text-shaped values inside the allowed
  fields are a ValueError (names, dates, identifiers, narratives are
  structurally unrepresentable);
- from_profile derives ONLY the closed set from a committed intake snapshot
  (5-year age bands with a 90+ top per 164.514, codes from the closed local
  term table — the diagnosis text itself never appears);
- the destination allow-list refuses off-list hosts;
- live=True raises EgressDisabled while the greenlight flag is off;
- EVERY query (mock included) writes exactly one identifier-free 'egress_query'
  audit record — it carries the de-identified outbound facts (codes/bands/
  tokens, e.g. an RxNorm/SNOMED code or a known-drug token), never raw chart
  text; a bounded, named exception to INV-8's no-values rule (accountability
  for exactly what left the machine), not a leak. The record joins the trail
  with an intact hash chain;
- rare-code roll-up (ICD-10 extension -> category) and query decomposition
  (condition alone outbound; age/sex/route withheld as local filters);
- the module docstring states the residual re-identification risk.

No network is ever touched: the only adapter is an in-memory recorder.
"""

import json
import re
import unittest
from pathlib import Path

from ossicro import audit as audit_mod
from ossicro import egress
from ossicro.egress import (
    ALLOWED_DESTINATIONS,
    DeidentifiedPredicates,
    EgressDisabled,
    age_band_from_age,
    decompose_query,
    egress_query,
    roll_up_condition_codes,
)

ENGINE_ROOT = Path(__file__).resolve().parent.parent

# A committed-intake snapshot mirroring the synthetic sample case. The
# distinctive strings exist HERE so asserting their absence downstream is
# meaningful.
SAMPLE_INTAKE = {
    "patient.coded_id": "PT-3926-014",
    "patient.age": "58",
    "patient.sex": "Female",
    "patient.diagnosis": ("Refractory metastatic intrahepatic "
                          "cholangiocarcinoma, progressing after "
                          "gemcitabine-cisplatin and FOLFOX; ECOG 1."),
    "investigator.name": "Jordan A. Rivera, MD",
    "investigator.phone": "(312) 555-0148",
    "drug.name": "Cytoravir",
    "drug.route": "Oral",
    "submission.fda_receipt_date": "2026-06-15",
    "site.name": "Fictional Oncology Associates, Rivertown, IL",
}

FORBIDDEN_STRINGS = ("Jordan", "Rivera", "555-0148", "2026-06-15",
                     "Rivertown", "PT-3926-014", "Refractory")


class _RecordingAdapter:
    """In-memory adapter: records exactly what reached it, returns nothing."""

    def __init__(self):
        self.calls = []

    def search(self, destination, condition_codes, drug_name=None,
               drug_rxnorm=None):
        self.calls.append({"destination": destination,
                           "condition_codes": list(condition_codes),
                           "drug_name": drug_name, "drug_rxnorm": drug_rxnorm})
        return []


def _predicates(**overrides):
    base = dict(condition_codes=("70179006", "C22.1"), drug_name="Cytoravir",
                age_band="55-59", sex="female", route_code="26643006")
    base.update(overrides)
    return DeidentifiedPredicates(**base)


class TestClosedStruct(unittest.TestCase):
    """The struct's field set is CLOSED: nothing else can be represented."""

    def test_identifier_field_rejected_at_construction(self):
        for bad_kwarg in ("patient_name", "mrn", "birth_date", "address",
                          "free_text", "diagnosis_text"):
            with self.assertRaises(TypeError, msg=bad_kwarg):
                DeidentifiedPredicates(condition_codes=("C22.1",),
                                       **{bad_kwarg: "anything"})

    def test_date_shaped_values_rejected_everywhere(self):
        with self.assertRaises(ValueError):
            DeidentifiedPredicates(condition_codes=("1968-03-14",))
        with self.assertRaises(ValueError):
            _predicates(age_band="1968-03-14")
        with self.assertRaises(ValueError):
            _predicates(drug_name="03/14/1968")

    def test_free_text_rejected(self):
        # Multi-word strings (names, narratives) cannot pass as codes or drug.
        with self.assertRaises(ValueError):
            _predicates(drug_name="pt Harriet Quimby started drug")
        with self.assertRaises(ValueError):
            DeidentifiedPredicates(condition_codes=("metastatic disease",))
        with self.assertRaises(ValueError):
            _predicates(sex="female, per note by Dr. Rivera")

    def test_single_token_identifiers_rejected_as_codes(self):
        # MAJOR-1: a surname, an 8-digit DOB, and a coded patient id are all
        # single tokens that passed the old permissive regex — the two-shape
        # code check must reject each.
        for bad in ("Rivera", "19680314", "PT3926.014", "Cytoravir"):
            with self.assertRaises(ValueError):
                DeidentifiedPredicates(condition_codes=(bad,))
        # ...while real SNOMED / ICD-10-CM codes still construct.
        ok = DeidentifiedPredicates(condition_codes=("70179006", "C22.1"))
        self.assertEqual(ok.condition_codes, ("70179006", "C22.1"))

    def test_raw_age_rejected_only_bands_allowed(self):
        with self.assertRaises(ValueError):
            _predicates(age_band="58")          # a raw age is not a band
        with self.assertRaises(ValueError):
            _predicates(age_band="55-60")       # not a 5-year band
        _predicates(age_band="90+")             # the safe-harbor top: fine
        _predicates(age_band=None)              # honest absence: fine

    def test_struct_is_frozen(self):
        p = _predicates()
        with self.assertRaises(Exception):
            p.drug_name = "Other"


class TestFromProfile(unittest.TestCase):
    """from_profile derives ONLY the closed set — never names/dates/text."""

    def test_sample_intake_derivation(self):
        p = DeidentifiedPredicates.from_profile(SAMPLE_INTAKE)
        self.assertEqual(p.age_band, "55-59")        # 58 -> 5-year band
        self.assertEqual(p.sex, "female")
        # Cytoravir is investigational — not in the closed drug table, so it
        # resolves to None (honest absence); the raw name never egresses (MAJOR-2).
        self.assertIsNone(p.drug_name)
        self.assertEqual(p.route_code, "26643006")   # Oral -> SNOMED coded
        self.assertIn("70179006", p.condition_codes)
        self.assertIn("C22.1", p.condition_codes)

    def test_no_identifier_or_date_survives(self):
        p = DeidentifiedPredicates.from_profile(SAMPLE_INTAKE)
        serialized = json.dumps(p.as_dict())
        for s in FORBIDDEN_STRINGS:
            self.assertNotIn(s, serialized)
        self.assertNotIn("58", json.dumps(p.as_dict()["age_band"]))  # band, not age

    def test_age_90_plus_top_band(self):
        p = DeidentifiedPredicates.from_profile({"patient.age": "94"})
        self.assertEqual(p.age_band, "90+")
        self.assertEqual(age_band_from_age(90), "90+")
        self.assertEqual(age_band_from_age(89), "85-89")
        self.assertEqual(age_band_from_age(0), "0-4")
        self.assertIsNone(age_band_from_age("unknown"))
        self.assertIsNone(age_band_from_age(None))

    def test_unrecognized_diagnosis_yields_no_codes_never_text(self):
        p = DeidentifiedPredicates.from_profile(
            {"patient.diagnosis": "an extremely unusual syndrome of Dr. Foo"})
        self.assertEqual(p.condition_codes, ())
        self.assertNotIn("syndrome", json.dumps(p.as_dict()))

    def test_drug_derived_from_closed_table_only(self):
        # MAJOR-2: raw drug.name text must NEVER egress. A known agent resolves
        # to its canonical token; an investigational/unrecognized agent — or a
        # name mistyped into the drug field — resolves to None.
        known = DeidentifiedPredicates.from_profile(
            {"drug.name": "Gemcitabine 1000 mg/m2"})
        self.assertEqual(known.drug_name, "gemcitabine")
        for raw in ("Cytoravir (investigational, per Dr. Rivera)",
                    "Rivera investigational compound",   # a surname in the drug field
                    "pt Harriet Quimby's study drug"):
            p = DeidentifiedPredicates.from_profile({"drug.name": raw})
            self.assertIsNone(p.drug_name)
            self.assertNotIn("Rivera", json.dumps(p.as_dict()))
            self.assertNotIn("Quimby", json.dumps(p.as_dict()))


class TestAllowListAndLiveFlag(unittest.TestCase):

    def test_allow_list_contents(self):
        self.assertEqual(ALLOWED_DESTINATIONS,
                         {"clinicaltrials.gov", "eutils.ncbi.nlm.nih.gov",
                          "api.fda.gov"})

    def test_off_list_destination_refused_before_any_query(self):
        adapter, trail = _RecordingAdapter(), []
        for bad in ("evil.example.com", "clinicaltrials.gov.evil.com",
                    "www.clinicaltrials.gov", ""):
            with self.assertRaises(ValueError, msg=bad):
                egress_query(_predicates(), bad, adapter=adapter, trail=trail)
        self.assertEqual(adapter.calls, [])   # nothing reached the adapter
        self.assertEqual(trail, [])           # and nothing egressed to audit

    def test_live_true_raises_egress_disabled(self):
        adapter, trail = _RecordingAdapter(), []
        with self.assertRaises(EgressDisabled) as ctx:
            egress_query(_predicates(), "clinicaltrials.gov",
                         adapter=adapter, trail=trail, live=True)
        self.assertIn("requires greenlight", str(ctx.exception))
        self.assertEqual(adapter.calls, [])
        self.assertFalse(egress._LIVE_EGRESS_ENABLED)  # the flag ships OFF

    def test_raw_dict_cannot_cross_the_boundary(self):
        with self.assertRaises(TypeError):
            egress_query({"condition_codes": ["C22.1"]},  # type: ignore[arg-type]
                         "clinicaltrials.gov",
                         adapter=_RecordingAdapter(), trail=[])


class TestAuditTrail(unittest.TestCase):
    """Every query — mock included — writes ONE value-free audit record."""

    def test_every_query_audit_logged(self):
        adapter, trail = _RecordingAdapter(), []
        egress_query(_predicates(), "clinicaltrials.gov",
                     adapter=adapter, trail=trail)
        egress_query(_predicates(), "api.fda.gov",
                     adapter=adapter, trail=trail)
        self.assertEqual(len(trail), 2)
        for rec in trail:
            self.assertEqual(rec["action"], "egress_query")
        self.assertEqual(trail[0]["target"], "clinicaltrials.gov")
        self.assertEqual(trail[1]["target"], "api.fda.gov")
        self.assertEqual(audit_mod.verify_chain(trail), [])   # chain intact

    def test_audit_detail_is_value_free_and_decomposed(self):
        trail = []
        egress_query(DeidentifiedPredicates.from_profile(SAMPLE_INTAKE),
                     "clinicaltrials.gov", adapter=_RecordingAdapter(),
                     trail=trail)
        serialized = json.dumps(trail)
        for s in FORBIDDEN_STRINGS:
            self.assertNotIn(s, serialized)
        detail = trail[0]["detail"]
        # Decomposition is recorded: age/sex/route were WITHHELD.
        self.assertTrue(detail["decomposed"])
        self.assertIn("age_band", detail["withheld_local_filters"])
        self.assertIn("sex", detail["withheld_local_filters"])
        for key in ("age_band", "sex", "route_code"):
            self.assertNotIn(key, [k for k in detail
                                   if k != "withheld_local_filters"])
        self.assertFalse(detail["live"])


class TestInferenceMitigations(unittest.TestCase):
    """SERIOUS 4: roll-up + decomposition, with the residual documented."""

    def test_icd10_extension_rolls_up_to_category(self):
        self.assertEqual(roll_up_condition_codes(["C22.1"]), ["C22"])
        self.assertEqual(roll_up_condition_codes(["G12.21", "G12.29"]), ["G12"])
        # SNOMED passes through unchanged (documented residual).
        self.assertEqual(roll_up_condition_codes(["70179006"]), ["70179006"])
        # A bare category stays itself; order preserved, de-duplicated.
        self.assertEqual(roll_up_condition_codes(["C22", "C22.1", "70179006"]),
                         ["C22", "70179006"])

    def test_outbound_query_carries_condition_alone(self):
        outbound, local = decompose_query(_predicates())
        self.assertEqual(set(outbound),
                         {"condition_codes", "drug_name", "drug_rxnorm"})
        self.assertEqual(outbound["condition_codes"], ["70179006", "C22"])
        self.assertEqual(sorted(local), ["age_band", "route_code", "sex"])

    def test_adapter_never_sees_age_or_sex(self):
        adapter, trail = _RecordingAdapter(), []
        egress_query(_predicates(), "clinicaltrials.gov",
                     adapter=adapter, trail=trail)
        call = adapter.calls[0]
        serialized = json.dumps(call)
        self.assertNotIn("55-59", serialized)
        self.assertNotIn("female", serialized)
        self.assertNotIn("26643006", serialized)          # route stays local
        self.assertEqual(call["condition_codes"], ["70179006", "C22"])  # rolled

    def test_residual_risk_documented_in_module_docstring(self):
        doc = egress.__doc__ or ""
        self.assertIn("RESIDUAL", doc.upper())
        self.assertIn("re-identification", doc.lower())

    def test_module_never_names_the_phi_ingestion_path(self):
        src = (ENGINE_ROOT / "ossicro" / "egress.py").read_text(encoding="utf-8")
        self.assertNotIn("fhir" + "_ingest", src)
        self.assertIsNone(re.search(r"^\s*(?:import|from)\s+\w*fhir", src,
                                    re.MULTILINE))


if __name__ == "__main__":
    unittest.main(verbosity=2)
