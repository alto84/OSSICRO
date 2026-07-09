---
title: "ClinicalTrials.gov Registration Record"
doc_id: "clinicaltrials-gov-registration-record"
category: "registration"
governing_citations: ["42 CFR Part 11", "FDAAA 801"]
owner: "sponsor-investigator"
receiver: "public-registry"
gate: "none"
status: template
updated: 2026-07-09
---

# ClinicalTrials.gov Registration Record  — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [42 CFR Part 11](https://www.law.cornell.edu/cfr/text/42/part-11) (Clinical Trials Registration and Results Information Submission — the FDAAA 801 final rule, 81 FR 64982, effective 2017-01-18), implementing [FDAAA 801](https://www.govinfo.gov/content/pkg/PLAW-110publ85/pdf/PLAW-110publ85.pdf) (Pub. L. 110-85 § 801), codified at [42 U.S.C. 282(j)](https://www.law.cornell.edu/uscode/text/42/282). Key operative sections: [42 CFR 11.22](https://www.law.cornell.edu/cfr/text/42/11.22) (which trials must be registered), [42 CFR 11.24](https://www.law.cornell.edu/cfr/text/42/11.24) (when — not later than 21 calendar days after enrollment of the first participant), [42 CFR 11.28](https://www.law.cornell.edu/cfr/text/42/11.28) (what — required registration data elements), [42 CFR 11.64](https://www.law.cornell.edu/cfr/text/42/11.64) (updates and corrections), [42 CFR 11.44](https://www.law.cornell.edu/cfr/text/42/11.44) (results submission deadlines). Registry submission portal: [ClinicalTrials.gov PRS](https://register.clinicaltrials.gov/). FDA enforcement context: [FD&C Act § 301(jj)](https://www.law.cornell.edu/uscode/text/21/331) (prohibited acts) and civil money penalties under [FD&C Act § 303(f)(3)](https://www.law.cornell.edu/uscode/text/21/333). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

> [!note] Disambiguation
> "42 CFR Part 11" (this document — ClinicalTrials.gov registration) is distinct from **21 CFR Part 11** (FDA electronic records/electronic signatures). Do not conflate the two when citing.

**Purpose.** This record is the structured data set the responsible party enters into the ClinicalTrials.gov Protocol Registration and Results System (PRS) to register an applicable clinical trial (ACT), due not later than 21 calendar days after enrollment of the first participant (42 CFR 11.24(a)). It is the source document behind the NCT number cited on Form FDA 3674 and in the informed consent form, and it defines the public, legally-audited description of the trial that must be kept current under 42 CFR 11.64.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Field names below track the PRS data-element headings so the completed worksheet can be transcribed directly into PRS. The engine drafts the record; a human with PRS credentials for {{sponsor_name}}'s PRS organization account enters, verifies, and **releases** it — release to the registry is an accountable act of the responsible party, not of software.

## Template

## SECTION A — Applicability and Responsible Party (complete before registering)

### A.1 Applicable Clinical Trial (ACT) determination — 42 CFR 11.22
- **Is this an interventional clinical study of a drug/biologic subject to FDA regulation (other than a Phase 1 study), or of a device (other than a small feasibility study)?** {{act_determination}}   [INSTRUCTION: Apply 42 CFR 11.22(b). For a drug/biologic trial the elements are: interventional; one or more U.S. sites, OR conducted under an IND, OR drug manufactured in and exported from the U.S.; and NOT a Phase 1 trial. A trial conducted under an IND is an ACT even with no U.S. site. Phase 1-only trials are not ACTs (registration is then voluntary but recommended — NIH-funded trials must register regardless under the NIH policy). Record the determination and its basis; this determination is a human regulatory judgment.]
- **Basis for determination:** {{act_determination_basis}}
- **Determined by / date:** {{act_determined_by}}, {{act_determination_date}}

### A.2 Responsible party — 42 CFR 11.4(c), 11.10(a)
- **Responsible party type:** {{responsible_party_type}}   [INSTRUCTION: One of: "Sponsor"; "Principal Investigator" (sponsor-designated PI who is responsible for conducting the trial, has access to and control over the data, and has the right to publish); or "Sponsor-Investigator". For an investigator-initiated IND study, the sponsor-investigator is ordinarily the responsible party.]
- **Responsible party:** {{responsible_party}}
- **Responsible party organizational affiliation:** {{responsible_party_affiliation}}

### A.3 Registration deadline tracking — 42 CFR 11.24(a)
- **Date first participant enrolled (actual or projected):** {{first_enrollment_date}}
- **Registration due date (first enrollment + 21 calendar days):** {{registration_due_date}}
- **Date record released to ClinicalTrials.gov:** {{registration_date}}
- **NCT number assigned:** {{nct_number}}   [INSTRUCTION: Assigned by ClinicalTrials.gov after release and quality review. Propagate the NCT number to Form FDA 3674, the informed consent form, and IND correspondence once assigned.]

---

## SECTION B — Registration Data Elements (42 CFR 11.28(a)(2); PRS field order)

### B.1 Descriptive information — 11.28(a)(2)(i)
- **Brief title:** {{brief_title}}   [INSTRUCTION: Lay-language title, ≤300 characters, intelligible to patients.]
- **Official title:** {{official_title}}   [INSTRUCTION: Must match the protocol title exactly.]
- **Acronym (optional):** {{study_acronym}}
- **Brief summary:** {{brief_summary}}   [INSTRUCTION: Short lay-language description of purpose; ≤5000 characters. No conclusory efficacy claims.]
- **Detailed description (optional):** {{detailed_description}}
- **Primary purpose:** {{primary_purpose}}   [INSTRUCTION: e.g., Treatment, Prevention, Diagnostic, Supportive Care.]
- **Study type:** Interventional   [INSTRUCTION: This template covers interventional ACTs. Observational studies use a different element set.]
- **Study phase:** {{study_phase}}
- **Interventional study model:** {{interventional_model}}   [INSTRUCTION: Single Group, Parallel, Crossover, Factorial, or Sequential.]
- **Number of arms:** {{number_of_arms}}
- **Arm information (title, type, description per arm):** {{arm_information}}
- **Allocation:** {{allocation}}   [INSTRUCTION: Randomized / Nonrandomized / N/A (single-arm).]
- **Masking:** {{masking}}   [INSTRUCTION: None (Open Label), Single, Double, etc.; list who is masked (Participant, Care Provider, Investigator, Outcomes Assessor).]
- **Condition(s) or focus of study:** {{conditions}}
- **Intervention name(s) and description(s):** {{interventions}}   [INSTRUCTION: Use the nonproprietary name if one exists; include dose/regimen at the level in the protocol. Include comparators and placebo as separate interventions.]
- **Study start date (actual or anticipated):** {{study_start_date}}
- **Primary completion date (actual or anticipated):** {{primary_completion_date}}   [INSTRUCTION: Date of final data collection for the primary outcome — this date starts the 1-year results-submission clock under 42 CFR 11.44(a).]
- **Study completion date (actual or anticipated):** {{study_completion_date}}
- **Enrollment (target or actual):** {{enrollment_target}}
- **Primary outcome measure(s) (title, time frame, description):** {{primary_outcome_measures}}   [INSTRUCTION: Must match the protocol/SAP pre-specification. Discrepancies between registered and reported outcomes are a recognized integrity finding.]
- **Secondary outcome measure(s):** {{secondary_outcome_measures}}
- **Eligibility criteria (inclusion/exclusion):** {{eligibility_criteria}}
- **Sex/gender eligible:** {{sex_eligible}}
- **Age limits:** {{minimum_age}} to {{maximum_age}}
- **Accepts healthy volunteers:** {{accepts_healthy_volunteers}}

### B.2 Recruitment information — 11.28(a)(2)(ii)
- **Overall recruitment status:** {{recruitment_status}}   [INSTRUCTION: Not yet recruiting / Recruiting / Enrolling by invitation / Active, not recruiting / Suspended / Terminated / Completed / Withdrawn. Changes must be updated in PRS within 30 calendar days (42 CFR 11.64(a)(1)(ii)).]
- **Why study stopped (if suspended/terminated/withdrawn):** {{why_stopped}}
- **Availability of expanded access:** {{expanded_access_availability}}   [INSTRUCTION: For an investigational drug, state whether expanded access is available; if yes, link/reference the expanded access record NCT number.]

### B.3 Location and contact information — 11.28(a)(2)(iii)
- **Sponsor (lead):** {{sponsor_name}}
- **Collaborators (if any):** {{collaborators}}
- **Central contact (name, phone, email):** {{central_contact}}   [INSTRUCTION: Required while recruiting; this is the contact patients and referring physicians will use.]
- **Overall official (PI) (name, affiliation, role):** {{overall_official}}
- **Facility information (per site: name, city, state, ZIP, country, status, site contact):** {{facility_information}}

### B.4 Administrative data — 11.28(a)(2)(iv)
- **Unique protocol identification number:** {{unique_protocol_id}}
- **Secondary ID(s) (grant numbers, other registry IDs):** {{secondary_ids}}
- **U.S. FDA IND number:** {{ind_number}}   [INSTRUCTION: Enter the IND number and center (CDER/CBER). Marking the record as conducted under an IND makes it an ACT regardless of site location.]
- **Studies a U.S. FDA-regulated drug product:** {{fda_regulated_drug}}
- **Studies a U.S. FDA-regulated device product:** {{fda_regulated_device}}
- **Product manufactured in and exported from the U.S.:** {{us_manufactured_export}}
- **Human subjects protection review board status:** {{irb_status}}   [INSTRUCTION: Submitted / Approved / Exempt, with board name and affiliation. Do not release the record as "Approved" before the IRB approval letter is in hand.]
- **Record verification date:** {{record_verification_date}}   [INSTRUCTION: Must be refreshed at least every 12 months even if nothing changed (42 CFR 11.64(a)(1)(i)).]
- **Responsible party contact (name, title, phone, email):** {{responsible_party_contact}}
- **IPD sharing statement (plan to share individual participant data):** {{ipd_sharing_statement}}   [INSTRUCTION: Yes/No/Undecided plus description; required by the ICMJE and collected by PRS.]

---

## SECTION C — Maintenance obligations (record in study calendar on release)

| Obligation | Trigger | Deadline | Citation |
|---|---|---|---|
| Update any registration data element | Change in the information | At least every 12 months | 42 CFR 11.64(a)(1)(i) |
| Update recruitment status; completion dates; IRB status | Change | Within 30 calendar days | 42 CFR 11.64(a)(1)(ii) |
| Record verification date refresh | Elapsed time | Every 12 months | 42 CFR 11.64(a)(1)(i) |
| Results information submission | Primary completion date | Not later than 1 year after primary completion date (delay/extension per 11.44(b)-(e)) | 42 CFR 11.44 |
| Form FDA 3674 certification | Any FDA submission (IND, amendment, etc.) | With the submission | 42 U.S.C. 282(j)(5)(B) |
| ICF registry statement | Consent of ACT participants | In every ICF | 21 CFR 50.25(c) |

[INSTRUCTION: 21 CFR 50.25(c) requires the exact statement — "A description of this clinical trial will be available on http://www.ClinicalTrials.gov, as required by U.S. Law. This Web site will not include information that can identify you. At most, the Web site will include a summary of the results. You can search this Web site at any time." — verbatim in the ICF of every ACT. Confirm the ICF template carries it.]

> [!warning] Consequences of non-compliance
> Failure to register or update an ACT is a prohibited act under FD&C Act § 301(jj), subject to civil money penalties under § 303(f)(3) (inflation-adjusted, assessed per day after notice), potential NIH grant funding consequences (42 U.S.C. 282(j)(5)(A)(ii)), and ICMJE journals will refuse publication of trials not registered before first enrollment. The 21-day regulatory deadline is later than the ICMJE prospective-registration expectation (register **before** first enrollment) — OSSICRO defaults to the stricter ICMJE timing.

**Prepared by:** {{preparer_name}}, {{preparer_date}}
**Reviewed and released in PRS by (responsible party or delegate with PRS credentials):** _____________________ Date: _________

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{act_determination}} | study.registration.act_determination | 42 CFR 11.22(b) |
| {{act_determination_basis}} | study.registration.act_basis | 42 CFR 11.22(b) |
| {{act_determined_by}} | study.registration.act_determined_by | 42 CFR 11.22 |
| {{act_determination_date}} | study.registration.act_determination_date | 42 CFR 11.22 |
| {{responsible_party_type}} | study.registration.responsible_party_type | 42 CFR 11.10(a) |
| {{responsible_party}} | study.registration.responsible_party | 42 CFR 11.4(c) |
| {{responsible_party_affiliation}} | study.registration.responsible_party_affiliation | 42 CFR 11.28(a)(2)(iv) |
| {{first_enrollment_date}} | study.milestones.first_enrollment_date | 42 CFR 11.24(a) |
| {{registration_due_date}} | computed: first_enrollment_date + 21 days | 42 CFR 11.24(a) |
| {{registration_date}} | study.registration.registration_date | 42 CFR 11.24(a) |
| {{nct_number}} | study.registration.nct_number | 42 CFR 11.28(a); 42 U.S.C. 282(j)(5)(B) |
| {{brief_title}} | study.registration.brief_title | 42 CFR 11.28(a)(2)(i)(A) |
| {{official_title}} | study.protocol.title | 42 CFR 11.28(a)(2)(i)(B) |
| {{study_acronym}} | study.protocol.acronym | 42 CFR 11.28(a)(2)(i) |
| {{brief_summary}} | study.registration.brief_summary | 42 CFR 11.28(a)(2)(i)(C) |
| {{detailed_description}} | study.registration.detailed_description | 42 CFR 11.28(a)(2)(i) |
| {{primary_purpose}} | study.design.primary_purpose | 42 CFR 11.28(a)(2)(i)(E) |
| {{study_phase}} | study.phase | 42 CFR 11.28(a)(2)(i)(F) |
| {{interventional_model}} | study.design.interventional_model | 42 CFR 11.28(a)(2)(i)(D) |
| {{number_of_arms}} | study.design.arms.count | 42 CFR 11.28(a)(2)(i)(H) |
| {{arm_information}} | study.design.arms[] | 42 CFR 11.28(a)(2)(i)(H) |
| {{allocation}} | study.design.allocation | 42 CFR 11.28(a)(2)(i)(D) |
| {{masking}} | study.design.masking | 42 CFR 11.28(a)(2)(i)(D) |
| {{conditions}} | study.condition[] | 42 CFR 11.28(a)(2)(i)(I) |
| {{interventions}} | study.interventions[] | 42 CFR 11.28(a)(2)(i)(J) |
| {{study_start_date}} | study.milestones.start_date | 42 CFR 11.28(a)(2)(i)(L) |
| {{primary_completion_date}} | study.milestones.primary_completion_date | 42 CFR 11.28(a)(2)(i)(M); 11.44(a) |
| {{study_completion_date}} | study.milestones.completion_date | 42 CFR 11.28(a)(2)(i)(N) |
| {{enrollment_target}} | study.design.enrollment_target | 42 CFR 11.28(a)(2)(i)(P) |
| {{primary_outcome_measures}} | study.outcomes.primary[] | 42 CFR 11.28(a)(2)(i)(Q) |
| {{secondary_outcome_measures}} | study.outcomes.secondary[] | 42 CFR 11.28(a)(2)(i)(R) |
| {{eligibility_criteria}} | study.eligibility.criteria | 42 CFR 11.28(a)(2)(ii)(A) |
| {{sex_eligible}} | study.eligibility.sex | 42 CFR 11.28(a)(2)(ii)(B) |
| {{minimum_age}} | study.eligibility.min_age | 42 CFR 11.28(a)(2)(ii)(D) |
| {{maximum_age}} | study.eligibility.max_age | 42 CFR 11.28(a)(2)(ii)(D) |
| {{accepts_healthy_volunteers}} | study.eligibility.healthy_volunteers | 42 CFR 11.28(a)(2)(ii)(C) |
| {{recruitment_status}} | study.registration.recruitment_status | 42 CFR 11.28(a)(2)(ii)(E); 11.64(a)(1)(ii) |
| {{why_stopped}} | study.registration.why_stopped | 42 CFR 11.28(a)(2)(ii)(F) |
| {{expanded_access_availability}} | study.registration.expanded_access | 42 CFR 11.28(a)(2)(ii)(H) |
| {{sponsor_name}} | study.sponsor.name | 42 CFR 11.28(a)(2)(iii)(A) |
| {{collaborators}} | study.sponsor.collaborators[] | 42 CFR 11.28(a)(2)(iii) |
| {{central_contact}} | study.contacts.central | 42 CFR 11.28(a)(2)(iii)(C) |
| {{overall_official}} | study.investigator.name | 42 CFR 11.28(a)(2)(iii)(B) |
| {{facility_information}} | study.sites[] | 42 CFR 11.28(a)(2)(iii)(D) |
| {{unique_protocol_id}} | study.protocol.number | 42 CFR 11.28(a)(2)(iv)(A) |
| {{secondary_ids}} | study.identifiers.secondary[] | 42 CFR 11.28(a)(2)(iv)(B) |
| {{ind_number}} | study.ind.number | 42 CFR 11.28(a)(2)(iv)(C) |
| {{fda_regulated_drug}} | study.registration.fda_regulated_drug | 42 CFR 11.22(b); 11.28(a)(2)(iv) |
| {{fda_regulated_device}} | study.registration.fda_regulated_device | 42 CFR 11.22(b); 11.28(a)(2)(iv) |
| {{us_manufactured_export}} | study.registration.us_manufactured_export | 42 CFR 11.22(b) |
| {{irb_status}} | study.irb.status | 42 CFR 11.28(a)(2)(iv)(E) |
| {{record_verification_date}} | study.registration.record_verification_date | 42 CFR 11.64(a)(1)(i) |
| {{responsible_party_contact}} | study.registration.responsible_party_contact | 42 CFR 11.28(a)(2)(iv)(F) |
| {{ipd_sharing_statement}} | study.registration.ipd_sharing | PRS data element (ICMJE) |
| {{preparer_name}} | engine.preparer | — |
| {{preparer_date}} | engine.prepared_date | — |

## Related
- [[clinicaltrials-gov-registration]]
- [[form-fda-3674-clinicaltrialsgov-certification]]
- [[pre-ind-and-ind-preparation]]
- [[enrollment-and-consent]]
- [[informed-consent-form]]
- [[data-integrations-ctgov-pubmed]]
