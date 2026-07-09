---
title: "Pharmacovigilance / Safety Function"
section: "01-roles-responsibilities"
status: mixed
governing_authority:
  - "21 CFR 312.32 (IND safety reporting)"
  - "21 CFR 312.33 (annual reports) / ICH E2F (DSUR)"
  - "21 CFR 312.64(b) (investigator safety reports to sponsor)"
  - "ICH E2A; ICH E2B(R3)"
  - "FDA Guidance (Dec 2012): Safety Reporting Requirements for INDs and BA/BE Studies"
tags: [role/pharma, role/medical-monitor, cfr/312, ich/e2a, ich/e2b, ich/e2f, lifecycle/safety, fda-form/3500a]
aliases: ["PV", "Safety Function", "Drug Safety", "Pharmacovigilance"]
updated: 2026-07-09
---

# Pharmacovigilance / Safety Function

> [!authority] Governing authority
> 21 CFR 312.32 (IND safety reporting — definitions, review obligation, 15-day and 7-day expedited reports, follow-up); 21 CFR 312.33 (annual reports; ICH E2F DSUR accepted in lieu); 21 CFR 312.64(b) (investigator→sponsor reporting); ICH E2A (expedited-reporting definitions and standards); ICH E2B(R3) (electronic ICSR format); FDA final rule 75 FR 59935 (Sept. 29, 2010); FDA guidance *Safety Reporting Requirements for INDs and BA/BE Studies* (Dec 2012). Status: **Mixed** — reporting obligations, definitions, and clocks are confirmed; the OSSICRO intake/drafting boundary is an interpretive position, marked inline.

The pharmacovigilance (PV) function is the operational pipeline that turns an adverse event observed at the bedside into compliant safety information in the hands of FDA, all participating investigators, the [[irb-iec|IRB]], and (where constituted) the [[dsmb-dmc|DMC]] — on the regulatory clocks. In a conventional sponsor organization this is a dedicated safety department; in the OSSICRO [[sponsor-investigator]] model the *obligations* are identical but land on one physician, which is precisely why the function must be decomposed into (a) mechanical steps software can perform and (b) the medical judgments that only a qualified human — the [[medical-monitor]] — may make.

## 1. The controlling definitions (21 CFR 312.32(a); ICH E2A)

Every clock in this pipeline is armed or disarmed by definitions that embed medical judgment:

- **Adverse event (AE):** any untoward medical occurrence associated with the use of a drug in humans, whether or not considered drug related.
- **Suspected adverse reaction:** any AE for which there is a **reasonable possibility** that the drug caused it — i.e., evidence to suggest a causal relationship. This is the codified causality standard, deliberately set below "probable" and above mere temporal association (75 FR 59935).
- **Serious:** results in death, is life-threatening, requires or prolongs inpatient hospitalization, causes persistent or significant incapacity, is a congenital anomaly/birth defect, or is another important medical event that may jeopardize the patient and require intervention to prevent one of those outcomes.
- **Life-threatening:** the patient was at immediate risk of death from the reaction as it occurred.
- **Unexpected:** not listed in the [[investigators-brochure]] (or, absent an IB, the risk information in the general investigational plan/protocol) at the observed specificity or severity.

These definitions are harmonized with ICH E2A; a **SUSAR** (serious + unexpected + suspected adverse reaction) is the expedited-report trigger. See [[glossary]].

## 2. The pipeline, stage by stage

**Intake.** The [[investigator]] must report any serious adverse event to the sponsor **immediately**, whether or not considered drug-related, including a causality assessment; non-serious AEs are recorded and reported per the protocol schedule (21 CFR 312.64(b)). OSSICRO provides structured SAE intake forms keyed to the protocol and the [[safety-management-plan]], timestamps receipt (the receipt timestamp arms the regulatory clocks), and opens a SafetyReport record in the [[data-model]].

**Triage and medical assessment.** The medical monitor reviews each case for seriousness, expectedness against the current IB, and causality ("reasonable possibility"). The sponsor must **promptly review all information relevant to the safety of the drug** from any source, foreign or domestic — clinical and epidemiological investigations, animal or in vitro studies, commercial marketing experience, reports in the scientific literature, and unpublished papers (21 CFR 312.32(b)). This review obligation is continuous, not per-case.

**Coding.** AE terms are coded to a standardized medical dictionary — in practice [MedDRA](https://www.meddra.org/) — for aggregation, line listings, and electronic submission. Coding suggestions are checkable; the confirmed code on a serious case is reviewed by a qualified human because coding drives expectedness comparison and aggregate signal detection.

**Narrative.** Each reportable case carries a clinical narrative (patient course, drug exposure, event, dechallenge/rechallenge, outcome, assessor's reasoning). The narrative is a draft artifact OSSICRO generates from structured case data with full provenance ([[draft-provenance-model]]); the medical monitor owns its clinical accuracy.

**Expedited-report determination and drafting.** The sponsor must notify FDA and **all participating investigators** in an IND safety report of:
- any suspected adverse reaction that is both serious and unexpected — no later than **15 calendar days** after the sponsor determines the information qualifies (312.32(c)(1)(i));
- findings from other clinical, animal, or in vitro studies suggesting significant human risk (312.32(c)(1)(ii)–(iii));
- a clinically important **increased rate of occurrence** of serious suspected adverse reactions over that listed in the protocol or IB (312.32(c)(1)(iv));
- any **unexpected fatal or life-threatening suspected adverse reaction** — to FDA no later than **7 calendar days** after initial receipt (312.32(c)(2)), followed by a complete report within the 15-day frame.

Note the clock-start asymmetry: the 15-day clock runs from the sponsor's *determination that the information qualifies* (and the sponsor must make that determination promptly — FDA's 2012 guidance frames the surrounding diligence expectation), while the 7-day clock runs from *initial receipt* of the information. See [[safety-report-timelines-7-15-day]] and [[safety-clock-engine]].

**Format and submission.** IND safety reports are submitted in a narrative format, on [[form-fda-3500a-medwatch|FDA Form 3500A]], or in an FDA-accepted electronic format (312.32(c)(1)(v)); each must prominently identify itself as an "IND Safety Report" and identify all previously submitted reports concerning a similar reaction, with an analysis of significance. FDA has moved toward electronic ICSR submission in ICH E2B(R3) format for IND safety reports — confirm the currently operative submission channel before filing. Submission to FDA is a human-authorized act. See [[ind-safety-report]].

**Distribution.** The same 15-day reports go to all participating investigators (312.32(c)(1)); the investigator in turn must promptly report unanticipated problems involving risks to human subjects to the IRB (312.66; 56.108(b)); relevant safety data feed the DMC packets ([[dsmb-workflow]]); and, where a pharma partner supplies drug (IIS or expanded access), the safety-data-exchange terms of the agreement govern reciprocal notification ([[pharma-partner-interface-iis]], [[safety-management-plan]]).

**Follow-up.** The sponsor must promptly investigate all safety information it receives, submit relevant follow-up information as soon as available (15-day clock from when the follow-up information qualifies), and treat non-qualifying reports later found to qualify as newly triggered (312.32(d)).

**Aggregate and periodic reporting.** Within 60 days of the IND anniversary the sponsor files the annual report (312.33), including a narrative or tabular summary of the most frequent and most serious adverse experiences; FDA accepts the ICH E2F **DSUR** in lieu. OSSICRO assembles it from accumulated line listings — see [[ind-annual-report-dsur]] and [[annual-reporting-and-amendments]].

## 3. Division of labor: software vs. qualified human

> [!warning] Non-delegable
> **Causality ("reasonable possibility"), expectedness, and seriousness determinations are medical judgments** belonging to the sponsor's qualified physician — in the OSSICRO model, the [[medical-monitor]] (often the sponsor-investigator personally; 21 CFR 312.32(a), (c)). The aggregate judgment behind a 312.32(c)(1)(iv) increased-rate report, the significance analysis accompanying each report, and the release of any safety report to FDA are likewise human-owned. The investigator's immediate-SAE-report duty (312.64(b)) is personal to the investigator. OSSICRO computes clocks, drafts, and escalates; it never adjudicates a case and never files.

> [!interpretive] OSSICRO position — the supported perimeter
> OSSICRO's PV layer performs: structured intake with receipt timestamping; deadline computation and escalation ([[safety-clock-engine]]); MedDRA coding *suggestions* flagged for human confirmation; narrative drafting from structured case data; 3500A field population; recipient routing (FDA / investigators / IRB / DMC / pharma partner) as gated actions; reconciliation of the case log against the annual report/DSUR; and a complete Part 11 audit trail of who judged and signed what ([[part-11-and-ai-credibility]]). Each of these is a coordination or drafting function; none is an accountable determination. This decomposition is OSSICRO's design thesis, not a regulatory safe harbor — the sponsor-investigator remains accountable for every report's content and timeliness regardless of tooling.

## Related

- [[medical-monitor]] · [[safety-reporting-lifecycle]] · [[safety-reporting-workflow]] · [[safety-report-timelines-7-15-day]]
- [[ind-safety-report]] · [[form-fda-3500a-medwatch]] · [[ind-annual-report-dsur]] · [[safety-management-plan]]
- [[safety-clock-engine]] · [[non-delegable-functions-and-gates]] · [[draft-provenance-model]]
- [[dsmb-dmc]] · [[irb-iec]] · [[investigator]] · [[sponsor-investigator]] · [[sponsor]]
- [[investigators-brochure]] · [[pharma-partner-interface-iis]] · [[glossary]]

## Sources

- [21 CFR 312.32 — IND safety reporting (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
- [21 CFR 312.33 — Annual reports (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.33)
- [21 CFR 312.64 — Investigator reports (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.64)
- [Federal Register — Investigational New Drug Safety Reporting Requirements, Final Rule (75 FR 59935, Sept. 29, 2010)](https://www.govinfo.gov/content/pkg/FR-2010-09-29/html/2010-24296.htm)
- [FDA Guidance (Dec 2012) — Safety Reporting Requirements for INDs and BA/BE Studies](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-reporting-requirements-inds-investigational-new-drug-applications-and-babe-bioavailabilitybioequivalence-studies)
- [FDA — IND Application Reporting: IND Safety Reports](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-application-reporting-ind-safety-reports)
- [ICH E2A — Clinical Safety Data Management: Definitions and Standards for Expedited Reporting (PDF)](https://database.ich.org/sites/default/files/E2A_Guideline.pdf)
- [ICH E2B(R3) — Individual Case Safety Report (ICSR) Specification](https://ich.org/page/e2br3-individual-case-safety-report-icsr-specification-and-related-files)
- [ICH E2F — Development Safety Update Report (PDF)](https://database.ich.org/sites/default/files/E2F_Guideline.pdf)
- [FDA — MedWatch Forms (3500A) for FDA Safety Reporting](https://www.fda.gov/safety/medical-product-safety-information/medwatch-forms-fda-safety-reporting)
- [MedDRA — Medical Dictionary for Regulatory Activities](https://www.meddra.org/)
