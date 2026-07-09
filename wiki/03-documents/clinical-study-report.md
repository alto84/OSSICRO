---
title: "Clinical Study Report (CSR)"
section: "03-documents"
status: mixed
governing_authority:
  - "ICH E3 — Structure and Content of Clinical Study Reports (Step 4, November 1995; FDA guidance July 1996)"
  - "ICH E3 Questions & Answers (R1) (June 2012)"
  - "ICH E6(R3) Appendix C (essential record at closeout)"
  - "21 CFR 314.50(d)(5) (clinical data section of a marketing application)"
tags: [ich/e3, ich/e6r3, role/sponsor, role/biostatistician, role/investigator, lifecycle/closeout, ossicro/engine, status/confirmed, status/interpretive]
aliases: ["CSR", "Clinical Study Report", "final study report"]
updated: 2026-07-09
---

# Clinical Study Report (CSR)

> [!authority] Governing authority
> ICH E3 (Step 4, November 1995; issued as FDA guidance July 1996) defines the integrated full report of a clinical study; the ICH E3 Q&A (R1) (June 2012) clarifies that E3 is guidance on content, not a rigid template. The CSR is a confirmed essential record at closeout (ICH E6(R3) Appendix C; ICH E6(R2) §8.4.9), and it is the unit of clinical evidence in a marketing application's clinical data section (21 CFR 314.50(d)(5); eCTD Module 5). 21 CFR Part 312 does not itself use the term "clinical study report" — see the calibration note below. Status: **Mixed**.

The CSR is the single integrated document — clinical and statistical description, analysis, and appended data — that makes a completed trial's conduct and results reconstructable and reviewable. ICH E3's stated design goal is one core report acceptable to all ICH regions, in which the methods actually used, every departure from what was planned, and the results (favorable and unfavorable, on every enrolled subject) are presented without concealment. For OSSICRO's users the CSR is the closeout deliverable that converts a small trial into durable evidence: for FDA (if the data support an application), for the pharma partner under an [[iis-request-workflow|IIS agreement]], for the IRB's final report, and for publication.

## When a CSR is required — calibration

- **Confirmed:** a CSR-format report is required for each clinical study included in the clinical data section of a marketing application (21 CFR 314.50(d)(5); submitted in eCTD Module 5.3.5). The CSR is a confirmed essential record of trial closeout under ICH E6(R3) Appendix C (E6(R2) §8.4.9).
- **Confirmed:** studies begun after December 17, 2016 that are submitted to FDA in NDAs/BLAs (and INDs where applicable) must use the standardized study-data formats in the FDA Data Standards Catalog (CDISC SDTM/ADaM), per FDA's binding electronic-submissions guidance under FD&C Act §745A.
- **Calibration (confirmed absence):** 21 CFR Part 312 does not require a document called a "CSR" for an IND-only study. Study completion is handled through the [[ind-annual-report-dsur|annual report]] cycle (312.33), IND withdrawal (312.38) or inactivation (312.45), and the final IRB report ([[closeout]]). Producing an E3-format (or abbreviated) CSR for a completed sponsor-investigator study is nonetheless standard GCP practice and is what a pharma partner's support agreement will typically require by contract.
- **Distinct obligation:** ClinicalTrials.gov results posting under FDAAA 801 (generally within 12 months of primary completion) is a separate statutory duty and is not discharged by writing a CSR — see [[clinicaltrials-gov-registration]].
- **Abbreviated CSRs** are appropriate for aborted studies and for studies not material to the evaluation of effectiveness (E3 Q&A; regional practice); the synopsis and safety sections still carry full weight.

## Structure per ICH E3

The canonical section skeleton — OSSICRO's completeness checker validates a draft against every numbered heading:

| § | Content |
|---|---|
| 1 | Title page — study identifiers, drug, indication, phase, initiation/completion dates, sponsor, GCP-compliance statement, and the name of the sponsor's responsible medical officer |
| 2 | Synopsis (brief, standalone; numeric results, not just p-values) |
| 3 | Table of contents for the full report |
| 4 | List of abbreviations and definitions |
| 5 | Ethics — IRB/IEC review (§5.1), ethical conduct (§5.2), patient information and consent (§5.3) |
| 6 | Investigators and study administrative structure (incl. [[cro|CROs]] and the [[dsmb-dmc|DSMB]]) |
| 7 | Introduction |
| 8 | Study objectives |
| 9 | Investigational plan — design (§9.1–9.2), population selection (§9.3), treatments (§9.4), variables (§9.5), data quality assurance (§9.6), **planned statistical methods and sample size (§9.7)**, **changes in conduct or planned analyses (§9.8)** |
| 10 | Study patients — disposition (§10.1), **protocol deviations (§10.2)** |
| 11 | Efficacy evaluation — data sets analysed, demographics, compliance, results and individual-data tabulations |
| 12 | Safety evaluation — exposure (§12.1), adverse events (§12.2), **deaths, SAEs, other significant AEs (§12.3)**, laboratory (§12.4), vitals/physical findings (§12.5), safety conclusions (§12.6) |
| 13 | Discussion and overall conclusions |
| 14 | Tables, figures, graphs referred to but not in text |
| 15 | Reference list |
| 16 | Appendices — study information (16.1: protocol §16.1.1, sample CRF §16.1.2, IRB list + consent samples §16.1.3, investigator list/CVs §16.1.4, **signatures §16.1.5**, randomization scheme §16.1.7, audit certificates §16.1.8, statistical-methods documentation §16.1.9); patient data listings (16.2); CRFs for deaths/SAEs/AE-withdrawals (16.3); individual patient data listings (16.4) |

The E3 Q&A (R1) confirms flexibility: the numbering is a guide to content, and sections that do not apply (e.g., efficacy in a pure safety/PK study) are marked not applicable rather than fabricated.

## Authorship, signatures, and the SAP contract

The CSR is owned by the [[sponsor]] (for OSSICRO's core user, the [[sponsor-investigator]], with the [[biostatistician]]). Section 16.1.5 carries the signatures of the principal or coordinating investigator **or** the sponsor's responsible medical officer, per the receiving authority's requirement. The report must honor the [[statistical-analysis-plan]] as a contract: §9.7 reports what was planned, §9.8 discloses every change and when it was made relative to unblinding, and §16.1.9 appends the statistical documentation. A CSR whose analyses silently diverge from the SAP is a data-integrity finding, not a formatting issue.

> [!warning] Non-delegable
> Medical-writing drafting is automatable; ownership is not. The interpretation of results, the benefit-risk discussion and conclusions (§13), the decision how to characterize deaths and SAEs (§12.3, with the [[medical-monitor]]), the biostatistician's sign-off on the analyses, and the §16.1.5 signatures are qualified-human functions. OSSICRO drafts a complete, citation-carrying CSR for these humans to review, correct, own, and sign — it never issues conclusions in their name.

> [!interpretive] OSSICRO position
> OSSICRO assembles the CSR mechanically from artifacts it already holds: protocol and amendments, [[statistical-analysis-plan|SAP]] and TLF outputs, the [[drug-accountability-log]], deviation log, [[ind-safety-report|safety reports]], IRB correspondence, and the TMF ([[closeout-tmf-checklist]]). The check pass validates every E3 heading for presence-or-justified-absence, reconciles §10.1 disposition counts against enrollment logs, §12 safety tables against the safety database, and §9.8 against the SAP version history. Inferred or interpretive text (§7, §13) is routed to the human-judgment lane of the [[single-pass-review-ux]]; every factual span carries provenance per the [[draft-provenance-model]]. Consistency with ClinicalTrials.gov posted results is checked before finalization.

## Related
- [[statistical-analysis-plan]]
- [[closeout]]
- [[closeout-tmf-checklist]]
- [[ind-annual-report-dsur]]
- [[clinicaltrials-gov-registration]]
- [[biostatistician]]
- [[medical-monitor]]
- [[sponsor-investigator]]
- [[iis-request-workflow]]
- [[record-retention-and-archival]]
- [[non-delegable-functions-and-gates]]

## Sources
- [ICH E3 — Structure and Content of Clinical Study Reports (Step 4, Nov 1995)](https://database.ich.org/sites/default/files/E3_Guideline.pdf)
- [ICH E3 Questions & Answers (R1) (June 2012)](https://database.ich.org/sites/default/files/E3_Q%26As_R1_Q%26As.pdf)
- [FDA guidance — E3 Structure and Content of Clinical Study Reports](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e3-structure-and-content-clinical-study-reports)
- [21 CFR 314.50 — Content and format of an NDA (clinical data section, (d)(5))](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314/subpart-B/section-314.50)
- [21 CFR 312.33 — Annual reports](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.33)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025), Appendix C — Essential Records](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA — Study Data Standards Resources (Data Standards Catalog; standardized study data requirements)](https://www.fda.gov/industry/fda-data-standards-advisory-board/study-data-standards-resources)
- [ClinicalTrials.gov — FDAAA 801 and the Final Rule](https://clinicaltrials.gov/policy/fdaaa-801-final-rule)
