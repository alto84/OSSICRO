---
title: "IND Annual Report"
doc_id: "ind-annual-report-312-33"
category: "ind-application"
governing_citations: ["21 CFR 312.33", "ICH E2F (DSUR accepted alternative)"]
owner: "sponsor-investigator"
receiver: "fda"
gate: "submission-to-fda"
status: template
updated: 2026-07-09
---

# IND Annual Report  — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.33](https://www.law.cornell.edu/cfr/text/21/312.33) (IND annual reports) — a brief progress report due **within 60 days of the anniversary date the IND went into effect**. [ICH E2F](https://database.ich.org/sites/default/files/E2F_Guideline.pdf) (Development Safety Update Report, DSUR) is an FDA-accepted alternative to the 312.33 annual report. This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The annual report is the sponsor's periodic accounting to FDA on a live IND: what studies ran, the accumulating safety picture, what changed, and what is planned. It is distinct from the event-driven expedited [[ind-safety-report-7-15-day|IND safety reports]] (7-/15-day, 21 CFR 312.32); the annual report is the aggregate periodic rollup.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. In the sponsor-investigator model there is no separate sponsor entity — the physician who holds the IND owns the report and its 60-day clock.

## Template

[INSTRUCTION: Transmitted to FDA under a signed Form FDA 1571 as a numbered serial submission. The report is due within 60 days of the anniversary of the date the IND went into effect (30 days after FDA receipt, or the earlier may-proceed date) — not the submission date.]

**{{sponsor_name}}**
**IND Annual Report — 21 CFR 312.33**

- **IND Number:** {{ind_number}}
- **Serial Number:** {{serial_number}}
- **Drug/Biologic:** {{drug_name}}
- **IND effective date:** {{ind_effective_date}}
- **Reporting period (anniversary year):** {{reporting_period}}
- **Report due date (anniversary + 60 days):** {{report_due_date}}

### (a) Individual study information — 21 CFR 312.33(a)
{{study_status_summary}}
[INSTRUCTION: For EACH study in progress or completed during the past year, provide: title, purpose, patient population, and status; total number of subjects planned; number entered to date; number who completed as planned; number who dropped out (by reason where available); and, where available, brief demographic and study-results information.]

| Study | Purpose | Status | Planned N | Entered | Completed | Discontinued (reason) |
|---|---|---|---|---|---|---|
| {{study_title}} | {{study_purpose}} | {{study_status}} | {{planned_n}} | {{entered_n}} | {{completed_n}} | {{discontinued_n}} |

### (b) Summary safety information — 21 CFR 312.33(b)
{{safety_summary}}
[INSTRUCTION: Provide the aggregate-safety heart of the report: (i) a narrative or tabular summary of the most frequent and most serious adverse experiences by body system; (ii) a summary of all IND safety reports submitted during the year; (iii) a list of subjects who died during participation, with the cause of death for each; and (iv) a list of subjects who dropped out in association with any adverse experience, whether or not drug-related.]

- **Most frequent / most serious adverse experiences (by body system):** {{ae_summary}}
- **IND safety reports submitted this period:** {{safety_reports_list}}
- **Deaths during participation (with cause):** {{deaths_list}}
- **Dropouts associated with an adverse experience:** {{ae_dropouts_list}}

### (c) General investigational plan for the coming year — 21 CFR 312.33(c)
{{updated_investigational_plan}}
[INSTRUCTION: Describe the general investigational plan for the coming year (per 21 CFR 312.23(a)(3)(iv)).]

### (d) Investigator's Brochure revisions — 21 CFR 312.33(d)
{{ib_revisions}}
[INSTRUCTION: If the Investigator's Brochure was revised during the period, describe the revision. Write "No revision during this reporting period" if unchanged.]

### (e) Significant Phase 1 protocol modifications — 21 CFR 312.33(e)
{{protocol_modifications}}
[INSTRUCTION: Describe any significant Phase 1 protocol modifications made during the previous year and not previously reported in a protocol amendment. Write "None" if not applicable.]

### (f) Foreign marketing developments — 21 CFR 312.33(f)
{{foreign_marketing_developments}}
[INSTRUCTION: Briefly summarize significant foreign marketing developments (e.g., approval or withdrawal in any country). Write "None" if not applicable.]

### (g) Outstanding business — 21 CFR 312.33(g)
{{outstanding_business}}
[INSTRUCTION: Log any outstanding business with FDA the sponsor wishes to bring to the agency's attention (e.g., a meeting request or a clarification). Write "None" if not applicable.]

> [!note] DSUR alternative (ICH E2F)
> FDA accepts the ICH E2F Development Safety Update Report (DSUR) in place of the 312.33 annual report. The DSUR is a more structured, internationally portable report keyed to the Development International Birth Date (DIBD) / Data Lock Point; when elected, the DSUR (or a bridging cover) must still meet the 60-day 312.33 timing to the IND. For a solo sponsor-investigator running a single early-phase US trial, the plain 312.33 report is usually the lower-burden path.

> [!warning] Non-delegable
> Submission to FDA is executed by the sponsor-investigator (21 CFR 312.20, 312.23, 312.33, 312.40; FD&C Act 505(i)). Separately, the **characterization** of an adverse experience as "most serious," the causality context in death/dropout narratives, and the overall benefit-risk read are medical judgments owned by the [[medical-monitor|medical monitor / sponsor-investigator physician]] (21 CFR 312.32(a)). OSSICRO tabulates events, computes frequencies, drafts line-listings, and tracks the 60-day clock; the engine cannot finalize the report without a recorded human sign-off and never authors the seriousness characterization or the benefit-risk conclusion.

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{sponsor_name}} | study.sponsor.name | 21 CFR 312.33 |
| {{ind_number}} | study.ind.number | 21 CFR 312.33 |
| {{serial_number}} | annual_report.serial_number | 21 CFR 312.23(d) |
| {{drug_name}} | study.drug.name | 21 CFR 312.33 |
| {{ind_effective_date}} | study.ind.effective_date | 21 CFR 312.33 |
| {{reporting_period}} | annual_report.reporting_period | 21 CFR 312.33 |
| {{report_due_date}} | annual_report.due_date | 21 CFR 312.33 |
| {{study_status_summary}} | annual_report.studies[] | 21 CFR 312.33(a) |
| {{study_title}} | annual_report.studies[].title | 21 CFR 312.33(a) |
| {{study_purpose}} | annual_report.studies[].purpose | 21 CFR 312.33(a) |
| {{study_status}} | annual_report.studies[].status | 21 CFR 312.33(a) |
| {{planned_n}} | annual_report.studies[].planned_n | 21 CFR 312.33(a) |
| {{entered_n}} | annual_report.studies[].entered_n | 21 CFR 312.33(a) |
| {{completed_n}} | annual_report.studies[].completed_n | 21 CFR 312.33(a) |
| {{discontinued_n}} | annual_report.studies[].discontinued_n | 21 CFR 312.33(a) |
| {{safety_summary}} | annual_report.safety_summary | 21 CFR 312.33(b) |
| {{ae_summary}} | annual_report.ae_summary | 21 CFR 312.33(b) |
| {{safety_reports_list}} | annual_report.safety_reports[] | 21 CFR 312.33(b) |
| {{deaths_list}} | annual_report.deaths[] | 21 CFR 312.33(b) |
| {{ae_dropouts_list}} | annual_report.ae_dropouts[] | 21 CFR 312.33(b) |
| {{updated_investigational_plan}} | annual_report.investigational_plan | 21 CFR 312.33(c) |
| {{ib_revisions}} | annual_report.ib_revisions | 21 CFR 312.33(d) |
| {{protocol_modifications}} | annual_report.protocol_modifications | 21 CFR 312.33(e) |
| {{foreign_marketing_developments}} | annual_report.foreign_marketing | 21 CFR 312.33(f) |
| {{outstanding_business}} | annual_report.outstanding_business | 21 CFR 312.33(g) |

## Related
- [[ind-annual-report-dsur]]
- [[ind-application-312-23]]
- [[ind-safety-report-7-15-day]]
- [[investigators-brochure]]
- [[information-amendment]]
- [[protocol-amendment-change-in-protocol]]
- [[annual-reporting-and-amendments]]
- [[safety-reporting-lifecycle]]
- [[medical-monitor]]
- [[non-delegable-functions-and-gates]]
