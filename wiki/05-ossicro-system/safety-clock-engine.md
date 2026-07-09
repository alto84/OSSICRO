---
title: "The Safety-Clock Engine — 7/15-Day Deadline Computation and Escalation; Never Files, Never Decides Causality"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "21 CFR 312.32 (IND safety reporting: definitions (a); review (b); 15-day (c)(1); 7-day (c)(2); follow-up (d))"
  - "21 CFR 312.33 (annual reports); 312.56(d) (discontinuation); 312.64(b) (investigator SAE reporting)"
  - "ICH E2A (expedited-reporting definitions and standards)"
  - "Federal Register 75 FR 59935 (Sept 29, 2010, final rule)"
tags: [ossicro/engine, ossicro/gating, cfr/312, ich/e2a, ich/e2f, lifecycle/safety, role/medical-monitor, role/sponsor, role/pharmacovigilance-safety, status/interpretive]
aliases: ["Safety Clock Engine", "Safety Timers", "Deadline Engine"]
updated: 2026-07-09
---

# The Safety-Clock Engine — 7/15-Day Deadline Computation and Escalation

> [!authority] Governing authority
> [21 CFR 312.32](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32) sets the deadlines the engine computes: the **15-calendar-day** IND safety report (§312.32(c)(1)), the **7-calendar-day** report for unexpected fatal or life-threatening suspected adverse reactions (§312.32(c)(2)), and the follow-up duty (§312.32(d)); definitions are at §312.32(a), harmonized with ICH E2A, in the framework of [75 FR 59935 (Sept. 29, 2010)](https://www.govinfo.gov/content/pkg/FR-2010-09-29/html/2010-24296.htm). Adjacent clocks: [312.33](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.33) (annual report within 60 days of the IND anniversary), [312.56(d)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56) (discontinuation within 5 working days), [312.64(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.64) (investigator's immediate SAE report to the sponsor). Status: **Mixed** — the deadlines are black-letter; the engine that computes and escalates them is the OSSICRO design position.

The safety-clock engine is the dedicated OSSICRO subsystem that **computes regulatory safety deadlines and escalates as they run**. It exists because a missed expedited-report deadline is among the most damaging failures available to a [[sponsor-investigator]] — a compliance defect that is also a subject-protection defect — and because the *timeliness* layer of safety reporting is genuinely computable even though the *classification* layer never is. The engine's contract is two hard negatives stated up front: **it never files anything with FDA, and it never makes (or nudges) the seriousness/expectedness/causality determination.** It takes the qualified human's determinations as input, computes the correct clock from the correct start event, and makes it structurally difficult for a deadline to pass unnoticed. The regulatory content of the two clocks is specified on [[safety-report-timelines-7-15-day]]; the end-to-end routing is on [[safety-reporting-workflow]]; this page specifies the engine.

## Scope — what the engine owns and what it never touches

| Owned by the engine (computable) | Never touched (human judgment) |
|---|---|
| Deadline arithmetic (calendar-day and working-day) | Seriousness determination (§312.32(a)) |
| Correct start-event selection per clock | "Life-threatening" assessment |
| Escalation scheduling and delivery | Expectedness against the current [[investigators-brochure|IB]] |
| Clock state, audit logging, breach recording | Causality — "reasonable possibility" |
| Report-shell drafting and completeness checks | The decision that a report is owed |
| Recipient-list assembly (FDA, all investigators, IRB, DSMB) | Submission to FDA; any transmission to a regulator |

## The clocks it computes

| Clock | Authority | Duration | Starts on | Owner of the trigger |
|---|---|---|---|---|
| 7-day expedited (unexpected fatal/life-threatening suspected adverse reaction) | [312.32(c)(2)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32) | ≤ 7 **calendar** days | Sponsor's **initial receipt** of the information | [[medical-monitor]] / sponsor classifies; receipt itself is a recorded fact |
| 15-day expedited (SUSAR; qualifying aggregate/other findings; clinically important rate increase) | [312.32(c)(1)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32) | ≤ 15 **calendar** days | Sponsor's **determination** that the information qualifies | [[medical-monitor]] / sponsor |
| Complete written follow-up to a 7-day notification | 312.32(c)(2) | as a 15-day IND safety report | The 7-day report event | Sponsor |
| Follow-up with new information | [312.32(d)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32) | "as soon as … available"; a new qualifying determination re-arms a 15-day clock | New determination | Sponsor |
| IND annual report / DSUR | [312.33](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.33); ICH E2F | within 60 days of the IND anniversary date | IND effective-date anniversary (fixed, computable in advance) | Sponsor ([[ind-annual-report-dsur]]) |
| Unreasonable-risk discontinuation | [312.56(d)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56) | ≤ 5 **working** days | Sponsor's determination of unreasonable and significant risk | Sponsor |
| Investigator SAE report to sponsor | [312.64(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.64) | **immediately** (serious AEs); promptly (non-serious per protocol) | Investigator's awareness of the event | Investigator |
| Emergency individual expanded access — written submission | [312.310(d)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.310) | ≤ 15 **working** days after FDA's emergency authorization | The emergency authorization | Physician ([[expanded-access-workflow]]) |

Two semantics the engine must not blur. First, **the two expedited clocks start on different events**: the 7-day clock runs from *initial receipt* (urgency does not wait for full assessment); the 15-day clock runs from the *qualifying determination*. Conflating them under-counts the 7-day urgency. Second, **units differ**: §312.32's clocks are calendar days; §312.56(d) and §312.310(d) are working days. Each clock object carries its unit and computes accordingly; day-boundary handling is conservative (the deadline is the earliest defensible reading, never the latest).

## Clock lifecycle

Each clock is an object in the [[data-model]] — `{trigger, authority, start_event, start_timestamp, unit, deadline, owner, escalation_policy, state}` — moving through an explicit state machine:

1. **`ARMED`** — a captured serious event awaits the human classification. On capture, the engine records the receipt timestamp (which may already be running the 7-day clock if the case is fatal/life-threatening on its face pending confirmation) and pre-computes *candidate* deadlines for both clocks.
2. **`RUNNING`** — the qualified human has entered the §312.32(a) determinations; the engine resolves which clock applies, fixes the correct start event, and schedules escalations.
3. **`ESCALATING`** — threshold crossings fire the escalation ladder (below).
4. **`CLOSED`** — a human has performed and recorded the accountable act (FDA submission, investigator notification). The engine verifies the act is *recorded*, never performs it.
5. **`BREACHED`** — the deadline passed without the recorded act. A breach is written to the Part 11 audit trail and surfaced prominently; it is never suppressed or auto-resolved. Late submission with an explanation is the human's corrective path; the engine's duty is to make the lateness undeniable and documented.

Every state transition is written to the time-stamped, independent audit trail ([21 CFR 11.10(e)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10)); a running clock with an unmet human gate appears as an amber item on the [[completeness-ledger]] ("awaiting seriousness/expectedness/causality determination by [named medical monitor]").

## Escalation ladder

Escalation runs through the [[communication-hub]], on a policy proportional to remaining time — representative defaults, tunable in the [[safety-management-plan]]:

- **On capture:** notify the [[medical-monitor|medical monitor / safety physician]] and the [[sponsor-investigator]] that a case awaits classification, with the candidate deadlines shown.
- **Mid-clock and approaching deadline** (e.g., T−3 and T−1 for a 15-day clock; T−2 and T−1 for a 7-day clock): re-notify the owner; copy the [[micro-cro-accountable-layer|Micro-CRO]] where it holds a transferred safety-reporting obligation under a [[transfer-of-regulatory-obligations-toro|TORO]].
- **Deadline day:** highest-salience notification to every accountable human on the study.
- **Breach:** logged, surfaced on every dashboard, and included in the record that rolls up to the [[ind-annual-report-dsur|annual report]] and to [[dsmb-workflow|DSMB]] materials.

Escalation recipients and content respect roles: the IRB receives what IRB policy and [21 CFR 56.108(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56/subpart-B/section-56.108) require (unanticipated problems), all participating investigators receive IND safety reports per §312.32(c)(1), and the DSMB receives per its [[dsmb-charter|charter]] — the engine assembles the recipient list; humans authorize each transmission.

> [!warning] Non-delegable
> **The trigger is a medical judgment; the filing is a human act.** Seriousness, life-threatening status, expectedness, and causality under [21 CFR 312.32(a)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32) belong to the sponsor's qualified [[medical-monitor|medical monitor]] (in the [[sponsor-investigator]] model, the physician wearing the sponsor hat; see [[pharmacovigilance-safety]]). The engine must never auto-classify a SUSAR, never machine-set expectedness against the IB, never score "reasonable possibility," and never rank or suggest a causality answer. Equally, **submission to FDA is an explicit human-authorized action** — the engine prepares the [[form-fda-3500a-medwatch|Form 3500A]]/narrative draft and opens the submission task; a named human reviews, signs, and files. A deadline computed by software does not shift accountability: the §312.32 obligation remains the sponsor's regardless of any tool. See [[non-delegable-functions-and-gates]].

> [!interpretive] OSSICRO position
> Three design positions, none required by regulation: (1) **Conservative pre-arming** — on capture of any serious case, both candidate clocks are computed from the receipt timestamp before classification, so a slow determination can never *create* time; the regulation's 15-day clock formally runs from the determination, but a system that displays only that clock invites determination-drift. (2) **Breach visibility as a feature** — the engine's value in an inspection ([[fda-as-counterparty|BIMO]]) is a complete, honest timeliness record, including breaches; a tool that hid lateness would be worse than no tool. (3) **A dedicated subsystem** — safety deadlines get their own engine, separate from general milestone tracking, because their failure mode is patient-safety-relevant and their semantics (dual start events, mixed day-units, re-arming follow-ups) are too easy to get subtly wrong inside a generic scheduler.

## Engine behavior in the generate/check/validate frame

- **Generate:** drafts the report shell ([[ind-safety-report]], [[form-fda-3500a-medwatch]]) from captured case data, with every populated span carrying provenance ([[draft-provenance-model]]).
- **Check:** confirms the four minimum case elements (identifiable patient, reporter, suspect product, event), IND/protocol identifiers, and recipient-list completeness before the report can be authorized.
- **Validate:** holds the draft behind the §312.32(a) determination gate; on classification, resolves clock and start event, escalates as time runs, and opens the human-authorized submission and notification tasks — never advancing past a gate on its own ([[generate-check-validate-engine]]).

## Related
- [[safety-report-timelines-7-15-day]]
- [[safety-reporting-workflow]]
- [[safety-reporting-lifecycle]]
- [[ind-safety-report]]
- [[form-fda-3500a-medwatch]]
- [[safety-management-plan]]
- [[medical-monitor]]
- [[pharmacovigilance-safety]]
- [[sponsor-investigator]]
- [[ind-annual-report-dsur]]
- [[dsmb-workflow]]
- [[communication-hub]]
- [[completeness-ledger]]
- [[data-model]]
- [[generate-check-validate-engine]]
- [[non-delegable-functions-and-gates]]
- [[expanded-access-workflow]]
- [[part-11-and-ai-credibility]]

## Sources
- [21 CFR 312.32 — IND safety reporting (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
- [21 CFR 312.33 — Annual reports (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.33)
- [21 CFR 312.56 — Review of ongoing investigations (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56)
- [21 CFR 312.64 — Investigator reports (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.64)
- [21 CFR 312.310 — Individual patients, including for emergency use (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.310)
- [Federal Register 75 FR 59935 — IND Safety Reporting Requirements, Final Rule (Sept 29, 2010)](https://www.govinfo.gov/content/pkg/FR-2010-09-29/html/2010-24296.htm)
- [FDA — Safety Reporting Requirements for INDs and BA/BE Studies (guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-reporting-requirements-inds-and-babe-studies)
- [ICH E2A — Clinical Safety Data Management: Definitions and Standards for Expedited Reporting](https://www.ich.org/page/efficacy-guidelines)
- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
