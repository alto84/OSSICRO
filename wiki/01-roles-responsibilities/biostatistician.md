---
title: "Biostatistician — SAP, Estimand, and Statistical Accountability"
section: "01-roles-responsibilities"
status: mixed
governing_authority:
  - "ICH E9 (Statistical Principles for Clinical Trials)"
  - "ICH E9(R1) (Addendum on Estimands and Sensitivity Analysis)"
  - "ICH E6(R3) §3 (Investigator) / §5 (Sponsor) — data governance & recordkeeping"
  - "21 CFR 312.23(a)(6)(iii)(g) (statistical analysis in the protocol)"
  - "21 CFR 312.33 (annual report safety summaries)"
tags: [role/biostatistician, ich/e9, gcp/e6r3, cfr/312, status/mixed, ossicro/gating]
aliases: ["trial statistician", "study statistician", "SAP author"]
updated: 2026-07-09
---

# Biostatistician — SAP, Estimand, and Statistical Accountability

> [!authority] Governing authority
> ICH E9 (Statistical Principles for Clinical Trials) and ICH E9(R1) (estimand framework) govern trial statistics; ICH E6(R3) §5 places statistical planning inside the sponsor's quality-by-design and data-governance obligations; 21 CFR 312.23(a)(6) requires the protocol to describe the statistical methods. Status: **Mixed** — the statistical requirements are confirmed black-letter/guidance; the OSSICRO drafting boundary is an interpretive position, marked inline.

The biostatistician is the qualified professional who designs the analytic architecture of a trial and owns its statistical integrity: the target of estimation (the **estimand**), the analysis population, the randomization scheme, the sample-size justification, the pre-specified analyses, and the tables/listings/figures (TLFs) that render the result. In a [[sponsor-investigator]] IND the statistician's work is not cosmetic — a pre-specified, defensible [[statistical-analysis-plan]] is what separates a credible early-phase result from an uninterpretable one, and FDA reviewers read the SAP as the guarantee that the analysis was not chosen after seeing the data. OSSICRO drafts and completeness-checks statistical documentation; it does not author the scientific judgments those documents encode.

## Governing framework: ICH E9 and E9(R1)

**ICH E9 (1998, FDA-adopted)** is the foundational guidance on statistical principles: it establishes the primacy of a **pre-specified** analysis, the distinction between confirmatory and exploratory objectives, the roles of the full-analysis-set / intention-to-treat and per-protocol populations, the handling of multiplicity, and the requirement that the statistical plan be finalized before unblinding. Deviations from the pre-specified plan must be identified and justified.

**ICH E9(R1) (2019/2020 addendum)** overlays the **estimand framework**, which is now the organizing spine of modern trial design. An estimand is a precise description of *what is being estimated* — the treatment effect the trial is designed to quantify — defined by five attributes:

1. **Treatment** — the condition(s) being compared (and the treatment regimen, not just the drug).
2. **Population** — the patients targeted by the scientific question.
3. **Variable (endpoint)** — the outcome measured on each subject.
4. **Intercurrent-event strategy** — how the analysis handles events that occur after randomization and complicate interpretation (e.g., treatment discontinuation, rescue medication, death). E9(R1) names five strategies: treatment-policy, hypothetical, composite-variable, while-on-treatment, and principal-stratum.
5. **Population-level summary** — the statistic that expresses the effect (e.g., difference in means, hazard ratio, odds ratio).

The intercurrent-event strategy is the addendum's central contribution: the *same* raw data can support different treatment-effect estimates depending on how post-randomization complications are conceptualized, so the estimand must be chosen at design time, in dialogue with the clinical question, and stated in the protocol and SAP. E9(R1) also requires **sensitivity analyses** aligned to the estimand's assumptions and distinguishes them from **supplementary** analyses.

For early-phase (Phase 1/2) work the estimand discipline is lighter but not absent: dose-finding and preliminary-efficacy objectives still require a clearly stated target of estimation, a defined analysis population, and a handling rule for dropouts and rescue.

## Core deliverables and where accountability sits

| Deliverable | What the biostatistician owns | Governing authority |
|---|---|---|
| Estimand definition | The five-attribute target of estimation; the intercurrent-event strategy | ICH E9(R1) |
| Sample size / power | The justification, assumptions, and effect size | ICH E9 §3.5; protocol 312.23(a)(6) |
| Randomization & stratification | Allocation scheme, blocking, concealment | ICH E9 §2.3 |
| [[statistical-analysis-plan]] (SAP) | Full pre-specified analysis, populations, multiplicity, missing-data | ICH E9 / E9(R1) |
| TLF shells & programming spec | Table/listing/figure structure | ICH E3 (report), E9 |
| Interim-analysis / stopping rules | Statistical monitoring guidance for the [[dsmb-dmc]] | FDA 2006/2024 DMC guidance |
| Independent (unblinded) statistician | Firewalled DMC data analysis | FDA DMC guidance; see [[dsmb-workflow]] |
| Final analysis & statistical sign-off | Attestation that analyses match the pre-specified SAP | ICH E9; E6(R3) data governance |

Two distinct statistical roles must not be conflated. The **trial (blinded) statistician** writes the SAP and performs the final analysis after database lock. The **independent unblinded statistician** prepares the closed-session data packages for the [[dsmb-dmc]] and sits *outside* the sponsor firewall so that the sponsor/investigator team remains blinded during conduct (FDA 2006 DMC guidance; see [[dsmb-charter]]). In a solo sponsor-investigator setting the [[micro-cro-accountable-layer]] typically supplies the independent statistician, because the sponsor-investigator cannot simultaneously be blinded and unblinded.

## Non-delegable statistical judgment

> [!warning] Non-delegable
> **Estimand selection, SAP finalization, and final statistical sign-off are the biostatistician's accountable judgment.** Choosing the intercurrent-event strategy, justifying the sample size, adjudicating the analysis population, and attesting that the executed analysis matches the pre-specified plan are qualified-human acts (ICH E9/E9(R1); ICH E6(R3) §5 data governance). The pre-specification guarantee — that the plan was fixed before unblinding — is meaningful only because a named, accountable statistician stands behind it. OSSICRO can draft SAP structure and check for the required sections; it cannot select the estimand or sign the analysis.

> [!warning] Non-delegable
> **Interim-analysis interpretation and stopping recommendations belong to the independent statistician and the [[dsmb-dmc]].** A software-computed boundary crossing is an input, not a decision. The recommendation to continue, modify, or stop remains a conflict-free human committee's call (FDA 2006 DMC guidance).

## What OSSICRO drafts, checks, and validates

> [!interpretive] OSSICRO position
> OSSICRO treats statistical *document assembly* as a low-influence context of use (per the FDA 2025 AI-credibility draft framework; see [[part-11-and-ai-credibility]]): the software generates a SAP skeleton from structured study inputs (design, endpoints, population, planned comparisons), checks it for the ICH E9/E9(R1) required components (estimand attributes present, missing-data approach stated, multiplicity addressed, sensitivity analyses aligned), and validates cross-document consistency (protocol objective ↔ estimand ↔ SAP primary analysis ↔ TLF shells). The **generate** pass produces a draft; the **check** pass flags missing estimand attributes or an undefined intercurrent-event strategy as an *amber* open item in the [[completeness-ledger]]; the **validate** pass traces each SAP section to ICH E9/E9(R1). Every statistical *choice* fails to a human gate. This boundary is an OSSICRO design position, not a regulatory permission — the guidance nowhere authorizes AI-selected estimands.

Concretely, OSSICRO can: instantiate a SAP template with the estimand table pre-structured; auto-populate analysis-population definitions and randomization descriptors from the protocol; check that every protocol-stated objective has a corresponding pre-specified analysis; assemble TLF shells; and surface the annual-report safety summaries (most-frequent / most-serious adverse reactions, deaths, dropouts) that feed the [[ind-annual-report-dsur]] under 21 CFR 312.33. It cannot: choose the intercurrent-event strategy, set the effect size, decide the multiplicity strategy, or sign the final analysis.

## Coordination touchpoints

- Feeds the [[dsmb-dmc]] via the independent-statistician firewall ([[dsmb-workflow]]).
- The SAP is an essential record in the [[document-catalog]] and [[startup-tmf-checklist]] (finalized before unblinding).
- Safety line-listings the statistician summarizes flow into the [[ind-annual-report-dsur]] and the [[safety-reporting-workflow]].
- The final analysis populates the [[clinical-study-report]] (ICH E3).
- Estimand and analysis choices are surfaced to the [[medical-monitor]] and [[sponsor-investigator]] for scientific concurrence.

## Related

- [[statistical-analysis-plan]]
- [[clinical-study-report]]
- [[dsmb-dmc]]
- [[dsmb-charter]]
- [[dsmb-workflow]]
- [[medical-monitor]]
- [[sponsor-investigator]]
- [[micro-cro-accountable-layer]]
- [[clinical-protocol-and-synopsis]]
- [[non-delegable-functions-and-gates]]
- [[part-11-and-ai-credibility]]
- [[completeness-ledger]]

## Sources

- [ICH E9 — Statistical Principles for Clinical Trials (Step 4, 1998)](https://database.ich.org/sites/default/files/E9_Guideline.pdf)
- [ICH E9(R1) — Addendum on Estimands and Sensitivity Analysis in Clinical Trials (Step 4, 2019)](https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1203.pdf)
- [FDA — E9(R1) Statistical Principles for Clinical Trials: Addendum (guidance page)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e9r1-statistical-principles-clinical-trials-addendum-estimands-and-sensitivity-analysis-clinical)
- [ICH E6(R3) — Good Clinical Practice, Step 4 Final Guideline (2025-01-06)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [ICH E3 — Structure and Content of Clinical Study Reports](https://database.ich.org/sites/default/files/E3_Guideline.pdf)
- [21 CFR 312.23 — IND content and format (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23)
- [21 CFR 312.33 — Annual reports (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.33)
