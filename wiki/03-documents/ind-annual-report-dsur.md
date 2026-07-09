---
title: "IND Annual Report (21 CFR 312.33) and the ICH E2F DSUR"
section: "03-documents"
status: confirmed
governing_authority:
  - "21 CFR 312.33 (IND annual reports)"
  - "ICH E2F (Development Safety Update Report / DSUR)"
  - "FDA guidance accepting the DSUR in lieu of the 312.33 annual report"
tags: [lifecycle/annual, lifecycle/safety, cfr/312, ich/e2f, role/sponsor, role/sponsor-investigator, ossicro/engine, ossicro/gating, status/confirmed]
aliases: ["IND annual report", "312.33", "DSUR", "Development Safety Update Report", "annual report"]
updated: 2026-07-09
---

# IND Annual Report (21 CFR 312.33) and the ICH E2F DSUR

> [!authority] Governing authority
> **21 CFR 312.33** (annual reports) requires the sponsor to submit a brief progress report on the investigation **within 60 days of the anniversary date the IND went into effect**. **ICH E2F** defines the **Development Safety Update Report (DSUR)**, a harmonized annual aggregate safety report FDA accepts *in lieu of* the 312.33 annual report. Status: **Confirmed**. The 312.33 obligation is black-letter; the DSUR substitution is an FDA-accepted option, not a mandate.

The annual report is the sponsor's **periodic accounting to FDA** on a live IND: what studies ran, what the accumulating safety picture is, what changed, and what is planned. It is distinct from the **[[ind-safety-report|expedited IND safety reports]]** (7-/15-day, event-driven under [21 CFR 312.32](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)): the annual report is the *aggregate periodic* rollup, the safety report is the *individual expedited* alert. Both feed the same regulatory relationship and both draw from the same accumulating safety line-listings; OSSICRO assembles the annual report from the safety data it has already structured for expedited reporting.

In the [[sponsor-investigator]] model the annual report is a **self-directed sponsor obligation** with an outward flow to FDA. There is no separate sponsor entity to compile it — the physician who holds the IND owns the report, its content, and its timeliness. This is one of the recurring compliance failure points the literature flags for investigator-sponsors (Kim et al. 2014, PMID 24455986): the 60-day clock is easy to miss when no CRO is watching it. OSSICRO's value here is precisely the clock and the assembly.

## The 312.33 clock

The report is due **within 60 days of the IND anniversary** — the anniversary of the date the IND *went into effect* (i.e., 30 days after FDA received it, or the earlier may-proceed date), not the submission date. OSSICRO computes the anniversary from the IND effective date in the [[data-model]] and drives the deadline through the same milestone tracker that runs the [[safety-clock-engine]] for expedited reports. The annual-report clock is a **hard, recurring, calendar-driven** deadline for the life of the IND; missing it is a compliance deviation, not a safety event, but it is exactly the kind of lapse that draws an FDA information request or, cumulatively, a BIMO finding.

## Required content — 21 CFR 312.33

The regulation enumerates the content directly. Each item below is Confirmed per § 312.33(a)–(g); OSSICRO generates a draft populated from structured study data and holds the safety-characterization judgments for human review.

### (a) Individual study information
For **each study** in progress or completed in the past year: title, purpose, patient-population, and status; total subjects planned; number entered to date; number completed/dropped by reason; and, where available, brief demographic and study-results information. *§ 312.33(a).*

### (b) Summary safety information
The **most frequent** and **most serious** adverse experiences by body system; a summary of all **[[ind-safety-report|IND safety reports]]** submitted during the year; a list of subjects who **died** during participation, with cause; and a list of subjects who **dropped out** in association with any adverse experience, whether or not drug-related. *§ 312.33(b).* This is the aggregate-safety heart of the report.

> [!warning] Non-delegable
> The **characterization** of an adverse experience as "most serious," the **causality context** in the death/dropout narratives, and the sponsor's overall **benefit-risk read** on the accumulating data are medical judgments owned by the [[medical-monitor|medical monitor / sponsor-investigator physician]] (21 CFR 312.32(a), 312.33(b)). OSSICRO tabulates events, computes frequencies, and drafts line-listings from the structured safety data; it must never author the seriousness characterization or the benefit-risk conclusion. The engine surfaces the aggregate; the human interprets and signs. See [[non-delegable-functions-and-gates]].

### (c) A summary of the IND updates
A description of any **general investigational plan** for the coming year (§ 312.23(a)(3)). *§ 312.33(c).*

### (d) IB revisions
If the **[[investigators-brochure|Investigator's Brochure]]** was revised, a description of the revision. *§ 312.33(d).*

### (e) Significant protocol modifications
A description of any **significant Phase 1 protocol modifications** made during the previous year and not previously reported in a [protocol amendment](../02-lifecycle/annual-reporting-and-amendments.md). *§ 312.33(e).*

### (f) Foreign marketing developments
A brief summary of significant **foreign marketing developments** with the drug (e.g., approval or withdrawal in any country). *§ 312.33(f).*

### (g) Outstanding business
A log of any **outstanding business** with FDA the sponsor wants to bring to the agency's attention, e.g., a request for a meeting or a clarification. *§ 312.33(g).*

## The ICH E2F DSUR substitution

FDA accepts the **DSUR** — the ICH E2F harmonized annual safety report — in place of the 312.33 annual report. The DSUR is a more structured, internationally-portable document: one report can satisfy annual-safety-reporting obligations across FDA, EMA, and other ICH regulators for the same development program. Its **Data Lock Point (DLP)** is the anniversary of the **first authorization to conduct a clinical trial** in any country (the "Development International Birth Date," DIBD); the DSUR is due within a defined interval after the DLP. When a sponsor elects the DSUR route for an IND, FDA expects the 60-day 312.33 timing to be met — i.e., the DSUR (or a bridging cover) is submitted to the IND within 60 days of the IND anniversary even though the DSUR's own DLP may be set to the DIBD.

Key structural differences OSSICRO's engine encodes:

| Dimension | 312.33 annual report | ICH E2F DSUR |
|-----------|----------------------|--------------|
| Scope | One IND | Whole development program (all studies, all indications, all regions) |
| Clock anchor | IND effective-date anniversary (+60 days) | Development International Birth Date / DLP |
| Structure | Six enumerated content items | ~20 numbered sections + line-listing appendices |
| Safety framing | Most frequent / most serious; deaths; dropouts | Cumulative + interval; cumulative subject exposure; regional differences; benefit-risk evaluation |
| Portability | US-only | Multi-region (FDA, EMA, PMDA, …) |

For a solo [[sponsor-investigator]] running a **single early-phase US trial**, the plain 312.33 report is usually the lower-burden path; the DSUR earns its overhead when a program spans multiple studies or regions. OSSICRO offers both output modes over the same underlying safety dataset and recommends the 312.33 form as the default for the single-site sponsor-investigator scenario, flagging the DSUR as the choice when a [[pharma-partner-sponsor|pharma partner]] is running a parallel program that expects a harmonized report.

> [!interpretive] OSSICRO position
> OSSICRO builds the annual report **from the accumulated safety line-listings and study-status records already in the trial database** — the same E2B(R3)-structured cases that feed [[form-fda-3500a-medwatch|expedited 3500A reports]]. The "generate" pass instantiates the 312.33 or E2F skeleton and auto-populates the enumerable fields (enrollment counts, event frequencies, list of submitted safety reports, IB-version delta, protocol-amendment log). The "check" pass verifies each § 312.33(a)–(g) item is addressed. The "validate" pass holds the report in a **gated** state until the medical monitor confirms the safety characterization and the sponsor authorizes submission. The engine may compute the clock and draft the tables; it never files, and it never writes the benefit-risk conclusion.

## Relationship to the safety and coordination layer

The annual report is a node in the [[safety-reporting-lifecycle]]: expedited [[ind-safety-report|safety reports]] flow to FDA and investigators *during* the year and are then *summarized* in the annual report (§ 312.33(b)). The report is filed to FDA and copied into the [[regulatory-binder-isf-index|regulatory binder]] (Tab 13). Where a [[dsmb-dmc|DSMB]] operates, its periodic reviews inform — but do not replace — the sponsor's annual-report safety characterization. See [[annual-reporting-and-amendments]] for the amendment interplay and [[safety-reporting-workflow]] for the end-to-end routing.

## Related
- [[ind-safety-report]]
- [[safety-report-timelines-7-15-day]]
- [[safety-reporting-lifecycle]]
- [[safety-reporting-workflow]]
- [[annual-reporting-and-amendments]]
- [[investigators-brochure]]
- [[safety-clock-engine]]
- [[medical-monitor]]
- [[pharmacovigilance-safety]]
- [[regulatory-binder-isf-index]]
- [[non-delegable-functions-and-gates]]

## Sources
- [eCFR — 21 CFR 312.33 (annual reports)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.33)
- [21 CFR 312.33 (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.33)
- [FDA — E2F Development Safety Update Report (guidance, 2011)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e2f-development-safety-update-report) — local: `../../sources/ich/ICH_E2F_DSUR_Guideline.pdf`
- [ICH E2F Development Safety Update Report — Step 4 guideline](https://database.ich.org/sites/default/files/E2F_Guideline.pdf)
- Kim ES et al., investigator-sponsor regulatory-obligation gap — PMID 24455986
