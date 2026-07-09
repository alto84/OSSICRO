---
title: "Clinical Study Report (ICH E3)"
doc_id: "clinical-study-report-ich-e3"
category: "statistics"
governing_citations: ["ICH E3"]
owner: "sponsor-investigator"
receiver: "fda"
gate: "statistical-signoff"
status: template
updated: 2026-07-09
---

# Clinical Study Report (ICH E3) — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [ICH E3: Structure and Content of Clinical Study Reports](https://database.ich.org/sites/default/files/E3_Guideline.pdf), with the [E3 Questions & Answers (R1)](https://database.ich.org/sites/default/files/E3_Q%26As_R1_Q%26As.pdf) clarifying that E3 is a guidance on content, not a rigid format (see also the [ICH efficacy guidelines index](https://www.ich.org/page/efficacy-guidelines) and [FDA's adopted E3 guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e3-structure-and-content-clinical-study-reports)). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The Clinical Study Report (CSR) is the integrated full report of an individual trial — clinical and statistical description, presentation, and analysis in a single document — submitted to FDA at study completion (and forming the clinical basis of any later marketing application). Its statistical content must implement the final Statistical Analysis Plan; discrepancies must be disclosed in Section 9.8.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Section numbering below follows ICH E3; keep the numbering even for sections marked "not applicable" so reviewers can navigate. Do not draft efficacy or safety conclusions the data do not support — every claim must trace to a table, figure, or listing.

## Template

### Title Page

| | |
|---|---|
| Study title | {{protocol_title}} |
| Protocol number | {{protocol_number}} |
| Investigational product | {{drug_name}} |
| Indication studied | {{indication}} |
| Development phase | {{phase}} |
| Study initiation date (first subject enrolled) | {{study_start_date}} |
| Study completion date (last subject completed) | {{study_completion_date}} |
| Sponsor(-investigator) | {{sponsor_investigator_name}}, {{site_name}} |
| IND number | {{ind_number}} |
| Responsible biostatistician | {{biostatistician_name}} |
| Report version / date | {{csr_version}} / {{csr_date}} |
| GCP statement | This study was conducted in compliance with Good Clinical Practice (ICH E6), 21 CFR Parts 50, 54, 56, and 312, and the ethical principles of the Declaration of Helsinki. |

### 2. Synopsis

{{synopsis}}

[INSTRUCTION: Brief (usually ~3 pages) stand-alone summary per the ICH E3 synopsis format: name of sponsor; name of product; title of study; investigators; study centers; publication reference; studied period; phase; objectives; methodology; number of subjects (planned and analyzed); diagnosis and main criteria for inclusion; test product, dose, mode of administration, lot numbers; duration of treatment; reference therapy; criteria for evaluation (efficacy, safety); statistical methods; summary of results (efficacy, safety); conclusions; date of report. Include numerical results with confidence intervals, not just p-values.]

### 3. Table of Contents

[INSTRUCTION: Generate after content is final; include tables, figures, and appendices.]

### 4. List of Abbreviations and Definitions of Terms

{{abbreviations_list}}

### 5. Ethics

- **5.1 IRB.** The protocol, informed consent form, and amendments were reviewed and approved by {{irb_name}}; initial approval {{irb_approval_date}}. [INSTRUCTION: List all approved amendments and approval dates; approval letters in Appendix 16.1.3.]
- **5.2 Ethical conduct of the study.** [INSTRUCTION: GCP/Helsinki compliance statement.]
- **5.3 Subject information and consent.** Written informed consent was obtained from each subject before any study procedure, per 21 CFR Part 50. Consent form specimen in Appendix 16.1.3.

### 6. Investigators and Study Administrative Structure

Principal investigator: {{investigator_name}}, {{site_name}}. Biostatistician: {{biostatistician_name}}. Medical monitor: {{medical_monitor_name}}. [INSTRUCTION: List other key personnel (study coordinator, pharmacist, central lab, CRO and transferred obligations if any); CVs in Appendix 16.1.4; signature page of the sponsor-investigator in Appendix 16.1.5.]

### 7. Introduction

{{introduction}} [INSTRUCTION: Brief context: the disease, the investigational product, rationale, and where this study sits in the development plan. ~1 page.]

### 8. Study Objectives

Primary: {{primary_objective}}. Secondary: {{secondary_objectives}}. [INSTRUCTION: verbatim from the protocol.]

### 9. Investigational Plan

- **9.1 Overall study design and plan.** {{study_design}} [INSTRUCTION: design, randomization ratio, blinding, duration, schedule of assessments; a study-design schematic is strongly recommended.]
- **9.2 Discussion of study design, including choice of control group.** {{design_rationale}}
- **9.3 Selection of study population.** Inclusion criteria: {{inclusion_criteria}}. Exclusion criteria: {{exclusion_criteria}}. Removal criteria: {{withdrawal_criteria}}.
- **9.4 Treatments.** Treatments administered: {{treatment_arms}}; identity of investigational product(s) (formulation, lot numbers): {{ip_lots}}; method of assigning subjects to groups: {{randomization_method}}; dose selection rationale: {{dose_rationale}}; blinding: {{blinding_description}}; prior and concomitant therapy rules: {{conmed_rules}}; treatment compliance assessment: {{compliance_method}}.
- **9.5 Efficacy and safety variables.** {{endpoints_description}} [INSTRUCTION: define primary and secondary endpoints and measurement methods; state which is primary and why.]
- **9.6 Data quality assurance.** {{data_qa_description}} [INSTRUCTION: monitoring performed, audits, data management and query process.]
- **9.7 Statistical methods planned in the protocol and determination of sample size.** {{statistical_methods_summary}} [INSTRUCTION: summarize the final SAP (version {{sap_version}}): estimands, analysis sets, primary analysis model, multiplicity, interim analyses, missing-data handling, sample-size basis. The SAP itself goes in Appendix 16.1.9.]
- **9.8 Changes in the conduct of the study or planned analyses.** {{changes_in_conduct}} [INSTRUCTION: every protocol amendment and every deviation from the planned analyses, each with date and whether it preceded unblinding. If none, state so.]

### 10. Study Patients

- **10.1 Disposition of patients.** {{subject_disposition}} [INSTRUCTION: CONSORT-style accounting — screened, screen-failed (with reasons), randomized, treated, completed, discontinued (with reasons), by arm. Figure recommended.]
- **10.2 Protocol deviations.** {{protocol_deviations_summary}} [INSTRUCTION: important deviations grouped by category and arm; individual listings in Appendix 16.2.2.]

### 11. Efficacy Evaluation

{{efficacy_results}}

- **11.1 Data sets analyzed.** [INSTRUCTION: N per analysis set (FAS, PPS) per arm, with reasons for exclusion; must match SAP Section 4.]
- **11.2 Demographic and other baseline characteristics.** {{baseline_characteristics}} [INSTRUCTION: summary table by arm; note any imbalances.]
- **11.3 Measurements of treatment compliance.** {{compliance_results}}
- **11.4 Efficacy results and tabulations of individual patient data.**
  - 11.4.1 Analysis of efficacy: primary endpoint result — point estimate, {{confidence_level}} CI, p-value, per the pre-specified estimand; then secondary endpoints in SAP order. [INSTRUCTION: report estimates with precision, not p-values alone (ICH E3 §11.4.1); results of sensitivity analyses alongside the primary result.]
  - 11.4.2 Statistical/analytical issues: adjustments for covariates; handling of dropouts or missing data; interim analyses and data monitoring; multicenter studies (if applicable); multiple comparisons/multiplicity; use of an "efficacy subset"; active-control studies intended to show equivalence (if applicable); examination of subgroups.
  - 11.4.3 Tabulation of individual response data. [INSTRUCTION: individual efficacy listings in Appendix 16.2.6.]
  - 11.4.4 Drug dose, drug concentration, and relationships to response (if applicable).
  - 11.4.5 Drug-drug and drug-disease interactions (if applicable).
  - 11.4.6 By-patient displays (if applicable).
  - 11.4.7 Efficacy conclusions. [INSTRUCTION: conclusions strictly bounded by the pre-specified analyses; exploratory findings labeled as such.]

### 12. Safety Evaluation

{{safety_results}}

- **12.1 Extent of exposure.** {{exposure_summary}} [INSTRUCTION: duration and dose of exposure by arm.]
- **12.2 Adverse events.**
  - 12.2.1 Brief summary of adverse events: {{ae_overview}} [INSTRUCTION: overview table — any TEAE, related TEAE, severe TEAE, SAE, discontinuation due to AE, death; by arm.]
  - 12.2.2 Display of adverse events: TEAEs by System Organ Class and Preferred Term (MedDRA version {{meddra_version}}), by arm.
  - 12.2.3 Analysis of adverse events: [INSTRUCTION: severity, relatedness, dose relationship as applicable.]
  - 12.2.4 Listing of adverse events by patient (Appendix 16.2.7).
- **12.3 Deaths, other serious adverse events, and other significant adverse events.**
  - 12.3.1 Listing: deaths {{deaths_summary}}; SAEs {{sae_summary}}; other significant AEs (leading to discontinuation or dose modification).
  - 12.3.2 Narratives of deaths, other serious adverse events, and certain other significant adverse events. {{sae_narratives}} [INSTRUCTION: one narrative per death/SAE/significant event — subject identifier code (not name), age/sex, event, timing relative to dosing, course, outcome, and the investigator's and sponsor's causality assessments. Narratives may be placed here or in Appendix 16.3.2 with cross-reference.]
  - 12.3.3 Analysis and discussion of deaths, other serious adverse events, and other significant adverse events.
- **12.4 Clinical laboratory evaluation.** {{lab_results_summary}} [INSTRUCTION: summaries over time, shift tables, individual clinically significant abnormalities (E3 §12.4.2 lists Hy's-law-type evaluation for hepatic signals).]
- **12.5 Vital signs, physical findings, and other observations related to safety.** {{vitals_ecg_summary}}
- **12.6 Safety conclusions.** {{safety_conclusions}}

### 13. Discussion and Overall Conclusions

{{discussion_and_conclusions}} [INSTRUCTION: Integrate efficacy and safety; discuss clinical relevance, limitations (sample size, single-site, open-label, etc.), and benefit-risk in the studied population. No claims beyond the data.]

### 14. Tables, Figures, and Graphs Referred to but Not Included in the Text

[INSTRUCTION: Demographic (14.1), efficacy (14.2), and safety (14.3) summary tables/figures cited in Sections 10-12.]

### 15. Reference List

{{reference_list}}

### 16. Appendices

| Appendix | Content |
|---|---|
| 16.1.1 | Protocol and protocol amendments |
| 16.1.2 | Sample case report form |
| 16.1.3 | IRB approvals and sample consent form |
| 16.1.4 | Investigator CVs; list and description of investigators and other important study participants |
| 16.1.5 | Signatures of sponsor-investigator (signed report page) |
| 16.1.6 | Listing of patients receiving test drug from specific batches (where more than one batch used) |
| 16.1.7 | Randomization scheme and codes |
| 16.1.8 | Audit certificates (if available) |
| 16.1.9 | Documentation of statistical methods (final SAP, version {{sap_version}}) |
| 16.1.10 | Documentation of inter-laboratory standardization methods (if used) |
| 16.1.11 | Publications based on the study |
| 16.1.12 | Important publications referenced in the report |
| 16.2 | Patient data listings (16.2.1 discontinued patients; 16.2.2 protocol deviations; 16.2.3 patients excluded from efficacy analyses; 16.2.4 demographic data; 16.2.5 compliance/drug concentration; 16.2.6 individual efficacy response data; 16.2.7 adverse event listings; 16.2.8 individual laboratory listings) |
| 16.3 | Case report forms (16.3.1 CRFs for deaths, other SAEs, and withdrawals for AE; 16.3.2 other CRFs submitted) |

### Signature Page

The undersigned have read this report and confirm that to the best of their knowledge it accurately describes the conduct and results of the study.

| Role | Name | Signature | Date |
|---|---|---|---|
| Sponsor-Investigator | {{sponsor_investigator_name}} | ______________________ | ________ |
| Biostatistician (statistical content) | {{biostatistician_name}} | ______________________ | ________ |

> [!warning] Non-delegable
> Statistical sign-off is executed by the biostatistician (ICH E9 / E9(R1); ICH E3). OSSICRO drafts this template; the engine cannot finalize it without a recorded human sign-off.

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_title}} | study.protocol.title | ICH E3 §1 |
| {{protocol_number}} | study.identifiers.protocol_number | ICH E3 §1 |
| {{drug_name}} | study.product.name | ICH E3 §1 |
| {{indication}} | study.product.indication | ICH E3 §1 |
| {{phase}} | study.design.phase | ICH E3 §1 |
| {{study_start_date}} | study.milestones.first_subject_enrolled | ICH E3 §1 |
| {{study_completion_date}} | study.milestones.last_subject_completed | ICH E3 §1 |
| {{sponsor_investigator_name}} | study.sponsor_investigator.name | ICH E3 §1 |
| {{site_name}} | study.site.name | ICH E3 §1 |
| {{ind_number}} | study.identifiers.ind_number | ICH E3 §1 |
| {{biostatistician_name}} | personnel.biostatistician.name | ICH E3 §6 |
| {{csr_version}} | study.csr.version | ICH E3 §1 |
| {{csr_date}} | study.csr.date | ICH E3 §1 |
| {{synopsis}} | study.csr.synopsis | ICH E3 §2 |
| {{abbreviations_list}} | study.csr.abbreviations | ICH E3 §4 |
| {{irb_name}} | study.irb.name | ICH E3 §5.1 |
| {{irb_approval_date}} | study.irb.approval_date | ICH E3 §5.1 |
| {{investigator_name}} | personnel.investigator.name | ICH E3 §6 |
| {{medical_monitor_name}} | personnel.medical_monitor.name | ICH E3 §6 |
| {{introduction}} | study.csr.introduction | ICH E3 §7 |
| {{primary_objective}} | study.protocol.objectives.primary | ICH E3 §8 |
| {{secondary_objectives}} | study.protocol.objectives.secondary | ICH E3 §8 |
| {{study_design}} | study.design.summary | ICH E3 §9.1 |
| {{design_rationale}} | study.design.rationale | ICH E3 §9.2 |
| {{inclusion_criteria}} | study.protocol.eligibility.inclusion | ICH E3 §9.3.1 |
| {{exclusion_criteria}} | study.protocol.eligibility.exclusion | ICH E3 §9.3.2 |
| {{withdrawal_criteria}} | study.protocol.eligibility.withdrawal | ICH E3 §9.3.3 |
| {{treatment_arms}} | study.design.arms | ICH E3 §9.4.1 |
| {{ip_lots}} | study.product.lots | ICH E3 §9.4.2 |
| {{randomization_method}} | study.design.randomization | ICH E3 §9.4.3 |
| {{dose_rationale}} | study.design.dose_rationale | ICH E3 §9.4.4 |
| {{blinding_description}} | study.design.blinding | ICH E3 §9.4.6 |
| {{conmed_rules}} | study.protocol.conmeds | ICH E3 §9.4.7 |
| {{compliance_method}} | study.protocol.compliance_method | ICH E3 §9.4.8 |
| {{endpoints_description}} | study.protocol.endpoints | ICH E3 §9.5 |
| {{data_qa_description}} | study.data.qa_description | ICH E3 §9.6 |
| {{statistical_methods_summary}} | study.statistics.csr_methods_summary | ICH E3 §9.7 |
| {{sap_version}} | study.statistics.sap.version | ICH E3 §9.7, Appendix 16.1.9 |
| {{changes_in_conduct}} | study.csr.changes_in_conduct | ICH E3 §9.8 |
| {{subject_disposition}} | results.disposition | ICH E3 §10.1 |
| {{protocol_deviations_summary}} | results.deviations_summary | ICH E3 §10.2 |
| {{efficacy_results}} | results.efficacy | ICH E3 §11 |
| {{baseline_characteristics}} | results.baseline | ICH E3 §11.2 |
| {{compliance_results}} | results.compliance | ICH E3 §11.3 |
| {{confidence_level}} | study.statistics.primary_analysis.confidence_level | ICH E3 §11.4.1 |
| {{safety_results}} | results.safety | ICH E3 §12 |
| {{exposure_summary}} | results.safety.exposure | ICH E3 §12.1 |
| {{ae_overview}} | results.safety.ae_overview | ICH E3 §12.2.1 |
| {{meddra_version}} | study.data.meddra_version | ICH E3 §12.2.2 |
| {{deaths_summary}} | results.safety.deaths | ICH E3 §12.3.1 |
| {{sae_summary}} | results.safety.saes | ICH E3 §12.3.1 |
| {{sae_narratives}} | results.safety.narratives | ICH E3 §12.3.2 |
| {{lab_results_summary}} | results.safety.labs | ICH E3 §12.4 |
| {{vitals_ecg_summary}} | results.safety.vitals_ecg | ICH E3 §12.5 |
| {{safety_conclusions}} | results.safety.conclusions | ICH E3 §12.6 |
| {{discussion_and_conclusions}} | study.csr.discussion | ICH E3 §13 |
| {{reference_list}} | study.csr.references | ICH E3 §15 |

## Related

- [[03-documents/clinical-study-report-ich-e3]]
- [[03-documents/statistical-analysis-plan-ich-e9]] — the pre-specified analyses this report must implement (Appendix 16.1.9)
- [[03-documents/clinical-protocol-ich-m11-ceshharp]] — Appendix 16.1.1
- [[03-documents/fda-study-completion-ind-withdrawal-notice]] — closeout companion filing
