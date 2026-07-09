"""Register-tripwire tests. Run: `cd engine && python -m unittest tests.test_register_linter -v`.

The tripwire gates ONLY on tier-A hard rules (chat-transcript residue; 21 CFR
50.20 exculpatory-consent in consent context). Tier-B mannerisms are a
non-blocking smoke signal; voice authority is the concept-based reviewer.
"""

import unittest

from ossicro.register_linter import lint_text

CHAT_RESIDUE = (
    "It is important to note that we leverage a seamless, cutting-edge platform "
    "to delve into the complexities of trial paperwork. As an AI, I hope this helps. "
    "This is not just a tool but a game-changer."
)

MANNERISM_ONLY = (
    "We leverage a seamless, cutting-edge platform to delve into the complexities "
    "of clinical trial paperwork and unlock a paradigm shift."
)

CLEAN = (
    "The sponsor shall notify FDA and all participating investigators of any "
    "suspected adverse reaction that is both serious and unexpected no later than "
    "15 calendar days after receiving the information (21 CFR 312.32(c)(1)). A "
    "material change to the protocol requires IRB review and approval under "
    "21 CFR 56.111 before implementation, except to eliminate an apparent "
    "immediate hazard to a subject."
)

EXCULPATORY = (
    "By signing this consent form you waive any legal rights, and the sponsor "
    "will not be liable for any injury resulting from your participation."
)


class TierGatingTests(unittest.TestCase):
    def test_chat_residue_hard_fails(self):
        r = lint_text(CHAT_RESIDUE)
        self.assertFalse(r.passes(), "chat-transcript residue must hard-fail")
        hard_ids = {f.rule_id for f in r.hard_findings}
        self.assertIn("ai-self-reference", hard_ids)
        self.assertIn("i-hope-this", hard_ids)

    def test_mannerism_only_is_nonblocking(self):
        r = lint_text(MANNERISM_ONLY)
        self.assertTrue(r.passes(), "mannerism-only text must PASS (non-blocking smoke signal); "
                        "findings=%r" % [(f.rule_id, f.tier) for f in r.findings])
        self.assertGreater(len(r.example_findings), 0, "mannerisms should still be surfaced")
        self.assertEqual(r.hard_findings, [])

    def test_clean_regulatory_prose_passes(self):
        r = lint_text(CLEAN)
        self.assertTrue(r.passes(), "clean regulatory prose must PASS; findings=%r"
                        % [(f.rule_id, f.tier) for f in r.findings])


class ExculpatoryConsentTests(unittest.TestCase):
    def test_exculpatory_hard_fails_in_consent_context(self):
        r = lint_text(EXCULPATORY, doc_category="consent")
        self.assertFalse(r.passes(), "exculpatory language must hard-fail a consent document (21 CFR 50.20)")
        hard_ids = {f.rule_id for f in r.hard_findings}
        self.assertIn("excul-waive", hard_ids)
        self.assertIn("excul-not-liable", hard_ids)
        for f in r.hard_findings:
            self.assertEqual(f.citation, "21 CFR 50.20")

    def test_exculpatory_is_advisory_out_of_consent_context(self):
        # Same text with unknown category: scoped rules downgrade to advisory,
        # so 'shall not be liable' does not false-fail a contract.
        r = lint_text(EXCULPATORY, doc_category=None)
        self.assertTrue(r.passes(), "scoped hard rules must not gate outside their context")
        self.assertGreater(len(r.example_findings), 0)


class FalsePositiveControlTests(unittest.TestCase):
    def test_regulatory_terms_do_not_trip(self):
        for term in ("material change", "significant risk", "adequate and well-controlled",
                     "serious and unexpected", "an important potential risk"):
            r = lint_text("The submission notes %s per applicable regulation." % term)
            self.assertEqual(r.hard_findings, [], "%r produced a hard finding" % term)
            self.assertTrue(r.passes())

    def test_locations_reported(self):
        r = lint_text("Line one is fine.\nAs an AI, I note the second line.")
        f = next(x for x in r.findings if x.rule_id == "ai-self-reference")
        self.assertEqual(f.line, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
