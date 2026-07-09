---
title: "Source Document Worksheet Templates"
doc_id: "source-document-worksheet-templates"
category: "data"
governing_citations: ["21 CFR 312.62(b)", "ICH E6(R3) 4 (ALCOA++)"]
owner: "investigator"
receiver: "site-file"
gate: "none"
status: template
updated: 2026-07-09
---

# Source Document Worksheet Templates — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.62(b)](https://www.law.cornell.edu/cfr/text/21/312.62) (accurate case histories recording all observations) and [ICH E6(R3)](https://www.ich.org/page/efficacy-guidelines) Section 4 (data governance) — source data must be attributable, legible, contemporaneous, original, and accurate (ALCOA), and additionally complete, consistent, enduring, and available (ALCOA++). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Source document worksheets are the site's structured forms for capturing original observations at each study visit — the source records from which CRF/eCRF entries are transcribed and against which monitors verify data. This package defines the worksheet set for the study, the source data location list (what counts as source for each data element), and the entry/correction conventions that keep the records ALCOA++-compliant.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Build one worksheet per visit in the protocol's schedule of assessments, capturing every protocol-required data element for that visit. Finalize the source data location list before first subject in; monitors and inspectors will hold the site to it.

## Template

---

**SOURCE DOCUMENT WORKSHEET PACKAGE**

| | |
|---|---|
| Protocol number | {{protocol_number}} |
| Protocol title | {{protocol_title}} |
| Protocol version keyed to | {{protocol_version}} |
| Site | {{site_name}} |
| Investigator | {{investigator_name}} |
| Package version / effective date | {{worksheet_package_version}} / {{effective_date}} |

### Section 1 — Worksheet Inventory

[INSTRUCTION: enumerate every worksheet in the package — typically one per scheduled visit plus event-driven worksheets (unscheduled visit, AE assessment, early termination). This list is {{worksheet_list}}.]

| # | Worksheet | Visit / trigger | Version |
|---|---|---|---|
| 1 | Screening visit worksheet | Screening | |
| 2 | Baseline / enrollment worksheet | Baseline | |
| 3 | Treatment visit worksheet | [INSTRUCTION: one row per treatment visit or one reusable worksheet with visit checkbox] | |
| 4 | Unscheduled visit worksheet | As needed | |
| 5 | Adverse event assessment worksheet | AE identified | |
| 6 | End-of-study / early termination worksheet | Final visit | |

### Section 2 — Source Data Location List

[INSTRUCTION: for each data element, designate the ORIGINAL source. Anything designated "eCRF direct entry" has no upstream source and the eCRF IS the source — designate sparingly and only where no prior record naturally exists (e.g., some questionnaire responses). This list is {{source_data_location_list}}. Monitors verify CRF data against exactly these locations.]

| Data element | Source location |
|---|---|
| Informed consent | Signed ICF (original, in site file) |
| Demographics, medical history | Clinic/EMR record; this worksheet |
| Eligibility assessments | This worksheet + supporting lab/EMR records |
| Vital signs, physical exam | This worksheet |
| Laboratory results | Lab report ({{clinical_lab_name}}) |
| IP dosing and accountability | IP Accountability Log; this worksheet |
| Adverse events | This worksheet; EMR where care was delivered |
| Protocol-specific instruments | [INSTRUCTION: e.g., subject diary (subject-completed = source), rating scale worksheet] |

### Section 3 — Entry and Correction Conventions (ALCOA++)

All staff completing worksheets are trained on and bound by:

1. **Attributable.** Every entry signed or initialed and dated by the person who made the observation; that person holds the corresponding task on the Delegation of Authority Log.
2. **Legible / Original / Contemporaneous.** Indelible ink; recorded at the time of the observation, never back-filled from memory; the worksheet is the first place the observation is written down.
3. **Accurate / Complete / Consistent.** No blank fields — use ND / NA / UNK; dates DD-MMM-YYYY; units stated.
4. **Corrections.** Single line through the error (original remains legible), corrected entry, initials, date, and reason if not self-evident. No obliteration or correction fluid. A late entry is marked "late entry," dated the day written, and states the date of the actual observation.
5. **Enduring / Available.** Completed worksheets file in the subject's source binder, retained per the record-retention statement (21 CFR 312.62(c)), and are available for monitoring, audit, and FDA inspection (21 CFR 312.68).

### Section 4 — Generic Visit Worksheet Skeleton

[INSTRUCTION: instantiate this skeleton once per visit, adding/removing assessment blocks to mirror the schedule of assessments for that visit exactly.]

**{{protocol_number}} — {{visit_name}} Source Worksheet** (visit window: {{visit_window}})

| Field | Entry |
|---|---|
| Subject ID (coded) | ______ [INSTRUCTION: no direct identifiers on worksheets that leave the site or are copied for monitoring] |
| Visit date | DD-MMM-YYYY |
| Informed consent in place and current version? | Yes / No |
| Interval history since last visit | [free text] |
| Adverse events since last visit? | Yes (complete AE worksheet) / No |
| Concomitant medication changes? | Yes (record) / No |
| Vital signs | BP ___/___ mmHg · HR ___ bpm · Temp ___ °C · Weight ___ kg |
| Protocol assessments performed this visit | [INSTRUCTION: checklist from schedule of assessments — labs drawn (time), instruments administered, IP dispensed/returned with quantities] |
| IP dispensed / returned | Lot ______ · Qty dispensed ___ · Qty returned ___ (cross-entered on IP Accountability Log) |
| Deviations this visit? | Yes (record on Protocol Deviation Log) / No |
| Next visit scheduled | DD-MMM-YYYY |
| Completed by (signature/date) | ______________ / DD-MMM-YYYY |
| Investigator review (signature/date) | ______________ / DD-MMM-YYYY [INSTRUCTION: physician review required for medical assessments — eligibility, AE severity/causality, dose decisions] |

---

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | protocol_number | 21 CFR 312.62(b) |
| {{protocol_title}} | title | ICH E6(R3) Appendix C |
| {{protocol_version}} | protocol_version | ICH E6(R3) Appendix C |
| {{site_name}} | site.name | ICH E6(R3) Appendix C |
| {{investigator_name}} | investigator.name | 21 CFR 312.62(b) |
| {{clinical_lab_name}} | site.clinical_lab.name | 42 CFR Part 493 |
| {{worksheet_list}} | data.worksheet_list | 21 CFR 312.62(b) |
| {{worksheet_package_version}} | data.worksheet_package_version | ICH E6(R3) Appendix C |
| {{effective_date}} | data.worksheets_effective_date | ICH E6(R3) Appendix C |
| {{source_data_location_list}} | data.source_data_location_list | ICH E6(R3) 4 |
| {{visit_name}} / {{visit_window}} | existing_documents[clinical-protocol-ich-m11-ceshharp].fields (schedule of assessments) | 21 CFR 312.23(a)(6) |

## Related

- [[03-documents/source-document-worksheet-templates]]
- [[03-documents/document-catalog]]
- [[03-documents/conduct-tmf-checklist]]
- [[03-documents/delegation-of-authority-log]]
- [[04-coordination/risk-based-monitoring-e6r3]]
