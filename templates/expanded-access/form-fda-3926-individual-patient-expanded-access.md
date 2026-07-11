---
title: "Form FDA 3926 - Individual Patient Expanded Access Application"
doc_id: "form-fda-3926-individual-patient-expanded-access"
category: "expanded-access"
governing_citations: ["21 CFR 312.310", "Form FDA 3926"]
owner: "investigator"
receiver: "fda"
gate: "submission-to-fda"
status: template
updated: 2026-07-09
---

# Form FDA 3926 - Individual Patient Expanded Access Application — TEMPLATE (DRAFT for qualified human review)

> [!warning] Legacy paths (Overhaul P4, m5)
> The `## Fields` table below uses this template's ORIGINAL study-record vocabulary, which predates the canonical intake schema. The canonical dotted field ids live in `engine/registry/routes.json`, and the shipped generator is `ea_generators.gen_form_3926`. Key renames: `physician.*` → `investigator.*`; `drug.manufacturer` → `manufacturer.name`; `treatment_plan.dose/route/duration` → `drug.dose/route/duration`; `treatment_plan.monitoring_summary` → `treatment.monitoring_plan`; `patient.initials_coded` → `patient.coded_id`; `drug.loa_reference` → `manufacturer.ind_dmf_reference`; `site.irb.name` → `irb.name`; `submission.type` → computed from `submission.emergency` + `submission.initial_or_followup`. This table's 312.305(b)(2) pinpoints predate the P1/M8 remap — `engine/ossicro/citations.py` is canonical.

> [!authority] Governing authority
> [21 CFR 312.310](https://www.law.cornell.edu/cfr/text/21/312.310) (individual patient expanded access, including emergency use under 312.310(d)); criteria at [21 CFR 312.305(a)](https://www.law.cornell.edu/cfr/text/21/312.305); [Form FDA 3926](https://www.fda.gov/drugs/investigational-new-drug-ind-application/individual-patient-expanded-access-applications-form-fda-3926) (OMB No. 0910-0814). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Form FDA 3926 is the streamlined application a licensed physician uses to request FDA authorization to treat a single patient with an investigational drug outside a clinical trial (individual patient expanded access IND, 21 CFR 312.310). Submitting a completed 3926 with a manufacturer Letter of Authorization opens a new single-patient IND; the physician who submits becomes the sponsor-investigator for that IND. For non-emergency requests, treatment may not begin until 30 days after FDA receives the IND or FDA notifies the physician earlier that treatment may proceed (21 CFR 312.305(d), 312.40(b)); for emergencies, FDA may authorize use by telephone or other rapid means before written submission (21 CFR 312.310(d)).

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. This worksheet mirrors the numbered fields of the official OMB form — transcribe the finalized content onto the current Form FDA 3926 from fda.gov before submission; FDA accepts only the official form (or a full 1571/IND in its place).

## Template

**FORM FDA 3926 — INDIVIDUAL PATIENT EXPANDED ACCESS INVESTIGATIONAL NEW DRUG APPLICATION (IND)**

**1. Date of submission:** {{submission_date}}

**2. Type of submission:** {{submission_type}}
[INSTRUCTION: Check exactly one on the official form: (a) Initial application — request for individual patient expanded access IND; (b) Initial application for EMERGENCY use — treatment already authorized by FDA by telephone per 21 CFR 312.310(d) (state authorization date and the FDA official who authorized); (c) Follow-up submission to an existing individual patient expanded access IND; or (d) Annual report. For (c) or (d), enter the existing IND number: {{ind_number_if_followup}}.]

**3. Patient information and clinical presentation**

- Patient identifier (initials or code — do NOT use name or other direct identifiers): {{patient_initials_coded}}
- Age: {{patient_age}}  Sex: {{patient_sex}}
- Diagnosis / condition: {{diagnosis}}
- Current condition status: {{condition_status}}
  [INSTRUCTION: The condition must be serious or immediately life-threatening (21 CFR 312.305(a)(1)). State stage/severity concisely.]
- Prior therapies and outcomes: {{prior_therapies}}
- Rationale for requesting the investigational drug, including why there is no comparable or satisfactory alternative therapy: {{clinical_rationale}}
  [INSTRUCTION: This is the substantive core of the request under 312.305(a). Address: (1) seriousness of the condition; (2) absence of comparable or satisfactory alternative therapy for this patient (approved therapies exhausted, contraindicated, or unavailable); (3) why the potential benefit justifies the potential risks in the context of this disease.]

**4. Investigational drug**

- Name of investigational drug: {{drug_name}}
- Manufacturer / source: {{manufacturer_name}}

**5. Treatment plan**

{{treatment_plan_summary}}

- Dose: {{dose}}
- Route of administration: {{route}}
- Schedule / frequency: {{schedule}}
- Planned duration of treatment: {{planned_duration}}
- Monitoring for response and adverse events; planned dose modifications: {{monitoring_plan_summary}}
[INSTRUCTION: Keep this to the essentials the form field can hold; attach the full Expanded Access Treatment Plan ([[expanded-access-treatment-plan]]) if more detail is needed.]

**6. Letter of Authorization (LOA)**

- LOA obtained from the manufacturer/sponsor and attached: {{loa_reference}}
[INSTRUCTION: The LOA (21 CFR 312.23(b)) lets FDA cross-reference the manufacturer's IND/NDA/DMF for chemistry, manufacturing, and pharmacology/toxicology information, so the physician need not supply it. Enter the referenced application number(s) as they appear in the LOA. If no LOA is available, the physician must supply the 312.305(b) technical information directly — consult FDA before proceeding.]

**7. Physician's qualification statement**

{{physician_qualifications}}
[INSTRUCTION: Brief statement of training, experience, and licensure establishing the physician is qualified to administer the drug and manage the patient (21 CFR 312.305(c)(1)-(2)); a CV may be attached instead.]

**8. Institutional Review Board (IRB)**

- IRB name: {{irb_name}}
- Request for authorization to obtain IRB chairperson (or designee) concurrence in lieu of full IRB review before treatment begins: {{irb_waiver_requested}}
[INSTRUCTION: Field 10.b on the current form. Checking it requests the streamlined IRB concurrence procedure FDA announced with the October 2017 form revision; the physician remains obligated to obtain IRB review consistent with 21 CFR Part 56 and to obtain informed consent per Part 50. For emergency use, IRB notification within 5 working days applies (21 CFR 56.104(c)).]

**9. Certification statements**

[INSTRUCTION: Do not alter the pre-printed certifications on the official form. By signing, the physician certifies, among other things, that: informed consent will be obtained per 21 CFR Part 50; IRB review and approval per 21 CFR Part 56 will be obtained (or chair concurrence if authorized per field 10.b); treatment will not begin until 30 days after FDA receipt of the IND unless FDA notifies earlier that treatment may proceed (or, for emergencies, that authorization was already obtained); and the physician will comply with the sponsor-investigator responsibilities of 21 CFR 312.305(c) and 312.310, including safety reporting under 21 CFR 312.32 and the summary/annual reporting duty of 21 CFR 312.310(c)(2).]

**10. Physician (requestor / sponsor-investigator)**

- Name: {{physician_name}}
- Address: {{physician_address}}
- Telephone: {{physician_phone}}  Email: {{physician_email}}
- Signature: ______________________________  Date: {{signature_date}}
[INSTRUCTION: Wet or compliant electronic signature of the named physician only. This signature is a personal legal attestation — see gate below.]

> [!warning] Non-delegable
> Submission to FDA is executed by the sponsor-investigator (21 CFR 312.20, 312.23, 312.40; FD&C Act 505(i)) — for a single-patient IND, that is the requesting physician personally. OSSICRO drafts this template; the engine cannot finalize it without a recorded human sign-off, and OSSICRO never transmits anything to FDA.

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{submission_date}} | submission.date | Form FDA 3926 field 1 |
| {{submission_type}} | submission.type | Form FDA 3926 field 2; 21 CFR 312.310(d) |
| {{ind_number_if_followup}} | study.ind_number | Form FDA 3926 field 2 |
| {{patient_initials_coded}} | patient.initials_coded | Form FDA 3926 field 3; 21 CFR 312.310 |
| {{patient_age}} | patient.age | Form FDA 3926 field 3 |
| {{patient_sex}} | patient.sex | Form FDA 3926 field 3 |
| {{diagnosis}} | patient.diagnosis | Form FDA 3926 field 3 |
| {{condition_status}} | patient.condition_status | 21 CFR 312.305(a)(1) |
| {{prior_therapies}} | patient.prior_therapies | 21 CFR 312.305(a)(1)-(2) |
| {{clinical_rationale}} | request.clinical_rationale | 21 CFR 312.305(a); 312.310(a) |
| {{drug_name}} | drug.name | Form FDA 3926 field 4 |
| {{manufacturer_name}} | drug.manufacturer | Form FDA 3926 field 4 |
| {{treatment_plan_summary}} | treatment_plan.summary | 21 CFR 312.305(b)(2)(iii) |
| {{dose}} | treatment_plan.dose | 21 CFR 312.305(b)(2)(iii) |
| {{route}} | treatment_plan.route | 21 CFR 312.305(b)(2)(iii) |
| {{schedule}} | treatment_plan.schedule | 21 CFR 312.305(b)(2)(iii) |
| {{planned_duration}} | treatment_plan.duration | 21 CFR 312.305(b)(2)(iii) |
| {{monitoring_plan_summary}} | treatment_plan.monitoring_summary | 21 CFR 312.305(b)(2)(vii) |
| {{loa_reference}} | drug.loa_reference | 21 CFR 312.23(b) |
| {{physician_qualifications}} | physician.qualifications | 21 CFR 312.305(c)(1)-(2) |
| {{irb_name}} | site.irb.name | 21 CFR Part 56 |
| {{irb_waiver_requested}} | submission.irb_waiver_requested | Form FDA 3926 field 10.b |
| {{physician_name}} | physician.name | Form FDA 3926 field 10 |
| {{physician_address}} | physician.address | Form FDA 3926 field 10 |
| {{physician_phone}} | physician.phone | Form FDA 3926 field 10 |
| {{physician_email}} | physician.email | Form FDA 3926 field 10 |
| {{signature_date}} | submission.signature_date | Form FDA 3926 field 10 |

## Related
- [[03-documents/form-fda-3926-individual-patient-expanded-access]] — wiki document page
- [[expanded-access-treatment-plan]] — the full treatment plan attached to or summarized in field 5
- [[manufacturer-letter-of-authorization]] — the LOA referenced in field 6
- [[informed-consent-form-part50]] — consent obligation certified in field 9
