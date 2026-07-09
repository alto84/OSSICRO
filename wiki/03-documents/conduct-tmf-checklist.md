---
title: "Conduct TMF Checklist — During-Trial Essential Records"
section: "03-documents"
status: mixed
governing_authority:
  - "ICH E6(R3) Appendix C (during-trial essential records); E6(R2) §8.3"
  - "21 CFR 312.32 (IND safety reporting), 312.33 (annual report), 312.30 (amendments), 312.56, 312.62, 312.64"
  - "21 CFR 50.27 (documentation of consent); 21 CFR 56.108–56.115 (IRB continuing review)"
tags: [lifecycle/conduct, lifecycle/safety, lifecycle/annual, gcp/e6r3, cfr/312, cfr/50, cfr/56, ossicro/gating, status/mixed]
aliases: ["conduct checklist", "during-trial documents", "ongoing TMF", "in-life records"]
updated: 2026-07-09
---

# Conduct TMF Checklist — During-Trial Essential Records

> [!authority] Governing authority
> **ICH E6(R3) Appendix C** (during-trial essential records), with **E6(R2) §8.3** cross-numbering; **21 CFR 312.32** (IND safety reporting), **312.33** (annual report), **312.30** (amendments), **312.56/312.62/312.64**; **21 CFR 50.27** (consent documentation); **21 CFR 56.108–56.115** (IRB continuing review). Status: **Mixed** — items tagged Confirmed / Conditional inline.

This is the during-trial working checklist: the records generated while the trial runs, from first enrollment to last-subject-last-visit. It is where the **regulatory clocks** live — investigator SAE-to-sponsor, sponsor [[safety-report-timelines-7-15-day|7-day / 15-day]] IND safety reports, IRB continuing review, and the [[ind-annual-report-dsur|60-day annual report]] — and where the [[non-delegable-functions-and-gates|non-delegable acts]] fire most often: the consent event, and the causality/expectedness determination on every SAE. Full authority mapping for each row is in the [[document-catalog]] (section B). This page adds the timing dependencies and gate annotations. See [[conduct-and-monitoring]] and [[safety-reporting-lifecycle]] for the workflow view.

## The clocks that run during conduct

> [!warning] Non-delegable
> **Consent event** (per subject, before any study procedure) — a qualified investigator/designee conducts the conversation and obtains the signature (21 CFR 50.27; 312.62(b)). OSSICRO tracks that a signed [[informed-consent-form|ICF]] exists and is version-correct; it never *consents* the subject. See [[informed-consent-document-vs-event]].
>
> **SAE causality/expectedness** — on every serious adverse event, a qualified [[medical-monitor|physician]] determines relatedness, seriousness, and expectedness (21 CFR 312.32, 312.64(b); ICH E2A). This judgment sets the reporting clock; OSSICRO computes and escalates the [[safety-clock-engine|deadline]] but never adjudicates causality and never files.

| Clock | Trigger → Deadline | Authority |
|-------|--------------------|-----------|
| Investigator → sponsor SAE | Per protocol timeline (typically immediate/24h) | 21 CFR 312.64(b) |
| Sponsor → FDA + all investigators: **fatal/life-threatening, unexpected, suspected** | **7 calendar days** | 21 CFR 312.32(c)(1)(ii) |
| Sponsor → FDA + all investigators: **other serious, unexpected, suspected** | **15 calendar days** | 21 CFR 312.32(c)(1)(i) |
| IND annual report | Within **60 days** of the IND anniversary | 21 CFR 312.33 |
| IRB continuing review | At intervals appropriate to risk (FDA-regulated: still required under Part 56) | 21 CFR 56.109(f) |

## 1. Enrollment and consent records

- [ ] **Signed/executed [[informed-consent-form|ICFs]]** (per subject) — dated before any study procedure; original in site file, copy to subject. *21 CFR 50.27, 312.62(b); Confirmed. **Consenting act non-delegable.***
- [ ] **Screening log, enrollment log, subject identification code list** — accounts for all screened/enrolled subjects; coded IDs linked to identities confidentially. *21 CFR 312.62(b); Confirmed.* See [[enrollment-and-consent]].

## 2. Source data and case report forms

- [ ] **Completed source documents** — ALCOA++ original observations (vitals, visit notes, eligibility checklists). *ICH E6(R3) §6; 21 CFR 312.62(b); Confirmed.*
- [ ] **Completed CRFs/eCRFs + correction/audit trail** — reported data with corrections preserving the original entry. *21 CFR 312.62(b); Part 11 (if electronic); Confirmed.*
- [ ] **Signature sheet (updated) + site signature/initial log** — every signature/initial mapped to a named authorized person. *ICH E6(R3) §2; Confirmed.*

## 3. Safety records (the highest-liability stream)

- [ ] **[[form-fda-3500a-medwatch|SAE report — investigator-to-sponsor (MedWatch 3500A or equivalent)]]** + AE/SAE logs — with the investigator's causality assessment. *21 CFR 312.64(b); ICH E2A; Confirmed. **Causality non-delegable.***
- [ ] **[[ind-safety-report|IND safety reports — sponsor-to-FDA + all investigators (7-day / 15-day)]]** — expedited reporting of serious + unexpected + suspected events. In the [[sponsor-investigator]] model this is self-originated, not received from an external sponsor. *21 CFR 312.32(c), 312.55(b); Confirmed.* See [[safety-reporting-workflow]] and [[safety-clock-engine]].
- [ ] **[[investigators-brochure|Investigator's Brochure updates]] / revisions** — at least annual; keeps the safety reference current. *21 CFR 312.55(b), 312.23(a)(5); Confirmed.*
- [ ] **Final/ongoing safety reconciliation** — site AE/SAE database reconciled against sponsor safety database (also a closeout record). *21 CFR 312.62(b); Confirmed.*

## 4. Oversight records

- [ ] **[[monitoring-workflow-siv-imv-cov|Monitoring visit reports]] + monitoring log + follow-up letters** — evidence of sponsor oversight; findings and issue resolution. *ICH E6(R3) §6.9; 21 CFR 312.56; Confirmed.*
- [ ] **[[dsmb-workflow|DSMB/DMC meeting minutes]] + recommendations + interim-analysis reports** — independent safety reviews and continue/modify/stop recommendations (blinded to sponsor as required). *FDA DMC Guidance (2006); ICH E6(R3) §5; Conditional (DSMB exists).*
- [ ] **Protocol deviation / violation log + notes to file** — departures from protocol/GCP and their handling; reportable deviations to IRB. *ICH E6(R3) §2/§6; 21 CFR 312.66, 56.108(b); Confirmed.*
- [ ] **Correspondence log** (sponsor/IRB/FDA/partner) + significant communications. *ICH E6(R3) App C; Confirmed.*

## 5. Regulatory maintenance records

- [ ] **[[annual-reporting-and-amendments|Protocol amendments]] + IRB re-approval** — substantive changes require FDA amendment (312.30) and IRB approval **before** implementation, except to eliminate an immediate hazard. *21 CFR 312.30, 56.108(a)/56.110, 312.66; Confirmed.*
- [ ] **[[irb-review-workflow|IRB continuing review]] / annual re-approval + expedited approvals** — FDA-regulated research still requires continuing review under Part 56 (contrast the 2018 Common Rule's removal for some minimal-risk studies). *21 CFR 56.108(a), 56.109(f), 56.115; Confirmed.*
- [ ] **[[ind-annual-report-dsur|IND Annual Report]]** — within 60 days of the IND anniversary; prior year's progress, safety, accrual, plans. ICH **E2F DSUR** may substitute. *21 CFR 312.33; Confirmed.* See [[annual-reporting-and-amendments]].

## 6. Investigational product and logistics records

- [ ] **[[drug-accountability-log|Drug accountability (ongoing)]] + shipment/receipt records + temperature logs** — continuous chain of custody and storage-condition evidence; monitor reconciles. *21 CFR 312.57, 312.61, 312.62(a); Confirmed.*

## 7. Personnel and facility currency records

- [ ] **Updated CVs / licenses / training + delegation-log updates** — kept current as staff change; new investigators added via **1572 update**. *21 CFR 312.53(c); ICH E6(R3) §2; Confirmed.*
- [ ] **New-staff financial disclosures (3454/3455)** — for any added investigator/sub-investigator. *21 CFR 54.4; Confirmed.*
- [ ] **Updated lab certifications / normal-range revisions** — any change during the trial captured for correct result interpretation. *42 CFR Part 493; Confirmed.*

## Sponsor-investigator collapse during conduct

The most consequential collapse is in **safety reporting**. For an external sponsor, IND safety reports flow *to* the site; for a [[sponsor-investigator]], the physician **originates** the 7-day/15-day report to FDA and to any other participating investigators, and files it to the [[irb-iec|IRB]] — a self-directed obligation that does not lighten because there is only one entity. Likewise, the investigator's SAE-to-sponsor report and the sponsor's evaluation of it become a single internal step, but the causality determination and the outward FDA/IRB filings remain. See [[safety-reporting-lifecycle]].

## How OSSICRO drives the conduct record set

> [!interpretive] OSSICRO position
> During conduct OSSICRO operates primarily as a **timing and completeness engine**. The [[safety-clock-engine|safety-clock engine]] computes the 7/15-day deadline from the human causality determination and escalates as the clock runs — it never makes the causality call and never transmits the report. The [[completeness-ledger]] keeps the conduct checklist live (green/amber/red) as records accrue; the [[draft-provenance-model]] carries each drafted narrative span (e.g., a MedWatch narrative) back to its source datum and citation for the Part-11 audit trail ([[part-11-and-ai-credibility]]). Cross-document consistency checks flag, for example, an amendment not yet reflected in the IRB-approved ICF version.

> [!warning] Non-delegable
> During conduct the gated acts are: **administration of consent** (each subject), **SAE causality/expectedness** (each event), **the decision to submit** each safety report and amendment, and the **IRB's** continuing-review and amendment-approval judgments. OSSICRO drafts, checks, times, and routes; qualified humans judge, sign, and file. See [[non-delegable-functions-and-gates]].

## Related
- [[document-catalog]]
- [[startup-tmf-checklist]]
- [[closeout-tmf-checklist]]
- [[conduct-and-monitoring]]
- [[safety-reporting-lifecycle]]
- [[safety-report-timelines-7-15-day]]
- [[ind-safety-report]]
- [[form-fda-3500a-medwatch]]
- [[ind-annual-report-dsur]]
- [[annual-reporting-and-amendments]]
- [[medical-monitor]]
- [[non-delegable-functions-and-gates]]
- [[safety-clock-engine]]
- [[completeness-ledger]]

## Sources
- [ICH E6(R3) Step 4 Final Guideline — Appendix C](https://database.ich.org/sites/default/files/ICH_E6(R3)_Step4_FinalGuideline_2025_0106.pdf)
- [eCFR — 21 CFR 312.32 (IND safety reporting)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
- [eCFR — 21 CFR 312.33 (annual reports)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.33)
- [eCFR — 21 CFR 312.64 (investigator recordkeeping and reports)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.64)
- [eCFR — 21 CFR 56.109 (IRB review, including continuing review)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56/section-56.109)
- [FDA — Safety Reporting Requirements for INDs and BA/BE Studies (guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-reporting-requirements-inds-investigational-new-drug-applications-and-babe-bioavailability)
- [ICH E2A — Clinical Safety Data Management: Definitions and Standards for Expedited Reporting](https://database.ich.org/sites/default/files/E2A_Guideline.pdf)
