---
title: "Investigator CV, Medical License, and GCP Training"
doc_id: "investigator-cv-and-qualifications"
category: "site-management"
governing_citations: ["21 CFR 312.53(c)(2)", "ICH E6(R3) 2.1"]
owner: "investigator"
receiver: "sponsor"
gate: "none"
status: template
updated: 2026-07-09
---

# Investigator CV, Medical License, and GCP Training — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.53(c)(2)](https://www.law.cornell.edu/cfr/text/21/312.53) (before investigation begins, sponsor obtains a curriculum vitae or other statement of qualifications showing the investigator's education, training, and experience) and [ICH E6(R3) §2.1](https://www.ich.org/page/efficacy-guidelines) (investigator qualified by education, training, and experience; evidence provided via current CV and/or other relevant documentation). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Qualification packet cover sheet assembling the investigator's curriculum vitae, medical licensure, and GCP training evidence into a single dated, signed record demonstrating the investigator is qualified to conduct the study. Prepared at site startup for submission to the sponsor and filed in the Investigator Site File; refreshed when any component expires or materially changes.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

### Investigator Qualification Summary

| Field | Value |
|---|---|
| Investigator name | {{investigator_name}} |
| Degrees / credentials | {{education_degrees}} |
| Role on study | {{study_role}} |
| Protocol number | {{protocol_number}} |
| Site name | {{site_name}} |

### 1. Curriculum Vitae

| Field | Value |
|---|---|
| CV date (signed/dated by investigator) | {{cv_date}} |
| Attached | ☐ Yes |

[INSTRUCTION: Attach the current CV. The CV must be signed and dated by the investigator; many sponsors require the CV to be dated within 2 years of site activation — confirm the sponsor's currency requirement. The CV must substantiate qualifications relevant to this protocol (specialty, research experience). 21 CFR 312.53(c)(2) permits "other statement of qualifications" in lieu of a CV; if used, substitute it here and label accordingly.]

### 2. Medical License

| Field | Value |
|---|---|
| License number | {{license_number}} |
| Issuing state / jurisdiction | {{license_state}} |
| Expiration date | {{license_expiration_date}} |
| Copy attached | ☐ Yes |

[INSTRUCTION: Attach a copy of the current, unrestricted license (or verification printout from the state board). The license must be active in the jurisdiction where the investigator will perform study procedures. If the license expires during the study, calendar a refresh and file the renewed license upon issuance. Disclose any restrictions, board actions, or FDA disqualification/debarment proceedings to the sponsor.]

### 3. GCP Training

| Field | Value |
|---|---|
| Training program / provider | {{gcp_training_provider}} |
| Completion date | {{gcp_training_date}} |
| Certificate attached | ☐ Yes |

[INSTRUCTION: Attach the completion certificate. GCP training should be current per sponsor SOP (commonly a 3-year refresh cycle) and should cover ICH E6(R3). Record protocol-specific training separately on the site training log.]

### Investigator Attestation

I certify that the attached curriculum vitae, licensure documentation, and training records are current and accurate, and that I am qualified by education, training, and experience to assume responsibility for the proper conduct of this study (21 CFR 312.53(c)(2); ICH E6(R3) 2.1).

| | |
|---|---|
| Signature | ______________________ |
| Name (printed) | {{investigator_name}} |
| Date | ______________________ |

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{investigator_name}} | site.principal_investigator.name | 21 CFR 312.53(c)(2) |
| {{education_degrees}} | site.principal_investigator.degrees | 21 CFR 312.53(c)(2) |
| {{study_role}} | site.principal_investigator.study_role | ICH E6(R3) 2.1 |
| {{protocol_number}} | study.protocol.number | ICH E6(R3) Appendix C |
| {{site_name}} | site.name | ICH E6(R3) Appendix C |
| {{cv_date}} | site.principal_investigator.cv_date | 21 CFR 312.53(c)(2) |
| {{license_number}} | site.principal_investigator.license.number | ICH E6(R3) 2.1 |
| {{license_state}} | site.principal_investigator.license.state | ICH E6(R3) 2.1 |
| {{license_expiration_date}} | site.principal_investigator.license.expiration | ICH E6(R3) 2.1 |
| {{gcp_training_provider}} | site.principal_investigator.gcp_training.provider | ICH E6(R3) 2.1 |
| {{gcp_training_date}} | site.principal_investigator.gcp_training.date | ICH E6(R3) 2.1 |

## Related
- [[03-documents/investigator-cv-and-qualifications]]
- [[03-documents/form-fda-1572-statement-of-investigator]]
- [[03-documents/delegation-of-authority-log]]
