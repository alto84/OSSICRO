---
title: "Expanded Access Treatment Plan"
doc_id: "expanded-access-treatment-plan"
category: "expanded-access"
governing_citations: ["21 CFR 312.305(b)"]
owner: "investigator"
receiver: "fda"
gate: "none"
status: template
updated: 2026-07-09
---

# Expanded Access Treatment Plan — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.305(b)](https://www.law.cornell.edu/cfr/text/21/312.305) (submission requirements for all expanded access uses), read with the criteria of 21 CFR 312.305(a) and, for individual patients, [21 CFR 312.310](https://www.law.cornell.edu/cfr/text/21/312.310); see [FDA expanded access resources](https://www.fda.gov/news-events/public-health-focus/expanded-access). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The treatment plan (in lieu of a clinical protocol) is the clinical core of an expanded access submission: it states the rationale for treatment use, describes the patient, and specifies dosing, administration, monitoring, and safety handling per 21 CFR 312.305(b)(2). It accompanies Form FDA 3926 (or an expanded access IND under Form FDA 1571) and is what the treating physician actually follows at the bedside.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. This template is scoped to individual patient expanded access (312.310); for intermediate-size populations (312.315) or treatment INDs/protocols (312.320), expand the patient-selection section into population eligibility criteria.

## Template

**EXPANDED ACCESS TREATMENT PLAN**

**Drug:** {{drug_name}} | **Physician (sponsor-investigator):** {{physician_name}} | **Plan version/date:** {{plan_version_date}}
**Related submission:** Form FDA 3926 / IND {{ind_number_if_assigned}} | **LOA reference:** {{loa_reference}}

### 1. Rationale for treatment use (21 CFR 312.305(b)(2)(i))

{{treatment_rationale}}

[INSTRUCTION: Address, with relevant clinical detail: (a) the disease or condition and why it is serious or immediately life-threatening for this patient (312.305(a)(1)); (b) the evidence supporting potential benefit of {{drug_name}} in this condition (mechanism, trial data, case experience), sufficient to conclude potential benefit justifies potential risks (312.305(a)(2)); (c) why providing the drug will not interfere with the initiation, conduct, or completion of clinical investigations that could support marketing approval (312.305(a)(3)); (d) for individual patient use, why the patient cannot obtain the drug under another IND or protocol (312.310(a)(2)).]

### 2. Patient description and selection (21 CFR 312.305(b)(2)(ii))

- Patient identifier (coded): {{patient_initials_coded}}
- Diagnosis and disease status: {{diagnosis_and_status}}
- Prior therapies and responses: {{prior_therapies}}
- Comparable or satisfactory alternative therapies considered and why unavailable, exhausted, or unsuitable: {{alternative_therapy_assessment}}
- Relevant comorbidities, organ function, and concomitant medications bearing on risk: {{relevant_comorbidities}}

### 3. Treatment plan: method of administration, dose, and duration (21 CFR 312.305(b)(2)(iii))

{{dosing_plan}}

- Dose and formulation: {{dose_and_formulation}}
- Route and method of administration: {{route_and_method}}
- Schedule: {{schedule}}
- Planned duration of treatment and criteria for continuing beyond the initial course: {{planned_duration}}
- Pre-specified dose modifications for toxicity: {{dose_modification_rules}}
- Criteria for discontinuation (progression, unacceptable toxicity, patient withdrawal): {{stopping_criteria}}

### 4. Facility and personnel (21 CFR 312.305(b)(2)(iv))

- Treatment facility: {{facility_description}}
- Personnel and capabilities available to manage anticipated toxicities (e.g., ICU access, infusion-reaction management): {{facility_capabilities}}

### 5. Chemistry, manufacturing, and controls; pharmacology/toxicology (21 CFR 312.305(b)(2)(v)-(vi))

{{cmc_pharmtox_reference}}

[INSTRUCTION: Where a manufacturer Letter of Authorization is in place, satisfy (v) and (vi) by cross-reference: "CMC and pharmacology/toxicology information is incorporated by reference to {{referenced_application}} per the attached LOA (21 CFR 312.23(b))." Absent an LOA, the physician must supply this information directly — flag for human decision before proceeding.]

### 6. Monitoring plan (21 CFR 312.305(b)(2)(vii))

{{monitoring_plan}}

[INSTRUCTION: Specify, in a schedule-of-assessments style: baseline evaluations; on-treatment clinical and laboratory monitoring with frequencies (e.g., CBC, CMP, vitals, disease assessments); toxicity grading system (e.g., CTCAE v5.0); response assessment method and timing; and follow-up after the last dose.]

| Assessment | Baseline | On treatment (frequency) | End of treatment / follow-up |
|---|---|---|---|
| {{assessment_row_1}} | | | |
| {{assessment_row_2}} | | | |
[INSTRUCTION: One row per assessment; extend as needed.]

### 7. Safety reporting and sponsor-investigator responsibilities (21 CFR 312.305(c), 312.310(c))

- The physician, as sponsor-investigator, will report serious and unexpected suspected adverse reactions to FDA per 21 CFR 312.32 and comply with the investigator responsibilities of 21 CFR 312.60-312.69, including records and drug accountability.
- At the conclusion of treatment (or annually for ongoing use), a written summary of results, including adverse effects, will be provided to FDA per 21 CFR 312.310(c)(2).
- IRB review per 21 CFR Part 56 (or authorized chairperson concurrence) and informed consent per 21 CFR Part 50 will be obtained before treatment begins; for emergency use, the exceptions and 5-working-day notification provisions of 21 CFR 56.104(c) and 50.23 apply as applicable.
- Safety contact: {{safety_contact_name}}, {{safety_contact_phone}}

### 8. Signature

Treating physician (sponsor-investigator): {{physician_name}}

Signature: ______________________________ Date: {{plan_signature_date}}

[INSTRUCTION: The physician signs the plan as the person medically responsible for its execution; the binding regulatory attestations occur on Form FDA 3926 / 1571, not here.]

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{drug_name}} | drug.name | 21 CFR 312.305(b) |
| {{physician_name}} | physician.name | 21 CFR 312.305(c) |
| {{plan_version_date}} | treatment_plan.version_date | ICH E6(R3) 4 (documentation) |
| {{ind_number_if_assigned}} | study.ind_number | 21 CFR 312.310 |
| {{loa_reference}} | drug.loa_reference | 21 CFR 312.23(b) |
| {{treatment_rationale}} | request.clinical_rationale | 21 CFR 312.305(b)(2)(i); 312.305(a) |
| {{patient_initials_coded}} | patient.initials_coded | 21 CFR 312.305(b)(2)(ii) |
| {{diagnosis_and_status}} | patient.diagnosis | 21 CFR 312.305(b)(2)(ii) |
| {{prior_therapies}} | patient.prior_therapies | 21 CFR 312.305(b)(2)(ii) |
| {{alternative_therapy_assessment}} | request.alternative_therapy_assessment | 21 CFR 312.305(a)(1); 312.310(a)(2) |
| {{relevant_comorbidities}} | patient.comorbidities | 21 CFR 312.305(b)(2)(ii) |
| {{dosing_plan}} | treatment_plan.dosing_plan | 21 CFR 312.305(b)(2)(iii) |
| {{dose_and_formulation}} | treatment_plan.dose | 21 CFR 312.305(b)(2)(iii) |
| {{route_and_method}} | treatment_plan.route | 21 CFR 312.305(b)(2)(iii) |
| {{schedule}} | treatment_plan.schedule | 21 CFR 312.305(b)(2)(iii) |
| {{planned_duration}} | treatment_plan.duration | 21 CFR 312.305(b)(2)(iii) |
| {{dose_modification_rules}} | treatment_plan.dose_modifications | 21 CFR 312.305(b)(2)(iii) |
| {{stopping_criteria}} | treatment_plan.stopping_criteria | 21 CFR 312.305(b)(2)(iii) |
| {{facility_description}} | site.facility_description | 21 CFR 312.305(b)(2)(iv) |
| {{facility_capabilities}} | site.facility_capabilities | 21 CFR 312.305(b)(2)(iv) |
| {{cmc_pharmtox_reference}} | drug.cmc_pharmtox_reference | 21 CFR 312.305(b)(2)(v)-(vi) |
| {{referenced_application}} | loa.referenced_file_numbers | 21 CFR 312.23(b) |
| {{monitoring_plan}} | treatment_plan.monitoring_plan | 21 CFR 312.305(b)(2)(vii) |
| {{assessment_row_1}} | treatment_plan.assessments[0] | 21 CFR 312.305(b)(2)(vii) |
| {{assessment_row_2}} | treatment_plan.assessments[1] | 21 CFR 312.305(b)(2)(vii) |
| {{safety_contact_name}} | physician.safety_contact.name | 21 CFR 312.32 |
| {{safety_contact_phone}} | physician.safety_contact.phone | 21 CFR 312.32 |
| {{plan_signature_date}} | treatment_plan.signature_date | — |

## Related
- [[03-documents/expanded-access-treatment-plan]] — wiki document page
- [[form-fda-3926-individual-patient-expanded-access]] — the application this plan accompanies
- [[manufacturer-letter-of-authorization]] — supplies the section-5 cross-reference
- [[informed-consent-form-part50]] — consent obligation before treatment begins
