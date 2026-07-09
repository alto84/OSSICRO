---
title: "Statistical Analysis Plan (SAP)"
section: "03-documents"
status: mixed
governing_authority:
  - "ICH E9 — Statistical Principles for Clinical Trials (FDA guidance, September 1998)"
  - "ICH E9(R1) — Addendum: Estimands and Sensitivity Analysis in Clinical Trials (FDA guidance, May 2021)"
  - "ICH E6(R3) Appendix C (essential records); ICH E3 §§9.7–9.8, 16.1.9 (reporting of planned and changed analyses)"
tags: [ich/e9, ich/e3, ich/e6r3, role/biostatistician, role/dsmb, lifecycle/conduct, lifecycle/closeout, ossicro/engine, status/confirmed, status/interpretive]
aliases: ["SAP", "Statistical Analysis Plan"]
updated: 2026-07-09
---

# Statistical Analysis Plan (SAP)

> [!authority] Governing authority
> ICH E9 §5.1 (the principal features of the planned analysis belong in the protocol's statistical section; a SAP written as a separate document may elaborate them technically and must be finalized before the blind is broken); ICH E9(R1) (estimand framework and sensitivity analysis — FDA-adopted guidance, May 2021); ICH E6(R3) Appendix C (the SAP and randomization documentation are essential records); ICH E3 §§9.7–9.8 and §16.1.9 (the CSR reports the planned methods, every change to them, and appends the statistical documentation). Status: **Mixed** — the E9/E9(R1) requirements are confirmed adopted guidance; the OSSICRO drafting/validation workflow is interpretive.

The SAP is the prospective, technical specification of how a trial's data will be analyzed: estimands, analysis sets, statistical methods, missing-data handling, multiplicity control, and interim-analysis rules — written before the data can influence the choices. Its regulatory force comes from the pre-specification principle of ICH E9: an analysis chosen after seeing unblinded data cannot support confirmatory conclusions, and FDA reviewers and BIMO inspectors read the SAP's version history against the database-lock and unblinding dates. For the [[sponsor-investigator]] running an early-phase study, the SAP is also the discipline instrument that keeps a small trial's results interpretable and publishable.

## Relationship to the protocol, and timing

ICH E9 §5.1 places the *principal features* of the analysis in the [[clinical-protocol-and-synopsis|protocol]] itself (21 CFR 312.23(a)(6) requires the protocol's statistical outline for Phase 2/3). The SAP is the separate, more technical elaboration. The controlling timing rules, all confirmed:

1. The SAP is drafted after the protocol is final and **finalized before the blind is broken** (for unblinded/single-arm studies: before database lock).
2. Revisions during the **blind review** of data (ICH E9 §7.1 — the check of data between last-patient-last-visit and unblinding) are permitted and must be documented and justified.
3. Any change after unblinding is a post-hoc analysis and must be reported as such — ICH E3 §9.8 (changes in the conduct of the study or planned analyses) forces the disclosure in the [[clinical-study-report]].
4. The SAP, its amendments, and the randomization documentation are essential records (ICH E6(R3) Appendix C) retained in the TMF ([[conduct-tmf-checklist]], [[closeout-tmf-checklist]]).

## The estimand framework (ICH E9(R1))

E9(R1), FDA-adopted in May 2021, requires the trial's scientific question to be stated as an **estimand** with five attributes, defined *before* choosing the statistical method:

| Attribute | Content |
|---|---|
| Treatment | The treatment condition of interest (and comparator) |
| Population | The patients targeted by the question |
| Variable (endpoint) | The measurement obtained from each patient |
| Intercurrent-event strategies | How post-randomization events (discontinuation, rescue medication, death) are handled — the five named strategies: **treatment policy, hypothetical, composite variable, while on treatment, principal stratum** |
| Population-level summary | The measure of comparison (e.g., difference in means, hazard ratio, response-rate difference) |

Each primary estimand must be paired with a main estimator and **sensitivity analyses** targeting the same estimand under varied assumptions (E9(R1) A.5.2). The framework applies with proportionate rigor to early-phase and exploratory studies: pre-specification is what separates an exploratory finding that can seed a program from noise (ICH E9 §2.1.2).

## Required content of the SAP

A complete SAP for an OSSICRO-supported study contains, at minimum:

1. **Administrative** — protocol/IND identifiers, version history, author, and the signature/approval block.
2. **Objectives and endpoints** — restated verbatim from the protocol; discrepancies are a validation failure.
3. **Estimands** — per E9(R1), for primary and key secondary objectives.
4. **Design summary** — randomization method and ratio (ICH E9 §2.3), blinding, stratification.
5. **Analysis sets** — full analysis set (intention-to-treat principle), per-protocol set, safety set, with entry/exclusion rules (E9 §5.2).
6. **Sample-size justification** — assumptions, power or precision basis (E9 §3.5); for Phase 1/dose-escalation, the cohort logic and dose-decision rules.
7. **Statistical methods** — models, covariates, hypothesis-testing framework, significance levels, confidence intervals.
8. **Missing data** — prevention strategy, primary handling method, and sensitivity analyses (E9 §5.3; E9(R1)).
9. **Multiplicity** — control strategy across endpoints, doses, timepoints, and subgroups (E9 §5.6).
10. **Interim analyses** — timing, stopping guidelines, alpha-spending, and the firewall: for a monitored trial, interim outputs go to the [[dsmb-dmc|DSMB]] via an **independent statistician**, per the [[dsmb-charter]] and [[dsmb-workflow]]; the study team stays blinded.
11. **Safety analyses** — extent of exposure, AE coding and summarization conventions, laboratory shift analyses.
12. **Subgroup and exploratory analyses** — labeled as such.
13. **TLF shells** — mock tables, listings, and figures that predefine the presentation of results.

## Downstream obligations

The SAP is the contract the [[clinical-study-report]] must honor: ICH E3 §9.7 reports the methods *as planned*, §9.8 reports every change, and §16.1.9 appends the statistical documentation (with the randomization scheme at §16.1.7). Results posted to ClinicalTrials.gov under FDAAA 801 must be consistent with the pre-specified outcome measures ([[clinicaltrials-gov-registration]]). Where the study supports a marketing application, the SAP travels with the study data in the submission.

> [!warning] Non-delegable
> Statistical sign-off is accountable. The selection of estimands (a joint clinical–statistical judgment with the [[investigator]]/[[medical-monitor]]), the choice of analysis methods, the decision that a post-blind-review amendment is justified, and the approval signature on the SAP belong to a qualified [[biostatistician]] (ICH E9; ICH E6(R3) requires trials to be supported by qualified individuals). Interim-analysis review and any recommendation to stop or modify the trial belong to the [[dsmb-dmc|DSMB]] and the sponsor — never to software. OSSICRO drafts and structures; the biostatistician owns and signs.

> [!interpretive] OSSICRO position
> OSSICRO generates a complete SAP draft from the protocol's structured design data (endpoints, randomization, visit schedule), pre-populates the E9(R1) estimand table and forces all five attributes to be filled, checks endpoint-wording identity between protocol and SAP, validates that the version-history dates precede documented unblinding/database lock, and emits TLF shells consistent with the declared analyses. Every inferential choice (strategy for each intercurrent event, multiplicity method, missing-data model) is rendered as an amber judgment lane in the [[single-pass-review-ux]] and blocks finalization until the biostatistician resolves it — per the [[generate-check-validate-engine]] and [[non-delegable-functions-and-gates]]. Provenance of each SAP span is carried per the [[draft-provenance-model]].

## Related
- [[biostatistician]]
- [[clinical-protocol-and-synopsis]]
- [[clinical-study-report]]
- [[dsmb-dmc]]
- [[dsmb-charter]]
- [[dsmb-workflow]]
- [[clinicaltrials-gov-registration]]
- [[conduct-tmf-checklist]]
- [[closeout-tmf-checklist]]
- [[non-delegable-functions-and-gates]]
- [[generate-check-validate-engine]]

## Sources
- [ICH E9 — Statistical Principles for Clinical Trials (Step 4, 1998)](https://database.ich.org/sites/default/files/E9_Guideline.pdf)
- [ICH E9(R1) — Addendum on Estimands and Sensitivity Analysis (Step 4, Nov 2019)](https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1203.pdf)
- [FDA guidance — E9 Statistical Principles for Clinical Trials](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e9-statistical-principles-clinical-trials)
- [FDA guidance — E9(R1) Statistical Principles for Clinical Trials: Addendum: Estimands and Sensitivity Analysis in Clinical Trials (May 2021)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e9r1-statistical-principles-clinical-trials-addendum-estimands-and-sensitivity-analysis-clinical)
- [ICH E3 — Structure and Content of Clinical Study Reports (Step 4, 1995)](https://database.ich.org/sites/default/files/E3_Guideline.pdf)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025), Appendix C — Essential Records](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [21 CFR 312.23 — IND content and format (protocol statistical section)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23)
