---
title: "Site Feasibility / Qualification Questionnaire"
doc_id: "site-feasibility-questionnaire"
category: "site-management"
governing_citations: ["21 CFR 312.53(a)", "ICH E6(R3) 3.6"]
owner: "investigator"
receiver: "sponsor"
gate: "none"
status: template
updated: 2026-07-09
---

# Site Feasibility / Qualification Questionnaire — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.53(a)](https://www.law.cornell.edu/cfr/text/21/312.53) (sponsor shall select only investigators qualified by training and experience as appropriate experts to investigate the drug) and [ICH E6(R3) §3.6](https://www.ich.org/page/efficacy-guidelines) (sponsor selection of qualified investigators and sites with adequate resources). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Structured self-assessment completed by a candidate investigator/site and returned to the sponsor, providing the evidentiary basis for the sponsor's investigator-selection decision under 312.53(a). Completed before site selection, usually alongside a confidentiality agreement and protocol synopsis review.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

### A. Site and Investigator Identification

| Field | Value |
|---|---|
| Site name | {{site_name}} |
| Site address | {{site_address}} |
| Proposed Principal Investigator | {{investigator_name}} |
| PI specialty / relevant experience | {{investigator_specialty}} |
| Number of trials conducted as PI (past 5 years) | {{pi_trial_count}} |
| Protocol number / synopsis reviewed | {{protocol_number}} |

### B. Patient Population and Recruitment

| Question | Response |
|---|---|
| Estimated number of patients meeting key eligibility criteria seen at this site per month | {{patient_population}} |
| Primary recruitment sources (clinic, referral network, registry, database) | {{recruitment_sources}} |
| Projected enrollment (subjects/month) | {{projected_enrollment_rate}} |
| Competing studies enrolling from the same population | {{competing_studies}} |

[INSTRUCTION: Base the population estimate on verifiable data (clinic volumes, EHR query, registry counts), not impression. The sponsor may request the basis for the estimate; overstated feasibility is the leading cause of non-enrolling sites.]

### C. Staffing

| Question | Response |
|---|---|
| Sub-investigator(s) available | {{subinvestigators}} |
| Study coordinator support (name/FTE) | {{staffing}} |
| Pharmacist / IP-management support | {{pharmacy_support}} |
| Staff GCP training current | ☐ Yes ☐ No |

### D. Facilities and Equipment

| Question | Response |
|---|---|
| Equipment available for protocol procedures | {{equipment}} |
| Controlled IP storage (temperature-monitored, restricted access) | ☐ Yes ☐ No — describe: {{ip_storage_description}} |
| Specimen processing capability (centrifuge, -20°C / -70°C freezer) | {{specimen_processing_capability}} |
| Clinical laboratory (CLIA-certified) available | ☐ Yes ☐ No |
| Emergency equipment / resuscitation capability | ☐ Yes ☐ No |

### E. Regulatory and Institutional

| Question | Response |
|---|---|
| IRB of record (local or central; typical review timeline) | {{irb_name_and_timeline}} |
| Prior FDA inspection(s); any Form 483, warning letter, or restriction | {{regulatory_history}} |
| PI or site personnel subject to FDA debarment/disqualification proceedings | ☐ No ☐ Yes — explain |
| Contract/budget authority and typical execution timeline | {{contract_timeline}} |

[INSTRUCTION: Regulatory-history disclosure must be complete; the sponsor will verify against FDA's inspection and debarment databases. An affirmative debarment answer does not automatically disqualify the site but requires sponsor legal review.]

### F. Completion

I confirm the information above is accurate to the best of my knowledge and that I have sufficient time to properly conduct and complete the study within the agreed period.

| | |
|---|---|
| Signature (PI) | ______________________ |
| Name (printed) | {{investigator_name}} |
| Date | {{completion_date}} |

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{site_name}} | site.name | 21 CFR 312.53(a) |
| {{site_address}} | site.address | 21 CFR 312.53(a) |
| {{investigator_name}} | site.principal_investigator.name | 21 CFR 312.53(a) |
| {{investigator_specialty}} | site.principal_investigator.specialty | 21 CFR 312.53(a) |
| {{pi_trial_count}} | site.principal_investigator.trial_experience_count | 21 CFR 312.53(a) |
| {{protocol_number}} | study.protocol.number | ICH E6(R3) 3.6 |
| {{patient_population}} | site.feasibility.eligible_patients_per_month | ICH E6(R3) 3.6 |
| {{recruitment_sources}} | site.feasibility.recruitment_sources[] | ICH E6(R3) 3.6 |
| {{projected_enrollment_rate}} | site.feasibility.projected_enrollment_rate | ICH E6(R3) 3.6 |
| {{competing_studies}} | site.feasibility.competing_studies[] | ICH E6(R3) 3.6 |
| {{subinvestigators}} | site.staff[] (role = sub-investigator) | 21 CFR 312.53(a) |
| {{staffing}} | site.feasibility.coordinator_support | ICH E6(R3) 3.6 |
| {{pharmacy_support}} | site.feasibility.pharmacy_support | ICH E6(R3) 3.6 |
| {{equipment}} | site.feasibility.equipment[] | ICH E6(R3) 3.6 |
| {{ip_storage_description}} | site.feasibility.ip_storage | 21 CFR 312.62(a) |
| {{specimen_processing_capability}} | site.feasibility.specimen_processing | ICH E6(R3) 3.6 |
| {{irb_name_and_timeline}} | site.irb.name + site.irb.review_timeline | 21 CFR 56.103 |
| {{regulatory_history}} | site.feasibility.regulatory_history | 21 CFR 312.53(a) |
| {{contract_timeline}} | site.feasibility.contract_timeline | ICH E6(R3) 3.6 |
| {{completion_date}} | site.feasibility.completion_date | ICH E6(R3) 3.6 |

## Related
- [[03-documents/site-feasibility-questionnaire]]
- [[03-documents/site-initiation-visit-report]]
- [[03-documents/investigator-cv-and-qualifications]]
- [[03-documents/clinical-trial-agreement]]
