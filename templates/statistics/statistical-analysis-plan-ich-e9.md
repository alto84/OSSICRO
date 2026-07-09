---
title: "Statistical Analysis Plan (ICH E9)"
doc_id: "statistical-analysis-plan-ich-e9"
category: "statistics"
governing_citations: ["ICH E9", "ICH E9(R1)"]
owner: "sponsor-investigator"
receiver: "sponsor"
gate: "statistical-signoff"
status: template
updated: 2026-07-09
---

# Statistical Analysis Plan (ICH E9) — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [ICH E9: Statistical Principles for Clinical Trials](https://database.ich.org/sites/default/files/E9_Guideline.pdf) and [ICH E9(R1): Addendum on Estimands and Sensitivity Analysis in Clinical Trials](https://database.ich.org/sites/default/files/E9-R1_Step4_Guideline_2019_1203.pdf) (see also the [ICH efficacy guidelines index](https://www.ich.org/page/efficacy-guidelines) and [FDA's adopted E9(R1) guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e9r1-statistical-principles-clinical-trials-addendum-estimands-and-sensitivity-analysis-clinical)). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The Statistical Analysis Plan (SAP) pre-specifies, in technical detail, every planned statistical analysis of the trial before unblinding (or, for open-label trials, before database lock), so that analyses are protected from data-driven selection. It elaborates the statistical section of the protocol and is the biostatistician's controlling document for the analysis and for the statistical content of the Clinical Study Report.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Finalize and obtain the biostatistician's dated signature BEFORE unblinding or database lock; any later change must be documented in Section 12 with rationale and date relative to unblinding.

## Template

### Title and Administrative Information

**Statistical Analysis Plan**

| | |
|---|---|
| Protocol number | {{protocol_number}} |
| Protocol title | {{protocol_title}} |
| Protocol version / date this SAP is based on | {{protocol_version}} / {{protocol_version_date}} |
| SAP version | {{sap_version}} |
| SAP date | {{sap_date}} |
| Sponsor(-investigator) | {{sponsor_name}} |
| IND number | {{ind_number}} |
| Author (biostatistician) | {{biostatistician_name}}, {{biostatistician_degrees}} |

**SAP revision history**

| Version | Date | Author | Summary of changes | Before/after unblinding |
|---|---|---|---|---|
| {{sap_version}} | {{sap_date}} | {{biostatistician_name}} | [INSTRUCTION: "Initial release" for v1.0; otherwise itemize changes and state whether each occurred before or after unblinding/database lock (ICH E9 §5.6).] | |

### 1. Introduction

This SAP describes the planned statistical analyses for protocol {{protocol_number}}, "{{protocol_title}}." It is based on protocol version {{protocol_version}} dated {{protocol_version_date}} and supersedes the statistical section of the protocol where more detailed. [INSTRUCTION: If any planned analysis in this SAP differs from the protocol, itemize the differences here and cross-reference Section 12.]

### 2. Study Overview

- **Objectives.** Primary: {{primary_objective}}. Secondary: {{secondary_objectives}}. [INSTRUCTION: Copy verbatim from the protocol; do not paraphrase.]
- **Design.** {{study_design}} [INSTRUCTION: e.g., "randomized, double-blind, placebo-controlled, parallel-group, single-site Phase 2"; state randomization ratio, stratification factors, and blinding level per ICH E9 §2-3.]
- **Treatments.** {{treatment_arms}}
- **Planned sample size.** {{planned_sample_size}} (see Section 8).
- **Schedule.** Treatment duration {{treatment_duration}}; follow-up {{followup_duration}}.

### 3. Estimands (ICH E9(R1))

[INSTRUCTION: Define one estimand per objective, primary first. Each estimand MUST specify all five attributes of ICH E9(R1) §A.3. Repeat the block below for each estimand. The estimand definitions must match the protocol; the SAP may add analytic detail but may not silently redefine an estimand.]

**Estimand {{estimand_number}} ({{estimand_label}} — {{associated_objective}})**

| Attribute | Specification |
|---|---|
| Treatment condition | {{estimand_treatment}} [INSTRUCTION: the treatment regimen of interest and, as appropriate, the comparator.] |
| Population | {{estimand_population}} [INSTRUCTION: patients targeted by the clinical question, defined by eligibility criteria; note if a principal-stratum population is intended.] |
| Variable (endpoint) | {{estimand_variable}} [INSTRUCTION: exact endpoint, measurement scale, timepoint(s).] |
| Intercurrent events and handling strategies | {{estimand_intercurrent_events}} [INSTRUCTION: enumerate each anticipated intercurrent event (e.g., discontinuation of study drug, use of rescue medication, death) and the strategy applied to each: treatment policy, hypothetical, composite, while-on-treatment, or principal stratum (E9(R1) §A.3.2).] |
| Population-level summary | {{estimand_summary_measure}} [INSTRUCTION: e.g., difference in means at Week 12; hazard ratio; risk difference; odds ratio.] |

{{estimands}}
[INSTRUCTION: The placeholder above receives the full set of estimand blocks from the study record; verify each against the protocol objectives one-to-one.]

### 4. Analysis Populations (Analysis Sets)

{{analysis_populations}}

[INSTRUCTION: Define each analysis set precisely enough that membership is decidable per subject at the data-review meeting BEFORE unblinding (ICH E9 §5.2). Typical minimum set:]

| Analysis set | Definition | Used for |
|---|---|---|
| Full Analysis Set (FAS) | All randomized subjects, analyzed per randomized arm (intention-to-treat principle, ICH E9 §5.2.1) [INSTRUCTION: state any protocol-permitted exclusions, e.g., no post-baseline data, and justify.] | Primary efficacy |
| Per-Protocol Set (PPS) | FAS subjects without major protocol deviations affecting the primary endpoint [INSTRUCTION: enumerate the disqualifying deviations.] | Supportive/sensitivity efficacy |
| Safety Set | All subjects who received any amount of study intervention, analyzed per treatment actually received | All safety analyses |

Classification of subjects into analysis sets will be finalized and documented at the blinded data-review meeting prior to database lock/unblinding.

### 5. Statistical Methods — Primary Analysis

- **Primary endpoint:** {{primary_endpoint}}
- **Primary analysis model:** {{primary_analysis_method}} [INSTRUCTION: full model specification — e.g., MMRM with fixed effects for treatment, visit, treatment-by-visit, stratification factors, and baseline value as covariate; unstructured covariance; Kenward-Roger df. Name the estimator that targets Estimand 1.]
- **Null and alternative hypotheses:** {{hypotheses}}
- **Significance level:** {{alpha_level}} (two-sided) [INSTRUCTION: state one-sided alternatives explicitly if used, with justification per ICH E9 §5.5.]
- **Effect estimate to be reported:** point estimate, {{confidence_level}} confidence interval, and p-value for {{estimand_summary_measure}}.

### 6. Secondary and Exploratory Analyses

[INSTRUCTION: One subsection per secondary endpoint, each mapped to its estimand from Section 3, with model specification at the same rigor as Section 5. Label exploratory analyses as hypothesis-generating.]

{{secondary_analyses}}

**Multiplicity.** {{multiplicity_strategy}} [INSTRUCTION: If any secondary endpoint supports a claim, pre-specify the multiplicity adjustment (hierarchical testing, Hochberg, gatekeeping, etc.) per ICH E9 §5.6; otherwise state that secondary p-values are nominal and unadjusted.]

**Subgroup analyses.** {{subgroup_analyses}} [INSTRUCTION: pre-specify subgroups, the interaction-based approach, and the exploratory status of subgroup findings (ICH E9 §5.7).]

### 7. Sensitivity and Supplementary Analyses

[INSTRUCTION: Per ICH E9(R1) §A.5, pre-specify sensitivity analyses that vary the untestable assumptions of the main estimator for the SAME estimand (e.g., tipping-point analysis for missing-data assumptions), and distinguish them from supplementary analyses that target different estimands.]

{{sensitivity_analyses}}

### 8. Sample Size and Power

Planned enrollment: {{planned_sample_size}} ({{per_arm_n}} per arm). Basis: {{sample_size_assumptions}} [INSTRUCTION: assumed effect size and its source, variability, alpha, power, allocation ratio, attrition assumption, and the software/method used (ICH E9 §3.5). Reproduce the calculation so an independent statistician can verify it.]

### 9. Interim Analyses and Data Monitoring

{{interim_analysis_plan}} [INSTRUCTION: If any interim analysis is planned: timing/information fraction, endpoints examined, alpha-spending function and stopping boundaries (efficacy/futility/harm), who performs the unblinded analysis, and firewall procedures preserving trial integrity (ICH E9 §4.5-4.6). Cross-reference the DSMB Charter. If none, state "No interim analysis of efficacy is planned."]

### 10. Missing Data

{{missing_data_handling}} [INSTRUCTION: Primary missing-data approach must be consistent with the intercurrent-event strategies in Section 3 (e.g., MMRM under MAR for a hypothetical strategy; multiple imputation with reference-based methods for treatment-policy sensitivity). State conventions for partial dates and unscheduled visits. ICH E9 §5.3; E9(R1) §A.4.]

### 11. Safety Analyses

- Adverse events coded with MedDRA version {{meddra_version}}; treatment-emergent AE definition: {{teae_definition}}.
- Descriptive summaries by treatment arm: TEAEs, related TEAEs, SAEs, deaths, discontinuations due to AE — by System Organ Class and Preferred Term.
- Laboratory, vital sign, and ECG analyses: {{safety_analysis_methods}} [INSTRUCTION: shift tables, markedly-abnormal criteria, Hy's law screening as applicable. No hypothesis testing on safety unless pre-specified.]

### 12. Changes from Protocol-Specified Analyses

{{changes_from_protocol}} [INSTRUCTION: Itemize every difference between this SAP and the protocol's statistical section, with rationale and whether the change predates unblinding (ICH E9 §5.6; this list is reproduced in CSR §9.8).]

### 13. Programming and Data Standards

Analyses will be performed in {{statistical_software}} {{software_version}}. Datasets follow {{data_standards}} [INSTRUCTION: e.g., CDISC SDTM/ADaM versions]. All analysis programs are validated per {{validation_sop}}.

### 14. References

[INSTRUCTION: cite ICH E9, ICH E9(R1), the protocol, and any methodological literature relied on for the primary estimator.]

### Signature Page

By signing below, the biostatistician approves this SAP as the pre-specified analysis plan for protocol {{protocol_number}}.

| Role | Name | Signature | Date |
|---|---|---|---|
| Biostatistician | {{biostatistician_name}} | ______________________ | ________ |
| Sponsor-Investigator | {{sponsor_investigator_name}} | ______________________ | ________ |

> [!warning] Non-delegable
> Statistical sign-off is executed by the biostatistician (ICH E9 / E9(R1); ICH E3). OSSICRO drafts this template; the engine cannot finalize it without a recorded human sign-off.

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | study.identifiers.protocol_number | ICH E9 §2.1 |
| {{protocol_title}} | study.protocol.title | ICH E9 §2.1 |
| {{protocol_version}} | study.protocol.version | ICH E9 §5.1 |
| {{protocol_version_date}} | study.protocol.version_date | ICH E9 §5.1 |
| {{sap_version}} | study.statistics.sap.version | ICH E9 §5.1 |
| {{sap_date}} | study.statistics.sap.date | ICH E9 §5.1 |
| {{sponsor_name}} | study.sponsor.name | ICH E9 §1.1 |
| {{ind_number}} | study.identifiers.ind_number | 21 CFR 312.23(a)(6) |
| {{biostatistician_name}} | personnel.biostatistician.name | ICH E9 §1.1 |
| {{biostatistician_degrees}} | personnel.biostatistician.degrees | ICH E9 §1.1 |
| {{primary_objective}} | study.protocol.objectives.primary | ICH E9 §2.1 |
| {{secondary_objectives}} | study.protocol.objectives.secondary | ICH E9 §2.1 |
| {{study_design}} | study.design.summary | ICH E9 §3 |
| {{treatment_arms}} | study.design.arms | ICH E9 §3.1 |
| {{planned_sample_size}} | study.design.sample_size.total | ICH E9 §3.5 |
| {{per_arm_n}} | study.design.sample_size.per_arm | ICH E9 §3.5 |
| {{treatment_duration}} | study.design.treatment_duration | ICH E9 §3 |
| {{followup_duration}} | study.design.followup_duration | ICH E9 §3 |
| {{estimand_number}} | study.statistics.estimands[].number | ICH E9(R1) §A.3 |
| {{estimand_label}} | study.statistics.estimands[].label | ICH E9(R1) §A.3 |
| {{associated_objective}} | study.statistics.estimands[].objective_ref | ICH E9(R1) §A.3 |
| {{estimand_treatment}} | study.statistics.estimands[].treatment | ICH E9(R1) §A.3.1 |
| {{estimand_population}} | study.statistics.estimands[].population | ICH E9(R1) §A.3.1 |
| {{estimand_variable}} | study.statistics.estimands[].variable | ICH E9(R1) §A.3.1 |
| {{estimand_intercurrent_events}} | study.statistics.estimands[].intercurrent_events | ICH E9(R1) §A.3.2 |
| {{estimand_summary_measure}} | study.statistics.estimands[].summary_measure | ICH E9(R1) §A.3.1 |
| {{estimands}} | study.statistics.estimands | ICH E9(R1) §A.3 |
| {{analysis_populations}} | study.statistics.analysis_populations | ICH E9 §5.2 |
| {{primary_endpoint}} | study.protocol.endpoints.primary | ICH E9 §2.2.2 |
| {{primary_analysis_method}} | study.statistics.primary_analysis.method | ICH E9 §5.1 |
| {{hypotheses}} | study.statistics.primary_analysis.hypotheses | ICH E9 §5.5 |
| {{alpha_level}} | study.statistics.primary_analysis.alpha | ICH E9 §5.5 |
| {{confidence_level}} | study.statistics.primary_analysis.confidence_level | ICH E9 §5.5 |
| {{secondary_analyses}} | study.statistics.secondary_analyses | ICH E9 §5.1 |
| {{multiplicity_strategy}} | study.statistics.multiplicity | ICH E9 §5.6 |
| {{subgroup_analyses}} | study.statistics.subgroups | ICH E9 §5.7 |
| {{sensitivity_analyses}} | study.statistics.sensitivity_analyses | ICH E9(R1) §A.5 |
| {{sample_size_assumptions}} | study.statistics.sample_size.assumptions | ICH E9 §3.5 |
| {{interim_analysis_plan}} | study.statistics.interim.plan | ICH E9 §4.5 |
| {{missing_data_handling}} | study.statistics.missing_data | ICH E9 §5.3 |
| {{meddra_version}} | study.data.meddra_version | ICH E9 §6.1 |
| {{teae_definition}} | study.statistics.safety.teae_definition | ICH E9 §6.2 |
| {{safety_analysis_methods}} | study.statistics.safety.methods | ICH E9 §6 |
| {{changes_from_protocol}} | study.statistics.sap.changes_from_protocol | ICH E9 §5.6 |
| {{statistical_software}} | study.statistics.software.name | ICH E9 §5.8 |
| {{software_version}} | study.statistics.software.version | ICH E9 §5.8 |
| {{data_standards}} | study.data.standards | ICH E9 §5.8 |
| {{validation_sop}} | study.statistics.validation_sop | ICH E9 §5.8 |
| {{sponsor_investigator_name}} | study.sponsor_investigator.name | 21 CFR 312.3 |

## Related

- [[03-documents/statistical-analysis-plan-ich-e9]]
- [[03-documents/clinical-study-report-ich-e3]] — the CSR's statistical content must follow this SAP
- [[03-documents/clinical-protocol-ich-m11-ceshharp]] — the protocol's statistical section this SAP elaborates
- [[03-documents/dsmb-charter-single-site-low-risk]] — interim-analysis interface (Section 9)
