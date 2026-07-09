"""Golden zero-false-positive gate.

Run: `cd engine && python -m unittest tests.test_golden -v`.

A small corpus of clean, professional regulatory prose must yield:
- ZERO tier-A (hard-rule) register-tripwire findings, and
- ZERO 'deficient' (hard) concept-stub findings.

This is the false-positive floor. If a future tripwire pattern or stub mapping
starts firing on legitimate regulatory register, this test catches it before it
erodes reviewer trust (docs/VALIDATION-PHILOSOPHY.md §1: over-firing is a decay
mode, not a feature).
"""

import unittest

from ossicro.register_linter import lint_text
from ossicro.review_port import DeterministicStubReviewer, load_writing_principles

# Clean regulatory prose across several document registers. Formal passives,
# "shall", defined-term repetition, and cited requirements are legitimate here
# and must NOT trip a hard rule or a deficient concept finding.
GOLDEN = {
    "ind-safety": (
        "The sponsor shall notify FDA and all participating investigators of any "
        "suspected adverse reaction that is both serious and unexpected no later "
        "than 15 calendar days after the sponsor receives the information "
        "(21 CFR 312.32(c)(1)(i)). For an unexpected fatal or life-threatening "
        "suspected adverse reaction, the sponsor shall notify FDA no later than 7 "
        "calendar days after receiving the information (21 CFR 312.32(c)(2))."
    ),
    "protocol": (
        "This is a single-patient study of XYZ-101 in refractory focal epilepsy. "
        "The primary objective is to characterize safety and tolerability. The "
        "secondary objective is to describe the change in monthly seizure "
        "frequency. Eligible subjects are adults with at least four seizures per "
        "month who have failed at least two antiseizure medications. The protocol "
        "version and date appear on the title page so that amendments remain "
        "traceable under 21 CFR 312.30."
    ),
    "consent": (
        "You are being asked to take part in a research study. Taking part is "
        "voluntary. If you decide not to take part, you will not lose any benefits "
        "to which you are otherwise entitled, and you may stop at any time. "
        "Possible risks include dizziness, drowsiness, and elevated liver enzymes. "
        "Because the study drug is investigational, there may be risks that are not "
        "yet known. If you believe you have been injured as a result of this "
        "research, contact the study physician at the number listed below."
    ),
    "correspondence": (
        "This letter transmits the response to the Agency's information request "
        "dated 1 June 2026. The requested chemistry, manufacturing, and controls "
        "information is provided in Section 3. The protocol has been amended to "
        "add the laboratory reference ranges; the revised protocol is included as "
        "Appendix B. The sponsor requests that the clinical hold be lifted."
    ),
}


class GoldenNoHardTripwire(unittest.TestCase):
    def test_no_tier_a_findings(self):
        for name, text in GOLDEN.items():
            category = name if name == "consent" else None
            report = lint_text(text, doc_category=category)
            self.assertEqual(
                report.hard_findings, [],
                "clean %s prose produced tier-A findings: %r"
                % (name, [(f.rule_id, f.match_text) for f in report.hard_findings]),
            )
            self.assertTrue(report.passes())


class GoldenNoDeficientConcept(unittest.TestCase):
    def test_no_deficient_concept_findings(self):
        reviewer = DeterministicStubReviewer()
        principles = load_writing_principles()
        for name, text in GOLDEN.items():
            report = reviewer.review(text, None, principles)
            self.assertEqual(
                report.hard_findings, [],
                "clean %s prose produced deficient concept findings: %r"
                % (name, [(f.principle_id, f.span) for f in report.hard_findings]),
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
