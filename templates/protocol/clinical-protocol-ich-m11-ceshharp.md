---
title: "Clinical Protocol (ICH M11 CeSHarP structure)"
doc_id: "clinical-protocol-ich-m11-ceshharp"
category: "protocol"
governing_citations: ["21 CFR 312.23(a)(6)", "ICH M11", "ICH E6(R3) Appendix B"]
owner: "sponsor-investigator"
receiver: "irb"
gate: "none"
status: template
updated: 2026-07-09
---

# Clinical Protocol (ICH M11 CeSHarP structure) — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.23(a)(6)](https://www.law.cornell.edu/cfr/text/21/312.23) (protocol content required in an IND); [ICH M11 — Clinical electronic Structured Harmonised Protocol (CeSHarP)](https://www.ich.org/page/multidisciplinary-guidelines) (harmonised protocol template and technical specification); [ICH E6(R3) Appendix B](https://www.ich.org/page/efficacy-guidelines) (trial protocol contents). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The clinical protocol is the controlling document of the trial: it states the objectives, design, methodology, statistical considerations, and organization of the study, and it is the document against which the investigator commits to conduct the trial (Form FDA 1572, box 9). This template follows the ICH M11 CeSHarP section structure and satisfies the minimum protocol elements of 21 CFR 312.23(a)(6)(iii) for submission in an IND and to the reviewing IRB.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Sections marked "Not applicable" must state why rather than be deleted — M11 uses a "complete or state not applicable" convention. Phase 1 protocols may be less detailed on efficacy analyses but may NOT abbreviate safety monitoring (21 CFR 312.23(a)(6)(i) permits flexibility in Phase 1 design description only).

## Template

# TITLE PAGE

| | |
|---|---|
| **Full Title** | {{title}} |
| **Protocol Number** | {{protocol_number}} |
| **Protocol Version** | {{protocol_version}} |
| **Protocol Date** | {{protocol_date}} |
| **Amendment Number** | {{amendment_number}} [INSTRUCTION: "Original Protocol" for version 1; otherwise the sequential amendment number with a version history table in Section 14.] |
| **Investigational Product** | {{drug_name}} |
| **IND Number** | {{ind_number}} |
| **Sponsor-Investigator** | {{investigator_name}}, {{investigator_degrees}} |
| **Sponsor-Investigator Address** | {{investigator_address}} |
| **Trial Phase** | {{phase}} |
| **Registry Identifier** | {{nct_number}} [INSTRUCTION: enter "Pending" if not yet issued; must be completed before first subject enrollment per FDAAA 801.] |

**Confidentiality Statement.** This document contains confidential information of {{sponsor_name}}. It is provided to you as an investigator, potential investigator, or consultant for review by you, your staff, and the responsible IRB. Do not disclose it to third parties without written authorization, except to obtain informed consent from potential trial participants.

---

## 1. PROTOCOL SUMMARY

### 1.1 Protocol Synopsis
[INSTRUCTION: Insert the synopsis (see companion document [[03-documents/protocol-synopsis]]). Keep it consistent with the body; the body controls in any conflict.]

{{protocol_synopsis}}

### 1.2 Trial Schema
[INSTRUCTION: Insert a diagram of the trial design — screening, treatment period(s), arms, key decision points, follow-up. A simple flow diagram is acceptable.]

{{trial_schema}}

### 1.3 Schedule of Activities (SoA)
[INSTRUCTION: One table; rows = assessments/procedures; columns = visits with study day and visit window. Every procedure described in Section 8 must appear here, and vice versa.]

{{schedule_of_activities}}

## 2. INTRODUCTION

### 2.1 Purpose of Trial
{{trial_purpose}}

### 2.2 Summary of Benefits and Risks
[INSTRUCTION: Summarize known and potential risks and benefits to participants (source: current Investigator's Brochure edition {{ib_edition}}, or package insert for approved products), and state the benefit-risk conclusion supporting conduct of the trial. Cross-reference, do not restate, the full IB. ICH E6(R3) 2.4: a trial should be initiated only if anticipated benefits justify the risks.]

{{benefit_risk_summary}}

## 3. TRIAL OBJECTIVES, ENDPOINTS AND ESTIMANDS

[INSTRUCTION: State each objective with its paired endpoint(s). For each primary (and key secondary) objective in a confirmatory setting, define the estimand per ICH E9(R1): population, treatment condition, variable, intercurrent-event strategies, population-level summary. For exploratory Phase 1 objectives a full estimand framework may be marked not applicable with justification.]

### 3.1 Primary Objective and Endpoint
{{objectives}}

| Objective | Endpoint | Estimand attributes |
|---|---|---|
| {{primary_objective}} | {{primary_endpoint}} | {{primary_estimand}} |

### 3.2 Secondary Objectives and Endpoints
{{secondary_objectives_endpoints}}

### 3.3 Exploratory Objectives and Endpoints
{{exploratory_objectives_endpoints}} [INSTRUCTION: or "Not applicable."]

## 4. TRIAL DESIGN

### 4.1 Description of Trial Design
[INSTRUCTION: State type (e.g., open-label, randomized, double-blind, placebo-controlled, dose-escalation), number of arms, allocation ratio, duration of participation per subject, number of sites, and overall trial duration. 21 CFR 312.23(a)(6)(iii)(c) requires description of the kind of control group, if any, and methods to minimize bias.]

{{trial_design_description}}

### 4.2 Rationale for Trial Design
{{design_rationale}} [INSTRUCTION: justify comparator choice, blinding or its absence, and dose-escalation scheme if any.]

### 4.3 Rationale for Dose and Regimen
[INSTRUCTION: Justify starting dose, dose levels, maximum dose, and duration of exposure against nonclinical and prior human data. 21 CFR 312.23(a)(6)(iii)(d): the method for determining doses, the maximum dosage, and the duration of individual patient exposure must be stated.]

{{dose_rationale}}

### 4.4 End of Trial Definition
{{end_of_trial_definition}} [INSTRUCTION: e.g., last visit of the last participant.]

## 5. TRIAL POPULATION

[INSTRUCTION: 21 CFR 312.23(a)(6)(iii)(b) requires the criteria for patient selection and exclusion and an estimate of the number of patients to be studied.]

**Planned enrollment:** {{planned_enrollment}} participants at {{number_of_sites}} site(s).

### 5.1 Inclusion Criteria
{{eligibility_criteria}}

[INSTRUCTION: Numbered list. Each criterion must be objectively verifiable from source documents. Include: age range, diagnosis with confirmation method, disease stage/severity, organ-function thresholds, contraception requirements, and capacity to consent (or the permitted LAR pathway).]

1. {{inclusion_criterion_1}}
2. [INSTRUCTION: continue as needed.]

### 5.2 Exclusion Criteria
1. {{exclusion_criterion_1}}
2. [INSTRUCTION: continue as needed. Include prohibited prior/concomitant therapy, safety-based exclusions tied to the IB risk profile, and pregnancy/lactation where applicable.]

### 5.3 Lifestyle and Concomitant-Restriction Considerations
{{lifestyle_restrictions}} [INSTRUCTION: or "Not applicable."]

### 5.4 Screen Failures and Rescreening
{{screen_failure_policy}}

## 6. TRIAL INTERVENTION AND CONCOMITANT THERAPY

### 6.1 Description of Investigational Product
| | |
|---|---|
| Name/Code | {{drug_name}} |
| Dosage form / strength | {{dosage_form_strength}} |
| Route | {{route_of_administration}} |
| Manufacturer / supplier | {{ip_supplier}} |
| Storage conditions | {{storage_conditions}} |

### 6.2 Dosing and Administration
[INSTRUCTION: The complete dosing plan: dose(s), schedule, administration instructions, dose-escalation rules (if any) with cohort review criteria, and maximum permitted dose and exposure duration.]

{{dosing_plan}}

### 6.3 Dose Modification and Toxicity Management
{{dose_modification_rules}} [INSTRUCTION: dose-hold, dose-reduction, and permanent-discontinuation criteria keyed to graded toxicity (e.g., CTCAE v{{ctcae_version}}).]

### 6.4 Blinding and Unblinding
{{blinding_procedures}} [INSTRUCTION: or "Not applicable — open-label." If blinded, state emergency unblinding mechanism available to the investigator 24/7.]

### 6.5 Treatment Assignment / Randomization
{{randomization_method}} [INSTRUCTION: or "Not applicable — single arm."]

### 6.6 IP Accountability, Handling, and Disposition
Investigational product is received, stored, dispensed, and reconciled per [[03-documents/drug-accountability-log]] and returned or destroyed per 21 CFR 312.59 and 312.62(a). {{ip_accountability_summary}}

### 6.7 Treatment Compliance
{{compliance_assessment_method}}

### 6.8 Concomitant Therapy
Permitted: {{permitted_concomitant_meds}}
Prohibited: {{prohibited_concomitant_meds}}
Rescue: {{rescue_medication_plan}} [INSTRUCTION: or "Not applicable."]

## 7. DISCONTINUATION OF TRIAL INTERVENTION AND PARTICIPANT WITHDRAWAL

### 7.1 Discontinuation of Trial Intervention
{{intervention_discontinuation_criteria}} [INSTRUCTION: distinguish discontinuation of intervention (participant continues in follow-up) from withdrawal from the trial.]

### 7.2 Participant Withdrawal from the Trial
{{withdrawal_criteria}} [INSTRUCTION: participants may withdraw consent at any time without penalty; state data-handling for withdrawn participants.]

### 7.3 Lost to Follow-Up
{{lost_to_followup_procedures}}

### 7.4 Trial or Site Stopping Criteria
{{trial_stopping_criteria}} [INSTRUCTION: sponsor-investigator halting rules — e.g., specified rates of DLTs or SAEs triggering enrollment pause and safety review. Cross-reference DSMB charter if one exists: [[03-documents/dsmb-charter-single-site-low-risk]].]

## 8. TRIAL ASSESSMENTS AND PROCEDURES

[INSTRUCTION: 21 CFR 312.23(a)(6)(iii)(e)-(g): describe the observations and measurements to fulfill the objectives, and the clinical procedures, laboratory tests, or other measures taken to monitor the effects of the drug in human subjects and to minimize risk.]

### 8.1 Efficacy Assessments
{{efficacy_assessments}} [INSTRUCTION: method, timing (per SoA), and who performs each.]

### 8.2 Safety Assessments
{{safety_monitoring}}

[INSTRUCTION: Must include, at minimum: physical examinations; vital signs; clinical laboratory tests (hematology, chemistry, urinalysis) with the certified laboratory identified; ECGs if applicable; pregnancy testing where applicable; and the specific monitoring keyed to the known risk profile in the IB (e.g., LFT monitoring for hepatotoxicity signal). State abnormal-value follow-up rules.]

### 8.3 Adverse Events and Serious Adverse Events

- **Definitions.** AE, SAE, suspected adverse reaction, and unexpected are used as defined in 21 CFR 312.32(a).
- **Collection period.** From {{ae_collection_start}} (e.g., first dose; or consent for SAEs related to protocol procedures) through {{ae_collection_end}}.
- **Grading.** {{ae_grading_scale}}. **Causality** is assessed by the investigator for each event.
- **SAE reporting.** The investigator reports SAEs to the sponsor-investigator's safety contact within {{sae_reporting_window}} (immediately per 21 CFR 312.64(b)) using [[03-documents/sae-report-investigator-to-sponsor]]. IND safety reports to FDA follow 21 CFR 312.32(c) timelines (7-day for fatal/life-threatening unexpected suspected adverse reactions; 15-day otherwise).
- **Pregnancy.** {{pregnancy_reporting_procedure}} [INSTRUCTION: or "Not applicable."]

### 8.4 Pharmacokinetics
{{pk_assessments}} [INSTRUCTION: or "Not applicable."]

### 8.5 Biomarkers / Pharmacodynamics / Genetics
{{biomarker_assessments}} [INSTRUCTION: or "Not applicable." If future-use specimens are collected, ensure the consent form covers them.]

### 8.6 Other Assessments
{{other_assessments}} [INSTRUCTION: e.g., patient-reported outcomes, health economics; or "Not applicable."]

## 9. STATISTICAL CONSIDERATIONS

{{statistical_section}}

### 9.1 Sample Size Determination
{{sample_size_justification}} [INSTRUCTION: for Phase 1/pilot designs without formal power, state the practical basis (e.g., 3+3 escalation, precision of estimate).]

### 9.2 Analysis Populations
{{analysis_populations}} [INSTRUCTION: e.g., safety population, evaluable population, ITT/mITT as applicable.]

### 9.3 Statistical Analyses
{{statistical_analysis_summary}} [INSTRUCTION: primary and secondary endpoint analysis methods, handling of missing data, multiplicity if any. A separate SAP ([[03-documents/statistical-analysis-plan-ich-e9]]) is finalized before database lock; the SAP elaborates, and may not contradict, this section.]

### 9.4 Interim Analyses
{{interim_analysis_plan}} [INSTRUCTION: or "None planned."]

## 10. GENERAL CONSIDERATIONS: REGULATORY, ETHICAL AND TRIAL OVERSIGHT

### 10.1 Regulatory and Ethical Compliance
The trial will be conducted in accordance with the protocol, ICH E6(R3) GCP, 21 CFR Parts 50, 54, 56, and 312, and applicable state law. The protocol, consent form, and recruitment materials will be approved by {{irb_name}} before any subject is enrolled (21 CFR 312.66).

### 10.2 Informed Consent
Legally effective informed consent will be obtained from each participant (or legally authorized representative) per 21 CFR 50.20-50.27 before any protocol-specific procedure, using the IRB-approved form ([[03-documents/informed-consent-form-part50]]). The consent event is performed by the investigator or a qualified delegated clinician; it is never performed by software.

### 10.3 Data Protection and Confidentiality
{{confidentiality_plan}} [INSTRUCTION: coding of subject identities, who holds the key ([[03-documents/subject-identification-code-list]]), HIPAA authorization, records-access statement for FDA/IRB/sponsor monitors per 21 CFR 312.68.]

### 10.4 Committees
{{oversight_committees}} [INSTRUCTION: DSMB/safety-review committee if any, with cross-reference to its charter; or "Not applicable — safety oversight per Section 7.4 and the Data and Safety Monitoring Plan."]

### 10.5 Data Handling and Record Keeping
Case histories are maintained per 21 CFR 312.62(b) and retained per 21 CFR 312.62(c) (2 years after marketing approval, or 2 years after investigation discontinuation and FDA notification). {{data_management_summary}}

### 10.6 Protocol Amendments and Deviations
Changes to this protocol are made only by formal amendment ([[03-documents/protocol-amendment-change-in-protocol]]) submitted to FDA per 21 CFR 312.30(b) and approved by the IRB before implementation, except where necessary to eliminate an apparent immediate hazard to trial participants. Deviations are documented on the deviation log and reported to the IRB per its policy.

### 10.7 Publication Policy
{{publication_policy}}

## 11. GENERAL CONSIDERATIONS: RISK MANAGEMENT AND QUALITY ASSURANCE

{{quality_management_summary}} [INSTRUCTION: identify the critical-to-quality factors for this trial (ICH E6(R3) 3.10) and the proportionate monitoring approach; cross-reference [[03-documents/risk-based-monitoring-plan]] and [[03-documents/data-safety-monitoring-plan]].]

## 12. APPENDIX: SUPPORTING DETAILS OF TRIAL PROCEDURES
{{procedure_appendices}} [INSTRUCTION: e.g., detailed PK sampling instructions, imaging charter reference; or "Not applicable."]

## 13. APPENDIX: GLOSSARY OF TERMS AND ABBREVIATIONS
{{glossary}}

## 14. APPENDIX: REFERENCES AND VERSION HISTORY

### 14.1 Literature References
{{references}}

### 14.2 Protocol Version History
[INSTRUCTION: One row per version/amendment. Version 1 is the original protocol; each amendment increments the number and states the substantive change and its regulatory handling (21 CFR 312.30(b) submission and IRB approval before implementation).]

| Version | Date | Amendment No. | Summary of change | IRB approval date | FDA submission date |
|---|---|---|---|---|---|
| {{protocol_version}} | {{protocol_date}} | {{amendment_number}} | {{version_change_summary}} | {{irb_approval_date}} | {{fda_submission_date}} |

---

## SIGNATURE PAGE

**Sponsor-Investigator statement.** I have read this protocol and agree that it contains all the information required to conduct this trial. I agree to conduct the trial as described and in compliance with the protocol, ICH E6(R3) GCP, and 21 CFR Parts 50, 54, 56, and 312.

| Role | Name | Signature | Date |
|---|---|---|---|
| Sponsor-Investigator | {{investigator_name}}, {{investigator_degrees}} | ____________________ | ________ |

[INSTRUCTION: The investigator's protocol commitment is also attested on Form FDA 1572 ([[03-documents/form-fda-1572-statement-of-investigator]]), box 9. The signature above is a human act; OSSICRO drafts the protocol but does not sign it.]

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{title}} | study.protocol.title | 21 CFR 312.23(a)(6); ICH M11 |
| {{protocol_number}} | study.protocol.number | 21 CFR 312.23(a)(6); ICH M11 |
| {{protocol_version}} | study.protocol.version | ICH M11 |
| {{protocol_date}} | study.protocol.date | ICH M11 |
| {{amendment_number}} | study.protocol.amendment_number | 21 CFR 312.30(b) |
| {{drug_name}} | study.ip.name | 21 CFR 312.23(a)(6) |
| {{ind_number}} | study.ind.number | 21 CFR 312.23(a)(6) |
| {{investigator_name}} | study.sponsor_investigator.name | 21 CFR 312.23(a)(6) |
| {{investigator_degrees}} | study.sponsor_investigator.degrees | 21 CFR 312.53(c)(2) |
| {{investigator_address}} | study.sponsor_investigator.address | 21 CFR 312.23(a)(6) |
| {{phase}} | study.phase | 21 CFR 312.21 |
| {{nct_number}} | study.registration.nct_number | FDAAA 801; 42 CFR Part 11 |
| {{sponsor_name}} | study.sponsor.name | 21 CFR 312.23(a)(1) |
| {{protocol_synopsis}} | study.protocol.synopsis | ICH M11 §1.1 |
| {{trial_schema}} | study.protocol.schema | ICH M11 §1.2 |
| {{schedule_of_activities}} | study.protocol.soa | ICH M11 §1.3 |
| {{trial_purpose}} | study.protocol.introduction.purpose | ICH M11 §2.1 |
| {{ib_edition}} | study.ib.edition | 21 CFR 312.55 |
| {{benefit_risk_summary}} | study.protocol.benefit_risk | ICH E6(R3) 2.4; ICH M11 §2.2 |
| {{objectives}} | study.protocol.objectives | 21 CFR 312.23(a)(6)(iii)(a) |
| {{primary_objective}} | study.protocol.objectives.primary.objective | ICH M11 §3.1 |
| {{primary_endpoint}} | study.protocol.objectives.primary.endpoint | ICH M11 §3.1 |
| {{primary_estimand}} | study.protocol.objectives.primary.estimand | ICH E9(R1) |
| {{secondary_objectives_endpoints}} | study.protocol.objectives.secondary[] | ICH M11 §3.2 |
| {{exploratory_objectives_endpoints}} | study.protocol.objectives.exploratory[] | ICH M11 §3.3 |
| {{trial_design_description}} | study.protocol.design.description | 21 CFR 312.23(a)(6)(iii)(c); ICH M11 §4.1 |
| {{design_rationale}} | study.protocol.design.rationale | ICH M11 §4.2 |
| {{dose_rationale}} | study.protocol.design.dose_rationale | 21 CFR 312.23(a)(6)(iii)(d); ICH M11 §4.3 |
| {{end_of_trial_definition}} | study.protocol.design.end_of_trial | ICH M11 §4.4 |
| {{planned_enrollment}} | study.protocol.population.planned_enrollment | 21 CFR 312.23(a)(6)(iii)(b) |
| {{number_of_sites}} | study.sites.count | 21 CFR 312.23(a)(6)(iii) |
| {{eligibility_criteria}} | study.protocol.population.criteria | 21 CFR 312.23(a)(6)(iii)(b) |
| {{inclusion_criterion_1}} | study.protocol.population.inclusion[] | 21 CFR 312.23(a)(6)(iii)(b) |
| {{exclusion_criterion_1}} | study.protocol.population.exclusion[] | 21 CFR 312.23(a)(6)(iii)(b) |
| {{lifestyle_restrictions}} | study.protocol.population.lifestyle | ICH M11 §5.3 |
| {{screen_failure_policy}} | study.protocol.population.screen_failure | ICH M11 §5.4 |
| {{dosage_form_strength}} | study.ip.dosage_form_strength | 21 CFR 312.23(a)(6)(iii)(d) |
| {{route_of_administration}} | study.ip.route | ICH M11 §6.1 |
| {{ip_supplier}} | study.ip.supplier | 21 CFR 312.23(a)(7) |
| {{storage_conditions}} | study.ip.storage | ICH E6(R3) Appendix C |
| {{dosing_plan}} | study.protocol.intervention.dosing_plan | 21 CFR 312.23(a)(6)(iii)(d); ICH M11 §6.2 |
| {{ctcae_version}} | study.protocol.safety.ctcae_version | ICH M11 §6.3 |
| {{dose_modification_rules}} | study.protocol.intervention.dose_modification | ICH M11 §6.3 |
| {{blinding_procedures}} | study.protocol.intervention.blinding | ICH M11 §6.4 |
| {{randomization_method}} | study.protocol.intervention.randomization | 21 CFR 312.23(a)(6)(iii)(c); ICH M11 §6.5 |
| {{ip_accountability_summary}} | study.protocol.intervention.accountability | 21 CFR 312.59; 312.62(a) |
| {{compliance_assessment_method}} | study.protocol.intervention.compliance | ICH M11 §6.7 |
| {{permitted_concomitant_meds}} | study.protocol.intervention.concomitant.permitted | ICH M11 §6.8 |
| {{prohibited_concomitant_meds}} | study.protocol.intervention.concomitant.prohibited | ICH M11 §6.8 |
| {{rescue_medication_plan}} | study.protocol.intervention.rescue | ICH M11 §6.8 |
| {{intervention_discontinuation_criteria}} | study.protocol.discontinuation.intervention | ICH M11 §7.1 |
| {{withdrawal_criteria}} | study.protocol.discontinuation.withdrawal | 21 CFR 50.25(a)(8); ICH M11 §7.2 |
| {{lost_to_followup_procedures}} | study.protocol.discontinuation.ltfu | ICH M11 §7.3 |
| {{trial_stopping_criteria}} | study.protocol.discontinuation.stopping_rules | ICH M11 §7.4 |
| {{efficacy_assessments}} | study.protocol.assessments.efficacy | 21 CFR 312.23(a)(6)(iii)(e); ICH M11 §8.1 |
| {{safety_monitoring}} | study.protocol.assessments.safety | 21 CFR 312.23(a)(6)(iii)(g); ICH M11 §8.2 |
| {{ae_collection_start}} | study.protocol.safety.ae_collection.start | 21 CFR 312.32(a) |
| {{ae_collection_end}} | study.protocol.safety.ae_collection.end | 21 CFR 312.32(a) |
| {{ae_grading_scale}} | study.protocol.safety.grading_scale | ICH M11 §8.3 |
| {{sae_reporting_window}} | study.protocol.safety.sae_reporting_window | 21 CFR 312.64(b) |
| {{pregnancy_reporting_procedure}} | study.protocol.safety.pregnancy | ICH M11 §8.3 |
| {{pk_assessments}} | study.protocol.assessments.pk | ICH M11 §8.4 |
| {{biomarker_assessments}} | study.protocol.assessments.biomarker | ICH M11 §8.5 |
| {{other_assessments}} | study.protocol.assessments.other | ICH M11 §8.6 |
| {{statistical_section}} | study.protocol.statistics | 21 CFR 312.23(a)(6)(iii)(h); ICH E9 |
| {{sample_size_justification}} | study.protocol.statistics.sample_size | ICH E9 §3.5 |
| {{analysis_populations}} | study.protocol.statistics.populations | ICH E9 §5.2 |
| {{statistical_analysis_summary}} | study.protocol.statistics.methods | ICH E9 |
| {{interim_analysis_plan}} | study.protocol.statistics.interim | ICH E9 §4.5 |
| {{irb_name}} | study.irb.name | 21 CFR 312.66 |
| {{confidentiality_plan}} | study.protocol.oversight.confidentiality | 21 CFR 312.68 |
| {{oversight_committees}} | study.protocol.oversight.committees | ICH M11 §10.4 |
| {{data_management_summary}} | study.protocol.oversight.data_management | 21 CFR 312.62(b) |
| {{publication_policy}} | study.protocol.oversight.publication | ICH M11 §10.7 |
| {{quality_management_summary}} | study.protocol.quality | ICH E6(R3) 3.10 |
| {{procedure_appendices}} | study.protocol.appendices.procedures | ICH M11 §12 |
| {{glossary}} | study.protocol.appendices.glossary | ICH M11 §13 |
| {{references}} | study.protocol.appendices.references | ICH M11 §14 |
| {{version_change_summary}} | study.protocol.version_history[].summary | 21 CFR 312.30(b) |
| {{irb_approval_date}} | study.protocol.version_history[].irb_approval_date | 21 CFR 312.66 |
| {{fda_submission_date}} | study.protocol.version_history[].fda_submission_date | 21 CFR 312.30(b) |

## Related

- [[03-documents/clinical-protocol-ich-m11-ceshharp]]
- [[03-documents/protocol-synopsis]]
- [[03-documents/protocol-amendment-change-in-protocol]]
- [[03-documents/informed-consent-form-part50]]
- [[03-documents/investigators-brochure]]
- [[03-documents/statistical-analysis-plan-ich-e9]]
- [[03-documents/data-safety-monitoring-plan]]
- [[03-documents/risk-based-monitoring-plan]]
- [[02-lifecycle/pre-ind-and-ind-preparation]]
- [[02-lifecycle/irb-submission-and-approval]]
