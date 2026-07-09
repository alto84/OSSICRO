---
title: "IND Application — Content and Format (21 CFR 312.23)"
section: "03-documents"
status: confirmed
governing_authority:
  - "21 CFR 312.23 (IND content and format)"
  - "21 CFR 312.22 (general principles)"
  - "21 CFR 312.20 (requirement for an IND)"
  - "Form FDA 1571 (IND cover)"
tags: [cfr/312, fda-form/1571, lifecycle/ind, ossicro/engine, status/confirmed]
aliases: ["IND", "IND application", "312.23", "IND content and format"]
updated: 2026-07-09
---

# IND Application — Content and Format (21 CFR 312.23)

> [!authority] Governing authority
> 21 CFR 312.20 (requirement for an IND); 21 CFR 312.22 (general principles); **21 CFR 312.23** (IND content and format); Form FDA 1571 as the transmittal cover. Status: **Confirmed**. Interpretive positions (OSSICRO assembly/validation behavior, ICH M11 structured target, eCTD packaging) are separately flagged.

An Investigational New Drug Application (IND) is the submission by which a sponsor obtains an exemption from the federal prohibition (FDCA §505(a); 21 CFR 312.20) on shipping an unapproved drug in interstate commerce, so that the drug may lawfully be administered to human subjects under an authorized clinical investigation. No clinical investigation of a drug subject to §312.2(a) may begin until an IND is in effect (21 CFR 312.40): the sponsor submits, and dosing may not start until **30 days after FDA receipt** unless FDA notifies earlier that studies may proceed, and provided the IND is not on clinical hold (21 CFR 312.42, [[ind-submission-and-30-day-clock]]).

This page is the master content/format explainer for the IND submission. It enumerates the seven required sections of 21 CFR 312.23(a), the general assembly principles of 312.22, the [[form-fda-1571-ind-cover|Form FDA 1571]] transmittal that binds them, and where OSSICRO's [[generate-check-validate-engine]] drafts, checks completeness, and gates the non-delegable signature. In the [[sponsor-investigator]] model (21 CFR 312.3(b)) the same physician who signs the IND is also the [[investigator]] who signs the [[form-fda-1572-statement-of-investigator|1572]]; this page describes what that physician-sponsor must assemble and hold.

## 1. Regulatory basis and scope

- **21 CFR 312.20** — the sponsor **shall** submit an IND if intending to conduct a clinical investigation with a new drug or biological product otherwise subject to §312.2(a); the sponsor shall not begin until the IND is in effect.
- **21 CFR 312.22** — general principles: FDA's primary objectives in reviewing an IND are, in **all phases**, to assure the **safety and rights of subjects**, and, in **Phase 2 and 3**, to help assure that the quality of the scientific evaluation is adequate to permit an evaluation of effectiveness and safety. The amount of information needed is **graded to phase, scope, and duration** — early-phase INDs may carry less CMC and toxicology detail than later phases, but the safety floor is never waived.
- **21 CFR 312.23(a)(1)–(a)(10)** — the enumerated content requirements, below.

> [!interpretive] OSSICRO position
> OSSICRO assembles the 312.23 package as a **draft submission for qualified human review**: it instantiates each section from structured study data, checks section-level completeness against the essential-records matrix, and validates form-field rules — but it never transmits to FDA and never applies the sponsor signature. Filing is an explicit human-authorized action ([[non-delegable-functions-and-gates]]). See [[compliance-mapping]] for the artifact→authority→gate manifest.

## 2. The seven content requirements of 21 CFR 312.23(a)

The IND is organized as a cover form plus the following, in order:

### (a)(1) Cover sheet — Form FDA 1571
The [[form-fda-1571-ind-cover|Form FDA 1571]] identifies the sponsor, the drug, the phase(s), and each protocol; it carries the sponsor's dated **signature** committing (i) not to begin clinical investigations until 30 days after FDA receipt (or earlier notice), (ii) not to begin or continue if the studies are on clinical hold, and (iii) that an [[irb-iec|IRB]] complying with 21 CFR Part 56 will be responsible for initial and continuing review. It names any person responsible for monitoring and for safety-report review/evaluation.

> [!warning] Non-delegable
> The **1571 signature** is a legal attestation of sponsor responsibility for the entire investigation (21 CFR 312.23(a)(1)). OSSICRO drafts and completeness-checks the 1571; the human sponsor (or [[sponsor-investigator]]) signs. Software is not a permissible signatory and, per 21 CFR 312.52, cannot be the accountable party. See [[form-fda-1571-ind-cover]].

### (a)(2) Table of contents
A complete table of contents for the submission.

### (a)(3) Introductory statement and general investigational plan
- **Introductory statement** — the drug name and all active ingredients, pharmacological class, structural formula, formulation/dosage form, route of administration, and the broad **objectives and planned duration** of the proposed investigation(s). A brief summary of previous human experience, references to other INDs/marketing applications if relevant, and any withdrawal from investigation or marketing in any country for safety/effectiveness reasons.
- **General investigational plan (312.23(a)(3)(iv))** — the rationale for the drug or research study; the indication(s) to be studied; the general approach to be followed; the kinds of clinical trials to be conducted in the **first year following submission**; the estimated number of subjects; and any risks of particular severity or seriousness anticipated on the basis of toxicological or prior human data. This is a **plan, not a commitment**; the level of detail is proportionate to early-phase uncertainty.

### (a)(4) Investigator's brochure
For each drug, a copy of the [[investigators-brochure|Investigator's Brochure (IB)]] containing the information required by 21 CFR 312.23(a)(5): a brief description of the drug substance and formulation; a summary of pharmacological and toxicological effects in animals and, to the extent known, in humans; a summary of pharmacokinetics and biological disposition; a summary of safety and effectiveness information from prior human studies; and a description of possible risks and side effects and of precautions/special monitoring. For a **lawfully marketed** drug being studied for a new use, the approved **package insert** may substitute for the IB (see [[investigators-brochure]]).

### (a)(5) Protocols
A [[clinical-protocol-and-synopsis|protocol]] for each planned study. **Phase 1** protocols may be brief outlines specifying objectives, an estimate of the number of subjects, safety exclusions, and dosing details (duration, dose, method of determining dose). **Phase 2 and 3** protocols must be more detailed: objectives; criteria for subject selection/exclusion and estimated number; description of design including controls and bias-minimization methods; dose and route; observations and measurements to fulfill objectives; and a description of clinical procedures/laboratory tests to monitor drug effects and minimize risk. Each protocol also identifies each investigator, each sub-investigator, each research facility, and each reviewing IRB — content that maps to the [[form-fda-1572-statement-of-investigator|1572]] and the [[investigator]] page. See [[clinical-protocol-and-synopsis]] and, for statistical content, the [[statistical-analysis-plan|SAP]] (ICH E9/E9(R1)).

### (a)(6) Chemistry, manufacturing, and control (CMC) information
A section describing the composition, manufacture, and control of the drug substance and drug product, sufficient to assure **proper identification, quality, purity, and strength**; a description of stability data supporting the study duration; and, where relevant, environmental analysis or claim of categorical exclusion (21 CFR 312.23(a)(7)(iv)(e)). Phase-appropriate: FDA expects CMC detail to increase across phases; early-phase gaps that could affect subject safety are the review focus.

> [!note] Numbering note
> The regulation groups CMC under 312.23(a)(7) in the codified text; the "seven sections" framing here follows the conventional IND assembly order (cover, TOC, introductory/plan, IB, protocols, CMC, pharm/tox, prior human experience, additional, relevant). Cite the specific paragraph — e.g., 21 CFR 312.23(a)(7) for CMC — rather than an ordinal.

### (a)(7) Pharmacology and toxicology information
Adequate information about pharmacological and toxicological studies (in vitro and animal) on the basis of which the sponsor concludes it is **reasonably safe** to conduct the proposed clinical investigations, including the identity and qualifications of individuals who evaluated the animal safety data and a statement of where the studies were conducted and where records are available for inspection. Integrated summaries of toxicological effects, with full data available on request.

### (a)(8) Previous human experience
A summary of previous human experience with the drug, with emphasis on safety and on any prior experience that bears on the safety of the proposed investigation or the drug's potential effectiveness; references to prior INDs/NDAs/BLAs; and any experience that would support the proposed study population and dosing. For drugs marketed outside the US, foreign marketing/withdrawal history for safety/effectiveness.

### (a)(9) and (a)(10) Additional and relevant information
Any additional information the sponsor believes relevant (e.g., special drug-dependence/abuse potential, radioactive drug data, pediatric plans), and any other information FDA requests. Relevant information not otherwise submitted is included as needed.

## 3. General assembly and submission mechanics (312.22, 312.23(d)–(f))

- **Three copies** historically; modern practice is **electronic Common Technical Document (eCTD)** submission where required for commercial INDs; individual-investigator/sponsor-investigator and expanded-access INDs may have different format expectations (verify current FDA electronic-submission requirements and any waiver).
- **Numbered serial submissions.** The original IND and every subsequent amendment, safety report, and correspondence is a numbered serial submission to the same IND number. [[annual-reporting-and-amendments|Protocol amendments (312.30), information amendments (312.31)]], [[ind-safety-report|IND safety reports (312.32)]], and the [[ind-annual-report-dsur|annual report (312.33)]] all file into this IND.
- **English language; environmental claim.** Non-English literature translated; environmental assessment or categorical-exclusion claim per 312.23(a)(7)(iv)(e) and 21 CFR Part 25.
- **Charging/promotion.** Promotion and commercial distribution of an investigational drug are prohibited (21 CFR 312.7); charging for an investigational drug requires prior authorization (312.8).

> [!interpretive] OSSICRO position — ICH M11 structured target
> OSSICRO's priority protocol schema is the **ICH M11 (CeSHarP)** structured, machine-readable clinical-protocol template (FDA-adopted; final template 2025-11-19). Building the (a)(5) protocol to M11 lets the [[generate-check-validate-engine]] populate the IND protocol section and the downstream [[clinical-study-report|CSR]] and [[statistical-analysis-plan|SAP]] from one structured source of truth. This is a forward-standard design choice, flagged interpretive; the black-letter requirement remains 312.23(a)(6)/(a)(5) content, not any particular schema.

## 4. Sponsor-investigator specifics

In a [[sponsor-investigator]] IND (21 CFR 312.3(b)), one physician both initiates and conducts the investigation and therefore assembles and holds the full 312.23 package while **also** discharging every [[investigator]] obligation (21 CFR 312.60–312.69). Practical consequences for the IND content:

- The same individual signs the **1571 (as sponsor)** and holds/references the **1572 (as investigator)**. The 1572 is retained by the sponsor-investigator and referenced in the IND, not filed separately to FDA (see [[form-fda-1572-statement-of-investigator]]).
- The **financial disclosure** (21 CFR Part 54; [[form-fda-3454-3455-financial-disclosure|Forms 3454/3455]]) becomes a **self-disclosure**: the physician cannot certify away their own disclosable interest.
- FDA's **2015 draft guidance** "Investigational New Drug Applications Prepared and Submitted by Sponsor-Investigators" is the single most on-point walk-through of the dual-role IND. **Flag: draft status** — cite as FDA current thinking, not a binding mandate.
- For the single-patient treatment case, the streamlined [[form-fda-3926-expanded-access|Form FDA 3926]] individual-patient expanded-access IND (21 CFR 312.310) substitutes for the full 312.23 assembly; see [[expanded-access-workflow]].

## 5. Completeness and the OSSICRO gate

OSSICRO's [[completeness-ledger]] renders the IND as a per-section open-items contract: **green** where a section is validated against 312.23, **amber** where a human judgment is required (e.g., the sponsor's "reasonably safe" conclusion under (a)(7)), and **red** where required data is missing with the exact resolving question. The [[draft-provenance-model]] carries each drafted span back to its source datum and CFR citation. The submission itself remains a gated, human-authorized act.

> [!warning] Non-delegable
> The conclusion that available pharm/tox data make it **reasonably safe** to proceed (21 CFR 312.23(a)(8)/(a)(7)), the **content sign-off**, and the **decision to submit** are sponsor judgments. OSSICRO checks completeness and timeliness; a qualified human owns the scientific conclusion and the filing.

## Related
- [[form-fda-1571-ind-cover]]
- [[clinical-protocol-and-synopsis]]
- [[investigators-brochure]]
- [[form-fda-1572-statement-of-investigator]]
- [[form-fda-3454-3455-financial-disclosure]]
- [[ind-submission-and-30-day-clock]]
- [[pre-ind-and-ind-preparation]]
- [[sponsor-investigator]]
- [[sponsor]]
- [[ind-annual-report-dsur]]
- [[ind-safety-report]]
- [[annual-reporting-and-amendments]]
- [[expanded-access-workflow]]
- [[form-fda-3926-expanded-access]]
- [[non-delegable-functions-and-gates]]
- [[generate-check-validate-engine]]
- [[completeness-ledger]]

## Sources
- [21 CFR 312.20 — Requirement for an IND](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.20)
- [21 CFR 312.22 — General principles of the IND submission](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.22)
- [21 CFR 312.23 — IND content and format](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23)
- [21 CFR 312.40 — General requirements for use of an investigational new drug in a clinical investigation](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-C/section-312.40)
- [21 CFR 312.42 — Clinical holds and requests for modification](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-C/section-312.42)
- [Form FDA 1571 (IND application)](https://www.fda.gov/media/72335/download)
- [FDA Draft Guidance (2015) — IND Applications Prepared and Submitted by Sponsor-Investigators](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigational-new-drug-applications-prepared-and-submitted-sponsor-investigators)
- [ICH M11 — Clinical electronic Structured Harmonised Protocol (CeSHarP)](https://www.ich.org/page/multidisciplinary-guidelines)
