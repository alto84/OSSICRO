---
title: "IND Safety Report — 7-Day and 15-Day Expedited Reporting (21 CFR 312.32)"
section: "03-documents"
status: confirmed
governing_authority:
  - "21 CFR 312.32 (IND safety reporting)"
  - "Federal Register 75 FR 59935 (Sept 29 2010) — IND Safety Reporting Final Rule"
  - "ICH E2A (definitions/expedited-reporting framework); FDA IND safety-reporting guidance"
tags: [lifecycle/safety, cfr/312, ich/e2a, fda-form/3500a, role/sponsor, role/sponsor-investigator, role/medical-monitor, role/pharmacovigilance-safety, ossicro/gating, status/confirmed]
aliases: ["IND safety report", "312.32", "SUSAR", "7-day report", "15-day report", "expedited safety report"]
updated: 2026-07-09
---

# IND Safety Report — 7-Day and 15-Day Expedited Reporting (21 CFR 312.32)

> [!authority] Governing authority
> **21 CFR 312.32** (IND safety reporting), as established by the **IND Safety Reporting Final Rule, 75 FR 59935 (Sept 29 2010)**. Definitions at § 312.32(a); reporting obligations at § 312.32(c); review duty at § 312.32(b); format at § 312.32(c) (narrative or **[[form-fda-3500a-medwatch|Form FDA 3500A]]** / electronic ICSR). Harmonized with **ICH E2A**. Status: **Confirmed** — this is black-letter FDA expedited-safety-reporting law.

An **IND safety report** is the sponsor's expedited alert to FDA (and to all participating investigators) when accumulating safety information crosses a defined threshold. Two clocks govern it: a **15-calendar-day** report for a suspected adverse reaction that is **serious and unexpected**, and a **7-calendar-day** report for one that is **unexpected, fatal or life-threatening**. The report is event-driven and individual, distinct from the periodic aggregate **[[ind-annual-report-dsur|annual report / DSUR]]** (§ 312.33). This page specifies the trigger definitions, the two clocks, the content, and the bright non-delegable line: OSSICRO computes and escalates the clock and drafts the report, but the **causality, seriousness, and expectedness determinations that start the clock are the sponsor physician's** — never the software's.

In the [[sponsor-investigator]] model the ordinary two-party flow (investigator reports the SAE to the sponsor; sponsor assesses and reports the SUSAR to FDA) **collapses to a self-directed obligation plus the outward flow to FDA and to any other participating investigators**. The physician receives the event as investigator, assesses it as sponsor, and — if it qualifies — reports it to FDA as sponsor and notifies co-investigators. The obligation does not shrink because the roles merge; it concentrates on one person, which is exactly why the timing-and-drafting burden is where OSSICRO helps.

## The three definitional predicates — § 312.32(a)

A report is triggered only when **three attributes co-occur**. Each is a defined term, and each is a **human medical judgment**, not a data-field lookup.

- **Suspected adverse reaction** — any adverse event for which there is a **reasonable possibility** that the drug caused the event. "Reasonable possibility" means the evidence suggests a causal relationship. This is a **lower** causality bar than "adverse reaction" (established causal relationship) but a **higher** bar than "adverse event" (any untoward occurrence, causality aside). The causality read is the safety physician's.
- **Serious** — an adverse event or suspected adverse reaction is serious if it results in **death, a life-threatening event, inpatient hospitalization or prolongation of existing hospitalization, a persistent or significant disability/incapacity, a congenital anomaly/birth defect**, or is a medically important event that may jeopardize the patient and require intervention to prevent one of those outcomes. *§ 312.32(a).*
- **Unexpected** — an event is unexpected if it is **not listed in the [[investigators-brochure|Investigator's Brochure]]** (or is not listed at the observed specificity or severity), or, for an unbrochured drug, is not consistent with the risk information in the general investigational plan or elsewhere in the IND. Expectedness is judged against the **current IB** — so an IB update can change a future event's expectedness classification.

A **SUSAR** — Suspected, Unexpected, Serious Adverse Reaction — is the intersection of all three, and it is the paradigmatic 15-day trigger.

> [!warning] Non-delegable
> **Seriousness, expectedness, and causality ("reasonable possibility") are medical determinations owned by the sponsor's qualified [[medical-monitor|medical monitor / safety physician]]** under 21 CFR 312.32(a) and ICH E2A. OSSICRO must never auto-adjudicate any of the three predicates, never machine-classify an event as a SUSAR, and never machine-decide the 7-vs-15-day report type. The engine captures the event, pre-populates the descriptive fields, computes and surfaces the deadline from the date of the qualifying determination, and routes the case to the physician; **the human assesses, classifies, and authorizes.** Submission to FDA is a human act. This is the load-bearing gate of the entire safety subsystem. See [[non-delegable-functions-and-gates]].

## The two clocks — § 312.32(c)

### 15-calendar-day report — § 312.32(c)(1)
The sponsor must report **as soon as possible, but no later than 15 calendar days** after **determining** the information qualifies, any:
- **Serious and unexpected suspected adverse reaction** (the SUSAR). *§ 312.32(c)(1)(i).*
- **Findings from other sources** — other studies, animal or in vitro testing — that suggest a significant human risk. *§ 312.32(c)(1)(ii)–(iii).*
- **Aggregate analysis** finding: a clinically important **increased rate** of occurrence of serious suspected adverse reactions over the expected rate. *§ 312.32(c)(1)(iv).*

The clock starts on **determination** that the information qualifies, not on first awareness of the raw event — but the sponsor cannot defer the determination unreasonably; § 312.32(b) imposes a duty to **promptly review** all safety information from any source, foreign or domestic.

### 7-calendar-day report — § 312.32(c)(2)
Any **unexpected fatal or life-threatening suspected adverse reaction** must be reported **as soon as possible but no later than 7 calendar days** after the sponsor's **initial receipt** of the information — by any means (telephone, fax, electronic) — followed by a **complete written 15-day follow-up report**. Note the different clock anchor: the 7-day clock runs from **initial receipt**, the 15-day clock from **determination**.

### Follow-up — § 312.32(c)(1)(v), (d)
The sponsor must **promptly investigate** all safety information and submit **follow-up reports** as relevant new information arrives, within 15 calendar days of receipt. If, after further evaluation, the sponsor concludes an event previously reported does not meet the threshold, it may notify FDA in a follow-up.

## Content and format

An IND safety report may be submitted as a **narrative** or on **[[form-fda-3500a-medwatch|Form FDA 3500A]]** (or in FDA-processable electronic ICSR format to FAERS). The minimum ICSR elements are an **identifiable patient**, an **identifiable reporter**, a **suspect product**, and an **event**. The sponsor must also **notify all participating investigators** of new safety information in an IND safety report (§ 312.32(c)) — in the sponsor-investigator single-site case this outward-to-investigators flow may be trivial or absent, but in any multi-investigator study it is a hard obligation. Investigators, in turn, report SAEs to the sponsor per protocol (§ 312.64(b)) and report **unanticipated problems** to their IRB per IRB policy (see [[irb-review-workflow]]).

## Timeline mechanics OSSICRO encodes

> [!interpretive] OSSICRO position
> OSSICRO's [[safety-clock-engine]] is a **dedicated deadline computer and escalator** for § 312.32. On intake of a serious event it opens **both** candidate clocks (7-day from receipt, 15-day from determination), surfaces the running deadline in the tracker, and escalates as the clock burns down — but it **computes and escalates; it never files, and it never makes the causality call.** The clock cannot resolve to a report type until the [[medical-monitor|medical monitor]] sets seriousness, expectedness, and causality; only then does § 312.32(c)(1) vs (c)(2) resolve. Mayo Clinic's report-type × trigger × deadline matrix is the encodable model OSSICRO reimplements as validation rules, each traced to its § 312.32 subsection. A drafted report carries an explicit **"awaiting causality/seriousness determination by [named medical monitor]"** gate — an **amber** item on the [[completeness-ledger]] — until the human closes it. The provenance of every auto-populated field is recorded per the [[draft-provenance-model]] for the Part-11 audit trail.

The engine's clerical/timeliness layer (which it may automate) is strictly separated from the medical-judgment layer (which it may not): this is the operating version of the HARD LINE for the safety domain.

## Relationship to the rest of the safety layer

Each expedited report is later **summarized** in the [[ind-annual-report-dsur|annual report / DSUR]] (§ 312.33(b)). Reports are filed to FDA, copied to the [[regulatory-binder-isf-index|regulatory binder]] (Tab 10), and — where one operates — inform the [[dsmb-dmc|DSMB]]'s accumulating-data review. The end-to-end routing (site AE capture → sponsor assessment → FDA + investigators + IRB + DSMB) is the [[safety-reporting-workflow]]; the two clocks and their definitions are detailed in [[safety-report-timelines-7-15-day]]; the whole flow across the lifecycle is [[safety-reporting-lifecycle]].

## Related
- [[form-fda-3500a-medwatch]]
- [[safety-report-timelines-7-15-day]]
- [[safety-reporting-workflow]]
- [[safety-reporting-lifecycle]]
- [[ind-annual-report-dsur]]
- [[safety-management-plan]]
- [[safety-clock-engine]]
- [[medical-monitor]]
- [[pharmacovigilance-safety]]
- [[investigators-brochure]]
- [[dsmb-dmc]]
- [[non-delegable-functions-and-gates]]

## Sources
- [eCFR — 21 CFR 312.32 (IND safety reporting)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
- [21 CFR 312.32 (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.32)
- [FDA — IND Application Reporting: IND Safety Reports](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-application-reporting-ind-safety-reports)
- [Federal Register 75 FR 59935 — IND Safety Reporting Final Rule (Sept 29 2010)](https://www.govinfo.gov/content/pkg/FR-2010-09-29/html/2010-24296.htm)
- [FDA — Safety Reporting Requirements for INDs and BA/BE Studies (guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-reporting-requirements-inds-and-babe-studies) — local: `../../sources/fda-guidance/FDA_Investigator-Safety-Reporting_2021.pdf`
- [ICH E2A — Clinical Safety Data Management: Definitions and Standards for Expedited Reporting](https://database.ich.org/sites/default/files/E2A_Guideline.pdf) — local: `../../sources/ich/ICH_E2A_Guideline_1994.pdf`
