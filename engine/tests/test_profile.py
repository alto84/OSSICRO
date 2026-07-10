"""INV-3 engine tests: canonicalization, commit, pending, staging, stamping.

Design spec: docs/ehr-integration/commit-profile-design.md §8 items 1-8.
Pure engine — no app import, no I/O beyond the fixtures directory.
"""

import hashlib
import json
import re
import unittest
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parents[1]

from ossicro import routes as routes_mod
from ossicro.ea_generators import build_study, generate_route_documents
from ossicro.models import Document, GateViolation, ProvenanceRecord
from ossicro.profile import (
    ProfileNotCommitted,
    canonicalize_intake,
    commit_profile,
    confirm_fields,
    field_value_hash,
    pending_fields,
    profile_hash,
    require_committed,
    stamp_input_hash,
)
from ossicro.registry import load_documents

ACTOR = "Jordan A. Rivera, MD"

BASE = {
    "patient.coded_id": "AB-01",
    "patient.diagnosis": "cholangiocarcinoma",
    "drug.name": "examplinib",
}


def _committed(flat=None, actor=ACTOR):
    return commit_profile(dict(flat or BASE), actor)


# ---------------------------------------------------------------------------
# §8 item 1 — canonicalization
# ---------------------------------------------------------------------------

class TestCanonicalization(unittest.TestCase):

    def test_key_order_independent(self):
        a = {"b.two": "2", "a.one": "1"}
        b = {"a.one": "1", "b.two": "2"}
        self.assertEqual(profile_hash(a), profile_hash(b))
        self.assertEqual(canonicalize_intake(a), canonicalize_intake(b))

    def test_whitespace_newline_equivalence(self):
        self.assertEqual(
            profile_hash({"k": "some  clinical\nnarrative\ttext "}),
            profile_hash({"k": "some clinical narrative text"}),
        )

    def test_nfc_equivalence(self):
        composed = {"k": "Rivière"}     # e-grave, precomposed
        decomposed = {"k": "Rivière"}  # e + COMBINING GRAVE ACCENT
        self.assertEqual(profile_hash(composed), profile_hash(decomposed))
        self.assertEqual(field_value_hash("Rivière"),
                         field_value_hash("Rivière"))

    def test_distinct_values_distinct_hash(self):
        self.assertNotEqual(profile_hash({"k": "alpha"}),
                            profile_hash({"k": "beta"}))
        self.assertNotEqual(field_value_hash("alpha"), field_value_hash("beta"))

    def test_empty_after_normalization_dropped(self):
        self.assertEqual(profile_hash({"a": "1", "gone": "   \n\t "}),
                         profile_hash({"a": "1"}))
        self.assertEqual(profile_hash({"a": "1", "gone": None}),
                         profile_hash({"a": "1"}))

    def test_non_string_scalars_hash_as_json_text(self):
        self.assertEqual(profile_hash({"k": True}), profile_hash({"k": "true"}))
        self.assertEqual(profile_hash({"k": 3}), profile_hash({"k": "3"}))
        self.assertEqual(field_value_hash(True), field_value_hash("true"))
        # ...and NOT as Python str() forms
        self.assertNotEqual(profile_hash({"k": True}), profile_hash({"k": "True"}))

    def test_preimage_domain_prefix_present(self):
        canon = canonicalize_intake(BASE)
        with_prefix = "sha256:" + hashlib.sha256(
            ("ossicro-profile-v1\n" + canon).encode("utf-8")).hexdigest()
        without_prefix = "sha256:" + hashlib.sha256(
            canon.encode("utf-8")).hexdigest()
        self.assertEqual(profile_hash(BASE), with_prefix)
        self.assertNotEqual(profile_hash(BASE), without_prefix)


# ---------------------------------------------------------------------------
# §8 item 2 — commit refusals
# ---------------------------------------------------------------------------

class TestCommitRefusals(unittest.TestCase):

    def test_blank_actor_gate_violation(self):
        with self.assertRaises(GateViolation):
            commit_profile(dict(BASE), "")
        with self.assertRaises(GateViolation):
            commit_profile(dict(BASE), "   ")

    def test_empty_intake_refused(self):
        with self.assertRaises(GateViolation):
            commit_profile({}, ACTOR)
        with self.assertRaises(GateViolation):
            commit_profile({"k": "   "}, ACTOR)  # canonically empty

    def test_commit_stores_hashes_never_values(self):
        cp = _committed()
        blob = json.dumps(cp)
        for value in BASE.values():
            self.assertNotIn(value, blob)
        self.assertEqual(set(cp["field_hashes"]), set(BASE))
        for h in cp["field_hashes"].values():
            self.assertTrue(h.startswith("sha256:"))


# ---------------------------------------------------------------------------
# §8 item 3 — pending_fields
# ---------------------------------------------------------------------------

class TestPendingFields(unittest.TestCase):

    def test_edit_pends_exactly_that_field(self):
        cp = _committed()
        flat = dict(BASE, **{"drug.name": "otherdrug"})
        self.assertEqual(pending_fields(flat, cp), ["drug.name"])

    def test_add_pends(self):
        cp = _committed()
        flat = dict(BASE, **{"drug.dose": "10 mg"})
        self.assertEqual(pending_fields(flat, cp), ["drug.dose"])

    def test_delete_pends(self):
        cp = _committed()
        flat = dict(BASE)
        del flat["patient.diagnosis"]
        self.assertEqual(pending_fields(flat, cp), ["patient.diagnosis"])

    def test_revert_clears(self):
        cp = _committed()
        flat = dict(BASE, **{"drug.name": "otherdrug"})
        self.assertEqual(pending_fields(flat, cp), ["drug.name"])
        flat["drug.name"] = BASE["drug.name"]   # reverted
        self.assertEqual(pending_fields(flat, cp), [])
        self.assertEqual(profile_hash(flat), cp["profile_hash"])

    def test_whitespace_only_edit_clears(self):
        cp = _committed()
        flat = dict(BASE, **{"patient.diagnosis": " cholangiocarcinoma \n"})
        self.assertEqual(pending_fields(flat, cp), [])


# ---------------------------------------------------------------------------
# §8 item 4 — staging + auto-recommit
# ---------------------------------------------------------------------------

class TestStaging(unittest.TestCase):

    def test_partial_confirm_stages_then_full_confirm_recommits(self):
        cp = _committed()
        old_hash = cp["profile_hash"]
        flat = dict(BASE, **{"drug.name": "otherdrug",
                             "patient.diagnosis": "new dx"})
        self.assertEqual(pending_fields(flat, cp),
                         ["drug.name", "patient.diagnosis"])
        # confirm 1 of 2 -> still CONFIRMING, staged recorded
        cp2 = confirm_fields(flat, cp, ACTOR, ["drug.name"])
        self.assertEqual(pending_fields(flat, cp2), ["patient.diagnosis"])
        self.assertIn("drug.name", cp2["staged"])
        self.assertEqual(cp2["profile_hash"], old_hash)  # no recommit yet
        # edit the staged field AGAIN -> it re-enters pending
        flat2 = dict(flat, **{"drug.name": "thirddrug"})
        self.assertEqual(pending_fields(flat2, cp2),
                         ["drug.name", "patient.diagnosis"])
        # confirm the last pending on the original edit -> auto-recommit
        cp3 = confirm_fields(flat, cp2, ACTOR, ["patient.diagnosis"])
        self.assertNotEqual(cp3["profile_hash"], old_hash)
        self.assertEqual(cp3["profile_hash"], profile_hash(flat))
        self.assertEqual(cp3["staged"], {})
        self.assertEqual(len(cp3["history"]), 1)
        self.assertEqual(cp3["history"][0]["profile_hash"], old_hash)
        self.assertEqual(cp3["history"][0]["reconfirmed_fields"],
                         ["drug.name", "patient.diagnosis"])
        self.assertEqual(pending_fields(flat, cp3), [])

    def test_confirmed_deletion_recommits(self):
        cp = _committed()
        flat = dict(BASE)
        del flat["patient.diagnosis"]
        cp2 = confirm_fields(flat, cp, ACTOR, ["patient.diagnosis"])
        self.assertEqual(pending_fields(flat, cp2), [])
        self.assertNotIn("patient.diagnosis", cp2["field_hashes"])
        self.assertEqual(cp2["profile_hash"], profile_hash(flat))


# ---------------------------------------------------------------------------
# §8 item 5 — non-pending confirm fails loud
# ---------------------------------------------------------------------------

class TestConfirmFailsLoud(unittest.TestCase):

    def test_non_pending_field_valueerror(self):
        cp = _committed()
        with self.assertRaises(ValueError):
            confirm_fields(dict(BASE), cp, ACTOR, ["patient.coded_id"])

    def test_unknown_field_valueerror(self):
        cp = _committed()
        with self.assertRaises(ValueError):
            confirm_fields(dict(BASE), cp, ACTOR, ["no.such.field"])

    def test_blank_actor_gate_violation(self):
        cp = _committed()
        flat = dict(BASE, **{"drug.name": "otherdrug"})
        with self.assertRaises(GateViolation):
            confirm_fields(flat, cp, "  ", ["drug.name"])


# ---------------------------------------------------------------------------
# §8 item 6 — require_committed
# ---------------------------------------------------------------------------

class TestRequireCommitted(unittest.TestCase):

    def test_none_raises_never_committed(self):
        with self.assertRaises(ProfileNotCommitted) as ctx:
            require_committed(dict(BASE), None)
        self.assertEqual(ctx.exception.state, "UNCOMMITTED")
        self.assertIn("never committed", str(ctx.exception))
        self.assertNotIsInstance(ctx.exception, GateViolation)

    def test_drifted_raises_with_pending(self):
        cp = _committed()
        flat = dict(BASE, **{"drug.name": "otherdrug"})
        with self.assertRaises(ProfileNotCommitted) as ctx:
            require_committed(flat, cp)
        self.assertEqual(ctx.exception.state, "CONFIRMING")
        self.assertEqual(ctx.exception.pending, ["drug.name"])

    def test_matching_returns_hash(self):
        cp = _committed()
        self.assertEqual(require_committed(dict(BASE), cp), cp["profile_hash"])


# ---------------------------------------------------------------------------
# §8 item 7 — stamp_input_hash over real generated documents
# ---------------------------------------------------------------------------

class TestStampInputHash(unittest.TestCase):

    def test_every_record_and_document_stamped(self):
        with open(ENGINE_ROOT / "fixtures" / "ea_sample_case.json",
                  encoding="utf-8") as f:
            data = json.load(f)
        fields = data.get("fields", data)
        route = routes_mod.route_for_emergency(False)
        study = build_study(dict(fields), route)
        documents = generate_route_documents(study, route, load_documents())
        self.assertTrue(documents)
        h = profile_hash(fields)
        stamp_input_hash(documents, h)
        total_records = 0
        for doc in documents.values():
            self.assertEqual(doc.input_hash, h)
            for rec in doc.provenance:   # field, literal, AND verbatim spans
                total_records += 1
                self.assertEqual(rec.input_hash, h)
        self.assertGreater(total_records, 0)

    def test_default_constructed_record_back_compat(self):
        rec = ProvenanceRecord(span="s", source="src", citation="c")
        self.assertEqual(rec.input_hash, "")
        doc = Document(doc_id="d", title="t")
        self.assertEqual(doc.input_hash, "")


# ---------------------------------------------------------------------------
# §8 item 8 — egress boundary: profile.py imports no network client
# (the sweep in test_fhir_ingest.TestEngineEgressBoundary globs *.py and so
# covers profile.py; this asserts it directly and proves the module exists)
# ---------------------------------------------------------------------------

class TestProfileEgressBoundary(unittest.TestCase):

    def test_profile_module_has_no_outbound_client(self):
        path = ENGINE_ROOT / "ossicro" / "profile.py"
        self.assertTrue(path.is_file())
        forbidden = re.compile(
            r"^\s*(?:import|from)\s+(urllib\.request|socket|requests|httpx|"
            r"httplib2|aiohttp|http\.client)\b", re.MULTILINE)
        self.assertIsNone(forbidden.search(path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
