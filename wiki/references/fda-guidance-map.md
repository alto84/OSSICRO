---
title: "FDA Guidance Map"
section: "references"
status: confirmed
governing_authority:
  - "FDA guidance documents (non-binding; 21 CFR 10.115 good guidance practices)"
tags: [status/confirmed, cfr/312, cfr/50, cfr/11, ossicro/ai-credibility, lifecycle/conduct, lifecycle/safety]
aliases: ["FDA guidance status table"]
updated: 2026-07-09
---

# FDA Guidance Map

> [!authority] Governing authority
> FDA guidance documents issued under the good-guidance-practices regulation (21 CFR 10.115). Guidance is **non-binding**: it describes FDA's current thinking and creates no enforceable rights or obligations; an alternative approach may be used if it satisfies the applicable statute and regulations. **Draft** guidance is not even current thinking — it is distributed for comment only. Status: **Confirmed** (statuses stated as of 2026-07-09; rows carrying residual uncertainty are flagged).

This page tracks every FDA guidance the OSSICRO wiki and engine rely on, with final/draft status, issuing date, and the pages each governs. The final/draft distinction is load-bearing: OSSICRO's validate pass treats a claim resting only on draft guidance as an interpretive position requiring an inline flag ([[confirmed-vs-interpretive]]), and the [[regulatory-change-log]] watches every row for status changes. Where a local snapshot exists under `sources/fda-guidance/`, it is linked; the FDA guidance database is the living source.

## Core guidances (the citation spine)

| Guidance | Status | Date | Governs / cited by | Link |
|---|---|---|---|---|
| **Investigator Responsibilities — Protecting the Rights, Safety, and Welfare of Study Subjects** | Final | Oct 2009 | The supervision/delegation standard behind [[investigator]], [[subinvestigator-and-delegation]], [[delegation-of-authority-log]] | [FDA PDF](https://www.fda.gov/media/77765/download) · Local: `../sources/fda-guidance/FDA_Investigator-Responsibilities_2009.pdf` |
| **Investigational New Drug Applications Prepared and Submitted by Sponsor-Investigators** | **Draft** — never finalized; cite with draft flag | May 2015 (FDA-2015-D-1484) | The single most on-point FDA document for OSSICRO's core user; anchors [[sponsor-investigator]], [[pre-ind-and-ind-preparation]], [[ind-application-312-23]] | [FDA PDF](https://www.fda.gov/files/drugs/published/Investigational-New-Drug-Applications-Prepared-and-Submitted-by-Sponsor-Investigators.pdf) · Local: `../sources/fda-guidance/FDA_IND_Applications_Sponsor-Investigators.pdf` |
| **Frequently Asked Questions — Statement of Investigator (Form FDA 1572)** (information sheet) | Final | 2010 | Field-by-field 1572 interpretation; [[form-fda-1572-statement-of-investigator]], [[site-activation]] | [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/frequently-asked-questions-statement-investigator-form-fda-1572) |
| **Financial Disclosure by Clinical Investigators** | Final | Feb 2013 | Part 54 interpretation, 3454-vs-3455 selection; [[form-fda-3454-3455-financial-disclosure]] | [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/financial-disclosure-clinical-investigators) |
| **Establishment and Operation of Clinical Trial Data Monitoring Committees** | Final | 2006 | DMC/DSMB structure and independence; [[dsmb-dmc]], [[dsmb-charter]], [[dsmb-workflow]] | [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/establishment-and-operation-clinical-trial-data-monitoring-committees) · Local: `../sources/fda-guidance/FDA_DMC_EstablishmentOperation_Guidance.pdf` |
| **Use of Data Monitoring Committees in Clinical Trials** | **Draft** (intended to supersede the 2006 final when finalized) | 2024 | Tracked for the risk-tiered DMC model; [[dsmb-dmc]], [[dsmb-charter]] | [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-data-monitoring-committees-clinical-trials) · Local: `../sources/fda-guidance/FDA_DMC-Use_Draft_2024.pdf` |
| **Oversight of Clinical Investigations — A Risk-Based Approach to Monitoring** | Final | Aug 2013 | The RBM foundation; [[monitoring-plan]], [[risk-based-monitoring-e6r3]], [[conduct-and-monitoring]], [[clinical-monitor-cra]] | [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/oversight-clinical-investigations-risk-based-approach-monitoring) · Local: `../sources/fda-guidance/FDA_Risk-Based-Monitoring_2013.pdf` |
| **A Risk-Based Approach to Monitoring of Clinical Investigations: Questions and Answers** | Final | Apr 2023 | Companion Q&A to the 2013 RBM guidance; [[risk-based-monitoring-e6r3]], [[monitoring-plan]] | [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/risk-based-approach-monitoring-clinical-investigations-questions-and-answers) · Local: `../sources/fda-guidance/FDA_Risk-Based-Monitoring_QA_2023.pdf` |
| **Use of Electronic Informed Consent: Questions and Answers** (joint FDA/OHRP) | Final | Dec 2016 | eConsent mechanics under Part 50 + Part 11; [[informed-consent-form]], [[informed-consent-document-vs-event]], [[part-11-and-ai-credibility]] | [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers) · Local: `../sources/fda-guidance/FDA_eConsent_QA_2016.pdf` |
| **Conducting Clinical Trials With Decentralized Elements** | Final | Sept 2024 (FR Doc. 2024-21078, 2024-09-18; finalizes May 2023 draft; FDORA § 3606 mandate) | The enabling authority for distributed/physician-operable trial logistics; key principle: decentralization changes logistics, **not** obligations. [[regulatory-landscape]], [[form-fda-1572-statement-of-investigator]] (local-HCP note), [[single-patient-site-enrollment]], [[hcp-physician]] | [FDA PDF](https://www.fda.gov/media/167696/download) · Local: `../sources/fda-guidance/FDA_Decentralized-Clinical-Trials_Final_2024.pdf` |
| **Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making for Drug and Biological Products** | **Draft** — comments closed 2025-04-07; still draft as of 2026-07-09 | Jan 2025 (FR Doc. 2024-31542, 2025-01-07; docket FDA-2024-D-4689) | The 7-step context-of-use / model-risk credibility framework; [[part-11-and-ai-credibility]], [[claude-sdk-ai-in-the-loop]], [[matching-eligibility-adjudication]], [[risks-and-limitations]] | [Federal Register](https://www.federalregister.gov/documents/2025/01/07/2024-31542/) · Local: `../sources/fda-guidance/FDA_AI-in-Drug-Development_Draft_2025.pdf` |
| **Expanded Access to Investigational Drugs for Treatment Use — Questions and Answers** | Final (periodically updated) | most recent update per FDA guidance database | Subpart I interpretation; [[expanded-access-workflow]], [[expanded-access-coordination]], [[the-three-pathways-triage]] | [FDA PDF](https://www.fda.gov/media/162793/download) |
| **Individual Patient Expanded Access Applications: Form FDA 3926** | Final | June 2016, updated Oct 2017 | Streamlined single-patient IND submissions; [[form-fda-3926-expanded-access]], [[single-patient-site-enrollment]] | [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/individual-patient-expanded-access-applications-form-fda-3926) · Local: `../sources/fda-guidance/FDA_Expanded-Access-Form-3926-Instructions.pdf` |
| **E6(R3) Good Clinical Practice** (ICH adoption) | Final guidance | Sept 2025 (FR Doc. 2025-17311; **no US compliance date set**) | See the full status entry in the [[ich-guideline-map]] | [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp) · Local: `../sources/ich/FDA_ICH_E6R3_GCP_Guidance.pdf` |
| **Part 11, Electronic Records; Electronic Signatures — Scope and Application** | Final | Aug 2003 | The enforcement-discretion interpretation that narrows Part 11 to FDA-required records; [[part-11-and-ai-credibility]] | [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application) |
| **Safety Reporting Requirements for INDs and BA/BE Studies** | Final | Dec 2012 (implements the 2010 final rule, 75 FR 59935) | Operational 312.32 interpretation — aggregate analyses, unexpectedness, reporting thresholds; [[ind-safety-report]], [[safety-reporting-lifecycle]], [[safety-clock-engine]], [[form-fda-3500a-medwatch]] | [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-reporting-requirements-inds-investigational-new-drug-applications-and-babe) · Local: `../sources/fda-guidance/FDA_SmallEntityComplianceGuide_IND_SafetyReporting.pdf` |

## Supporting guidances and reference documents

| Document | Status | Notes | Link / local |
|---|---|---|---|
| **Overview of Sponsor-Investigator Roles and Responsibilities** | FDA reference document | Named-role summary used by [[sponsor-investigator]] | [FDA PDF](https://www.fda.gov/media/174660/download) |
| **IND Application Procedures: Investigator's Responsibilities** | FDA program page | Confirms the dual-obligation inheritance of the sponsor-investigator | [FDA page](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-application-procedures-investigators-responsibilities) |
| **Instructions for Filling Out Form FDA 1572** | FDA instructions | The official field-by-field completion reference the [[generate-check-validate-engine]] validates against | [FDA PDF](https://www.fda.gov/media/79326/download) |
| **Investigator Responsibilities — Safety Reporting for Investigational Drugs and Devices** | **Draft**, 2021 | Investigator-side safety-reporting expectations; pairs with the 2012 final; [[ind-safety-report]] | Local: `../sources/fda-guidance/FDA_Investigator-Safety-Reporting_2021.pdf` |
| **Sponsor Responsibilities — Safety Reporting Requirements and Safety Assessment for IND and BA/BE Studies** | 2025 edition in local library — **verify final/draft status against the FDA guidance database before citing** | Successor treatment of sponsor-side 312.32 duties | Local: `../sources/fda-guidance/FDA_2025_SponsorResponsibilities_SafetyReporting_IND_BABE.pdf` |
| **Protocol deviations** (draft guidance) | **Draft** — verify current title/date before citing | Deviation-classification vocabulary for [[conduct-and-monitoring]] | Local: `../sources/fda-guidance/FDA_Protocol-Deviations_Draft.pdf` |
| **IND annual report / DSUR substitution** | Guidance on using the ICH E2F DSUR to satisfy 21 CFR 312.33 — verify current title/date | [[ind-annual-report-dsur]] | Local: `../sources/fda-guidance/FDA_IND_AnnualReporting_DSUR_Substitution.pdf` |
| **E2F Development Safety Update Report** (ICH adoption) | Final, 2011 | US adoption of the DSUR format | Local: `../sources/fda-guidance/FDA_E2F_DSUR_Guidance_2011.pdf` |
| **Determining Whether Human Research Studies Can Be Conducted Without an IND** | Final, 2013 | The IND-requirement screen used by [[the-three-pathways-triage]] | Local: `../sources/fda-guidance/FDA_IND-Determination-Without-IND.pdf` |
| **Certifications To Accompany Drug, Biological Product, and Device Applications/Submissions (Form FDA 3674)** | Final (rev. June 2017) | [[form-fda-3674-clinicaltrialsgov-certification]] | [FDA page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/certifications-accompany-drug-biological-product-and-device-applicationssubmissions-compliance) |
| **Information Sheet Guidance for Sponsors, Clinical Investigators, and IRBs** | Final information sheets | FAQ layer across Parts 50/56/312; [[irb-iec]], [[investigator]] | Local: `../sources/fda-guidance/FDA_InformationSheet_Sponsors_Investigators_IRBs.pdf` |

## Reading rules

1. **A draft guidance is a signpost, not a floor.** Pages resting on draft guidance (Sponsor-Investigator IND 2015; AI-credibility 2025; DMC 2024) say so inline, every time. When FDA finalizes one, the [[regulatory-change-log]] flags every citing page.
2. **Guidance never substitutes for the CFR.** Where guidance and regulation are both cited, the regulation carries the requirement and the guidance carries the interpretation — the [[cfr-citation-map]] row is the requirement's home.
3. **"Verify" rows are deliberate.** Two rows above carry explicit verify flags because the local library holds an edition whose docket status has not been re-confirmed against the FDA guidance database. Honest uncertainty in a reference table is cheaper than a confident error propagated into a validation rule.

> [!interpretive] OSSICRO position
> OSSICRO's AI-credibility argument rests on the January 2025 **draft** guidance: document drafting for qualified human review is a low-model-influence, low-decision-consequence context of use, while patient-trial matching that could gate access is a higher-influence COU designed and evaluated accordingly ([[matching-evaluation-and-benchmarks]]). Because the anchor guidance is draft, the entire argument is interpretive and is re-evaluated on finalization. That re-evaluation is a standing entry in the [[regulatory-change-log]].

> [!warning] Non-delegable
> Choosing to depart from a final guidance (permissible, since guidance is non-binding, but a justification FDA may probe at inspection or review) is a regulatory-strategy judgment reserved to the sponsor/[[sponsor-investigator]] with qualified regulatory support ([[micro-cro-accountable-layer]]). OSSICRO's engine flags any generated artifact that deviates from guidance-recommended practice; it never silently adopts the deviation.

## Related
- [[index|References — how to cite in OSSICRO]]
- [[regulatory-landscape]]
- [[confirmed-vs-interpretive]]
- [[cfr-citation-map]]
- [[ich-guideline-map]]
- [[part-11-and-ai-credibility]]
- [[risk-based-monitoring-e6r3]]
- [[dsmb-dmc]]
- [[expanded-access-workflow]]
- [[regulatory-change-log]]

## Sources
- [FDA Search for Guidance Documents (the authoritative status database)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents)
- [21 CFR 10.115 — Good guidance practices](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-10/subpart-B/section-10.115)
- [Federal Register 2024-21078 — DCT final guidance availability](https://www.federalregister.gov/documents/2024/09/18/2024-21078/)
- [Federal Register 2024-31542 — AI draft guidance availability](https://www.federalregister.gov/documents/2025/01/07/2024-31542/)
- [Federal Register 2025-17311 — E6(R3) availability](https://www.federalregister.gov/documents/2025/09/09/2025-17311/)
- [75 FR 59935 (2010-09-29) — IND Safety Reporting Requirements final rule](https://www.govinfo.gov/content/pkg/FR-2010-09-29/html/2010-24296.htm)
- Local originals: `../sources/fda-guidance/` (151 documents; see `../sources/MANIFEST.md`)
