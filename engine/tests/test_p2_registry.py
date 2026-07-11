"""Overhaul P2 — registry + intake-schema foundation tests.

Covers the P2 contracts later packages consume:

- M5: ``submission.date`` is a live intake field, the primary ``as_of``
  anchor, and the 30-day IND clock's backstop trigger;
- M7: the drug-accountability log is a SHELL filled at dispensing — required
  fields reduced to the drug name, honest MISSING columns, green-with-note
  ledger row on the sample case;
- [PT-4]: every document registry entry carries a valid ``author_party``
  (who authors/signs the real-world instrument) and the loader fails closed
  without it;
- P2 field contracts: the external-party receipt facts, anchor/attestation
  fields, and triage facts exist in the schema with the declared ids, types,
  and options, and their citations reconcile with the single-source table;
- m7: the IRB concurrence request sits in eCTD Module 1, not Module 5;
- [PT-3]: the claim registry loads, is complete, and fails closed.

Run: `cd engine && python -m unittest tests.test_p2_registry -v`.
"""

import datetime
import json
import unittest
from pathlib import Path

from ossicro import ea_generators, registry, routes
from ossicro.citations import cite
from ossicro.ea_generators import (
    build_study,
    compute_clocks,
    derive_as_of,
    generate_route_documents,
)
from ossicro.pipeline import run_check
from ossicro.registry import (
    AUTHOR_PARTIES,
    RegistryError,
    load_claims,
    load_documents,
    load_gates,
)

ENGINE_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_PATH = ENGINE_ROOT / "fixtures" / "ea_sample_case.json"

D = datetime.date

# The P2 field contracts: id -> declared type. Later packages use these ids
# exactly as written here (OVERHAUL-PLAN P2 spec items 1, 4, 5).
P2_NEW_FIELDS = {
    "submission.date": "date",
    "manufacturer.loa_received_date": "date",
    "manufacturer.loa_signatory": "text",
    "manufacturer.loa_document_sha256": "text",
    "submission.fda_authorization_date": "date",
    "treatment.conclusion_date": "date",
    "consent.timing_attestation": "select",
    "consent.injury_compensation_statement": "textarea",
    "consent.cost_statement": "textarea",
    "drug.quantity_requested": "text",
    "submission.needed_by_date": "date",
    "submission.cost_recovery_statement": "textarea",
}

TIMING_OPTIONS = ["obtained-before-treatment", "exception-50.23-documented",
                  "not-yet-obtained"]


def _sample_fields():
    data = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    return dict(data.get("fields", data))


def _schema_by_id():
    return {f["id"]: f for f in routes.intake_fields()}


# ---------------------------------------------------------------------------
# P2 spec item 5 — the new intake-field contracts
# ---------------------------------------------------------------------------

class NewIntakeFieldContractTests(unittest.TestCase):
    def test_every_p2_field_exists_with_declared_type_and_is_optional(self):
        by_id = _schema_by_id()
        for field_id, ftype in P2_NEW_FIELDS.items():
            self.assertIn(field_id, by_id, field_id)
            field = by_id[field_id]
            self.assertEqual(field["type"], ftype, field_id)
            # None of the new fields is required: each records a fact that
            # may honestly not exist yet (HC2 — never force an invention).
            self.assertFalse(field.get("required"), field_id)
            # House style: every field carries a citation and (almost) all
            # carry help; at minimum the keys exist.
            self.assertTrue(field.get("citation"), field_id)
            self.assertIn("help", field, field_id)

    def test_timing_attestation_options_exact(self):
        field = _schema_by_id()["consent.timing_attestation"]
        self.assertEqual(field.get("options"), TIMING_OPTIONS)

    def test_new_field_citations_reconcile_with_single_source_table(self):
        # routes.json cannot call cite() — this reconciliation is the
        # single-source guarantee for the P2 pinpoints ([PT-2] discipline).
        by_id = _schema_by_id()
        self.assertEqual(by_id["consent.injury_compensation_statement"]["citation"],
                         cite("consent.element_injury_compensation"))
        self.assertEqual(by_id["submission.cost_recovery_statement"]["citation"],
                         cite("charging.expanded_access"))
        self.assertEqual(by_id["treatment.conclusion_date"]["citation"],
                         cite("ea.end_of_treatment_summary"))
        cost = by_id["consent.cost_statement"]["citation"]
        self.assertIn(cite("consent.element_costs"), cost)
        self.assertIn("312.8(d)", cost)          # charging.consent_disclosure
        timing = by_id["consent.timing_attestation"]["citation"]
        self.assertIn(cite("consent.general_requirements"), timing)
        self.assertIn("50.23", timing)           # consent.emergency_exception

    def test_p2_pinpoints_registered_pending(self):
        # HITL: new pinpoints ship PENDING-HUMAN-VERIFICATION, never silently
        # asserted final.
        from ossicro import citations
        for key in ("consent.general_requirements", "consent.emergency_exception",
                    "consent.element_injury_compensation", "consent.element_costs",
                    "charging.expanded_access", "charging.consent_disclosure",
                    "ea.end_of_treatment_summary"):
            row = citations.CITATIONS[key]
            self.assertEqual(row.status, citations.PENDING_HUMAN_VERIFICATION, key)


# ---------------------------------------------------------------------------
# M5 — submission.date is live: anchor + clock backstop
# ---------------------------------------------------------------------------

class SubmissionDateTests(unittest.TestCase):
    def test_sample_fixture_carries_submission_date(self):
        self.assertEqual(_sample_fields().get("submission.date"), "2026-06-15")

    def test_submission_date_is_the_primary_as_of_anchor(self):
        self.assertEqual(ea_generators._AS_OF_FIELDS[0], "submission.date")
        route = routes.route_for_emergency(False)
        fields = _sample_fields()
        # only submission.date remains among the anchor fields
        del fields["submission.fda_receipt_date"]
        fields["submission.date"] = "2026-06-12"
        study = build_study(fields, route)
        self.assertEqual(derive_as_of(study), D(2026, 6, 12))
        documents = generate_route_documents(study, route, load_documents())
        cover = documents["expanded-access-cover-letter"]
        self.assertEqual(cover.fields.get("cover_date"), "2026-06-12")
        self.assertNotIn("[[MISSING: cover_date]]", cover.rendered)

    def test_30_day_clock_backstops_on_submission_date(self):
        # The previously dead fallback (compute_clocks) is now reachable from
        # the intake form: receipt date absent, submission.date present.
        route = routes.route_for_emergency(False)
        fields = _sample_fields()
        del fields["submission.fda_receipt_date"]
        study = build_study(fields, route)
        (clock,) = compute_clocks(study, route)
        self.assertTrue(clock["armed"])
        self.assertEqual(clock["trigger_value"], "2026-06-15")
        self.assertEqual(clock["deadline"], "2026-07-15")


# ---------------------------------------------------------------------------
# M7 — drug-accountability shell semantics (decided: filled at dispensing)
# ---------------------------------------------------------------------------

class DrugAccountabilityShellTests(unittest.TestCase):
    def test_required_fields_reduced_to_drug_name(self):
        entry = load_documents()["drug-accountability-log"]
        self.assertEqual(entry["required_fields"], ["drug_name"])

    def test_registry_description_states_the_decision(self):
        entry = load_documents()["drug-accountability-log"]
        self.assertIn("filled at dispensing", entry.get("description", "").lower())

    def test_sample_fixture_carries_no_dispensing_values(self):
        fields = _sample_fields()
        self.assertNotIn("drug.lot_numbers", fields)
        self.assertNotIn("drug.dispensing_entries", fields)

    def test_ledger_green_with_honest_missing_columns(self):
        # Re-baseline: the shell goes green on the drug name alone; the
        # dispensing-time columns stay explicit MISSING markers, and the
        # rendered note says why that is honest.
        fields = _sample_fields()
        route = routes.route_for_emergency(False)
        study = build_study(fields, route)
        documents = generate_route_documents(study, route, load_documents())
        doc = documents["drug-accountability-log"]
        self.assertIn("[[MISSING: lot_numbers]]", doc.rendered)
        self.assertIn("[[MISSING: dispensing_entries]]", doc.rendered)
        self.assertIn("honestly absent at submission time", doc.rendered)
        result = run_check(study, documents, load_documents(), load_gates())
        item = next(i for i in result.ledger
                    if i.doc_id == "drug-accountability-log")
        self.assertEqual(item.status, "green")
        self.assertEqual(item.questions, [])   # no resolving question remains


# ---------------------------------------------------------------------------
# [PT-4] — author_party on every document; loader fails closed
# ---------------------------------------------------------------------------

class AuthorPartyTests(unittest.TestCase):
    def test_every_entry_carries_a_valid_author_party(self):
        for doc_id, entry in load_documents().items():
            self.assertIn(entry.get("author_party"), AUTHOR_PARTIES, doc_id)

    def test_declared_assignments(self):
        docs = load_documents()
        # The plan's explicit assignments: the LOA is the manufacturer's
        # instrument; requests drafted for the physician's own hand stay
        # physician; the IRB's own letter is the IRB's.
        self.assertEqual(docs["manufacturer-letter-of-authorization"]["author_party"],
                         "manufacturer")
        self.assertEqual(docs["irb-initial-approval-letter"]["author_party"], "irb")
        self.assertEqual(docs["irb-concurrence-request"]["author_party"], "physician")
        self.assertEqual(docs["manufacturer-loa-request"]["author_party"], "physician")
        self.assertEqual(
            docs["form-fda-3926-individual-patient-expanded-access"]["author_party"],
            "physician")
        self.assertEqual(docs["expanded-access-cover-letter"]["author_party"],
                         "physician")

    def test_loader_fails_closed_on_missing_author_party(self):
        with self.assertRaises(RegistryError):
            registry._require_author_party({"id": "no-party-doc"})

    def test_loader_fails_closed_on_unknown_author_party(self):
        with self.assertRaises(RegistryError):
            registry._require_author_party(
                {"id": "bad-party-doc", "author_party": "vendor"})

    def test_valid_author_party_passes(self):
        for party in AUTHOR_PARTIES:
            registry._require_author_party({"id": "ok", "author_party": party})


# ---------------------------------------------------------------------------
# m7 — eCTD placement of the IRB concurrence request
# ---------------------------------------------------------------------------

class EctdPlacementTests(unittest.TestCase):
    def test_irb_concurrence_request_in_module_1_not_module_5(self):
        for emergency in (False, True):
            route = routes.route_for_emergency(emergency)
            modules = {m["module"]: m["doc_ids"] for m in route["ectd_map"]}
            self.assertIn("irb-concurrence-request", modules["Module 1"],
                          route["route_id"])
            self.assertNotIn("irb-concurrence-request", modules["Module 5"],
                             route["route_id"])


# ---------------------------------------------------------------------------
# [PT-3] — the claim registry loads and fails closed
# ---------------------------------------------------------------------------

class ClaimRegistryTests(unittest.TestCase):
    REQUIRED_CLAIMS = ("nothing-submitted-to-fda", "chart-data-stays-local",
                       "drafts-only-banner", "no-direct-identifiers-in-view")

    def test_starting_claim_set_present_and_complete(self):
        claims = load_claims()
        for cid in self.REQUIRED_CLAIMS:
            self.assertIn(cid, claims)
            claim = claims[cid]
            for key in ("text", "true_when", "tripwire"):
                self.assertTrue(str(claim.get(key, "")).strip(), (cid, key))
            # the tripwire literal must actually be distinctive OF the claim
            self.assertIn(claim["tripwire"].lower(), claim["text"].lower(), cid)

    def test_loader_fails_closed_on_incomplete_claim(self):
        with self.assertRaises(RegistryError):
            registry._validate_claim_entry({"id": "x", "text": "y"})
        with self.assertRaises(RegistryError):
            registry._validate_claim_entry(
                {"id": "x", "text": "", "true_when": "t", "tripwire": "w"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
