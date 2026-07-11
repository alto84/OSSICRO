"""Overhaul P6 — the EA-profiled informed-consent form (engine half).

Covers:
- Both 3926 routes swap in ``informed-consent-form-part50-ea`` (documents /
  fda_package / ectd_map); the generic ``informed-consent-form-part50``
  stays registered for non-EA routes and its template is untouched.
- The EA ICF renders all 8 verbatim-locked 50.25(a) element headings,
  BYTE-IDENTICAL to the generic form (same tuples by construction), and
  rule R-ICF-50.25-EA verifies them by provenance + SHA-256.
- HITL: the draft banner carries the PENDING-HUMAN-VERIFICATION consent-
  language line (removed only by a qualified human review), the registry
  description names the human review as the release precondition, and the
  deferred concept rule R-ICF-50.25-ADEQ-EA exists (never executed).
- M3: element 6 renders ``consent.injury_compensation_statement`` — absent,
  it is an explicit MISSING marker and the ledger question names the span
  the fix-loop maps to the intake field.
- EA-specific disclosures: treatment-use framing, not-FDA-approved /
  no-evidence-it-works, manufacturer-may-stop-supplying, costs from
  ``consent.cost_statement`` (50.25(b)(3); 312.8(d)), stopping treatment
  (50.25(b)(4)), significant new findings (50.25(b)(5)), voluntariness
  restated (50.25(a)(8)).
- m12: the grown tier-A exculpatory tripwires fire on the FDA guidance
  examples in consent context; the EA ICF's own prose stays tier-A clean
  (false-positive floor); the HC6 note in the registry metadata carries the
  enumerated-constructions / judgment-owns-the-class wording.

Run: `cd engine && python -m unittest tests.test_p6_icf_ea -v`.
"""

import hashlib
import json
import unittest
from pathlib import Path

from ossicro import citations, ea_generators, routes
from ossicro.citations import cite
from ossicro.ea_generators import (
    ICF_EA_PENDING_BANNER,
    build_study,
    generate_route_documents,
)
from ossicro.generate import TEMPLATES, VERBATIM_SPANS, generate_document
from ossicro.pipeline import run_check
from ossicro.register_linter import lint_document, lint_text
from ossicro.registry import load_documents, load_gates
from ossicro.rules import load_rules
from ossicro.validate import run_rules

ENGINE_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_PATH = ENGINE_ROOT / "fixtures" / "ea_sample_case.json"
BANNED_PATH = ENGINE_ROOT / "registry" / "banned-constructions.json"

EA_ICF = "informed-consent-form-part50-ea"
GENERIC_ICF = "informed-consent-form-part50"


def _sample_fields():
    data = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    return dict(data.get("fields", data))


def _route_docs(fields=None, emergency=False):
    route = routes.route_for_emergency(emergency)
    study = build_study(fields if fields is not None else _sample_fields(),
                        route)
    return study, generate_route_documents(study, route, load_documents()), route


class RouteSwapTests(unittest.TestCase):
    def test_both_routes_carry_the_ea_icf_not_the_generic(self):
        for emergency in (False, True):
            route = routes.route_for_emergency(emergency)
            for key in ("documents", "fda_package"):
                self.assertIn(EA_ICF, route[key], (route["route_id"], key))
                self.assertNotIn(GENERIC_ICF, route[key],
                                 (route["route_id"], key))
            modules = {m["module"]: m["doc_ids"] for m in route["ectd_map"]}
            self.assertIn(EA_ICF, modules["Module 5"], route["route_id"])
            self.assertNotIn(GENERIC_ICF, modules["Module 5"],
                             route["route_id"])

    def test_generic_icf_stays_registered_for_non_ea_routes(self):
        docs = load_documents()
        self.assertIn(GENERIC_ICF, docs)
        self.assertIn(EA_ICF, docs)
        self.assertEqual(docs[EA_ICF]["gate"], "informed-consent")
        self.assertEqual(docs[EA_ICF]["author_party"], "physician")
        self.assertEqual(docs[EA_ICF]["category"], "consent")

    def test_route_generation_produces_the_ea_icf(self):
        for emergency in (False, True):
            _study, documents, _route = _route_docs(emergency=emergency)
            self.assertIn(EA_ICF, documents)
            self.assertNotIn(GENERIC_ICF, documents)


class VerbatimHeadingTests(unittest.TestCase):
    """The 8 basic-element headings: byte-identical, hash-locked, rule-run."""

    def setUp(self):
        self.study, self.documents, _ = _route_docs()
        self.icf = self.documents[EA_ICF]

    def test_ea_spans_are_the_same_objects_as_the_generic_spans(self):
        # Aliased, not copied: identity guarantees the headings cannot drift.
        self.assertIs(VERBATIM_SPANS[EA_ICF], VERBATIM_SPANS[GENERIC_ICF])

    def test_all_eight_headings_render_and_hash_to_the_rule_lock(self):
        rule = next(r for r in load_rules() if r.id == "R-ICF-50.25-EA")
        self.assertEqual(rule.doc_id, EA_ICF)
        self.assertEqual(len(rule.params["spans"]), 8)
        for span_id in rule.params["spans"]:
            text, _citation = VERBATIM_SPANS[EA_ICF][span_id]
            self.assertIn(text, self.icf.rendered, span_id)
            self.assertEqual(
                hashlib.sha256(text.encode("utf-8")).hexdigest(),
                rule.params["sha256"][span_id], span_id)

    def test_rule_r_icf_5025_ea_passes_on_the_rendered_document(self):
        results = {r.rule_id: r for r in run_rules(self.study, self.documents)}
        self.assertIn("R-ICF-50.25-EA", results)
        self.assertTrue(results["R-ICF-50.25-EA"].passed,
                        results["R-ICF-50.25-EA"].message)

    def test_provenance_records_stamped_for_every_heading(self):
        spans = {p.span for p in self.icf.provenance}
        for n in range(1, 9):
            self.assertIn("icf-element-%d" % n, spans)

    def test_adequacy_rule_exists_deferred_for_the_ea_doc(self):
        adeq = next(r for r in load_rules() if r.id == "R-ICF-50.25-ADEQ-EA")
        self.assertEqual(adeq.strategy, "concept")
        self.assertEqual(adeq.doc_id, EA_ICF)
        # never executed by run_rules
        ids = {r.rule_id for r in run_rules(self.study, self.documents)}
        self.assertNotIn("R-ICF-50.25-ADEQ-EA", ids)


class HitlBannerTests(unittest.TestCase):
    def setUp(self):
        _s, documents, _r = _route_docs()
        self.rendered = documents[EA_ICF].rendered

    def test_pending_human_verification_banner_present(self):
        # HITL (P6): the spec's exact line, in the draft banner. Removed only
        # by the qualified human review — never by code.
        self.assertIn(ICF_EA_PENDING_BANNER, self.rendered)
        self.assertIn("PENDING-HUMAN-VERIFICATION", ICF_EA_PENDING_BANNER)
        self.assertIn("consent language not yet reviewed by a qualified human",
                      self.rendered)

    def test_pending_citation_footer_also_present(self):
        # The b(4)/b(5)/framing pinpoints are table rows still pending human
        # verification, so the P1 footer rides along too.
        self.assertIn(citations.PENDING_FOOTER, self.rendered)

    def test_registry_description_names_the_human_release_precondition(self):
        desc = load_documents()[EA_ICF].get("description", "")
        self.assertIn("NOT adequacy", desc)
        self.assertIn("release precondition", desc)
        self.assertIn("PENDING-HUMAN-VERIFICATION", desc)

    def test_new_p6_citation_rows_ship_pending(self):
        for key in ("consent.element_stopping", "consent.element_new_findings",
                    "ea.consent.treatment_framing"):
            row = citations.CITATIONS[key]
            self.assertEqual(row.status,
                             citations.PENDING_HUMAN_VERIFICATION, key)
        self.assertEqual(cite("consent.element_stopping"),
                         "21 CFR 50.25(b)(4)")
        self.assertEqual(cite("consent.element_new_findings"),
                         "21 CFR 50.25(b)(5)")


class FramingAndDisclosureTests(unittest.TestCase):
    def setUp(self):
        _s, documents, _r = _route_docs()
        self.icf = documents[EA_ICF]
        self.rendered = self.icf.rendered

    def test_treatment_use_framing_opens_the_form(self):
        # Both-directions therapeutic misconception, resolved explicitly.
        self.assertIn("This is treatment, not a research study, but laws "
                      "that protect research participants also protect you.",
                      self.rendered)
        by_span = {p.span: p.citation for p in self.icf.provenance}
        self.assertEqual(by_span["treatment_framing"],
                         cite("ea.consent.treatment_framing"))

    def test_not_approved_and_no_evidence_disclosure(self):
        self.assertIn("is not approved\n   by the FDA for your condition",
                      self.rendered)
        self.assertIn("NOT evidence that the drug works", self.rendered)

    def test_manufacturer_may_decline_or_stop_supplying(self):
        self.assertIn("decides whether to\n   provide the drug", self.rendered)
        self.assertIn("stop supplying it, at\n   any time", self.rendered)

    def test_cost_statement_rendered_from_intake_with_table_pinpoints(self):
        fields = _sample_fields()
        self.assertIn(fields["consent.cost_statement"], self.rendered)
        header = "C. COSTS TO YOU — %s; %s" % (
            cite("consent.element_costs"), cite("charging.consent_disclosure"))
        self.assertIn(header, self.rendered)

    def test_stopping_treatment_paragraph_5025b4(self):
        self.assertIn("D. STOPPING TREATMENT — %s"
                      % cite("consent.element_stopping"), self.rendered)
        self.assertIn("Stopping is your choice at any time", self.rendered)

    def test_significant_new_findings_paragraph_5025b5(self):
        self.assertIn("E. NEW INFORMATION — %s"
                      % cite("consent.element_new_findings"), self.rendered)
        self.assertIn("significant new findings", self.rendered)

    def test_voluntariness_restated(self):
        self.assertIn("F. YOUR CHOICE, RESTATED — 21 CFR 50.25(a)(8)",
                      self.rendered)
        self.assertIn("Refusing or stopping will not affect the regular "
                      "medical care", self.rendered)

    def test_element_6_rendered_from_injury_compensation_statement(self):
        fields = _sample_fields()
        self.assertIn(fields["consent.injury_compensation_statement"],
                      self.rendered)
        by_span = {p.span: p.citation for p in self.icf.provenance}
        self.assertEqual(by_span["injury_compensation_statement"],
                         cite("consent.element_injury_compensation"))


class ElementSixMissingTests(unittest.TestCase):
    """M3: a(6) absent -> honest MISSING + a ledger question naming the span
    (the app's fix-loop maps that span to the intake field)."""

    def test_missing_marker_and_red_ledger_question(self):
        fields = _sample_fields()
        del fields["consent.injury_compensation_statement"]
        study, documents, _ = _route_docs(fields)
        icf = documents[EA_ICF]
        self.assertIn("[[MISSING: injury_compensation_statement]]",
                      icf.rendered)
        self.assertNotIn("injury_compensation_statement",
                         icf.fields)   # omitted, so the ledger goes red
        result = run_check(study, documents, load_documents(), load_gates())
        item = next(i for i in result.ledger if i.doc_id == EA_ICF)
        self.assertEqual(item.status, "red")
        self.assertTrue(any("injury_compensation_statement" in q
                            for q in item.questions), item.questions)

    def test_sample_case_stays_zero_red_with_the_ea_icf(self):
        study, documents, _ = _route_docs()
        result = run_check(study, documents, load_documents(), load_gates())
        statuses = {i.doc_id: i.status for i in result.ledger}
        self.assertNotIn("red", statuses.values())
        self.assertEqual(statuses[EA_ICF], "amber")   # the human consent gate


class ExculpatoryTripwireTests(unittest.TestCase):
    """m12: tier-A grown from the FDA exculpatory-language guidance examples;
    deterministic tier hard-fails the ENUMERATED constructions only."""

    GUIDANCE_EXAMPLES = {
        "excul-hold-harmless":
            "By agreeing to this use you will hold the hospital and its "
            "agents harmless from any claims.",
        "excul-waive-compensation":
            "I waive any possibility of compensation for injuries that I "
            "may receive as a result of this treatment.",
        "excul-agree-to-pay-injury":
            "By signing this form you agree to pay all costs of treating "
            "any injury resulting from the treatment.",
        "excul-assumes-no-responsibility":
            "The sponsor assumes no responsibility for any injury you may "
            "suffer.",
    }

    def test_each_guidance_example_hard_fails_in_consent_context(self):
        for rule_id, text in self.GUIDANCE_EXAMPLES.items():
            report = lint_text(text, doc_category="consent")
            self.assertFalse(report.passes(), rule_id)
            self.assertIn(rule_id, {f.rule_id for f in report.hard_findings})

    def test_scoped_rules_do_not_gate_outside_consent_context(self):
        # A CTA can legitimately carry hold-harmless terms: out of consent
        # context the scoped hard rules never hard-fail.
        for text in self.GUIDANCE_EXAMPLES.values():
            report = lint_text(text, doc_category="contracts")
            self.assertTrue(report.passes(), text)

    def test_rendered_ea_icf_is_tier_a_clean(self):
        # False-positive floor: the shipped consent draft itself must never
        # trip the grown tier-A list.
        _s, documents, _r = _route_docs()
        report = lint_document(documents[EA_ICF], doc_category="consent")
        self.assertEqual(
            report.hard_findings, [],
            [(f.rule_id, f.match_text) for f in report.hard_findings])

    def test_hc6_note_reworded_in_registry_metadata(self):
        meta = json.loads(BANNED_PATH.read_text(encoding="utf-8"))["_meta"]
        note = meta.get("hc6_note", "")
        self.assertIn("hard-fails the ENUMERATED constructions", note)
        self.assertIn("judgment owns the CLASS", note)
        self.assertIn("amendment path", note)   # Constitution edited only there


class GenericIcfRegressionTests(unittest.TestCase):
    """The generic Part-50 ICF is untouched for non-EA routes."""

    def test_generic_template_carries_no_ea_framing(self):
        template = TEMPLATES[GENERIC_ICF]
        self.assertIn("You are being asked to take part in a research study.",
                      template)
        self.assertNotIn("expanded access", template.lower())
        self.assertNotIn("PENDING-HUMAN-VERIFICATION", template)

    def test_generic_generation_unchanged(self):
        route = routes.route_for_emergency(False)
        study = build_study(_sample_fields(), route)
        doc = generate_document(study, GENERIC_ICF, load_documents())
        self.assertEqual(doc.doc_id, GENERIC_ICF)
        for n in range(1, 9):
            span_text = VERBATIM_SPANS[GENERIC_ICF]["icf-element-%d" % n][0]
            self.assertIn(span_text, doc.rendered)
        self.assertNotIn("EXPANDED-ACCESS DISCLOSURES", doc.rendered)


if __name__ == "__main__":
    unittest.main(verbosity=2)
