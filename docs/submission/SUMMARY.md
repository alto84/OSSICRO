# Submission — written description (paste into the CV platform)

_~165 words. The event asks for a 100–200-word written description / summary._

---

OSSICRO gives a physician who has the right patient a compliant, low-cost path to run the trial. A neurologist whose patient could benefit from an investigational drug normally faces months and tens of thousands of dollars of CRO work just to become an FDA sponsor-investigator. OSSICRO is open-source software (pure Python) that generates the required regulatory documentation from the patient's intake — FDA Form 3926, single-patient expanded access — checks every document against the exact regulation that governs it, and coordinates each party. Crucially, it refuses, in code, to perform the acts only a human may: obtaining consent, IRB judgment, causality, signing. Its micro-CRO layer even refuses to draft a transfer of informed consent to a CRO, because that obligation is non-delegable under 21 CFR Part 50. Built entirely with Claude Code in one week: a 25-module engine with 593 passing tests, a 131-page cited regulatory wiki authored by multi-agent orchestration, governance enforced as code, and every citation verified against primary FDA sources. It runs with one command.
