---
title: "Monitoring Plan — Risk-Based Monitoring, Critical-to-Quality Factors, and Quality Tolerance Limits"
section: "03-documents"
status: mixed
governing_authority:
  - "ICH E6(R3) Section 5 (Quality Management; Monitoring) and Section 6.9"
  - "21 CFR 312.50; 21 CFR 312.53(d); 21 CFR 312.56"
  - "FDA Guidance: A Risk-Based Approach to Monitoring of Clinical Investigations (2013, rev. 2023)"
tags: [role/monitor, role/sponsor, gcp/e6r3, lifecycle/conduct, ossicro/engine, ossicro/gating, status/mixed]
aliases: ["monitoring plan", "RBM plan", "risk-based monitoring plan", "clinical monitoring plan"]
updated: 2026-07-09
---

# Monitoring Plan — Risk-Based Monitoring, CtQ Factors, and Quality Tolerance Limits

> [!authority] Governing authority
> ICH E6(R3) §5 (sponsor quality management, risk-based quality management, monitoring) and §6.9; 21 CFR 312.50 and 312.56 (sponsor duty to monitor the progress of all investigations); 21 CFR 312.53(d) (selection of qualified monitors); FDA Guidance "A Risk-Based Approach to Monitoring of Clinical Investigations" (2013, revised 2023). Status: **Mixed** — the sponsor's obligation to monitor and to document a monitoring strategy is **confirmed**; the *risk-proportionate form* of that strategy (centralized/statistical monitoring in lieu of default 100% SDV) is the current standard under E6(R3) but its encoding in OSSICRO's engine is an **interpretive** position, and the monitor's judgments remain a non-delegable human function.

The **monitoring plan** is the sponsor's written strategy for overseeing the conduct and progress of a clinical investigation so as to protect participants and ensure the reliability of reported data. Under [21 CFR 312.56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56) the sponsor must monitor all investigations under its IND; ICH E6(R3) §5 elevates *how* by requiring a **risk-based** design built on identified **critical-to-quality (CtQ) factors** and governed by pre-specified **quality tolerance limits (QTLs)**. For a [[sponsor-investigator]], the monitoring obligation is part of the sponsor half of the dual role; the plan may be executed by a qualified [[clinical-monitor-cra|monitor/CRA]] or, where warranted, the [[micro-cro-accountable-layer|micro-CRO layer]].

OSSICRO generates the monitoring-plan template, tracks visit completion, and computes QTL excursions against incoming data. It does not perform the monitoring judgments — source-data verification decisions, deviation adjudication, root-cause assessment — which belong to the qualified monitor.

## The E6(R3) shift: quality by design, not fixed checklists

E6(R3) (FDA-adopted 9 September 2025; EMA effective 23 July 2025) reframes monitoring around **risk-proportionality**. The prior default of 100% on-site source-data verification is replaced by a strategy that concentrates effort on the data and processes that matter most to participant safety and result reliability. The plan is therefore a *design artifact*, not a checklist: it names what is critical, states the risks to it, and allocates monitoring proportionately.

> [!interpretive] OSSICRO position
> This proportionality is precisely the shift the OSSICRO [[generate-check-validate-engine]] encodes: the "check" pass is not a fixed universal list but a **risk-proportionate essential-records matrix** keyed to the study's CtQ factors. The engine's contribution is to make the risk assessment explicit, cited, and versioned — never to decide, on its own, that a risk is acceptable. See [[risk-based-monitoring-e6r3]].

## Plan section map

| # | Section | Contents | Basis |
|---|---------|----------|-------|
| 1 | **Scope and objectives** | The investigation(s) covered; participant-protection and data-reliability objectives | 21 CFR 312.56; E6(R3) §5 |
| 2 | **Critical-to-quality (CtQ) factors** | The attributes essential to meaningful, reliable results and participant safety (eligibility, consent, primary endpoint, key safety data, IP accountability) | E6(R3) §5.1 |
| 3 | **Risk assessment** | For each CtQ factor: what can go wrong, likelihood, detectability, impact; the risk register | E6(R3) §5.1 |
| 4 | **Quality tolerance limits (QTLs)** | Pre-specified thresholds on parameters where a deviation beyond the limit signals a systemic quality problem; the review/escalation trigger | E6(R3) §5.1 (QTLs) |
| 5 | **Monitoring methods and mix** | Centralized/statistical monitoring; on-site visits; remote monitoring; the proportionate blend | FDA 2013/2023 RBM; E6(R3) §6.9 |
| 6 | **Source-data verification (SDV) approach** | Targeted/risk-based SDV rather than 100% default; which data verified, at what sampling | FDA 2013/2023 RBM; E6(R3) §6.9 |
| 7 | **Visit types and cadence** | [[monitoring-workflow-siv-imv-cov|SIV, IMV/routine, COV]] triggers and frequency | E6(R3) §6.9; visit reports are essential records |
| 8 | **Monitor qualifications** | Training/experience of the monitor(s) | 21 CFR 312.53(d) |
| 9 | **Reporting and follow-up** | Visit reports; findings; follow-up letters; escalation path | E6(R3) §6.9 |
| 10 | **Deviation/issue management and escalation** | How findings and QTL excursions are triaged, root-caused, and corrected (CAPA) | E6(R3) §5 |
| 11 | **Documentation / TMF filing** | Where monitoring records live; the auditable trail | E6(R3) essential records; [[record-retention-and-archival]] |

## Critical-to-quality (CtQ) factors

CtQ factors are the small set of attributes without which the trial cannot yield reliable, ethically defensible results. Canonical early-phase CtQ factors: **eligibility determination** (right participants), **informed consent** (valid, documented), **primary-endpoint data** (accurate, complete), **key safety data** (SAEs captured and reported on time), and **investigational-product accountability** ([[drug-accountability-log]]). The plan states each CtQ factor, the risks to it, and the monitoring allocated to protect it. OSSICRO seeds a CtQ register from the protocol and study attributes; the sponsor/monitor confirms and adjusts it — the register is a proposal for human judgment.

## Quality tolerance limits (QTLs)

A **QTL** is a pre-specified threshold on a quality parameter — e.g., a rate of eligibility deviations, consent-timing deviations, missing primary-endpoint data, or overdue SAE reporting — beyond which the sponsor concludes a *systematic* problem may exist and reviews for root cause. QTLs are distinct from individual protocol deviations: they detect **patterns**, not single events. E6(R3) requires QTLs where appropriate and requires that excursions be evaluated and documented.

> [!interpretive] OSSICRO position
> OSSICRO's [[completeness-ledger|centralized-monitoring layer]] computes QTL parameters continuously from the study's structured data and raises an **amber** ledger state — a human-review trigger — when a parameter crosses its QTL. The engine **computes and escalates**; it does not decide that an excursion is or is not a systemic problem, does not author the root-cause finding, and does not close the excursion. Every computation carries its source data and citation per the [[draft-provenance-model]] so the monitor's review rests on an auditable trail. This mirrors the [[safety-clock-engine]] pattern: automate the arithmetic and the alarm, never the judgment.

## Non-delegable gate

> [!warning] Non-delegable
> Monitoring **judgments** — whether a source-data discrepancy is material, whether a protocol deviation is reportable, the root-cause assessment of a QTL excursion, the adequacy of a site's corrective action, and the decision to escalate to securing compliance or discontinuing a non-compliant investigator (21 CFR 312.56(b)) — are the qualified [[clinical-monitor-cra|monitor's]] and the sponsor's human responsibilities. OSSICRO schedules visits, computes QTL parameters, drafts visit-report and follow-up-letter templates, and surfaces excursions; it never adjudicates a deviation, never certifies a site as compliant, and never closes a monitoring finding. The sponsor's ultimate accountability for monitoring is not transferable to software (21 CFR 312.52; E6(R3) §5 oversight). See [[non-delegable-functions-and-gates]].

## OSSICRO engine behavior
- **Generate:** produces the risk-based monitoring-plan draft with a CtQ register and candidate QTLs derived from the protocol; produces SIV/IMV/COV visit-report and follow-up-letter templates.
- **Check:** validates the plan carries all required sections (CtQ factors, risk assessment, QTLs, method mix, SDV approach, monitor qualifications, escalation); flags an absent CtQ register or absent QTLs.
- **Validate:** computes QTL parameters from incoming structured data and raises human-review triggers on excursions; reconciles the plan with the [[safety-management-plan]] and [[dsmb-charter]]; holds every excursion in a gated state pending the monitor's assessment. It never advances or closes a finding autonomously.

## Related
- [[clinical-monitor-cra]]
- [[risk-based-monitoring-e6r3]]
- [[monitoring-workflow-siv-imv-cov]]
- [[safety-management-plan]]
- [[dsmb-charter]]
- [[completeness-ledger]]
- [[safety-clock-engine]]
- [[draft-provenance-model]]
- [[drug-accountability-log]]
- [[sponsor]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 312.56 — Review of ongoing investigations](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56)
- [21 CFR 312.50 — General responsibilities of sponsors](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.50)
- [FDA — A Risk-Based Approach to Monitoring of Clinical Investigations (2013, rev. 2023)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/risk-based-approach-monitoring-clinical-investigations-questions-and-answers)
- [ICH E6(R3) Good Clinical Practice — Step 4 Final Guideline (2025)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA — E6(R3) Good Clinical Practice (GCP) guidance page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
