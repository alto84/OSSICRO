"""Register-linter tests. Run: `cd engine && python -m unittest tests.test_register_linter -v`."""

import unittest

from ossicro.register_linter import lint_text

SLOP = (
    "It is important to note that we leverage a seamless, cutting-edge platform "
    "to delve into the complexities of trial paperwork. As an AI, I hope this helps. "
    "This is not just a tool but a game-changer."
)

CLEAN = (
    "The sponsor shall notify FDA and all participating investigators of any "
    "suspected adverse reaction that is both serious and unexpected no later than "
    "15 calendar days after receiving the information (21 CFR 312.32(c)(1)). A "
    "material change to the protocol requires IRB review and approval under "
    "21 CFR 56.111 before implementation, except to eliminate an apparent "
    "immediate hazard to a subject."
)


class RegisterLinterTests(unittest.TestCase):
    def test_slop_is_flagged_and_fails(self):
        r = lint_text(SLOP)
        ids = {f.rule_id for f in r.findings}
        for expected in ("hedge-note", "leverage-verb", "seamless", "cutting-edge",
                         "delve", "ai-self-reference", "i-hope-this", "not-just-but",
                         "game-changer"):
            self.assertIn(expected, ids, expected)
        self.assertFalse(r.passes(), "slop text must FAIL")
        self.assertGreater(r.weighted_score, 0)

    def test_clean_regulatory_prose_passes(self):
        r = lint_text(CLEAN)
        self.assertTrue(r.passes(), "clean regulatory prose must PASS; findings=%r"
                        % [(f.rule_id, f.match_text) for f in r.findings])

    def test_false_positive_control_regulatory_terms(self):
        # legitimate regulatory vocabulary must not trip the linter
        for term in ("material change", "significant risk", "adequate and well-controlled",
                     "serious and unexpected", "an important potential risk"):
            r = lint_text("The submission notes %s per applicable regulation." % term)
            highs = [f for f in r.findings if f.severity == "high"]
            self.assertEqual(highs, [], "%r produced a high finding" % term)

    def test_locations_reported(self):
        r = lint_text("Line one is fine.\nIt is important to note the second line.")
        note = next(f for f in r.findings if f.rule_id == "hedge-note")
        self.assertEqual(note.line, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
