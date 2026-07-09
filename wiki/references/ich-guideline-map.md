---
title: "ICH Guideline Map"
section: "references"
status: confirmed
governing_authority:
  - "ICH E6(R3), E8(R1), E9/E9(R1), E2A, E2B(R3), E2D, E2F, E3, M11 (as adopted by FDA)"
tags: [status/confirmed, ich/e6r3, ich/e8r1, ich/e9, ich/e2a, ich/e2b, ich/e2d, ich/e2f, ich/e3, ich/m11]
aliases: ["ICH map", "ICH status table"]
updated: 2026-07-09
---

# ICH Guideline Map

> [!authority] Governing authority
> The ICH guidelines enumerated below, in the versions and adoption statuses stated. ICH guidelines are **non-binding**: in the US they state FDA's current thinking only once FDA publishes them as guidance; they never override 21 CFR. Status: **Confirmed** (the status/date facts below are verifiable against the ICH database and the Federal Register; rows carrying residual uncertainty are explicitly flagged).

This page tracks every ICH guideline the OSSICRO wiki and engine rely on: its Step 4 (ICH adoption) date, its FDA adoption status, supersession relationships, and the wiki pages it governs. Two facts about ICH status matter operationally and are commonly gotten wrong: (1) **Step 4 is ICH adoption, not US effect** — a guideline binds nothing in the US until FDA publishes it, and even then it is guidance, not regulation; (2) **adoption dates diverge by region** — E6(R3) was effective in the EU on 2025-07-23 but FDA published it 2025-09-09 with *no US compliance date set*. OSSICRO templates are built to the forward standard (E6(R3), M11) because that is what investigators will be held to, while validation rules cite the binding CFR floor. See [[regulatory-landscape]] for the binding/non-binding architecture and [[regulatory-change-log]] for the change watch.

## Core efficacy guidelines

| Guideline | Title | ICH Step 4 | FDA status | Notes | Link |
|---|---|---|---|---|---|
| **E6(R3)** | Good Clinical Practice (GCP) | 2025-01-06 | FDA final guidance published **2025-09-09** (FR Doc. 2025-17311, docket FDA-2023-D-1955); **no US compliance date set** as of 2026-07-09 | Supersedes E6(R2). Principles-based, risk-proportionate; Annex 1 (interventional trials) finalized with the guideline; **Appendix C** replaces E6(R2) § 8 essential documents (see [[document-catalog]]). EU effective 2025-07-23. **Annex 2** (decentralized/pragmatic elements) reached Step 2 draft Nov 2024 — still draft; do not cite as final. | [ICH PDF](https://database.ich.org/sites/default/files/ICH_E6(R3)_Step4_FinalGuideline_2025_0106.pdf) · [FDA](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp) · Local: `../sources/ich/ICH_E6R3_Step4_FinalGuideline_2025-01-06.pdf` |
| **E6(R2)** | GCP — Integrated Addendum | 2016-11-09 | FDA guidance March 2018; now superseded by E6(R3) as the reference standard | Retained for § 8 essential-documents cross-numbering (many sponsor SOPs and TMF systems still index to E6(R2) § 8.2/8.3/8.4). | [ICH PDF](https://database.ich.org/sites/default/files/E6_R2_Addendum.pdf) · Local: `../sources/ich/ich_e6r2_integrated-addendum_2016.pdf` |
| **E8(R1)** | General Considerations for Clinical Studies | 2021-10-06 | FDA final guidance 2022 | Quality-by-design; critical-to-quality (CtQ) factors that E6(R3) and the [[monitoring-plan]] operationalize. | [ICH PDF](https://database.ich.org/sites/default/files/ICH_E8-R1_Guideline_Step4_2021_1006.pdf) · Local: `../sources/ich/ICH_E8R1_Step4_Guideline_2021-10-06.pdf` |
| **E9** | Statistical Principles for Clinical Trials | 1998-02-05 | FDA guidance September 1998 | Pre-specification, analysis sets, multiplicity; governs the [[statistical-analysis-plan]]. | [ICH PDF](https://database.ich.org/sites/default/files/E9_Guideline.pdf) · Local: `../sources/ich/ICH_E9_Guideline_1998.pdf` |
| **E9(R1)** | Addendum: Estimands and Sensitivity Analysis | 2019-11-20 | FDA final guidance May 2021 | Estimand framework; addendum to (does not replace) E9. Statistical sign-off remains the [[biostatistician]]'s accountable act. | [ICH PDF](https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1203.pdf) · Local: `../sources/ich/ICH_E9R1_Addendum_Step4_Guideline_2019.pdf` |
| **E3** | Structure and Content of Clinical Study Reports | 1995-11-30 | FDA guidance July 1996; E3 Q&A (R1) 2012 | Governs the [[clinical-study-report]]; closes the lifecycle from IND to final report. | [ICH PDF](https://database.ich.org/sites/default/files/E3_Guideline.pdf) · Local: `../sources/fda-guidance/ICH_E3_ClinicalStudyReports_FDA_1996.pdf` |

## Safety / pharmacovigilance guidelines (E2 family)

| Guideline | Title | ICH Step 4 | FDA status | Notes | Link |
|---|---|---|---|---|---|
| **E2A** | Clinical Safety Data Management: Definitions and Standards for Expedited Reporting | 1994-10-27 | FDA guidance March 1995 | Defines AE/ADR/serious/unexpected and the expedited-reporting concepts that 21 CFR 312.32 operationalizes (as amended by the 2010 IND safety-reporting final rule, 75 FR 59935). Governs [[safety-reporting-lifecycle]], [[ind-safety-report]], [[safety-clock-engine]]. | [ICH PDF](https://database.ich.org/sites/default/files/E2A_Guideline.pdf) · Local: `../sources/ich/ICH_E2A_Guideline_1994.pdf` |
| **E2B(R3)** | Electronic Transmission of Individual Case Safety Reports (ICSR) — specification and implementation guide | 2013 (implementation package; subsequent Q&A/IG revisions through 2025) | FDA accepts E2B(R3) ICSRs to FAERS; regional implementation is staged — **verify the current FDA technical-conformance status before building a submission interface** | The structured data-element standard behind [[form-fda-3500a-medwatch]] content and any electronic safety gateway. EMA mandated E2B(R3) from 2022-06-30. | [ICH E2B page](https://www.ich.org/page/e2br3-individual-case-safety-report-icsr-specification-and-related-files) · Local: `../sources/ich/ICH_E2BR3_ImplementationGuide_Step3_2025-07-18.pdf` |
| **E2D** | Post-Approval Safety Data Management | 2003-11-12 | FDA guidance 2005 | Post-marketing analogue of E2A; relevant when an OSSICRO-supported product approaches approval. | [ICH PDF](https://database.ich.org/sites/default/files/E2D_Guideline.pdf) · Local: `../sources/ich/ICH_E2D_Guideline_2003.pdf` |
| **E2D(R1)** | Post-Approval Safety Data: Definitions and Standards for Management and Reporting | Step 4 reached 2025 (training material issued 2025-12-11) | FDA adoption pending — **verify before citing as FDA position** | Revision of E2D; tracked because it will eventually update post-approval reporting language. | [ICH E2D(R1) page](https://www.ich.org/page/efficacy-guidelines) · Local: `../sources/ich/ICH_E2DR1_Step4_FinalGuideline_2025.pdf` |
| **E2F** | Development Safety Update Report (DSUR) | 2010-08-17 | FDA guidance 2011 | The internationally harmonized annual safety report; FDA accepts a DSUR in satisfaction of the 21 CFR 312.33 IND annual report — see [[ind-annual-report-dsur]]. | [ICH PDF](https://database.ich.org/sites/default/files/E2F_Guideline.pdf) · Local: `../sources/ich/ICH_E2F_DSUR_Guideline.pdf` |

## Multidisciplinary

| Guideline | Title | ICH Step 4 | FDA status | Notes | Link |
|---|---|---|---|---|---|
| **M11** | Clinical Electronic Structured Harmonised Protocol (CeSHarP) — template + technical specification | Final template dated **2025-11-19** (technical specification advanced through 2025; FR notice 2025-10359 of 2025-06-06 announced the tech-spec draft) | FDA participating; formal US guidance adoption in progress — **treat the template as the forward target schema, not a US requirement** | The first regulator-endorsed machine-readable structured protocol format; harmonized with CDISC USDM. OSSICRO's priority protocol-generation schema — see [[clinical-protocol-and-synopsis]] and [[generate-check-validate-engine]]. | [ICH final template PDF](https://database.ich.org/sites/default/files/ICH_Step4_M11_Final_Template_2025_1119.pdf) · Local: `../sources/protocol-template/ich-m11-ceSHarP-template-final-2025.pdf` |

## Supplementary guidelines held in the source library

Cited situationally; not part of the core citation spine.

| Guideline | Title / relevance | Status |
|---|---|---|
| **E11 / E11(R1) / E11A** | Clinical investigation of medicinal products in the pediatric population; addendum; pediatric extrapolation (E11A Step 4, 2024) | Relevant whenever a pediatric subject is enrolled (with 21 CFR 50 Subpart D). Local: `../sources/ich/ich_e11a_pediatric_extrapolation_step4_2024.pdf` |
| **E2C(R2)** | Periodic Benefit-Risk Evaluation Report (PBRER) | Post-approval periodic reporting; outside the IND-phase spine. Local: `../sources/ich/ICH_E2CR2_PBRER_Guideline.pdf` |
| **E2E** | Pharmacovigilance Planning | Safety-specification/PV-plan concepts referenced by the [[safety-management-plan]]. Local: `../sources/ich/ICH_E2E_PharmacovigilancePlanning.pdf` |
| **Q9(R1)** | Quality Risk Management | Risk-management vocabulary backing E6(R3)'s risk-proportionate approach. Local: `../sources/ich/ich_q9r1_quality-risk-management.pdf` |

## How the engine consumes this table

> [!interpretive] OSSICRO position
> Each row is encoded as a versioned authority object (guideline, revision, step-4 date, FDA adoption status + date, supersession pointer). Templates declare which authority version they were built to; the validate pass fails a document to a human gate when its declared authority has been superseded or its status has changed since authoring ([[regulatory-change-log]]). E6(R3) and M11 are the build targets; E6(R2) § 8 numbering is retained as a cross-reference index because counterpart sponsors and eTMF systems still use it. This dual-numbering practice is an OSSICRO design decision, not a regulatory requirement.

> [!warning] Non-delegable
> Deciding *which* GCP standard a specific trial will be held to — for example, whether to commit to E6(R3) conduct standards in a protocol before FDA sets a US compliance date, or how to resolve an E6(R2)-contracted sponsor's requirements against E6(R3) practice — is a regulatory-strategy judgment for the sponsor/[[sponsor-investigator]] (with the [[micro-cro-accountable-layer|micro-CRO]] or regulatory counsel where engaged). OSSICRO surfaces the status divergence; it does not resolve it.

## Related
- [[index|References — how to cite in OSSICRO]]
- [[regulatory-landscape]]
- [[cfr-citation-map]]
- [[fda-guidance-map]]
- [[document-catalog]]
- [[clinical-protocol-and-synopsis]]
- [[statistical-analysis-plan]]
- [[clinical-study-report]]
- [[ind-annual-report-dsur]]
- [[safety-reporting-lifecycle]]
- [[regulatory-change-log]]

## Sources
- [ICH Efficacy Guidelines index](https://www.ich.org/page/efficacy-guidelines)
- [ICH Multidisciplinary Guidelines index (M11)](https://www.ich.org/page/multidisciplinary-guidelines)
- [ICH E6(R3) Step 4 final guideline (2025-01-06)](https://database.ich.org/sites/default/files/ICH_E6(R3)_Step4_FinalGuideline_2025_0106.pdf)
- [FDA — E6(R3) Good Clinical Practice guidance page (Sept 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
- [Federal Register 2025-17311 (2025-09-09) — E6(R3) availability](https://www.federalregister.gov/documents/2025/09/09/2025-17311/)
- [ICH M11 final template (2025-11-19)](https://database.ich.org/sites/default/files/ICH_Step4_M11_Final_Template_2025_1119.pdf)
- [ICH E2F DSUR guideline](https://database.ich.org/sites/default/files/E2F_Guideline.pdf)
- Local originals: `../sources/ich/` (74 documents; see `../sources/MANIFEST.md`)
