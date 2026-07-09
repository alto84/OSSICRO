---
title: "Pre-IND & IND Preparation"
section: "02-lifecycle"
status: confirmed
governing_authority:
  - "21 CFR 312.20–312.23 (requirement for an IND; content and format)"
  - "21 CFR 312.47 (meetings with FDA, incl. pre-IND)"
  - "ICH M11 (structured protocol); ICH E6(R3)"
tags: [lifecycle/ind, cfr/312, fda-form/1571, ich/m11, gcp/e6r3, role/sponsor-investigator, status/confirmed]
aliases: ["Pre-IND", "IND Preparation", "312.23 Package"]
updated: 2026-07-09
---

# Pre-IND & IND Preparation

> [!authority] Governing authority
> [21 CFR 312.20](https://www.ecfr.gov/current/title-21/section-312.20)–[312.23](https://www.ecfr.gov/current/title-21/section-312.23) (requirement for, and content and format of, an IND); [21 CFR 312.22](https://www.ecfr.gov/current/title-21/section-312.22) (general principles); [21 CFR 312.47](https://www.ecfr.gov/current/title-21/section-312.47) (meetings, including the pre-IND meeting); FDA "Formal Meetings Between the FDA and Sponsors or Applicants of PDUFA Products" guidance; ICH M11 (structured protocol) and ICH E6(R3). Status: **Confirmed**.

Before a single human is dosed under an investigational new drug, the sponsor — in the OSSICRO core case, the **sponsor-investigator** ([[sponsor-investigator]], [21 CFR 312.3(b)](https://www.ecfr.gov/current/title-21/section-312.3)) — must assemble and submit an IND that meets the content-and-format requirements of [21 CFR 312.23](https://www.ecfr.gov/current/title-21/section-312.23). This is the single largest document-assembly task in the lifecycle and the one that most reliably defeats a solo clinician without a research office. It is precisely the coordination-and-paperwork burden OSSICRO exists to absorb — assembling, cross-checking, and version-controlling every section into a submission-ready draft, while the legal attestation on the cover form stays with the human. A well-run **pre-IND meeting** ([21 CFR 312.47](https://www.ecfr.gov/current/title-21/section-312.47)) de-risks the entire submission by surfacing FDA's expectations on CMC, nonclinical package adequacy, and clinical-protocol design *before* the 30-day clock starts.

## The pre-IND meeting (312.47)

A pre-IND meeting is a **Type B** formal meeting with the review division (CDER or CBER) that lets a prospective sponsor confirm, before filing, that the nonclinical package supports first-in-human dosing, that the CMC information is adequate for the proposed clinical supply, and that the initial protocol's design and safety monitoring are acceptable. It is not mandatory, but for a sponsor-investigator it is high-leverage: it converts a clinical-hold risk into a documented FDA-alignment record.

Mechanics:

- **Meeting request** with a proposed agenda, a list of specific questions, and the identity of attendees, submitted to the review division; FDA schedules Type B meetings within a target window per the PDUFA formal-meetings guidance.
- **Pre-IND meeting package (briefing document)** sent in advance: product description, development rationale, summary of nonclinical pharmacology/toxicology, CMC summary, the proposed clinical protocol synopsis, and the specific questions on which FDA feedback is sought.
- **FDA responses / meeting minutes** become part of the development record and inform the IND. Preliminary written responses may, in some cases, substitute for a live meeting.

> [!interpretive] OSSICRO position
> OSSICRO drafts the pre-IND meeting **request and briefing package** and assembles the **question list** from gaps its [[generate-check-validate-engine|check pass]] detects in the nascent IND (e.g., a nonclinical section that does not yet support the proposed starting dose). This is a draft for the sponsor-investigator's review and sign-off; OSSICRO does not communicate with FDA. Marked interpretive because the value of a pre-IND meeting and the framing of questions is a scientific-strategic judgment, not a regulatory requirement.

## The IND: when it is required (312.20)

[21 CFR 312.20](https://www.ecfr.gov/current/title-21/section-312.20) requires an IND for any clinical investigation of a drug not the subject of an approved marketing application, unless the investigation is **exempt** under [21 CFR 312.2(b)](https://www.ecfr.gov/current/title-21/section-312.2) (certain studies of lawfully-marketed drugs that do not, among other conditions, significantly increase risk or support a new indication or a labeling/advertising change). The IND-exemption determination is a threshold legal analysis and is treated as a gate.

> [!warning] Non-delegable
> Whether a proposed investigation qualifies for the [312.2(b)](https://www.ecfr.gov/current/title-21/section-312.2) IND exemption — and, more consequentially, whether it does **not** and therefore requires an IND — is a regulatory determination with direct patient-safety and enforcement consequences. OSSICRO can structure the 312.2(b) criteria and surface the analysis; a qualified human (sponsor-investigator, and ordinarily regulatory counsel) owns the determination. Getting this wrong — dosing a human without a required IND — is a serious violation.

## The 312.23 content-and-format package (confirmed)

[21 CFR 312.23(a)](https://www.ecfr.gov/current/title-21/section-312.23) enumerates the required IND contents in numbered order. The full package:

| 312.23(a) item | Content | OSSICRO handling | Cross-ref |
|---|---|---|---|
| (a)(1) **Cover sheet — Form FDA 1571** | Sponsor identity, drug, phase, commitments (IRB compliance, not to begin until 30 days elapse or FDA notifies, etc.); the sponsor's signature | Auto-populate from study data; **signature is a human gate** | [[form-fda-1571-ind-cover]] |
| (a)(2) **Table of contents** | Navigable index of the submission | Auto-generated from the assembled package | [[ind-application-312-23]] |
| (a)(3) **Introductory statement & general investigational plan** | Drug/name/structure, pharmacologic class, broad development plan for the coming year | Draft from structured inputs | [[ind-application-312-23]] |
| (a)(4) **Investigator's brochure** | Compiled clinical + nonclinical data; safety reference for expectedness | Assemble/format; for a marketed drug, package insert may substitute ([312.55](https://www.ecfr.gov/current/title-21/section-312.55)) | [[investigators-brochure]] |
| (a)(5) **Clinical protocol(s)** | Objectives, design, eligibility, dosing, safety monitoring, statistics | Draft to **ICH M11** structured schema; synopsis convention | [[clinical-protocol-and-synopsis]] |
| (a)(6) **Chemistry, manufacturing, and control (CMC)** | Composition, manufacture, stability, controls sufficient to assure identity/quality/purity/strength | Assemble from sponsor/manufacturer inputs | [[ind-application-312-23]] |
| (a)(7) **Pharmacology & toxicology** | Nonclinical studies supporting the safety of proposed human use; GLP statement | Assemble; **check** adequacy vs. proposed starting dose | [[ind-application-312-23]] |
| (a)(8) **Previous human experience** | Prior human use, if any (published or foreign) | Assemble from literature ([[data-integrations-ctgov-pubmed]]) | [[ind-application-312-23]] |
| (a)(9) **Additional information** | Special topics (dependence/abuse potential, radioactive drugs, pediatric plans, etc.) as applicable | Conditional, risk-proportionate | [[ind-application-312-23]] |

General principles under [312.22](https://www.ecfr.gov/current/title-21/section-312.22): FDA's primary IND objectives are to assure **subject safety** and, in later phases, to help assure that the investigation will produce data of adequate scientific quality. The **amount of information** needed scales with the phase, the novelty of the drug, and the extent of prior human experience — a Phase 1 first-in-human IND and a Phase 2 IND for a well-characterized agent differ materially in the depth of each section.

## Accompanying forms and registrations

- **Form FDA 3674** — certification of compliance with ClinicalTrials.gov registration requirements ([FDAAA 801](https://www.ecfr.gov/current/title-42/part-11)), submitted with the IND where applicable. See [[form-fda-3674-clinicaltrialsgov-certification]].
- **Financial disclosure** — the sponsor-investigator's own financial information is handled under Part 54; certification/disclosure (Forms 3454/3455) is compiled at [[site-activation]] and reconciled at closeout. See [[form-fda-3454-3455-financial-disclosure]].

## The IND number and submission mechanics

INDs are submitted to the appropriate center (CDER or CBER). Commercial INDs are submitted electronically in **eCTD** format via the ESG; sponsor-investigator INDs may, in defined circumstances, be submitted in paper or via alternative FDA-accepted means per current FDA policy. FDA assigns an **IND number** on receipt. Submission itself, and the running of the 30-day clock, are covered in [[ind-submission-and-30-day-clock]].

> [!warning] Non-delegable
> The act of **submitting the IND to FDA** is an explicit human-authorized action, and the **Form FDA 1571 signature** is the sponsor-investigator's binding legal commitment (including the commitment not to begin clinical investigations until 30 days after FDA receipt of the IND, and to conduct the investigation in accordance with all applicable regulations). OSSICRO assembles a submission-ready package and tracks the clock; a qualified human signs and submits. See [[non-delegable-functions-and-gates]].

## OSSICRO output at this phase

A submission-ready **IND dossier draft** with: a populated Form FDA 1571 (unsigned), a generated table of contents, all 312.23(a) sections assembled and cross-checked for internal consistency (drug name, protocol version, IND-holder identity, and dates identical across the cover, protocol, and IB — the adversarial cross-document consistency check per [[generate-check-validate-engine]]), a [[completeness-ledger]] (green/amber/red) naming every missing datum and the exact resolving question, and the pre-IND meeting package if elected. Every section carries a citation to its 312.23 subsection.

## Related
- [[index]]
- [[phase-model-overview]]
- [[ind-submission-and-30-day-clock]]
- [[ind-application-312-23]]
- [[form-fda-1571-ind-cover]]
- [[clinical-protocol-and-synopsis]]
- [[investigators-brochure]]
- [[sponsor-investigator]]
- [[fda-interactions-meetings-holds]]
- [[completeness-ledger]]

## Sources
- [21 CFR 312.23 — IND content and format (eCFR)](https://www.ecfr.gov/current/title-21/section-312.23)
- [21 CFR 312.20 — Requirement for an IND (eCFR)](https://www.ecfr.gov/current/title-21/section-312.20)
- [21 CFR 312.22 — General principles of the IND submission (eCFR)](https://www.ecfr.gov/current/title-21/section-312.22)
- [21 CFR 312.47 — Meetings (eCFR)](https://www.ecfr.gov/current/title-21/section-312.47)
- [21 CFR 312.2 — Applicability and exemptions (eCFR)](https://www.ecfr.gov/current/title-21/section-312.2)
- [FDA Guidance — Formal Meetings Between the FDA and Sponsors or Applicants of PDUFA Products](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/formal-meetings-between-fda-and-sponsors-or-applicants-pdufa-products)
- [FDA Draft Guidance (2015) — INDs Prepared and Submitted by Sponsor-Investigators](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigational-new-drug-applications-prepared-and-submitted-sponsor-investigators)
- [ICH M11 — Clinical electronic Structured Harmonised Protocol (CeSHarP)](https://www.ich.org/page/multidisciplinary-guidelines)
