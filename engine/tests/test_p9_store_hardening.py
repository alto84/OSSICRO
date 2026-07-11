"""Overhaul P9 engine tests: m14 keyed profile hashes + m20 identifier lint.

m14 — HMAC-SHA256 keyed hashing in ossicro.profile:
  - a keyed hash differs from the unkeyed hash AND from the same value under
    a different key (enumeration resistance comes from the key);
  - the "hmac-sha256:" prefix and the versioned hash_scheme tag are visible —
    the two schemes can never silently compare equal;
  - pending-detection and revert-equality semantics are UNCHANGED under a
    key (commit -> nothing pending; edit -> that field pending; revert ->
    nothing pending);
  - an old UNKEYED committed profile re-verified under a key fails LOUD
    (every field pending; require_committed refuses) — never silently wrong.

m20 — lint_free_text_identifiers in ossicro.egress:
  - fires on seeded identifier text (SSN shape, date shape, DOB label,
    "name:"-adjacent capitalized pair), naming the FIELD and the KIND;
  - never echoes the matched text into the warning;
  - stays silent on the synthetic sample case's free-text fields;
  - escalate-only shape: warnings are data; nothing is mutated.
"""

import json
import unittest
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parents[1]

from ossicro.egress import lint_free_text_identifiers
from ossicro.profile import (
    HASH_SCHEME_KEYED,
    HASH_SCHEME_UNKEYED,
    ProfileNotCommitted,
    commit_profile,
    confirm_fields,
    field_value_hash,
    hash_scheme,
    pending_fields,
    profile_hash,
    require_committed,
)

ACTOR = "Jordan A. Rivera, MD"
KEY_A = b"k" * 32
KEY_B = b"q" * 32

BASE = {
    "patient.coded_id": "AB-01",
    "patient.diagnosis": "cholangiocarcinoma",
    "drug.name": "examplinib",
}


# ---------------------------------------------------------------------------
# m14 — keyed hashing
# ---------------------------------------------------------------------------

class TestKeyedHashing(unittest.TestCase):

    def test_keyed_hash_differs_from_unkeyed_and_other_key(self):
        unkeyed = field_value_hash("cholangiocarcinoma")
        keyed_a = field_value_hash("cholangiocarcinoma", key=KEY_A)
        keyed_b = field_value_hash("cholangiocarcinoma", key=KEY_B)
        self.assertNotEqual(keyed_a, unkeyed)
        self.assertNotEqual(keyed_a, keyed_b)   # the key IS the protection
        # deterministic under the same key
        self.assertEqual(keyed_a, field_value_hash("cholangiocarcinoma", key=KEY_A))
        # same behavior for the whole-profile hash
        self.assertNotEqual(profile_hash(BASE, key=KEY_A), profile_hash(BASE))
        self.assertNotEqual(profile_hash(BASE, key=KEY_A),
                            profile_hash(BASE, key=KEY_B))

    def test_scheme_prefixes_and_tags_are_visible(self):
        self.assertTrue(field_value_hash("x", key=KEY_A).startswith("hmac-sha256:"))
        self.assertTrue(field_value_hash("x").startswith("sha256:"))
        self.assertEqual(hash_scheme(KEY_A), HASH_SCHEME_KEYED)
        self.assertEqual(hash_scheme(None), HASH_SCHEME_UNKEYED)
        keyed_cp = commit_profile(dict(BASE), ACTOR, key=KEY_A)
        self.assertEqual(keyed_cp["hash_scheme"], HASH_SCHEME_KEYED)
        unkeyed_cp = commit_profile(dict(BASE), ACTOR)
        self.assertEqual(unkeyed_cp["hash_scheme"], HASH_SCHEME_UNKEYED)
        for h in keyed_cp["field_hashes"].values():
            self.assertTrue(h.startswith("hmac-sha256:"))

    def test_keyed_commit_stores_hashes_never_values(self):
        cp = commit_profile(dict(BASE), ACTOR, key=KEY_A)
        blob = json.dumps(cp)
        for value in BASE.values():
            self.assertNotIn(value, blob)
        # ...and never the key itself
        self.assertNotIn(KEY_A.decode("ascii"), blob)

    def test_equality_semantics_preserved_under_key(self):
        cp = commit_profile(dict(BASE), ACTOR, key=KEY_A)
        # committed -> nothing pending, gate passes
        self.assertEqual(pending_fields(dict(BASE), cp, key=KEY_A), [])
        self.assertEqual(require_committed(dict(BASE), cp, key=KEY_A),
                         cp["profile_hash"])
        # edit -> exactly that field pending
        flat = dict(BASE, **{"drug.name": "otherdrug"})
        self.assertEqual(pending_fields(flat, cp, key=KEY_A), ["drug.name"])
        with self.assertRaises(ProfileNotCommitted):
            require_committed(flat, cp, key=KEY_A)
        # revert -> nothing pending again (revert-equality)
        flat["drug.name"] = BASE["drug.name"]
        self.assertEqual(pending_fields(flat, cp, key=KEY_A), [])
        self.assertEqual(profile_hash(flat, key=KEY_A), cp["profile_hash"])

    def test_confirm_fields_auto_recommits_under_the_same_key(self):
        cp = commit_profile(dict(BASE), ACTOR, key=KEY_A)
        flat = dict(BASE, **{"drug.name": "otherdrug"})
        cp2 = confirm_fields(flat, cp, ACTOR, ["drug.name"], key=KEY_A)
        self.assertEqual(pending_fields(flat, cp2, key=KEY_A), [])
        self.assertEqual(cp2["profile_hash"], profile_hash(flat, key=KEY_A))
        self.assertEqual(cp2["hash_scheme"], HASH_SCHEME_KEYED)

    def test_old_unkeyed_profile_fails_loud_under_key(self):
        # An old synthetic case committed UNKEYED, re-verified by a keyed
        # server: every field reads pending and the gate refuses — loud,
        # user-fixable (recommit), never a silent wrong match.
        old_cp = commit_profile(dict(BASE), ACTOR)          # sha256-v1
        self.assertEqual(old_cp["hash_scheme"], HASH_SCHEME_UNKEYED)
        pending = pending_fields(dict(BASE), old_cp, key=KEY_A)
        self.assertEqual(pending, sorted(BASE))             # ALL fields pending
        with self.assertRaises(ProfileNotCommitted) as ctx:
            require_committed(dict(BASE), old_cp, key=KEY_A)
        self.assertEqual(ctx.exception.state, "CONFIRMING")
        self.assertEqual(ctx.exception.pending, sorted(BASE))

    def test_blank_value_still_refused_keyed(self):
        with self.assertRaises(ValueError):
            field_value_hash("   ", key=KEY_A)

    def test_non_bytes_key_is_a_typeerror(self):
        with self.assertRaises(TypeError):
            field_value_hash("x", key="a-string-not-bytes")


# ---------------------------------------------------------------------------
# m20 — the identifier lint
# ---------------------------------------------------------------------------

class TestIdentifierLint(unittest.TestCase):

    def _kinds_for(self, text, field="request.clinical_rationale"):
        return {(w["field_id"], w["kind"])
                for w in lint_free_text_identifiers({field: text})}

    def test_ssn_shape_fires_naming_the_field(self):
        warnings = lint_free_text_identifiers(
            {"patient.no_alternative_basis": "insured under 123-45-6789"})
        self.assertEqual(len(warnings), 1)
        w = warnings[0]
        self.assertEqual(w["field_id"], "patient.no_alternative_basis")
        self.assertEqual(w["kind"], "ssn")
        self.assertIn("patient.no_alternative_basis", w["message"])
        # never a block, never a rewrite is the CALLER's contract; here we
        # assert the warning is pure data and echoes NO matched text
        self.assertNotIn("123-45-6789", w["message"])

    def test_date_shapes_fire(self):
        self.assertIn(("request.clinical_rationale", "date-like"),
                      self._kinds_for("progressed on 2025-11-03 despite tx"))
        self.assertIn(("request.clinical_rationale", "date-like"),
                      self._kinds_for("seen 11/03/2025 in clinic"))

    def test_dob_label_fires(self):
        self.assertIn(("request.clinical_rationale", "dob-label"),
                      self._kinds_for("DOB on file at the clinic"))
        self.assertIn(("request.clinical_rationale", "dob-label"),
                      self._kinds_for("her date of birth is on record"))

    def test_name_adjacent_capitalized_pair_fires(self):
        self.assertIn(("request.clinical_rationale", "name-label"),
                      self._kinds_for("Patient name: Jane Doe, per chart"))
        self.assertIn(("request.clinical_rationale", "name-label"),
                      self._kinds_for("name = John Q. Public"))

    def test_clean_clinical_narrative_is_silent(self):
        self.assertEqual(lint_free_text_identifiers({
            "request.clinical_rationale":
                "Metastatic cholangiocarcinoma, progressed after two lines; "
                "no comparable alternative therapy remains."}), [])

    def test_non_string_and_blank_values_ignored(self):
        self.assertEqual(lint_free_text_identifiers(
            {"a": None, "b": 5, "c": True, "d": "   "}), [])
        self.assertEqual(lint_free_text_identifiers({}), [])

    def test_silent_on_the_sample_case_free_text(self):
        # The synthetic sample case's TEXTAREA (free-text) fields carry no
        # identifier-shaped content — the lint must not cry wolf on the
        # shipped fixture. Field types come from the route schema itself.
        from ossicro import routes as routes_mod
        with open(ENGINE_ROOT / "fixtures" / "ea_sample_case.json",
                  encoding="utf-8") as f:
            fields = json.load(f)["fields"]
        textarea_ids = {f["id"] for f in routes_mod.intake_fields()
                        if f.get("type") == "textarea"}
        subset = {k: v for k, v in fields.items() if k in textarea_ids}
        self.assertTrue(subset)   # the sweep is meaningful, not vacuous
        self.assertEqual(lint_free_text_identifiers(subset), [])

    def test_multiple_fields_sorted_and_independent(self):
        warnings = lint_free_text_identifiers({
            "z.late": "SSN 987-65-4321",
            "a.early": "name: Jane Doe",
        })
        self.assertEqual([w["field_id"] for w in warnings],
                         ["a.early", "z.late"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
