---
title: "Monitoring Workflow — SIV / IMV / COV Visit Types, Reports, Follow-Up Letters, and TMF Filing"
section: "04-coordination"
status: mixed
governing_authority:
  - "21 CFR 312.56 (monitoring the progress of investigations)"
  - "21 CFR 312.53(d) (selecting qualified monitors)"
  - "ICH E6(R3) §5 (Sponsor: monitoring; risk-based quality management)"
  - "FDA Guidance — A Risk-Based Approach to Monitoring of Clinical Investigations (2013, rev. 2023)"
tags: [role/monitor, role/sponsor, cfr/312, gcp/e6r3, lifecycle/activation, lifecycle/conduct, lifecycle/closeout, ossicro/engine, status/mixed]
aliases: ["SIV", "IMV", "COV", "monitoring visits", "site initiation visit", "close-out visit", "monitoring workflow"]
updated: 2026-07-09
---

# Monitoring Workflow — SIV / IMV / COV, Reports, Follow-Up Letters, and TMF Filing

> [!authority] Governing authority
> Monitoring the progress of every investigation under an IND is a **sponsor obligation** ([21 CFR 312.56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56)); the monitor must be qualified by training and experience ([21 CFR 312.53(d)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53)). ICH E6(R3) §5 makes monitoring a risk-proportionate quality-management activity, and the FDA 2013/2023 risk-based monitoring guidance is the operating model. Status: **Mixed** — the visit sequence, the reports, and their status as essential records are confirmed; the line between what OSSICRO may schedule/track/assemble and the monitor's non-delegable verification judgment is an interpretive position, marked inline.

Monitoring is how the sponsor discharges its [21 CFR 312.56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56) duty to verify that a site protects participants, follows the protocol, and produces reliable data. It is executed by a **qualified human monitor** — the Clinical Research Associate ([[clinical-monitor-cra]]) — working from a written, risk-based [[monitoring-plan]] through a defined sequence of on-site and centralized activities. In a [[sponsor-investigator]] trial the sponsor-investigator holds the monitoring obligation; because a person cannot credibly monitor their own site, the function routes to the [[micro-cro-accountable-layer]] or an independent contract monitor. This page covers the **visit lifecycle** and its documentary output; the proportionality framework that governs *how much* verification each visit performs is on [[risk-based-monitoring-e6r3]].

## The three canonical visit types

| Visit | When | Purpose | Primary output |
|-------|------|---------|----------------|
| **SIV — Site Initiation Visit** | Before enrollment, after activation | Confirm training, delegation, IP readiness, essential-document completeness; formally "green-light" the site | SIV report + site-activation confirmation |
| **IMV — Interim / Routine Monitoring Visit** | Periodically during conduct | Verify consent execution, source data (SDV where risk warrants), IP accountability, protocol compliance, safety-reporting timeliness | IMV report + follow-up/action letter |
| **COV — Close-Out Visit** | At study end (or site termination) | Reconcile the site, IP accountability, query resolution, and TMF/ISF completeness | COV report + close-out confirmation |

### Site Initiation Visit (SIV)
The SIV **activates the site** and confirms readiness *before* the first participant is enrolled. The monitor verifies that site staff are trained on the protocol and procedures, that the [[delegation-of-authority-log]] is executed, that the investigational product has been received and can be stored/accounted for, that IRB approval and the executed [[clinical-trial-agreement-and-budget]] are in place, and that the [[regulatory-binder-isf-index|Investigator Site File]] is assembled. The SIV is the operational counterpart to the [[site-activation]] essential-document green-light: no enrollment before a documented SIV and the gates it confirms.

### Interim Monitoring Visit (IMV)
The IMV is the recurring conduct-phase visit. The monitor verifies:
- **Consent** — that a valid, current, IRB-approved [[informed-consent-form]] was executed for each enrolled participant *before* any study procedure (the [[informed-consent-document-vs-event|document vs. event]] distinction: the monitor verifies the record; the consent conversation itself was the investigator's non-delegable act).
- **Source data** — source-data verification / review (SDV/SDR) targeted to risk under E6(R3), not blanket 100% SDV (see [[risk-based-monitoring-e6r3]]).
- **Investigational product** — receipt, storage conditions, dispensing, and reconciliation against the [[drug-accountability-log]].
- **Protocol compliance** — eligibility, visit windows, and protocol deviations.
- **Safety reporting** — that SAEs were reported by the site to the sponsor within the protocol timeline and fed the [[safety-reporting-workflow]].

### Close-Out Visit (COV)
The COV reconciles the site at the end of participation: final IP accountability and return/destruction per the [[drug-accountability-log]], resolution of outstanding data queries, confirmation that all safety reports and deviations are filed, and a completeness check of the ISF/TMF. It feeds the trial-level [[closeout]] workflow.

## Visit reports and follow-up letters

Every visit produces a **monitoring visit report** and, for the IMV, a **follow-up / action letter** to the site enumerating findings and required corrective actions with due dates. These are the monitor's contemporaneous record of what was verified and what must be fixed, and they are **essential records** under ICH E6(R3) — they must be filed to the [Trial Master File](../02-lifecycle/record-retention-and-archival.md) and are subject to FDA inspection. The report is authored by the monitor from what the monitor observed; the follow-up letter's corrective-action items close a loop that the next IMV re-verifies.

> [!warning] Non-delegable
> The **verification judgment** at every visit — whether a source document supports a case-report-form entry, whether a deviation is significant, whether consent was validly obtained and documented, whether an IP discrepancy is a reconciliation error or a diversion — is the qualified monitor's determination under [21 CFR 312.53(d)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53) and [312.56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56). OSSICRO must never machine-declare a source-data field "verified," never auto-classify a deviation as non-significant, and never generate the substantive findings of a visit report. It schedules the visit, pre-assembles the checklist and the data pack, drafts the report *skeleton*, and tracks corrective-action closure — the human monitor supplies the findings and signs.

## TMF filing and the report lifecycle

Each report follows the document state machine (draft → checked → human-reviewed → signed → filed → archived) and lands in the TMF/ISF at the correct essential-records location, cross-referenced in the [[document-catalog]] and the [[regulatory-binder-isf-index]]. OSSICRO's coordination value here is the **completeness and timing loop**: it ensures a SIV report exists before enrollment, that IMV cadence matches the [[monitoring-plan]], that every follow-up-letter action item has an owner and a due date, and that a COV report and final reconciliation exist before [[closeout]]. Open corrective actions surface on the [[completeness-ledger]] as amber items until a human closes them.

> [!interpretive] OSSICRO position
> OSSICRO treats the *administrative envelope* of monitoring — scheduling against the risk-based cadence, assembling the visit checklist and the centralized-monitoring data pack, drafting the report skeleton, tracking action-item closure, and filing to the correct TMF slot — as automatable, and the *verification and findings* as non-delegable. The centralized/statistical-monitoring signals that direct on-site effort (outlier detection, query trends, enrollment/eligibility anomalies) are generated by the engine as **flags for the monitor**, never as verification conclusions. Every auto-populated field carries its source provenance per the [[draft-provenance-model]] for the Part-11 audit trail; the monitor's findings and signature are what convert a skeleton into an essential record.

## OSSICRO engine behavior

- **Generate:** drafts SIV/IMV/COV report skeletons and follow-up-letter templates pre-populated with site, protocol, and (for the IMV) the centralized-monitoring data pack.
- **Check:** confirms the enrollment gate (documented SIV + IRB approval + executed agreements) before allowing site activation; verifies IMV cadence conforms to the [[monitoring-plan]]; confirms a COV and final IP reconciliation exist before closeout.
- **Validate:** holds each visit report in a gated state until the qualified monitor supplies findings and signs; opens a tracked corrective-action item for every follow-up-letter finding and re-surfaces open items on the [[completeness-ledger]]; files the signed report to the correct TMF/ISF essential-records location.

## Related
- [[clinical-monitor-cra]]
- [[risk-based-monitoring-e6r3]]
- [[monitoring-plan]]
- [[site-activation]]
- [[conduct-and-monitoring]]
- [[closeout]]
- [[drug-accountability-log]]
- [[informed-consent-document-vs-event]]
- [[safety-reporting-workflow]]
- [[regulatory-binder-isf-index]]
- [[document-catalog]]
- [[completeness-ledger]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 312.56 — Review of ongoing investigations](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56)
- [21 CFR 312.53 — Selecting investigators and monitors](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53)
- [FDA — Oversight of Clinical Investigations: A Risk-Based Approach to Monitoring (2013, rev. 2023)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/oversight-clinical-investigations-risk-based-approach-monitoring)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06, PDF)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA — E6(R3) Good Clinical Practice (Sept 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
