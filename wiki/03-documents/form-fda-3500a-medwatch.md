---
title: "Form FDA 3500A — MedWatch Mandatory Reporting (ICSR / IND Safety Report Format)"
section: "03-documents"
status: confirmed
governing_authority:
  - "21 CFR 312.32 (IND safety reporting)"
  - "Form FDA 3500A, OMB No. 0910-0291"
  - "ICH E2A; ICH E2B(R3)"
tags: [fda-form/3500a, cfr/312, ich/e2a, ich/e2b, role/sponsor, role/medical-monitor, role/pharmacovigilance-safety, lifecycle/safety, ossicro/gating, status/confirmed]
aliases: ["3500A", "MedWatch", "ICSR", "mandatory MedWatch"]
updated: 2026-07-09
---

# Form FDA 3500A — MedWatch Mandatory Reporting

> [!authority] Governing authority
> 21 CFR 312.32 (IND safety reporting); Form FDA 3500A (OMB No. 0910-0291, MedWatch Mandatory Reporting, 09/2025 edition); ICH E2A (clinical safety data management) and ICH E2B(R3) (electronic ICSR transmission). Status: **Confirmed**.

Form FDA 3500A is the **mandatory** MedWatch reporting form — the Individual Case Safety Report (ICSR) format used by IND sponsors (and manufacturers, user facilities, importers, distributors, packers) to submit adverse-event and product-problem reports FDA requires. It is the format in which an IND sponsor renders a written **[IND safety report](ind-safety-report.md)** under [21 CFR 312.32(c)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32). It is distinct from the **voluntary** Form FDA 3500 used by health professionals and consumers; a sponsor's regulatory obligation is discharged on the 3500A (or via electronic E2B(R3) submission to FAERS), never the 3500.

The form does not, by itself, decide anything. The judgments that *trigger* a 3500A — that a suspected adverse reaction is **serious**, **unexpected**, and has a **reasonable possibility** of being caused by the drug — are the safety-physician determinations governed by § 312.32(a) and ICH E2A, and they are non-delegable (see gate). OSSICRO pre-populates the form from captured safety data and computes the reporting **clock**, but it never adjudicates causality, seriousness, or expectedness.

## Section map (Form FDA 3500A, 09/2025 edition, 9 pages)

| Section | Content | OSSICRO handling |
|---------|---------|------------------|
| A. Patient Information | Patient identifier (in confidence), age/DOB, sex, weight, race/ethnicity | Coded patient identifier only — never direct identifiers in egress; see [privacy gating](../05-ossicro-system/hipaa-and-privacy-gating.md) |
| B. Adverse Event or Product Problem | Type of report; **outcome** (death, life-threatening, hospitalization, disability, congenital anomaly, required intervention, other serious); date of event; free-text event description | The "outcome" checkboxes encode **seriousness** per § 312.32(a) — human-set |
| C. Suspect Products | Product name, strength, manufacturer, NDC/unique ID, lot, dose, route, therapy dates, indication, product type, dechallenge/rechallenge | Auto-populated from the investigational-product record |
| D. Suspect Medical Device | Device fields (drug-device combination products) | Populated only for combination products |
| E. Initial Reporter | Reporter name/address, health-professional status, occupation, whether also sent to FDA | Captures the site/investigator source |
| F. For Use by User Facility/Importer | Device-only user-facility fields | N/A for a drug IND |
| G. All Manufacturers | Contact office; report source; date received; **NDA/ANDA/IND/BLA #**; protocol #; **type of report (5-/7-/15-/30-day, non-expedited, initial/follow-up)**; adverse-event term(s) | Field G.4 (IND #), G.5 (protocol #), and G.6 (report type) carry the 312.32 timing classification |
| H. Device Manufacturers Only | Device manufacturer narrative/codes | N/A for a drug IND |

The seriousness and expedited-timeline logic lives at the intersection of Section B (outcome) and Section G.6 (report type): a fatal or life-threatening suspected adverse reaction that is unexpected drives a **7-calendar-day** report; other serious-and-unexpected suspected adverse reactions drive a **15-calendar-day** report (§ 312.32(c)(1)–(c)(2)). See [safety-report-timelines-7-15-day](../04-coordination/safety-report-timelines-7-15-day.md).

## Relationship to ICH E2A / E2B(R3)
ICH E2A supplies the definitions (serious, unexpected, suspected adverse reaction) and the expedited-reporting concept that § 312.32 operationalizes. ICH E2B(R3) is the structured electronic ICSR data-element specification underlying modern FAERS/gateway submission; the 3500A field content maps onto E2B(R3) data elements. OSSICRO's safety data model is built to the E2B(R3) element set so a drafted 3500A and an electronic ICSR are two renderings of one validated case.

## Non-delegable gate

> [!warning] Non-delegable
> The **causality, seriousness, and expectedness** determinations that trigger a 3500A IND safety report are medical judgments owned by the sponsor's qualified [medical monitor / safety physician](../01-roles-responsibilities/medical-monitor.md) under 21 CFR 312.32(a) and ICH E2A. OSSICRO must never auto-adjudicate "reasonable possibility of causal relationship," never machine-set the Section B seriousness outcome, and never machine-decide the report type in Section G.6. The engine pre-populates the descriptive fields, computes and surfaces the deadline, and routes the case to the safety physician; the human assesses, classifies, and authorizes submission. Submission to FDA is a human act.

> [!interpretive] OSSICRO position
> OSSICRO separates the **clerical/timeliness** layer (which it may automate) from the **medical-judgment** layer (which it may not). The [safety-clock-engine](../05-ossicro-system/safety-clock-engine.md) computes the 7-/15-day deadline from the date of receipt and escalates as the clock runs, but it computes and escalates — it does not file and does not make the causality call. A drafted 3500A carries a completeness state and an explicit "awaiting causality/seriousness determination by [named medical monitor]" gate until the human closes it. The provenance of every auto-populated field (source datum → citation) is recorded per the [draft-provenance model](../05-ossicro-system/draft-provenance-model.md) for the Part-11 audit trail.

## OSSICRO engine behavior
- **Generate:** renders a 3500A from the E2B(R3)-structured case (Sections A, C, E, and the descriptive part of B).
- **Check:** verifies the IND number (G.4), protocol number (G.5), suspect-product record (C), and reporter (E) are present; flags missing minimum ICSR elements (an identifiable patient, an identifiable reporter, a suspect product, an event).
- **Validate:** holds the report in a gated state until the medical monitor sets seriousness (B), expectedness, and causality; only then does the report-type/timeline (G.6) resolve and the case become authorizable. The engine never advances a case past the causality gate on its own.

## Related
- [[ind-safety-report]]
- [[safety-report-timelines-7-15-day]]
- [[safety-reporting-workflow]]
- [[safety-reporting-lifecycle]]
- [[pharmacovigilance-safety]]
- [[medical-monitor]]
- [[safety-clock-engine]]
- [[non-delegable-functions-and-gates]]
- [[hipaa-and-privacy-gating]]

## Sources
- [21 CFR 312.32 — IND safety reporting](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
- [FDA Form 3500A (MedWatch Mandatory Reporting)](https://www.fda.gov/media/82728/download) — local original: `../sources/fda-form/FDA_Form-3500A.pdf`
- [FDA — Safety Reporting Requirements for INDs and BA/BE Studies (guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-reporting-requirements-inds-and-babe-studies) — local original: `../sources/fda-guidance/FDA_Investigator-Safety-Reporting_2021.pdf`
- [ICH E2A — Clinical Safety Data Management: Definitions and Standards for Expedited Reporting](https://www.ich.org/page/efficacy-guidelines)
- [ICH E2B(R3) — Electronic Transmission of Individual Case Safety Reports](https://www.ich.org/page/efficacy-guidelines)
