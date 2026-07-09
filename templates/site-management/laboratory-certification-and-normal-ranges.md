---
title: "Laboratory Certification (CLIA/CAP) and Normal Ranges"
doc_id: "laboratory-certification-and-normal-ranges"
category: "site-management"
governing_citations: ["42 CFR Part 493 (CLIA)", "ICH E6(R3) Appendix C"]
owner: "investigator"
receiver: "sponsor"
gate: "none"
status: template
updated: 2026-07-09
---

# Laboratory Certification (CLIA/CAP) and Normal Ranges — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [42 CFR Part 493](https://www.law.cornell.edu/cfr/text/42/part-493) (Clinical Laboratory Improvement Amendments — laboratory requirements) and [ICH E6(R3) Appendix C](https://www.ich.org/page/efficacy-guidelines) (essential records — documentation of laboratory certification/accreditation and normal values/ranges for medical/laboratory/technical procedures included in the protocol). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Documents that each laboratory performing protocol-required tests is currently certified/accredited and records the version and effective dates of its reference (normal) ranges, so laboratory results in the trial record can be interpreted against the correct ranges. Established at startup for each lab used; refreshed on certificate expiry or any reference-range change.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

### Study Identification

| Field | Value |
|---|---|
| Protocol number | {{protocol_number}} |
| Site name | {{site_name}} |

### Laboratory Identification

| Field | Value |
|---|---|
| Laboratory name | {{lab_name}} |
| Laboratory address | {{lab_address}} |
| Laboratory director | {{lab_director_name}} |
| Tests performed for this protocol | {{tests_performed}} |

[INSTRUCTION: Complete one copy of this record for EACH laboratory performing protocol-required testing (local site lab, central lab, specialty lab). This laboratory must match a facility listed in Item 4 of the investigator's Form FDA 1572.]

### Certification / Accreditation

| Field | Value |
|---|---|
| CLIA certificate number | {{clia_number}} |
| CLIA certificate type | {{clia_certificate_type}} |
| CLIA certificate expiration | {{certification_expiry}} |
| CAP accreditation number (if applicable) | {{cap_number}} |
| CAP accreditation expiration (if applicable) | {{cap_expiry}} |
| Copies of certificates attached | ☐ CLIA ☐ CAP |

[INSTRUCTION: CLIA certificate type is one of: Certificate of Waiver, Certificate of Compliance, Certificate of Accreditation, Certificate for Provider-Performed Microscopy. The certificate type must cover the complexity level of the tests performed for this protocol (42 CFR 493.5, 493.20, 493.25). Attach current certificates. Calendar renewals: an expired certificate during the conduct period is a reportable quality event to the sponsor.]

### Normal (Reference) Ranges

| Field | Value |
|---|---|
| Reference ranges document version | {{normal_ranges_version}} |
| Effective date | {{normal_ranges_effective_date}} |
| Signed by laboratory director | ☐ Yes |
| Attached | ☐ Yes |

[INSTRUCTION: Attach the laboratory's current reference-range document covering every analyte in the protocol's schedule of assessments, including age- and sex-specific ranges where applicable. When the lab updates any range mid-study, obtain the new version, record its effective date, retain BOTH versions in the site file, and notify the sponsor/data management so results are interpreted against the range in effect on the collection date.]

### Investigator Acknowledgment

| | |
|---|---|
| Signature (PI or designee per delegation log) | ______________________ |
| Name (printed) | {{acknowledging_staff_name}} |
| Date | ______________________ |

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | study.protocol.number | ICH E6(R3) Appendix C |
| {{site_name}} | site.name | ICH E6(R3) Appendix C |
| {{lab_name}} | site.laboratories[].name | ICH E6(R3) Appendix C |
| {{lab_address}} | site.laboratories[].address | 21 CFR 312.53(c)(1) (1572 Item 4) |
| {{lab_director_name}} | site.laboratories[].director | 42 CFR 493.1403 |
| {{tests_performed}} | site.laboratories[].protocol_tests[] | ICH E6(R3) Appendix C |
| {{clia_number}} | site.laboratories[].clia.number | 42 CFR Part 493 |
| {{clia_certificate_type}} | site.laboratories[].clia.certificate_type | 42 CFR 493.5 |
| {{certification_expiry}} | site.laboratories[].clia.expiration | 42 CFR Part 493 |
| {{cap_number}} | site.laboratories[].cap.number | 42 CFR 493.551 (accreditation) |
| {{cap_expiry}} | site.laboratories[].cap.expiration | 42 CFR 493.551 (accreditation) |
| {{normal_ranges_version}} | site.laboratories[].reference_ranges.version | ICH E6(R3) Appendix C |
| {{normal_ranges_effective_date}} | site.laboratories[].reference_ranges.effective_date | ICH E6(R3) Appendix C |
| {{acknowledging_staff_name}} | site.staff[].name | ICH E6(R3) 2.7 |

## Related
- [[03-documents/laboratory-certification-and-normal-ranges]]
- [[03-documents/form-fda-1572-statement-of-investigator]]
- [[03-documents/regulatory-binder-isf-index]]
