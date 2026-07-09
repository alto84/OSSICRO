---
title: "Blank Case Report Form / eCRF"
doc_id: "blank-crf-ecrf"
category: "data"
governing_citations: ["21 CFR 312.62(b)", "ICH E6(R3) Appendix C"]
owner: "sponsor-investigator"
receiver: "site-file"
gate: "none"
status: template
updated: 2026-07-09
---

# Blank Case Report Form / eCRF — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.62(b)](https://www.law.cornell.edu/cfr/text/21/312.62) (investigator recordkeeping — case histories) and [ICH E6(R3)](https://www.ich.org/page/efficacy-guidelines) Appendix C (essential records — a blank/sample CRF is an essential record filed before the trial commences). For electronic CRFs, [21 CFR Part 11](https://www.law.cornell.edu/cfr/text/21/part-11) governs electronic records and signatures. This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The blank Case Report Form (CRF) casebook is the data-collection instrument for the study: it defines every data point captured on each subject, visit by visit, and is filed in the investigator site file / TMF as the reference version against which completed CRFs are checked. Under 21 CFR 312.62(b) the investigator must maintain accurate case histories recording all observations and other data pertinent to the investigation for each subject.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Align every module and visit column with the protocol's schedule of assessments — the CRF must collect exactly what the protocol requires (no less, and no untethered extra data collection). Version-control the casebook: any change after first subject in requires a new CRF version filed alongside the old one.

## Template

---

**CASE REPORT FORM — BLANK CASEBOOK**

| | |
|---|---|
| Protocol number | {{protocol_number}} |
| Protocol title | {{protocol_title}} |
| Investigational product | {{drug_name}} |
| Sponsor-investigator | {{sponsor_investigator_name}} |
| Site | {{site_name}} |
| CRF version / date | {{crf_version}} / {{crf_version_date}} |
| Data capture mode | [INSTRUCTION: state "Paper CRF" or "eCRF in {{edc_system_name}}". If eCRF, confirm the system provides Part 11-compliant audit trails, unique user credentials, and record retention/copies per 21 CFR 11.10.] |

### CRF Completion Conventions

[INSTRUCTION: These conventions appear on the casebook cover and bind all completing staff. Adapt to the EDC system's built-in rules if electronic.]

1. **Attribution.** Entries are made only by staff delegated the task on the Delegation of Authority Log. Paper: complete in indelible ink; each page initialed/dated by the completer. eCRF: entries are made under the user's own login only — credential sharing is prohibited (21 CFR 11.10(d), (g)).
2. **Corrections.** Paper: single line through the erroneous entry (original must remain legible), corrected value, initials, date, and reason if not self-evident. No obliteration, overwriting, or correction fluid. eCRF: corrections via the system audit trail only.
3. **Missing data.** ND = not done; NA = not applicable; UNK = unknown. Never leave a field blank without one of these codes.
4. **Dates** in DD-MMM-YYYY. Partial dates per the completion guideline.
5. **Source.** CRF data must be traceable to source documents except for items pre-designated as "CRF-as-source" in the Source Document Worksheet package / source data location list.

### Subject and Visit Header (repeats on every CRF page/screen)

| Field | Entry |
|---|---|
| Subject ID | {{subject_id_format}} [INSTRUCTION: coded ID only — never name, initials plus full DOB, or other direct identifiers. The link to identity lives solely in the confidential Subject Identification Code List held at the site.] |
| Visit | [INSTRUCTION: visit name/number from the protocol schedule of assessments: {{visit_schedule_reference}}] |
| Visit date | DD-MMM-YYYY |
| Page completed by / date | ______________ / DD-MMM-YYYY |

### Module 1 — Informed Consent Verification

| Field | Entry |
|---|---|
| Written informed consent obtained before any study procedure? | Yes / No [INSTRUCTION: "No" is a reportable deviation — stop and escalate.] |
| Date of consent | DD-MMM-YYYY |
| ICF version consented | ___ |
| HIPAA authorization signed | Yes / No / NA |

### Module 2 — Demographics

Date of birth (or age) · Sex · Race · Ethnicity [INSTRUCTION: use the categories specified in the protocol/SAP; collect DOB only if the source data location list designates it as CRF-collected.]

### Module 3 — Medical History

| Condition (verbatim) | Onset date | Ongoing? (Y/N) | Resolved date |
|---|---|---|---|
| | | | |

### Module 4 — Eligibility

[INSTRUCTION: reproduce every inclusion and exclusion criterion from protocol {{protocol_number}} verbatim, one row each, with Yes/No/NA response and a final investigator eligibility confirmation line (signature/date of the physician-investigator or delegated sub-investigator).]

| # | Criterion (verbatim from protocol) | Met? |
|---|---|---|
| I-1 | | Yes / No |
| E-1 | | Yes / No |

Subject eligible for enrollment: Yes / No — Investigator signature / date: ______________

### Module 5 — Prior and Concomitant Medications

| Medication (generic name) | Indication | Dose / route / frequency | Start date | Stop date or ongoing |
|---|---|---|---|---|
| | | | | |

### Module 6 — Vital Signs / Physical Examination

| Assessment | Result | Units | Clinically significant? |
|---|---|---|---|
| Blood pressure (sitting) | ___/___ | mmHg | Y / N |
| Heart rate | | bpm | Y / N |
| Temperature | | °C | Y / N |
| Weight | | kg | Y / N |
| Physical exam | Normal / Abnormal (describe) | — | Y / N |

[INSTRUCTION: match the vital-sign and exam panel exactly to the protocol schedule of assessments for each visit; delete rows not collected at a given visit.]

### Module 7 — Laboratory Assessments

| Panel | Collected? | Collection date/time | Result location |
|---|---|---|---|
| [INSTRUCTION: list the protocol-required panels, e.g. CBC, CMP, LFTs, urinalysis, pregnancy test] | Y / ND | | Central lab report / local lab report |

### Module 8 — Investigational Product Administration / Exposure

| Field | Entry |
|---|---|
| Product | {{drug_name}} |
| Lot number dispensed | [INSTRUCTION: cross-reference the IP Accountability Log] |
| Dose / route / frequency | per protocol dosing plan |
| Date of first dose (this interval) | DD-MMM-YYYY |
| Date of last dose (this interval) | DD-MMM-YYYY |
| Dose modification / interruption? | Yes / No — if Yes, reason: ______ |
| Compliance assessment | count returned / expected: ___/___ |

### Module 9 — Efficacy / Protocol-Specific Assessments

[INSTRUCTION: one sub-form per protocol-specified endpoint instrument (e.g., seizure diary review, rating scale, imaging assessment). Reproduce the instrument's fields exactly; do not paraphrase validated instruments.]

### Module 10 — Adverse Events

| AE term (verbatim) | Onset date | Resolution date / ongoing | Severity (grade) | Serious? (Y/N) | Relationship to IP | Action taken with IP | Outcome |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

[INSTRUCTION: seriousness and causality entries in this log record the investigator's medical judgment (21 CFR 312.64(b)); OSSICRO never pre-fills them. If Serious = Y, complete the SAE Report to sponsor — see [[03-documents/ind-safety-report]] timelines.]

### Module 11 — Subject Disposition / End of Study

| Field | Entry |
|---|---|
| Completion status | Completed / Discontinued |
| Date of completion or discontinuation | DD-MMM-YYYY |
| Primary reason for discontinuation | AE / withdrawal of consent / lost to follow-up / investigator decision / death / other: ___ |

### Module 12 — Investigator Casebook Signature

I have reviewed this case report form casebook and confirm the data are accurate, complete, and traceable to source records (21 CFR 312.62(b); ICH E6(R3)).

Investigator: {{sponsor_investigator_name}} — Signature: ______________ Date: DD-MMM-YYYY

[INSTRUCTION: for eCRF, this is the electronic casebook signature applied within {{edc_system_name}} under 21 CFR Part 11; the signature manifest must show name, date/time, and meaning of signature (21 CFR 11.50).]

---

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | protocol_number | 21 CFR 312.23(a)(6) |
| {{protocol_title}} | title | ICH E6(R3) Appendix C |
| {{drug_name}} | drug.name | 21 CFR 312.62(b) |
| {{sponsor_investigator_name}} | investigator.name | 21 CFR 312.62(b) |
| {{site_name}} | site.name | ICH E6(R3) Appendix C |
| {{crf_version}} | data.crf_version | ICH E6(R3) Appendix C |
| {{crf_version_date}} | data.crf_version_date | ICH E6(R3) Appendix C |
| {{edc_system_name}} | data.edc_system_name | 21 CFR Part 11 |
| {{subject_id_format}} | data.subject_id_format | 21 CFR 312.62(b) |
| {{visit_schedule_reference}} | existing_documents[clinical-protocol-ich-m11-ceshharp].fields (schedule of assessments) | 21 CFR 312.23(a)(6) |

## Related

- [[03-documents/blank-crf-ecrf]]
- [[03-documents/document-catalog]]
- [[03-documents/conduct-tmf-checklist]]
- [[04-coordination/risk-based-monitoring-e6r3]]
- [[04-coordination/monitoring-workflow-siv-imv-cov]]
