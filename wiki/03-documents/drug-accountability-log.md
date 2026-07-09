---
title: "Drug Accountability Log"
section: "03-documents"
status: mixed
governing_authority:
  - "21 CFR 312.57 (sponsor recordkeeping: receipt, shipment, disposition)"
  - "21 CFR 312.59 (disposition of unused supply)"
  - "21 CFR 312.61 (investigator control of the investigational drug)"
  - "21 CFR 312.62(a), (c) (investigator disposition records; retention)"
  - "21 CFR 312.69 (controlled substances); 21 CFR 312.6 (investigational labeling)"
  - "ICH E6(R3) (investigational product management; Appendix C essential records); ICH E6(R2) §4.6"
tags: [cfr/312, ich/e6r3, role/investigator, role/sponsor, role/monitor, lifecycle/conduct, lifecycle/closeout, ossicro/gating, status/confirmed, status/interpretive]
aliases: ["IP accountability log", "drug accountability", "investigational product log"]
updated: 2026-07-09
---

# Drug Accountability Log

> [!authority] Governing authority
> 21 CFR 312.61 (the investigator administers the drug only under personal or subinvestigator supervision and supplies it to no unauthorized person); 312.62(a) (investigator maintains adequate disposition records — dates, quantity, use by subjects — and returns or disposes of unused drug per 312.59); 312.57(a) (sponsor maintains receipt/shipment/disposition records — investigator name, date, quantity, batch or code mark); 312.59 (sponsor assures return or authorizes non-hazardous alternative disposition of unused supplies); 312.69 (controlled substances: securely locked, substantially constructed enclosure with limited access); 312.6 (investigational caution labeling); ICH E6(R3) investigational-product provisions and Appendix C (ICH E6(R2) §4.6). Status: **Mixed** — the recordkeeping duties are confirmed; the OSSICRO log-automation boundary is interpretive.

The drug accountability log is the continuous chain-of-custody record for the investigational product (IP): every unit received, stored, dispensed, returned, and destroyed, reconciled to zero. It is the artifact FDA inspectors and monitors reach for first, because it cannot be reconstructed after the fact and every discrepancy is either a documentation failure or a subject who received something unrecorded. In the [[sponsor-investigator]] model the physician holds **both** halves of the duty: the sponsor's disposition records (312.57(a)) and the investigator's disposition records (312.62(a)) — the log OSSICRO maintains is designed to satisfy both simultaneously.

## The custody chain and who owns each link

| Step | Duty holder | Requirement | Citation |
|---|---|---|---|
| Shipment | [[sponsor]] | Ship only to participating investigators; record investigator, date, quantity, batch/code mark | 312.53(b); 312.57(a) |
| Labeling | Sponsor | "Caution: New Drug — Limited by Federal (or United States) law to investigational use." | 312.6 |
| Receipt | [[investigator]]/pharmacy | Document delivery: date, quantity, batch/serial/lot, condition on arrival | 312.62(a); ICH E6(R2) §4.6.3 |
| Storage | Investigator/pharmacy | Store per sponsor specifications; document conditions and temperature excursions; controlled substances in a securely locked, substantially constructed enclosure with limited access | ICH E6(R2) §4.6.4; 312.69 |
| Dispensing | Investigator (supervising) | Administer only under the investigator's personal supervision or that of a responsible [[subinvestigator-and-delegation|subinvestigator]]; never supply to any person not authorized under Part 312 | 312.61 |
| Subject use & returns | Investigator | Record dates, quantity, and use by subjects; log subject returns of unused product | 312.62(a); E6(R2) §4.6.3 |
| Reconciliation | Investigator + monitor | Account for all IP received from the sponsor; the [[clinical-monitor-cra|monitor]] verifies at interim visits and at closeout ([[monitoring-workflow-siv-imv-cov]]) | E6(R2) §4.6.3; 312.56(a) |
| Return / destruction | Sponsor decision; investigator executes | On termination, suspension, discontinuation, or completion, return unused supplies to the sponsor **or** dispose under 312.59; the sponsor may authorize alternative disposition only if it does not expose humans to risk; written disposition records per 312.57 | 312.62(a); 312.59 |

## Required log fields

A log satisfying 312.57(a), 312.62(a), and ICH E6(R2) §4.6.3 captures, per line entry: date; transaction type (receipt / dispense / subject return / transfer / return-to-sponsor / destruction); quantity and unit; batch/lot/serial number and code mark; expiration date; subject identifier (coded) for dispensing entries; the dose per protocol; balance on hand; and the identity (initials/signature, dated) of the person recording — the attribution element of ALCOA++ data integrity. Storage-condition records (continuous temperature logs and excursion reports) travel with the log. Blinded studies add the kit/randomization code linkage, held so that the blind is preserved ([[statistical-analysis-plan]]; [[dsmb-workflow]]).

## Delegation, and its limit

ICH E6(R2) §4.6.1–4.6.2 (carried forward in E6(R3)'s investigational-product provisions) places IP accountability at the site on the investigator/institution, and permits assignment of some or all of these *duties* to a pharmacist or other appropriate individual under the investigator's responsibility, recorded on the [[delegation-of-authority-log]]. What is assigned is labor; 312.61's control obligation and 312.62(a)'s recordkeeping obligation remain the investigator's. Hospital investigational drug services (IDS pharmacies) are the standard institutional implementation.

## Retention and inspection

Investigator records: retain for 2 years following approval of a marketing application for the drug for the investigated indication, or — if no application is filed or it is not approved — until 2 years after the investigation is discontinued and FDA is notified (312.62(c)). Sponsor records: the parallel rule at 312.57(c). Both record sets are open to FDA inspection (312.58 sponsor-side; 312.68 investigator-side), and controlled-substance records are additionally available to DEA. See [[record-retention-and-archival]]. The initialized log is a startup essential record; the ongoing log a conduct record; the final reconciliation and destruction records are closeout essential records (ICH E6(R3) Appendix C; [[startup-tmf-checklist]], [[conduct-tmf-checklist]], [[closeout-tmf-checklist]], [[closeout]]).

## Expanded access and single-patient notes

The same accountability duties apply to expanded-access use: an individual-patient IND ([[form-fda-3926-expanded-access]], [[expanded-access-workflow]]) still requires receipt, storage, dispensing, and disposition records, and the manufacturer's letter of authorization does not transfer them. For a one-patient site ([[single-patient-site-enrollment]]), the log is short but its completeness is exactly what makes the site credible to a pharma partner ([[single-patient-site-and-pharma-acceptance]], [[verifiable-site-qualification-dossier]]).

> [!warning] Non-delegable
> Physical custody and administration of the investigational drug under the investigator's supervision (21 CFR 312.61), the attribution of each log entry to the human who performed the transaction, and the sponsor's authorization of destruction or alternative disposition (21 CFR 312.59 — a gated sponsor decision, since a wrong call can expose humans to risk or destroy required evidence) are human functions. Software neither dispenses drug nor authorizes its destruction. OSSICRO structures, checks, and reconciles the record; the humans move, count, and sign for the product.

> [!interpretive] OSSICRO position
> OSSICRO initializes the log at [[site-activation]] from the shipment manifest, enforces per-entry field completeness (batch, quantity, subject code, dated initials), continuously recomputes the running balance and flags any reconciliation gap the day it appears rather than at the closeout visit, ingests temperature-logger exports and opens an excursion event (with a quarantine recommendation pending a human usability decision), pre-drafts the return/destruction memorandum for sponsor authorization, and renders the whole chain as an inspection-ready report. Dispensing entries are recorded by, and attributed to, the human who dispensed — the engine validates, it never originates a custody event. Traceability follows [[compliance-mapping]] and the Part 11 audit-trail treatment in [[part-11-and-ai-credibility]].

## Related
- [[investigator]]
- [[sponsor]]
- [[sponsor-investigator]]
- [[subinvestigator-and-delegation]]
- [[delegation-of-authority-log]]
- [[conduct-and-monitoring]]
- [[monitoring-workflow-siv-imv-cov]]
- [[closeout]]
- [[startup-tmf-checklist]]
- [[conduct-tmf-checklist]]
- [[closeout-tmf-checklist]]
- [[record-retention-and-archival]]
- [[expanded-access-workflow]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 312.57 — Recordkeeping and record retention (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.57)
- [21 CFR 312.59 — Disposition of unused supply of investigational drug (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.59)
- [21 CFR 312.61 — Control of the investigational drug (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.61)
- [21 CFR 312.62 — Investigator recordkeeping and record retention (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.62)
- [21 CFR 312.69 — Handling of controlled substances (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.69)
- [21 CFR 312.6 — Labeling of an investigational new drug (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A/section-312.6)
- [ICH E6(R2) Integrated Addendum — §4.6 Investigational Product(s)](https://database.ich.org/sites/default/files/E6_R2_Addendum.pdf)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025) — investigational product provisions; Appendix C](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA Guidance (2009) — Investigator Responsibilities: Protecting the Rights, Safety, and Welfare of Study Subjects](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigator-responsibilities-protecting-rights-safety-and-welfare-study-subjects)
