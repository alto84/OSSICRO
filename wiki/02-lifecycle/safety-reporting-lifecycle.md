---
title: "Safety Reporting Lifecycle: AE → SAE → SUSAR"
section: "02-lifecycle"
status: mixed
governing_authority:
  - "21 CFR 312.32 (IND safety reporting)"
  - "21 CFR 312.64(b) (investigator reports)"
  - "21 CFR 312.66; 21 CFR 56.108(b) (IRB reporting)"
  - "ICH E2A; ICH E6(R3)"
tags: [lifecycle/safety, cfr/312, cfr/56, ich/e2a, ich/e6r3, fda-form/3500a, role/medical-monitor, ossicro/gating]
aliases: ["safety reporting", "SUSAR workflow", "expedited reporting"]
updated: 2026-07-09
---

# Safety Reporting Lifecycle: AE → SAE → SUSAR

> [!authority] Governing authority
> 21 CFR 312.32 (IND safety reporting; 7- and 15-calendar-day expedited reports); 21 CFR 312.64(b) (investigator SAE reports to sponsor); 21 CFR 312.66 and 21 CFR 56.108(b) (unanticipated-problem reporting to the IRB); ICH E2A (definitions and expedited-reporting standards); ICH E6(R3) (safety assessment and reporting, FDA-adopted 2025-09-09). The current 312.32 framework was established by the IND safety-reporting final rule, 75 FR 59935 (Sept. 29, 2010). Status: **Mixed** — the reporting obligations and clocks are confirmed black-letter requirements; OSSICRO's routing/clock automation is an interpretive position, marked below.

The safety-reporting lifecycle is the highest-consequence recurring workflow in an IND study: an adverse event observed at the bedside must be captured, medically assessed, escalated to the sponsor, and — when it qualifies — reported to FDA, all participating investigators, the [[irb-iec|IRB]], and the [[dsmb-dmc|DSMB/DMC]] on fixed calendar-day clocks. For the [[sponsor-investigator]], the investigator→sponsor arrow collapses into a self-directed obligation, but no reporting duty disappears. This page defines the terms, walks the escalation chain, and states the clocks; the operational routing map is at [[safety-reporting-workflow]] and the clock detail at [[safety-report-timelines-7-15-day]].

## 1. Definitions (21 CFR 312.32(a); ICH E2A)

These definitions are load-bearing: each expedited-reporting trigger is a conjunction of them.

| Term | Definition (312.32(a)) |
|---|---|
| **Adverse event (AE)** | Any untoward medical occurrence associated with the use of a drug in humans, whether or not considered drug related. |
| **Adverse reaction** | Any adverse event caused by a drug. |
| **Suspected adverse reaction** | Any adverse event for which there is a *reasonable possibility* that the drug caused the event — i.e., evidence to suggest a causal relationship. "Suspected adverse reaction" implies a lesser degree of certainty than "adverse reaction." |
| **Unexpected** | Not listed in the [[investigators-brochure|investigator's brochure]] at the observed specificity or severity (or, if no IB is required, not consistent with the risk information in the general investigational plan or elsewhere in the IND). Events *mentioned* in the IB as anticipated from the pharmacological class but not specifically described as occurring with the particular drug are unexpected. |
| **Serious** | Death, a life-threatening adverse event, inpatient hospitalization or prolongation of existing hospitalization, persistent or significant incapacity or substantial disruption of the ability to conduct normal life functions, congenital anomaly/birth defect, or an important medical event that may jeopardize the patient and require intervention to prevent one of these outcomes (medical judgment). |
| **Life-threatening** | The patient was, in the view of the investigator or sponsor, at immediate risk of death from the event as it occurred (not hypothetically had it been more severe). |

A **SUSAR** (serious *and* unexpected *and* suspected adverse reaction — ICH E2A terminology) is the event class that triggers the 15-day IND safety report; the fatal/life-threatening subset triggers the 7-day report.

## 2. The escalation chain

### Stage 1 — Site capture and investigator report (21 CFR 312.64(b))

The [[investigator]] must **immediately** report to the [[sponsor]] any serious adverse event, *whether or not considered drug related*, and the report must include an assessment of whether there is a reasonable possibility the drug caused the event. Study endpoints specified in the protocol (e.g., all-cause mortality in a mortality trial) are excepted from immediate reporting unless there is evidence suggesting a causal relationship. Non-serious AEs are recorded and reported to the sponsor per the protocol's timetable. Source capture, MedDRA coding, and narrative drafting are the [[pharmacovigilance-safety|safety function's]] work product.

### Stage 2 — Sponsor review (21 CFR 312.32(b))

The sponsor must **promptly review** all information relevant to the drug's safety from any source, foreign or domestic — animal and in-vitro studies, clinical and epidemiological investigations, commercial marketing experience, reports in the scientific literature, and unpublished papers. In the sponsor-investigator model this review duty belongs to the same physician who received the site report; it is discharged, not dissolved, by the role collapse.

### Stage 3 — Expedited IND safety reports (21 CFR 312.32(c))

The sponsor must notify **FDA and all participating investigators** in an IND safety report of potential serious risks, as soon as possible but no later than **15 calendar days** after the sponsor determines the information qualifies, for:

1. **Serious and unexpected suspected adverse reaction** — 312.32(c)(1)(i). Per the 2010 final rule and the December 2012 FDA guidance, a single occurrence suffices only for events with strong drug-causation signatures (e.g., angioedema, Stevens-Johnson syndrome, agranulocytosis); events commonly occurring in the study population may require aggregate analysis before "reasonable possibility" is met.
2. **Findings from other studies** (clinical, epidemiological, pooled analyses) suggesting a significant human risk — 312.32(c)(1)(ii).
3. **Findings from animal or in-vitro testing** suggesting a significant human risk (mutagenicity, teratogenicity, carcinogenicity, significant organ toxicity) — 312.32(c)(1)(iii).
4. **Clinically important increased rate of occurrence** of serious suspected adverse reactions over that listed in the protocol or IB — 312.32(c)(1)(iv).

**7-calendar-day report** — 312.32(c)(2): any **unexpected fatal or life-threatening suspected adverse reaction** must be reported to FDA no later than 7 calendar days after the sponsor's initial receipt of the information, followed by a complete report within the 15-day frame.

**Format** — narrative, [[form-fda-3500a-medwatch|FDA Form 3500A]], or an electronic format FDA can process (ICH E2B for CBER-regulated products); each report is prominently identified as an "IND safety report" and submitted to the reviewing division. Relevant follow-up information must be submitted **as soon as the information is available**, identified as a follow-up IND safety report (312.32(d)). Submission of a safety report does not constitute an admission that the drug caused the event (312.32(e)).

### Stage 4 — IRB and DSMB routing

- **IRB:** the investigator must promptly report to the IRB "all unanticipated problems involving risk to human subjects or others" (21 CFR 312.66; 21 CFR 56.108(b)(1)). Not every IND safety report is an unanticipated problem; the IRB's own policy governs the format and window. See [[irb-review-workflow]].
- **DSMB/DMC:** where constituted, the charter defines which events flow to the committee, in what blinding state, and on what cadence; the committee's continue/modify/stop **recommendation** returns to the sponsor, who decides. See [[dsmb-workflow]] and [[dsmb-charter]].
- **Pharma partner:** where a manufacturer supplies drug (IIS or expanded access), the safety-data exchange agreement in the [[safety-management-plan]] governs bidirectional ICSR exchange. See [[pharma-partner-interface-iis]].

## 3. The clocks at a glance

| Trigger | Clock start | Deadline | Recipient |
|---|---|---|---|
| SAE at site | Event awareness | Immediately | Investigator → sponsor (312.64(b)) |
| Serious + unexpected + suspected AR | Sponsor determines it qualifies | 15 calendar days | FDA + all participating investigators (312.32(c)(1)) |
| Unexpected fatal/life-threatening suspected AR | Sponsor's initial receipt | 7 calendar days | FDA (312.32(c)(2)); complete report within 15 |
| Follow-up information | Information available | As soon as available (312.32(d)) | FDA + investigators |
| Unanticipated problem | Investigator awareness | Promptly, per IRB policy | IRB (312.66; 56.108(b)(1)) |
| Annual rollup | IND anniversary | Within 60 days | FDA — see [[annual-reporting-and-amendments]] |

> [!warning] Non-delegable
> The determinations that arm every clock — **seriousness**, **expectedness** against the current IB, and **causality** ("reasonable possibility") — are medical judgments belonging to the sponsor (in practice the [[medical-monitor]]; in the sponsor-investigator model, the physician personally) under 21 CFR 312.32(a)–(c). The **release of any safety report to FDA** is a human-authorized regulatory act. OSSICRO drafts the narrative, populates Form 3500A, computes the deadline, and escalates; a qualified human owns the judgment and signs the submission. See [[non-delegable-functions-and-gates]].

> [!interpretive] OSSICRO position
> The [[safety-clock-engine]] computes and escalates the 7/15-day deadlines from the moment a qualifying determination is *entered by the human assessor*; it never starts a regulatory clock on its own inference, never adjudicates causality, and never files. Draft ICSRs and 3500A instances carry span-level provenance ([[draft-provenance-model]]) so the reviewing physician can verify every populated field against source. This automation boundary is an OSSICRO design position, not a regulatory safe harbor; the FDA 2025 AI-credibility draft framework is applied to it at [[part-11-and-ai-credibility]].

## 4. Sponsor-investigator collapse

Under 21 CFR 312.3(b) the investigator-to-sponsor report (312.64(b)) and the sponsor's review (312.32(b)) are performed by the same person. OSSICRO still generates the internal SAE report record — the documentation trail must show the event was captured, assessed, and adjudicated on time, because FDA inspects the sponsor-investigator against **both** obligation sets ([[fda-as-counterparty]], BIMO). The safety database, line listings, and adjudication records feed the [[ind-annual-report-dsur|annual report/DSUR]] and the final reconciliation at [[closeout]].

## Related

- [[safety-reporting-workflow]] — end-to-end routing map
- [[safety-report-timelines-7-15-day]] — clock definitions in depth
- [[ind-safety-report]] — the report document itself
- [[form-fda-3500a-medwatch]] — mandatory MedWatch format
- [[safety-management-plan]] — the operational plan artifact
- [[safety-clock-engine]] — OSSICRO deadline computation
- [[medical-monitor]] · [[pharmacovigilance-safety]] — the accountable humans
- [[dsmb-dmc]] · [[dsmb-workflow]] · [[irb-iec]] — oversight recipients
- [[annual-reporting-and-amendments]] — the aggregate rollup
- [[conduct-and-monitoring]] — where AEs are first captured
- [[non-delegable-functions-and-gates]] — the gating matrix

## Sources

- [21 CFR 312.32 — IND safety reporting (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
- [21 CFR 312.64 — Investigator reports (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.64)
- [21 CFR 312.66 — Assurance of IRB review (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.66)
- [21 CFR 56.108 — IRB functions and operations (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/56.108)
- [Final rule: Investigational New Drug Safety Reporting Requirements, 75 FR 59935 (Sept. 29, 2010)](https://www.govinfo.gov/content/pkg/FR-2010-09-29/html/2010-24296.htm)
- [FDA Guidance: Safety Reporting Requirements for INDs and BA/BE Studies (December 2012)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-reporting-requirements-inds-and-babe-studies)
- [FDA — IND Application Reporting: IND Safety Reports](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-application-reporting-ind-safety-reports)
- [ICH E2A — Clinical Safety Data Management: Definitions and Standards for Expedited Reporting](https://database.ich.org/sites/default/files/E2A_Guideline.pdf)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [Federal Register — FDA adoption of ICH E6(R3) (Sept. 9, 2025)](https://www.federalregister.gov/documents/2025/09/09/2025-17311/e6r3-good-clinical-practice-international-council-for-harmonisation-guidance-for-industry)
