---
title: "Regulatory Landscape — Binding Law vs. Guidance"
section: "00-overview"
status: mixed
governing_authority:
  - "21 CFR Parts 11, 50, 54, 56, 312"
  - "45 CFR 46 (Common Rule); 45 CFR Parts 160/164 (HIPAA)"
  - "42 U.S.C. 282(j) / 42 CFR Part 11 (FDAAA 801)"
  - "ICH E6(R3), E8(R1), E9/E9(R1), E2A/E2B(R3)/E2D/E2F, E3, M11 (as FDA-adopted guidance)"
  - "FDA guidance documents (21 CFR 10.115 good guidance practices)"
tags: [cfr/11, cfr/50, cfr/54, cfr/56, cfr/312, ich/e6r3, ich/e8r1, ich/e9, ich/e2a, ich/e3, ich/m11, lifecycle/ind, status/confirmed, status/interpretive]
aliases: [Binding Law vs Guidance, Authority Map]
updated: 2026-07-09
---

# Regulatory Landscape — Binding Law vs. Guidance

> [!authority] Governing authority
> 21 CFR Parts 11, 50, 54, 56, and 312; 45 CFR 46; 45 CFR Parts 160/164 (HIPAA); 42 CFR Part 11 (ClinicalTrials.gov); ICH guidelines as FDA-adopted guidance; FDA guidance documents under 21 CFR 10.115. Status: **Mixed** — the classification of each authority is confirmed; the "build to forward standards" posture is an interpretive OSSICRO position, marked below.

Every artifact OSSICRO generates must trace to a specific, current authority — and the *kind* of authority matters. Regulations carry the force of law and are enforceable by FDA through clinical holds, warning letters, disqualification, and referral; guidance documents state the agency's current thinking and "do not establish legally enforceable responsibilities" (21 CFR 10.115(d)), yet in practice define the standard a submission is reviewed against. This page is the map: which authorities bind, which persuade, which are in active motion, and where the two US human-subjects regimes overlap.

## 1. The hierarchy of authority

1. **Statute** — the Federal Food, Drug, and Cosmetic Act (e.g., 21 U.S.C. 355(i), the IND authority; 21 U.S.C. 360bbb, expanded access) and the Public Health Service Act (42 U.S.C. 282(j), trial registration). Congress binds FDA and regulated parties alike.
2. **Regulation** — the CFR parts promulgated by notice-and-comment rulemaking. Binding on everyone. Violations are enforceable.
3. **Guidance** — FDA guidance documents, including ICH guidelines FDA has adopted as guidance. Non-binding; an alternative approach may be used if it satisfies the underlying statute and regulations (21 CFR 10.115(d)). Draft guidance carries less weight still: it is published for comment and "not for implementation."

The practical rule OSSICRO encodes in [[compliance-mapping]]: **a regulation is a requirement; a final guidance is a strong default; a draft guidance is a flagged forecast.** Every generated document carries its citation and this classification.

## 2. Binding law

| Authority | Governs | OSSICRO touchpoint |
|---|---|---|
| [21 CFR Part 312](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312) — IND | The spine: definitions (§312.3(b), incl. [[sponsor-investigator]]), IND content (§312.23), safety reporting (§312.32), annual reports (§312.33), clinical hold (§312.42), sponsor duties (§§312.50–312.59) incl. CRO transfer (§312.52), investigator duties (§§312.60–312.69), expanded access (Subpart I, §§312.300–312.320) | Everything in [[02-lifecycle|the lifecycle]]; the load-bearing legal argument at [[legal-thesis-3123-vs-31252]] |
| [21 CFR Part 50](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50) — Protection of Human Subjects | Informed consent: general requirements (§50.20), elements (§50.25), documentation (§50.27), exceptions (§§50.23–50.24), children (Subpart D) | [[informed-consent-form]] drafting and element-checking; the consent **event** is gated ([[informed-consent-document-vs-event]]) |
| [21 CFR Part 54](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54) — Financial Disclosure | Certifiable/disclosable investigator financial interests (§54.2); certification or disclosure duty (§54.4) | [[form-fda-3454-3455-financial-disclosure]]; self-disclosure logic in the sponsor-investigator model |
| [21 CFR Part 56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56) — IRBs | IRB functions (§56.108), review (§56.109), expedited review (§56.110), approval criteria (§56.111), records (§56.115) | [[irb-submission-package]] pre-checks against §56.111; enrollment gated on documented approval ([[irb-iec]]) |
| [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) — Electronic Records; Electronic Signatures | Any e-record required by a predicate rule that OSSICRO creates, modifies, maintains, or transmits; audit trails (§11.10(e)); e-signatures (§§11.50–11.300) | The compliance boundary that makes OSSICRO outputs admissible regulatory records: [[part-11-and-ai-credibility]], [[draft-provenance-model]]. Interpretive layer: FDA's 2003 *Part 11 Scope and Application* guidance narrows enforcement discretion |
| [45 CFR 46](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46) — Common Rule (2018 Requirements) | HHS-conducted or -supported research: approval criteria (§46.111), single-IRB mandate for cooperative research (§46.114(b)), consent incl. key information (§46.116), documentation (§46.117), Subparts B/C/D vulnerable populations | Dual-regulation logic (§4 below); [[single-irb-mandate-and-central-irbs]] |
| [45 CFR Parts 160/164](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512) — HIPAA Privacy Rule | PHI use/disclosure for research: authorization (§164.508), waiver (§164.512(i)(1)(i)), preparatory to research (§164.512(i)(1)(ii)), limited data sets (§164.514(e)), de-identification (§164.514(b)) | The privacy fulcrum: matching = preparatory review; enrollment = authorization/waiver ([[hipaa-and-privacy-gating]], [[privacy-state-machine]]) |
| [42 CFR Part 11](https://www.ecfr.gov/current/title-42/chapter-I/subchapter-A/part-11) + 42 U.S.C. 282(j) — FDAAA 801 | ClinicalTrials.gov registration and results submission for applicable clinical trials; Form FDA 3674 certification | [[clinicaltrials-gov-registration]], [[form-fda-3674-clinicaltrialsgov-certification]] |
| 42 U.S.C. 1320a-7b(b) (AKS) · 42 U.S.C. 1320a-7h (Sunshine) | Remuneration constraints on budgets/IIS support; transparency reporting of pharma payments to physicians | [[clinical-trial-agreement-and-budget]], [[iis-request-workflow]] |

> [!warning] Non-delegable
> Binding law fixes several functions on humans or accountable entities no matter what the tooling does: the consent event (21 CFR 50.20), the IRB approval determination (21 CFR 56.111), seriousness/expectedness/causality judgment (21 CFR 312.32), the 1571/1572 attestations (21 CFR 312.23(a)(1), 312.53(c)(1)), and the 312.52 rule that a transferee of sponsor obligations must be a legally accountable entity — software can never be that transferee. Master matrix: [[non-delegable-functions-and-gates]].

## 3. Non-binding guidance

### ICH guidelines as FDA-adopted guidance

| Guideline | Subject | US status |
|---|---|---|
| [ICH E6(R3)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf) | Good Clinical Practice — principles-based, risk-proportionate; essential records at Appendix C | ICH Step 4 2025-01-06; EU effective 2025-07-23; **FDA final guidance 2025-09-09** ([90 FR 2025-17311](https://www.federalregister.gov/documents/2025/09/09/2025-17311/e6r3-good-clinical-practice-international-council-for-harmonisation-guidance-for-industry)); **no US compliance date set** as of this writing |
| ICH E8(R1) | General considerations; quality-by-design; critical-to-quality factors | FDA-adopted (2022) |
| ICH E9 / E9(R1) | Statistical principles; estimands and sensitivity analysis | FDA-adopted (1998 / 2021); see [[statistical-analysis-plan]] |
| ICH E2A / E2B(R3) / E2D / E2F | Expedited-reporting definitions; electronic ICSR format; post-approval safety; DSUR | FDA-adopted; E2A/E2B operationalize 21 CFR 312.32 ([[safety-reporting-workflow]]); E2F DSUR accepted for the 312.33 annual report |
| ICH E3 | Clinical study report structure | FDA-adopted (1996); see [[clinical-study-report]] |
| ICH M11 | Harmonised structured protocol (CeSHarP) | Final template published 2025-11-19; the target schema for [[clinical-protocol-and-synopsis]] |

### FDA guidance documents

| Guidance | Status | Bearing on OSSICRO |
|---|---|---|
| [Conducting Clinical Trials With Decentralized Elements](https://www.fda.gov/media/167696/download) | **Final**, 2024-09-18 | Enabling authority for the distributed model; key principle: requirements are identical for decentralized and traditional trials — decentralization changes logistics, not obligations |
| [Considerations for the Use of AI to Support Regulatory Decision-Making](https://www.federalregister.gov/documents/2025/01/07/2024-31542/considerations-for-the-use-of-artificial-intelligence-to-support-regulatory-decision-making-for-drug) | **Draft**, 2025-01-07; comments closed 2025-04-07 | The 7-step COU/model-risk credibility framework governing OSSICRO's engine; see [[part-11-and-ai-credibility]] |
| [Use of Electronic Informed Consent: Q&A](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers) (with OHRP) | **Final**, Dec 2016 | Conditions eConsent on Part 50 elements + Part 11 e-signature + IRB oversight |
| [INDs Prepared and Submitted by Sponsor-Investigators](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigational-new-drug-applications-prepared-and-submitted-sponsor-investigators) | **Draft**, May 2015 | The single most on-point FDA document for [[sponsor-investigator]]; draft status flagged wherever cited |
| [Investigator Responsibilities](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigator-responsibilities-protecting-rights-safety-and-welfare-study-subjects) | **Final**, 2009 | Supervision and delegation standard behind [[subinvestigator-and-delegation]] |
| Establishment and Operation of Clinical Trial Data Monitoring Committees | **Final** 2006; superseding **draft** [Use of DMCs in Clinical Trials](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-data-monitoring-committees-clinical-trials), Feb 2024 | [[dsmb-dmc]] charters, independence, COI |
| [Oversight of Clinical Investigations — A Risk-Based Approach to Monitoring](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/oversight-clinical-investigations-risk-based-approach-monitoring) (2013) + RBM Q&A (final 2023) | **Final** | [[risk-based-monitoring-e6r3]], [[monitoring-plan]] |
| [Expanded Access to Investigational Drugs for Treatment Use — Q&A](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/expanded-access-investigational-drugs-treatment-use-questions-and-answers) | **Final** (periodically updated) | [[expanded-access-workflow]] |
| Part 11 Scope and Application | **Final**, 2003 | Narrows Part 11 enforcement discretion to FDA-required records; interpretive layer over the binding Part 11 text |

## 4. Dual regulation: FDA rules and the Common Rule

A study that is both FDA-regulated and HHS-supported must satisfy **both** regimes. FDA harmonized much — but not all — of Parts 50/56 with the revised Common Rule in its 2018–2024 alignment rulemakings (e.g., the 2024 final rules on informed-consent key information and cooperative-research/sIRB provisions). Divergences OSSICRO's validators must carry: the Common Rule's single-IRB mandate (§46.114(b)) binds federally funded cooperative research, while FDA regulations permit but do not compel central-IRB reliance; the Common Rule's continuing-review exemptions do not automatically apply to FDA-regulated studies. Vulnerable-population subparts (pregnant women, prisoners, children) attach on the HHS side; FDA has its own children's subpart at 21 CFR 50 Subpart D.

## 5. Authorities in active motion

The frame is not static, and stale citations are a patient-safety hazard. Current motion the [[regulatory-change-log]] watches:

- **ICH E6(R3)** — FDA final guidance published 2025-09-09, **no US compliance date set**; templates and validators are built to R3 with E6(R2) §8 cross-numbering retained.
- **ICH M11** — final protocol template 2025-11-19; structured-protocol tooling tracks the evolving technical specification.
- **FDA AI credibility guidance** — still **draft**; every OSSICRO claim resting on it is flagged draft in-page.
- **DMC guidance** — 2024 **draft** would supersede the 2006 final; both are cited with status until finalization.
- **21 CFR Part 11 modernization** — FDA continues to apply the 2003 scope-and-application enforcement posture; monitor for rulemaking.

> [!interpretive] OSSICRO position
> OSSICRO builds templates and validation rules to the *forward* standards — E6(R3) and M11 — even though FDA has set no E6(R3) compliance date, because these are the standards new trials will in practice be reviewed and inspected against, and building to E6(R2) would bake in imminent obsolescence. Every rule records the authority's adoption date and status, and draft-guidance-derived rules surface a visible draft flag to the reviewing human. This is a design judgment, not a regulatory requirement.

## Related

- [[what-is-ossicro]]
- [[glossary]]
- [[entity-map]]
- [[legal-thesis-3123-vs-31252]]
- [[confirmed-vs-interpretive]]
- [[non-delegable-functions-and-gates]]
- [[compliance-mapping]]
- [[part-11-and-ai-credibility]]
- [[hipaa-and-privacy-gating]]
- [[single-irb-mandate-and-central-irbs]]
- [[cfr-citation-map]]
- [[ich-guideline-map]]
- [[fda-guidance-map]]
- [[regulatory-change-log]]

## Sources

- [eCFR — Title 21, Chapter I (Parts 11, 50, 54, 56, 312)](https://www.ecfr.gov/current/title-21)
- [eCFR — 45 CFR Part 46 (Common Rule)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46)
- [eCFR — 45 CFR 164.512 (HIPAA research uses and disclosures)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512)
- [eCFR — 42 CFR Part 11 (ClinicalTrials.gov registration and results)](https://www.ecfr.gov/current/title-42/chapter-I/subchapter-A/part-11)
- [21 CFR 10.115 — Good guidance practices](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-10/subpart-B/section-10.115)
- [Federal Register — E6(R3) GCP guidance availability (2025-09-09)](https://www.federalregister.gov/documents/2025/09/09/2025-17311/e6r3-good-clinical-practice-international-council-for-harmonisation-guidance-for-industry)
- [FDA — E6(R3) Good Clinical Practice guidance page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp) · [PDF](https://www.fda.gov/media/169090/download)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [Federal Register — Decentralized Elements guidance availability (2024-09-18)](https://www.federalregister.gov/documents/2024/09/18/2024-21078/conducting-clinical-trials-with-decentralized-elements-guidance-for-industry-investigators-and-other) · [FDA PDF](https://www.fda.gov/media/167696/download)
- [Federal Register — FDA AI draft guidance (2025-01-07)](https://www.federalregister.gov/documents/2025/01/07/2024-31542/considerations-for-the-use-of-artificial-intelligence-to-support-regulatory-decision-making-for-drug)
- [FDA — INDs Prepared and Submitted by Sponsor-Investigators (draft, 2015)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigational-new-drug-applications-prepared-and-submitted-sponsor-investigators)
- [FDA/OHRP — Use of Electronic Informed Consent: Q&A (final, 2016)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers)
- [FDA — Use of Data Monitoring Committees in Clinical Trials (draft, 2024)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-data-monitoring-committees-clinical-trials)
- [ICH — Efficacy Guidelines](https://www.ich.org/page/efficacy-guidelines)
