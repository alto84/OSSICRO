---
title: "Coordination — How the Oversight Bodies Are Fed, Timed, and Connected"
section: "04-coordination"
status: mixed
governing_authority:
  - "21 CFR 312.32-312.33, 312.50-312.56, 312.66"
  - "21 CFR Part 56; 21 CFR Part 50"
  - "45 CFR Part 46 (revised Common Rule)"
  - "ICH E6(R3)"
tags: [lifecycle/conduct, lifecycle/irb, lifecycle/safety, role/irb, role/dsmb, role/monitor, cfr/312, cfr/56, cfr/50, ich/e6r3, ossicro/engine, ossicro/gating]
aliases: [coordination]
updated: 2026-07-09
---

# Coordination — How the Oversight Bodies Are Fed, Timed, and Connected

> [!authority] Governing authority
> 21 CFR Part 312 (sponsor/investigator duties, safety reporting), 21 CFR Parts 50/56 (consent, IRB), 45 CFR Part 46 (Common Rule), ICH E6(R3) as adopted by FDA September 9, 2025. Status: **Mixed** — the obligations are black-letter; the framing of coordination as OSSICRO's automatable layer is an OSSICRO position.

A clinical trial under an IND is not run by one entity. It is run by a set of legally distinct bodies — sponsor, investigator (or the collapsed [[sponsor-investigator]]), [[irb-iec|IRB/IEC]], [[dsmb-dmc|DSMB/DMC]], the qualified [[clinical-monitor-cra|monitor]], the [[pharmacovigilance-safety|safety function]], the [[pharma-partner-sponsor|pharma partner]], and [[fda-as-counterparty|FDA]] — each of which must be **fed** the right documents, **timed** against regulatory clocks, and **connected** to the others through defined reporting arrows. Every failure mode of an under-resourced site is a coordination failure: a consent version the IRB never approved, a 15-day safety clock that started silently, a continuing-review lapse that voids approval. This section maps those workflows.

## The three coordination problems

1. **Feeding.** Each body acts only on a defined document set: the IRB on the [[irb-submission-package]], the DSMB on the packet the independent statistician prepares, FDA on the IND and its amendments, the monitor on source and the [[regulatory-binder-isf-index|ISF]]. The [[document-catalog]] defines what each record is; this section defines who must receive it.
2. **Timing.** The trial runs on hard clocks: the 30-day IND safe-to-proceed ([[ind-submission-and-30-day-clock]]), the 7- and 15-day IND safety reports ([[safety-report-timelines-7-15-day]], 21 CFR 312.32(c)), continuing IRB review at least annually for FDA-regulated studies (21 CFR 56.109(f)), and the IND annual report within 60 days of the IND anniversary (21 CFR 312.33; [[ind-annual-report-dsur]]).
3. **Connecting.** A single event can obligate four arrows at once — one serious, unexpected, suspected adverse reaction flows investigator → sponsor → FDA **and** all participating investigators **and** the IRB **and** the DMC. The canonical arrows are drawn in [[inter-entity-document-flow-map]].

> [!interpretive] OSSICRO position
> The coordination layer — assembly, routing, deadline computation, version control, completeness checking — is exactly where CRO labor cost concentrates and is automatable. The judgment cores inside each body are not. OSSICRO's engine ([[generate-check-validate-engine]]) times and routes; it never approves, consents, adjudicates causality, or recommends stopping. See [[non-delegable-functions-and-gates]].

> [!warning] Non-delegable
> Every workflow in this section terminates in a human or committee judgment that software must gate, never own: the IRB's approval decision (21 CFR 56.109; 56.111), the consent event (21 CFR 50.20), causality/expectedness (21 CFR 312.32(a)), the DMC's continue/modify/stop recommendation and the sponsor's decision on it, and every release of a submission to FDA.

## Pages in this section

| Page | What it covers |
|---|---|
| [[inter-entity-document-flow-map]] | The canonical arrow diagram: every document, origin → destination, trigger, and clock |
| [[irb-review-workflow]] | Initial, continuing, and expedited IRB review; amendments; the ethics gate on enrollment |
| [[single-irb-mandate-and-central-irbs]] | 45 CFR 46.114 sIRB mandate; NIH policy; WCG/Advarra; SMART IRB and IREx reliance mechanics |
| [[informed-consent-document-vs-event]] | The bright line between the consent document (draftable) and the consent event (never delegable) |
| [[dsmb-workflow]] | Charter adoption, meeting cadence, open/closed sessions, the statistician firewall, recommendations |
| [[monitoring-workflow-siv-imv-cov]] | Site initiation, interim, and close-out visits; visit reports; TMF filing |
| [[risk-based-monitoring-e6r3]] | Centralized/statistical monitoring, proportionality, critical-to-quality factors under E6(R3) |
| [[safety-reporting-workflow]] | End-to-end pharmacovigilance routing from site AE capture to FDA submission and notifications |
| [[safety-report-timelines-7-15-day]] | The two expedited clocks; serious/unexpected/suspected definitions; follow-up duties |
| [[sponsor-cro-site-coordination]] | MSA/task-order/TORO relationships; who is enforceable for what; the sponsor-investigator collapse |
| [[pharma-partner-interface-iis]] | Medical Affairs routing, feasibility, portal interoperability, what pharma needs from a new site |
| [[single-patient-site-and-pharma-acceptance]] | The pharma-side backend that makes a one-physician, one-patient site acceptable |
| [[expanded-access-coordination]] | Physician ↔ manufacturer ↔ FDA ↔ IRB concurrence for expanded access |
| [[fda-interactions-meetings-holds]] | Pre-IND meetings, clinical-hold response, BIMO inspection readiness |

## The clock inventory (quick reference)

| Clock | Duration | Authority |
|---|---|---|
| IND safe-to-proceed | 30 calendar days after FDA receipt | 21 CFR 312.40(b) |
| Fatal/life-threatening unexpected suspected adverse reaction | 7 calendar days | 21 CFR 312.32(c)(2) |
| Serious + unexpected + suspected adverse reaction (SUSAR) | 15 calendar days | 21 CFR 312.32(c)(1) |
| Follow-up safety information | 15 calendar days | 21 CFR 312.32(d) |
| IND annual report / DSUR | within 60 days of IND anniversary | 21 CFR 312.33 |
| IRB continuing review (FDA-regulated) | intervals appropriate to risk, ≥ once/year | 21 CFR 56.109(f) |
| Investigator SAE report to sponsor | immediately | 21 CFR 312.64(b) |

Deadline computation and escalation for the safety clocks is the [[safety-clock-engine]]'s dedicated job; the [[communication-hub]] carries the routed artifacts.

## Related

- [[entity-map]] — the six coordinating entities and their legal relationships
- [[guiding-scenario]] — the narrative these workflows serve
- [[non-delegable-functions-and-gates]] — the master gating matrix
- [[document-catalog]] — what each record is; this section covers where it goes
- [[two-modes-site-vs-sponsor-investigator]] — how the arrows differ in Mode A vs Mode B

## Sources

- [21 CFR Part 312 (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312)
- [21 CFR Part 56 (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56)
- [21 CFR Part 50 (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50)
- [45 CFR Part 46 (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46)
- [ICH E6(R3) Step 4 Final Guideline (Jan 6, 2025, PDF)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA — E6(R3) Good Clinical Practice adoption (Sept 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
