---
title: "Conduct and Monitoring"
section: "02-lifecycle"
status: mixed
governing_authority:
  - "21 CFR 312.56 (review of ongoing investigations)"
  - "21 CFR 312.60–312.62, 312.68–312.69 (investigator conduct duties)"
  - "21 CFR 312.57–312.58 (sponsor records and inspection)"
  - "ICH E6(R3) Annex 1 §§2–4 and Appendix C"
  - "FDA Risk-Based Monitoring guidance (2013; Q&A 2023)"
tags: [lifecycle/conduct, cfr/312, cfr/11, ich/e6r3, role/monitor, ossicro/gating, status/confirmed, status/interpretive]
aliases: ["trial conduct", "study monitoring", "source data and CRFs"]
updated: 2026-07-09
---

# Conduct and Monitoring

> [!authority] Governing authority
> [21 CFR 312.56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56) (sponsor review of ongoing investigations); 21 CFR 312.60–312.62 (investigator conduct, drug control, case histories); 21 CFR 312.57–312.58, 312.68 (records and FDA inspection); ICH E6(R3) Annex 1 §3 (sponsor oversight and monitoring) and §4 (data governance); FDA guidance *Oversight of Clinical Investigations — A Risk-Based Approach to Monitoring* (2013) and its 2023 Q&A. Status: **Mixed** — recordkeeping and oversight duties are confirmed; the software-assisted centralized-monitoring boundary is an interpretive OSSICRO position.

Conduct runs from first enrollment to last-subject-last-visit. Four record streams must stay continuously true during this window — source data, CRFs, monitoring evidence, and drug accountability — while deviations are detected, judged, and reported. The parallel safety stream (AE→SAE→expedited report) has its own page: [[safety-reporting-lifecycle]]. This page covers the data and oversight spine; [[closeout]] covers its termination.

## Source data and case histories

The investigator must prepare and maintain **adequate and accurate case histories** recording all observations and other data pertinent to the investigation on each individual; case histories include the CRFs and supporting source documents (hospital and clinic charts, study worksheets), and must document that informed consent was obtained prior to participation (21 CFR 312.62(b)). E6(R3) Annex 1 §4 sets the data-governance standard: source data must be **ALCOA++** — attributable, legible, contemporaneous, original, accurate, plus complete, consistent, enduring, and available. Operationally:

- Original observations are recorded once, at the point of observation, in the designated source (EHR, source worksheet); the protocol-specific source-document plan fixes, per data element, what the source *is*, so monitors and inspectors never guess.
- Corrections preserve the original entry: single-line strike-through with initials, date, and reason on paper; a computer-generated, time-stamped audit trail in electronic systems (21 CFR 11.10(e); [[part-11-and-ai-credibility]]).
- Where chart data flow in via [[smart-on-fhir-integration|SMART-on-FHIR ingestion]], the EHR remains the source; OSSICRO's copy carries provenance back to the source datum ([[draft-provenance-model]]).
- Retention: investigator records are kept 2 years after marketing-application approval for the indication, or 2 years after the investigation is discontinued and FDA notified (21 CFR 312.62(c)); see [[record-retention-and-archival]].

## CRFs and data flow

The case report form is the sponsor-designed instrument for reporting protocol-required data per subject (blank version filed at [[site-activation|activation]]; completed CRFs and their correction audit trail are essential records — ICH E6(R3) Appendix C; E6(R2) §8.3.13–8.3.14). Data flow: source → CRF/eCRF entry by delegated staff ([[delegation-of-authority-log]]) → edit checks and queries → investigator's signature attesting the CRF data are accurate and complete. That signature is an accountable act; query responses that change data must trace to source. eCRF systems operate under Part 11 (validation, audit trails, access control, e-signatures).

## Monitoring

Monitoring is a **sponsor obligation**: the sponsor must monitor the progress of all investigations under its IND (21 CFR 312.50, 312.56(a)) through a monitor qualified by training and experience (312.53(d)), executing the written [[monitoring-plan|risk-based monitoring plan]]. E6(R3) (FDA-adopted September 2025) makes risk-proportionality the governing frame: monitoring focuses on critical-to-quality factors and critical data/processes, combines centralized/remote and on-site methods, and sets quality tolerance limits — 100% source-data verification is no longer the default expectation (ICH E6(R3) Annex 1 §3; FDA RBM guidance 2013/2023; [[risk-based-monitoring-e6r3]]).

**Interim monitoring visits (IMVs)** during conduct verify, at risk-scaled depth: presence and version-correctness of every executed ICF against the enrollment log; targeted SDV/source-data review of critical data (eligibility, endpoints, SAEs); [[drug-accountability-log|IP accountability]] and storage conditions; delegation-log currency against staff actually performing tasks; deviation identification; and ISF completeness ([[regulatory-binder-isf-index]]). Each visit yields a **monitoring visit report** to the sponsor TMF and a follow-up letter to the site with findings and required actions — essential records evidencing 312.56(a) oversight ([[monitoring-workflow-siv-imv-cov]], [[conduct-tmf-checklist]]).

**Escalation is regulated.** If an investigator does not comply with the signed 1572 agreement, the general investigational plan, or Part 312, the sponsor must promptly either **secure compliance or** discontinue drug shipments, **end the investigator's participation**, require drug return/disposition per 312.59, and notify FDA (21 CFR 312.56(b)). If the sponsor determines the drug presents an **unreasonable and significant risk** to subjects, it must discontinue the affected investigations as soon as possible and no later than **5 working days** after the determination, notify FDA, all IRBs, and all investigators, and assure drug disposition (312.56(d)). In the [[sponsor-investigator]] model these are self-executing duties; the [[micro-cro-accountable-layer|micro-CRO]] may hold the monitoring function under a written [[transfer-of-regulatory-obligations-toro|TORO]] (21 CFR 312.52), becoming subject to the same regulatory action as a sponsor for it.

> [!warning] Non-delegable
> The monitor is a qualified **human** (21 CFR 312.53(d)); monitoring-finding judgments — whether a discrepancy is a deviation, whether a pattern threatens subject safety or data reliability, whether escalation under 312.56(b) is warranted — are human determinations. So are the sponsor's compliance and unreasonable-risk decisions (312.56(b),(d)) and every causality/expectedness call in the parallel safety stream ([[medical-monitor]], 21 CFR 312.32). OSSICRO computes, flags, drafts, and timestamps; qualified humans judge and sign. See [[non-delegable-functions-and-gates]].

## Protocol deviations

No CFR section defines "protocol deviation"; the operative rules are: the investigator conducts the study according to the protocol (21 CFR 312.60; Form 1572 Field 9) and makes **no changes without IRB approval except to eliminate apparent immediate hazards to subjects** (21 CFR 312.66, 56.108(a)(4)); emergency departures are reported promptly to the IRB and sponsor. During conduct: deviations are captured on a deviation log with root cause and corrective action; those meeting the IRB's promptly-reportable criteria (typically deviations affecting subject safety, rights, or data integrity) go to the IRB per its written policy; recurring deviations are a monitoring signal requiring sponsor action under 312.56(b); important protocol deviations are ultimately disclosed in the [[clinical-study-report|CSR]] (ICH E3). Eligibility deviations deserve special flagging: prospective "waivers" of entry criteria have no regulatory basis — the compliant paths are amendment or non-enrollment.

## Drug accountability during conduct

The investigator administers the drug only to subjects under the investigator's (or a responsible subinvestigator's) personal supervision and supplies it to no one not authorized to receive it (21 CFR 312.61). The site maintains **disposition records** — dates, quantities, use by subjects (312.62(a)) — reconciled against the sponsor's shipment records (312.57(a)); storage conditions are maintained and logged; unused supplies are returned or destroyed per 312.59 with documentation. Controlled substances require securely locked, substantially constructed storage with diversion precautions (312.69). The running [[drug-accountability-log]] is verified at every IMV and must reconcile exactly at [[closeout]].

## Inspection readiness

Both halves of the record are open to FDA throughout conduct: the investigator must permit access to, copying, and verification of 312.62 records on request of an authorized FDA officer at reasonable times (21 CFR 312.68 — subject identities may ordinarily be withheld), and the sponsor likewise for sponsor records (312.58). BIMO inspection readiness is therefore a standing property of the TMF/ISF, not a pre-inspection scramble ([[fda-interactions-meetings-holds]], [[fda-as-counterparty]]).

## OSSICRO's function during conduct

OSSICRO maintains the conduct-phase [[completeness-ledger]] (every expected record per visit per subject: green/amber/red), runs cross-record consistency checks (enrollment log ↔ executed ICFs ↔ CRF subjects ↔ accountability log), drives visit scheduling and the deviation and re-consent flags, drafts monitoring visit reports and follow-up letters from the monitor's structured findings, and computes the safety clocks ([[safety-clock-engine]]). Every AI-drafted artifact carries provenance and lands in a human review lane ([[single-pass-review-ux]], [[draft-provenance-model]]).

> [!interpretive] OSSICRO position
> **The software-assisted monitoring boundary.** E6(R3) legitimizes centralized monitoring; OSSICRO's centralized analytics (outlier detection, enrollment-rate and query-rate signals, cross-site comparisons, missing-record detection) are an *input to* the qualified monitor's and sponsor's judgment, not a monitoring actor. The system's outputs are flags and drafts; no threshold crossing ever auto-triggers a 312.56(b) action, a deviation classification, or an IRB report. This boundary is an OSSICRO design position implementing confirmed law (312.50, 312.53(d), 312.56), and it is enforced in code as a gate, not observed as a custom.

## Related

- [[enrollment-and-consent]] — the preceding stage; consent verification is a core IMV task
- [[safety-reporting-lifecycle]] — the parallel AE/SAE/expedited-report stream
- [[monitoring-plan]] · [[risk-based-monitoring-e6r3]] · [[monitoring-workflow-siv-imv-cov]] · [[clinical-monitor-cra]]
- [[drug-accountability-log]] · [[delegation-of-authority-log]] · [[conduct-tmf-checklist]]
- [[annual-reporting-and-amendments]] — amendments, IB updates, continuing review during conduct
- [[closeout]] · [[record-retention-and-archival]] — where conduct records terminate
- [[medical-monitor]] · [[micro-cro-accountable-layer]] · [[transfer-of-regulatory-obligations-toro]]
- [[part-11-and-ai-credibility]] · [[draft-provenance-model]] · [[completeness-ledger]] · [[safety-clock-engine]]
- [[non-delegable-functions-and-gates]]

## Sources

- [21 CFR Part 312, Subpart D — Responsibilities of Sponsors and Investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D)
- [21 CFR 312.56 — Review of ongoing investigations (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56)
- [21 CFR 312.62 — Investigator recordkeeping and record retention (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.62)
- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [ICH E6(R3) Guideline for Good Clinical Practice, Step 4 Final (6 Jan 2025)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf) — FDA adopted September 2025
- [FDA Guidance — Oversight of Clinical Investigations: A Risk-Based Approach to Monitoring (2013)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/oversight-clinical-investigations-risk-based-approach-monitoring)
- [FDA Guidance — A Risk-Based Approach to Monitoring of Clinical Investigations: Questions and Answers (2023)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/risk-based-approach-monitoring-clinical-investigations-questions-and-answers)
- [FDA Guidance — Investigator Responsibilities: Protecting the Rights, Safety, and Welfare of Study Subjects (2009)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigator-responsibilities-protecting-rights-safety-and-welfare-study-subjects)
