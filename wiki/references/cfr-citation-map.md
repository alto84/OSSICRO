---
title: "CFR Citation Map"
section: "references"
status: confirmed
governing_authority:
  - "21 CFR Parts 11, 50, 54, 56, 312"
  - "42 CFR Parts 11, 403, 493; 42 CFR 1001.952"
  - "45 CFR Part 46; 45 CFR Part 164"
tags: [status/confirmed, cfr/11, cfr/50, cfr/54, cfr/56, cfr/312]
aliases: ["CFR map", "citation map"]
updated: 2026-07-09
---

# CFR Citation Map

> [!authority] Governing authority
> The Code of Federal Regulations sections enumerated below — 21 CFR Parts 11, 50, 54, 56, and 312; 42 CFR Parts 11, 403 (Subpart I), 493, and § 1001.952; 45 CFR Parts 46 and 164 — plus the underlying U.S. Code sections. All are binding law. Status: **Confirmed**.

This is the master index of every CFR (and U.S. Code) section the OSSICRO wiki relies on, with the official eCFR/LII URL and the principal pages that cite it. It is the human-readable projection of the citation-dependency graph: when a section changes, the "cited by" column identifies the pages, templates, and validation rules that must be re-verified (see [[regulatory-change-log]]). URLs point to the eCFR, the continuously updated official edition; local PDF snapshots of each Part are preserved under `sources/cfr/`. Citation form follows [[index|the OSSICRO citation conventions]].

## 21 CFR Part 11 — Electronic Records; Electronic Signatures

Part URL: [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) · Local: `../sources/cfr/21CFR-Part11-ElectronicRecordsSignatures_2025.pdf`

| Section | Subject | Principal citing pages |
|---|---|---|
| [§ 11.1 / § 11.3](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-A) | Scope; definitions | [[part-11-and-ai-credibility]] |
| [§ 11.10](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10) | Controls for closed systems, incl. § 11.10(e) audit trails | [[part-11-and-ai-credibility]], [[architecture]], [[draft-provenance-model]], [[data-model]] |
| [§ 11.50 / § 11.70](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B) | Signature manifestations; signature/record linking | [[part-11-and-ai-credibility]], [[verifiable-site-qualification-dossier]] |
| [§§ 11.100–11.300](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-C) | Electronic signatures — general, components, controls | [[part-11-and-ai-credibility]], [[informed-consent-form]] (eConsent), [[claude-sdk-ai-in-the-loop]] |

## 21 CFR Part 50 — Protection of Human Subjects (Informed Consent)

Part URL: [21 CFR Part 50](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50) · Local: `../sources/cfr/21CFR-Part50-InformedConsent_2025.pdf`

| Section | Subject | Principal citing pages |
|---|---|---|
| [§ 50.20](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-B/section-50.20) | General requirements for informed consent | [[informed-consent-form]], [[enrollment-and-consent]], [[informed-consent-document-vs-event]], [[patient]] |
| [§§ 50.23–50.24](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-B) | Exceptions (emergency; emergency research) | [[informed-consent-form]], [[expanded-access-workflow]] |
| [§ 50.25](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-B/section-50.25) | Elements of informed consent (basic + additional) | [[informed-consent-form]], [[irb-submission-package]], [[enrollment-and-consent]] |
| [§ 50.27](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-B/section-50.27) | Documentation of informed consent | [[informed-consent-form]], [[informed-consent-document-vs-event]] |
| [§§ 50.50–50.56 (Subpart D)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-D) | Additional safeguards for children | [[informed-consent-form]], [[irb-iec]], [[patient]] |

## 21 CFR Part 54 — Financial Disclosure by Clinical Investigators

Part URL: [21 CFR Part 54](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54) · Local: `../sources/cfr/21CFR-Part54-FinancialDisclosure_2025.pdf`

| Section | Subject | Principal citing pages |
|---|---|---|
| [§ 54.2](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54/section-54.2) | Definitions — disclosable financial arrangements/interests | [[form-fda-3454-3455-financial-disclosure]], [[sponsor-investigator]] |
| [§ 54.4](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54/section-54.4) | Certification and disclosure requirements | [[form-fda-3454-3455-financial-disclosure]], [[site-activation]], [[sponsor]] |

## 21 CFR Part 56 — Institutional Review Boards

Part URL: [21 CFR Part 56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56) · Local: `../sources/cfr/21CFR-Part56-IRBs_2025.pdf`

| Section | Subject | Principal citing pages |
|---|---|---|
| [§ 56.103](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56/subpart-A/section-56.103) | Circumstances requiring IRB review | [[irb-iec]], [[irb-submission-and-approval]] |
| [§§ 56.104–56.105](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56/subpart-A) | Exemptions; waivers (invoked by Form 3926 Fields 10.a/10.b) | [[form-fda-3926-expanded-access]], [[expanded-access-workflow]] |
| [§ 56.107](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56/subpart-B/section-56.107) | IRB membership | [[irb-iec]] |
| [§ 56.108](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56/subpart-C/section-56.108) | IRB functions and operations | [[irb-iec]], [[irb-review-workflow]] |
| [§ 56.109](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56/subpart-C/section-56.109) | IRB review of research | [[irb-review-workflow]], [[irb-submission-and-approval]] |
| [§ 56.110](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56/subpart-C/section-56.110) | Expedited review | [[irb-review-workflow]] |
| [§ 56.111](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56/subpart-C/section-56.111) | Criteria for IRB approval | [[irb-submission-package]], [[irb-submission-and-approval]], [[irb-review-workflow]], [[generate-check-validate-engine]] |
| [§ 56.113](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56/subpart-C/section-56.113) | Suspension/termination of IRB approval | [[irb-review-workflow]] |
| [§ 56.115](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56/subpart-D/section-56.115) | IRB records | [[irb-iec]], [[record-retention-and-archival]] |

## 21 CFR Part 312 — Investigational New Drug Application

Part URL: [21 CFR Part 312](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312) · Local: `../sources/cfr/21CFR-Part312-IND-FullPart_2025.pdf`

### Subpart A — General Provisions

| Section | Subject | Principal citing pages |
|---|---|---|
| [§ 312.2](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A/section-312.2) | Applicability (when an IND is required; exemptions) | [[the-three-pathways-triage]], [[pre-ind-and-ind-preparation]] |
| [§ 312.3(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A/section-312.3) | Definitions — sponsor, investigator, **sponsor-investigator**, CRO, subinvestigator | [[legal-thesis-3123-vs-31252]], [[sponsor-investigator]], [[glossary]], [[cro]], [[what-is-ossicro]] |
| [§ 312.6 / § 312.7](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A) | Labeling of investigational drug; promotion prohibition | [[drug-accountability-log]], [[pharma-partner-sponsor]] |
| [§ 312.10](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A/section-312.10) | Waivers | [[form-fda-3926-expanded-access]] |

### Subpart B — The IND

| Section | Subject | Principal citing pages |
|---|---|---|
| [§ 312.20](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.20) | Requirement for an IND | [[pre-ind-and-ind-preparation]], [[the-three-pathways-triage]] |
| [§ 312.22](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.22) | General principles of the IND submission | [[ind-application-312-23]], [[pre-ind-and-ind-preparation]] |
| [§ 312.23](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23) | IND content and format (incl. § 312.23(a)(1) Form 1571; (a)(5) IB; (a)(6) protocol) | [[ind-application-312-23]], [[form-fda-1571-ind-cover]], [[clinical-protocol-and-synopsis]], [[investigators-brochure]], [[pre-ind-and-ind-preparation]] |
| [§ 312.30](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.30) | Protocol amendments | [[annual-reporting-and-amendments]], [[clinical-protocol-and-synopsis]] |
| [§ 312.31](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.31) | Information amendments | [[annual-reporting-and-amendments]] |
| [§ 312.32](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32) | **IND safety reporting** (7-day/15-day expedited reports) | [[ind-safety-report]], [[safety-reporting-lifecycle]], [[safety-clock-engine]], [[form-fda-3500a-medwatch]], [[medical-monitor]], [[pharmacovigilance-safety]] |
| [§ 312.33](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.33) | Annual reports | [[ind-annual-report-dsur]], [[annual-reporting-and-amendments]] |
| [§ 312.38](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.38) | Withdrawal of an IND | [[closeout]] |

### Subpart C — Administrative Actions

| Section | Subject | Principal citing pages |
|---|---|---|
| [§ 312.40](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-C/section-312.40) | General requirements for use (the 30-day clock) | [[ind-submission-and-30-day-clock]] |
| [§ 312.41](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-C/section-312.41) | Comment and advice on an IND | [[fda-interactions-meetings-holds]] |
| [§ 312.42](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-C/section-312.42) | Clinical holds and requests for modification | [[ind-submission-and-30-day-clock]], [[fda-interactions-meetings-holds]], [[fda-as-counterparty]] |
| [§§ 312.44–312.45](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-C) | Termination; inactive status | [[closeout]] |
| [§ 312.47](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-C/section-312.47) | Meetings (incl. pre-IND) | [[pre-ind-and-ind-preparation]], [[fda-interactions-meetings-holds]] |

### Subpart D — Responsibilities of Sponsors and Investigators

| Section | Subject | Principal citing pages |
|---|---|---|
| [§ 312.50](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.50) | General responsibilities of sponsors | [[sponsor]], [[sponsor-investigator]] |
| [§ 312.52](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52) | **Transfer of obligations to a CRO** — the load-bearing constraint | [[legal-thesis-3123-vs-31252]], [[cro]], [[micro-cro-accountable-layer]], [[transfer-of-regulatory-obligations-toro]], [[sponsor-cro-site-coordination]], [[micro-cro]] |
| [§ 312.53](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53) | Selecting investigators and monitors (1572, CV, financial disclosure) | [[form-fda-1572-statement-of-investigator]], [[site-activation]], [[sponsor]], [[clinical-monitor-cra]] |
| [§ 312.54](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.54) | Emergency-research oversight (§ 50.24 studies) | [[irb-iec]] |
| [§ 312.55](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.55) | Informing investigators (IB; new safety information) | [[investigators-brochure]], [[sponsor]] |
| [§ 312.56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56) | Review of ongoing investigations (monitoring) | [[conduct-and-monitoring]], [[monitoring-plan]], [[risk-based-monitoring-e6r3]], [[sponsor]] |
| [§ 312.57](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.57) | Sponsor recordkeeping and retention | [[record-retention-and-archival]], [[document-catalog]], [[sponsor]] |
| [§ 312.58](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.58) | FDA inspection of sponsor records | [[fda-as-counterparty]] |
| [§ 312.59](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.59) | Disposition of unused drug supply | [[drug-accountability-log]], [[closeout]] |
| [§ 312.60](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.60) | General responsibilities of investigators | [[investigator]], [[sponsor-investigator]], [[hcp-physician]] |
| [§ 312.61](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.61) | Control of the investigational drug | [[drug-accountability-log]], [[investigator]] |
| [§ 312.62](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.62) | Investigator recordkeeping and retention (2-year rule) | [[investigator]], [[record-retention-and-archival]], [[drug-accountability-log]] |
| [§ 312.64](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.64) | Investigator reports (progress; immediate SAE-to-sponsor; final; financial) | [[investigator]], [[safety-reporting-lifecycle]], [[ind-safety-report]] |
| [§ 312.66](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.66) | Assurance of IRB review | [[investigator]], [[irb-submission-and-approval]] |
| [§ 312.68](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.68) | FDA inspection of investigator records (BIMO basis) | [[fda-as-counterparty]], [[investigator]] |
| [§ 312.69](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.69) | Handling of controlled substances | [[investigator]], [[drug-accountability-log]] |
| [§ 312.70](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.70) | Disqualification of a clinical investigator | [[fda-as-counterparty]] |

### Subpart E and Subpart I

| Section | Subject | Principal citing pages |
|---|---|---|
| [§§ 312.80–312.88 (Subpart E)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-E) | Drugs for life-threatening and severely debilitating illnesses | [[regulatory-landscape]] |
| [§ 312.305](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.305) | Expanded access — requirements for all uses | [[expanded-access-workflow]], [[form-fda-3926-expanded-access]], [[the-three-pathways-triage]] |
| [§ 312.310](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.310) | Individual patients, incl. emergency use | [[expanded-access-workflow]], [[form-fda-3926-expanded-access]], [[single-patient-site-enrollment]], [[expanded-access-coordination]] |
| [§ 312.315](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.315) | Intermediate-size patient populations | [[expanded-access-workflow]] |
| [§ 312.320](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.320) | Treatment IND / treatment protocol | [[expanded-access-workflow]] |

## 42 CFR — Public Health

| Section | Subject | URL | Principal citing pages |
|---|---|---|---|
| 42 CFR Part 11 | Clinical Trials Registration and Results Information Submission (FDAAA 801 final rule) | [eCFR](https://www.ecfr.gov/current/title-42/chapter-I/subchapter-A/part-11) · Local: `../sources/cfr/42CFR-Part11-ClinicalTrialsGov_2025.pdf` | [[clinicaltrials-gov-registration]], [[form-fda-3674-clinicaltrialsgov-certification]] |
| 42 CFR §§ 403.900–403.914 (Part 403, Subpart I) | Physician Payments Sunshine Act / Open Payments reporting | [eCFR](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/part-403/subpart-I) | [[iis-request-workflow]], [[clinical-trial-agreement-and-budget]], [[pharma-partner-interface-iis]] |
| 42 CFR Part 493 | CLIA — laboratory requirements (site lab certification) | [eCFR](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-G/part-493) | [[site-activation]], [[startup-tmf-checklist]] |
| 42 CFR § 1001.952(d) | Anti-Kickback Statute personal-services/management-contract safe harbor | [eCFR](https://www.ecfr.gov/current/title-42/chapter-V/subchapter-B/part-1001/subpart-C/section-1001.952) | [[clinical-trial-agreement-and-budget]], [[iis-request-workflow]] |

## 45 CFR — Public Welfare (HHS)

| Section | Subject | URL | Principal citing pages |
|---|---|---|---|
| 45 CFR Part 46, Subpart A (Common Rule, 2018 Requirements) | Protection of human subjects | [eCFR](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46) · Local: `../sources/cfr/45CFR-Part46-CommonRule_2025.pdf` | [[regulatory-landscape]], [[irb-iec]] |
| 45 CFR § 46.109 / § 46.111 | IRB review; criteria for approval | [eCFR](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.111) | [[irb-review-workflow]], [[irb-submission-package]] |
| 45 CFR § 46.114 | Cooperative research — **single-IRB mandate** | [eCFR](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.114) | [[single-irb-mandate-and-central-irbs]] |
| 45 CFR § 46.116 / § 46.117 | Consent (incl. key-information requirement); documentation | [eCFR](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.116) | [[informed-consent-form]], [[informed-consent-document-vs-event]] |
| 45 CFR Part 46, Subparts B/C/D | Pregnant women; prisoners; children | [eCFR](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46) | [[irb-iec]], [[patient]] |
| 45 CFR § 164.508 | HIPAA — authorization for research uses/disclosures | [eCFR](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.508) | [[hipaa-and-privacy-gating]], [[privacy-state-machine]], [[enrollment-and-consent]] |
| 45 CFR § 164.512(i) | Research without authorization — incl. § 164.512(i)(1)(ii) **reviews preparatory to research** and § 164.512(i)(1)(i) IRB/Privacy-Board waiver | [eCFR](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512) | [[hipaa-and-privacy-gating]], [[privacy-state-machine]], [[patient-trial-matching]], [[feasibility-and-patient-matching]], [[smart-on-fhir-integration]] |
| 45 CFR § 164.514(b)/(e) | De-identification; limited data sets | [eCFR](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/section-164.514) | [[hipaa-and-privacy-gating]], [[matching-engine]] |

## U.S. Code (statutory anchors)

| Section | Subject | URL | Principal citing pages |
|---|---|---|---|
| 21 U.S.C. § 355(i) | FDCA § 505(i) — statutory basis for the IND regulations | [LII](https://www.law.cornell.edu/uscode/text/21/355) | [[regulatory-landscape]], [[ind-application-312-23]] |
| 21 U.S.C. § 331(jj) | Prohibited acts — false 3674 certification / ClinicalTrials.gov noncompliance | [LII](https://www.law.cornell.edu/uscode/text/21/331) | [[form-fda-3674-clinicaltrialsgov-certification]] |
| 21 U.S.C. § 360bbb (FDCA § 561) | Expanded access to unapproved therapies | [LII](https://www.law.cornell.edu/uscode/text/21/360bbb) | [[expanded-access-workflow]] |
| 21 U.S.C. § 360bbb-0 (FDCA § 561A) | Manufacturer expanded-access policy (21st Century Cures) | [LII](https://www.law.cornell.edu/uscode/text/21/360bbb-0) | [[expanded-access-workflow]], [[expanded-access-coordination]] |
| 42 U.S.C. § 282(j) (PHS Act § 402(j), FDAAA 801) | ClinicalTrials.gov registration and results data bank | [LII](https://www.law.cornell.edu/uscode/text/42/282) | [[clinicaltrials-gov-registration]], [[form-fda-3674-clinicaltrialsgov-certification]] |
| 42 U.S.C. § 1320a-7b(b) | Anti-Kickback Statute | [LII](https://www.law.cornell.edu/uscode/text/42/1320a-7b) | [[clinical-trial-agreement-and-budget]], [[iis-request-workflow]] |
| 18 U.S.C. § 1001 | False statements (criminal-liability warning on FDA forms) | [LII](https://www.law.cornell.edu/uscode/text/18/1001) | [[form-fda-1571-ind-cover]], [[form-fda-1572-statement-of-investigator]] |

## Maintenance rules

1. **Additions.** A wiki page citing a CFR/U.S.C. section not listed here must add a row in the same edit.
2. **Change watch.** The [[regulatory-change-log]] diffs the eCFR on a cadence; a changed section flags every page in its "cited by" column for human re-verification.
3. **Snapshots.** Local PDF copies under `sources/cfr/` are dated; they are evidence of what the text said when a page was authored, not a substitute for the current eCFR text.

> [!interpretive] OSSICRO position
> The "principal citing pages" columns list load-bearing usage, not every incidental mention — the machine-maintained citation-dependency graph in [[compliance-mapping]] is exhaustive; this page is its curated human-readable view.

## Related
- [[index|References — how to cite in OSSICRO]]
- [[regulatory-landscape]]
- [[regulatory-change-log]]
- [[compliance-mapping]]
- [[ich-guideline-map]]
- [[fda-guidance-map]]
- [[fda-form-index]]
- [[bibliography]]

## Sources
- [eCFR Title 21, Chapter I (FDA)](https://www.ecfr.gov/current/title-21/chapter-I)
- [eCFR Title 42 (Public Health)](https://www.ecfr.gov/current/title-42)
- [eCFR Title 45 (Public Welfare)](https://www.ecfr.gov/current/title-45)
- [Cornell LII — U.S. Code](https://www.law.cornell.edu/uscode/text)
- Local CFR snapshots: `../sources/cfr/` (dated 2025 editions)
