---
title: "FDA Interactions: Pre-IND Meetings, Clinical Holds, and BIMO Inspection Readiness"
section: "04-coordination"
status: mixed
governing_authority:
  - "21 CFR 312.40 (IND in effect; 30-day clock)"
  - "21 CFR 312.42 (clinical holds and requests for modification)"
  - "21 CFR 312.47 (meetings with FDA)"
  - "21 CFR 312.23 / 312.82 (IND content; early consultation)"
  - "FDA BIMO Compliance Program 7348.811 (clinical investigator inspections)"
tags: [role/fda, role/sponsor, role/sponsor-investigator, cfr/312, lifecycle/ind, ossicro/gating, status/mixed]
aliases: ["FDA meetings", "pre-IND meeting", "clinical hold response", "BIMO readiness", "Type A B C meetings"]
updated: 2026-07-09
---

# FDA Interactions: Pre-IND Meetings, Clinical Holds, and BIMO Inspection Readiness

> [!authority] Governing authority
> 21 CFR 312.40 (conditions for an IND to go into effect; the 30-day clock); 21 CFR 312.42 (clinical holds and requests for modification); 21 CFR 312.47 (meetings between sponsors and FDA); 21 CFR 312.23 and 312.82 (IND content and early consultation for life-threatening/severely-debilitating illnesses); FDA guidance *Formal Meetings Between the FDA and Sponsors or Applicants of PDUFA Products* (meeting types, timelines); FDA Compliance Program 7348.811 (BIMO clinical-investigator inspections). Status: **Mixed** — the 30-day clock, the hold mechanics, and the meeting framework are black-letter or binding guidance (confirmed); OSSICRO's readiness-package and response-drafting design are interpretive.

FDA is a **counterparty**, not a service the sponsor buys. Three interactions define the relationship across an early-phase IND: the **pre-IND meeting** (align on the plan before filing), the **[30-day clock and clinical hold](../02-lifecycle/ind-submission-and-30-day-clock.md)** (the gate that lets — or stops — the study), and **BIMO inspection** (the Agency's on-site verification of conduct). For a solo [sponsor-investigator](../01-roles-responsibilities/sponsor-investigator.md), managing these directly is one of the most intimidating parts of holding an IND, and it is exactly where OSSICRO's coordination value is high — provided every substantive representation to the Agency remains a human's own, signed statement.

## Pre-IND meetings

The **pre-IND meeting** is the sponsor's opportunity to align with the FDA review division on the development plan, the adequacy of nonclinical data to support first-in-human dosing, the proposed clinical protocol, CMC, and the content of the planned IND — before the resources of a full submission are committed. For products for **life-threatening or severely-debilitating illnesses**, § 312.82 explicitly invites **early consultation** (pre-IND and end-of-Phase-1 meetings) to reach agreement on the design of the initial studies.

### The formal-meeting framework (meeting types)

FDA's PDUFA formal-meeting guidance sorts meetings into categories with different response and scheduling targets:

| Type | Purpose | FDA scheduling target (typical) |
|------|---------|--------------------------------|
| **Type A** | Critically needed to move a stalled program (e.g., clinical-hold resolution, dispute resolution) | ~30 days |
| **Type B** | Milestone meetings — **pre-IND**, end-of-Phase-1 (for §312.82 products), end-of-Phase-2, pre-NDA/BLA | ~60 days |
| **Type B (EOP)** | End-of-phase | ~70 days |
| **Type C** | Any other meeting about development of a product | ~75 days |
| **Type D / INTERACT** | Narrow-issue or very-early (pre-pre-IND) meetings | per current guidance |

The mechanics of requesting a meeting: a **meeting request** stating the product, meeting type, objectives, and proposed questions; then a **meeting package / briefing document** submitted ahead of the meeting with the data and specific questions on which FDA's advice is sought. FDA may grant the meeting, deny it, or respond via **written responses only** (WRO) in lieu of a live meeting.

> [!warning] Non-delegable
> **The scientific and regulatory positions a sponsor puts before FDA — the proposed dose rationale, the safety argument, the answers to FDA's questions, and every representation in a briefing document — are the sponsor's own statements, made by a qualified human who can stand behind them.** OSSICRO can assemble the meeting request and structure the briefing package; it cannot author the Agency-facing scientific judgment or attest to it. The sponsor-investigator (or a qualified regulatory professional) owns and signs. See [non-delegable-functions-and-gates](../05-ossicro-system/non-delegable-functions-and-gates.md).

## The 30-day clock (21 CFR 312.40)

An IND goes into effect **30 calendar days after FDA receives** it, **unless** FDA notifies the sponsor sooner that the studies may begin, **or** FDA places the IND on **clinical hold** (§ 312.40(b)). The sponsor **may not begin** a clinical investigation until the 30 days have elapsed without a hold or FDA affirmatively authorizes an earlier start. The clock is a safety gate: it gives FDA a fixed window to review for unreasonable risk before humans are dosed. See [ind-submission-and-30-day-clock](../02-lifecycle/ind-submission-and-30-day-clock.md).

## Clinical holds (21 CFR 312.42)

A **clinical hold** is an order FDA issues to **delay a proposed investigation or suspend an ongoing one**. Grounds for a Phase 1 hold under § 312.42(b)(1) include: subjects would be exposed to **unreasonable and significant risk**; the clinical investigators are not qualified; the [Investigator's Brochure](../03-documents/investigators-brochure.md) is misleading, erroneous, or materially incomplete; or the IND does not contain sufficient information to assess subject risk. Additional grounds apply to Phase 2/3 (including a deficient protocol design to meet stated objectives).

### The hold-response cycle

```
FDA imposes hold (usually by telephone, confirmed in a hold letter stating the deficiencies)
      │
      ├──► No new subjects dosed; ongoing subjects may continue only if FDA concurs
      │
      ├──► Sponsor submits a COMPLETE RESPONSE addressing EACH deficiency in the hold letter
      │
      └──► FDA has 30 DAYS from receipt of the complete response to act (§312.42(e));
               study may resume only on FDA notification that the hold is lifted
```

The operative discipline: FDA acts within **30 days of a complete response**, so a *complete* response — one that addresses **every** enumerated deficiency — is what starts that clock. A partial response does not. This is a completeness problem of exactly the kind OSSICRO's check/validate passes are built for: map each deficiency in the hold letter to the responsive element in the reply, and refuse to mark the response "complete" until every item is closed.

> [!interpretive] OSSICRO position
> On a clinical hold, OSSICRO parses the hold letter into a **deficiency ledger** (one row per enumerated deficiency), drafts the responsive content for each, and runs a [completeness-ledger](../05-ossicro-system/completeness-ledger.md) gate that will not classify the response as filing-ready until every deficiency has a mapped, human-approved answer. The engine computes the § 312.42(e) 30-day review window as an informational deadline. What it does **not** do: decide whether the scientific response actually resolves FDA's safety concern, or represent to the Agency that it does — that judgment and that signature are the sponsor's. Status: interpretive as to the automation boundary.

## BIMO inspection readiness

FDA's **Bioresearch Monitoring (BIMO)** program inspects clinical investigators, sponsors, IRBs, and other parties to verify GCP compliance and data integrity. Clinical-investigator inspections run under **Compliance Program 7348.811**. An inspection may be **study-oriented** (tied to a marketing application), **investigator-oriented** (triggered by a complaint, high enrollment, or anomalous data), or **for-cause**. Outcomes are classified **NAI** (no action indicated), **VAI** (voluntary action indicated), or **OAI** (official action indicated); serious deficiencies can produce a **Form FDA 483** (inspectional observations) and, ultimately, a Warning Letter or [data rejection](../02-lifecycle/closeout.md).

Readiness is a standing property of the [Trial Master File](../03-documents/document-catalog.md) / [Investigator Site File](../03-documents/regulatory-binder-isf-index.md), not a scramble on notice. An inspection-ready site can produce, on demand and reconciled: the signed [1572](../03-documents/form-fda-1572-statement-of-investigator.md) and [delegation-of-authority log](../03-documents/delegation-of-authority-log.md); [IRB](irb-review-workflow.md) approvals and continuing reviews; signed, dated [consent forms](../03-documents/informed-consent-form.md) for every subject with consent obtained **before** any study procedure; source documents supporting each CRF; [drug-accountability](../03-documents/drug-accountability-log.md) records; [safety reports](safety-reporting-workflow.md) with documented reporting timelines; and protocol-deviation logs. The ALCOA++ integrity of these records (Attributable, Legible, Contemporaneous, Original, Accurate, plus Complete, Consistent, Enduring, Available) is what an inspection tests.

> [!warning] Non-delegable
> **The investigator's representations to an FDA inspector, the conduct being inspected, and the integrity of the source data are the accountable human's — never the software's.** OSSICRO can keep the TMF/ISF continuously inspection-ready and generate a readiness self-assessment, but it cannot stand for the investigator at an inspection, cannot attest that consent was properly obtained, and cannot substitute for real source data. A generated document that misrepresents what actually happened is a fabrication, not a compliance artifact; the [evidence-based-validation](../05-ossicro-system/compliance-mapping.md) discipline forbids it.

## What OSSICRO generates vs. what stays human

- **Generates (drafts for review):** the meeting request and structured briefing package; the IND completeness pre-check that reduces avoidable-hold risk; the hold-letter deficiency ledger and per-deficiency response drafts; a BIMO readiness self-assessment and a continuously-reconciled TMF/ISF index.
- **Stays human/entity (gated):** every scientific/regulatory position put before FDA; the decision that a hold response resolves the concern; the signature on Agency-facing submissions; and the investigator's representations and source-data integrity at an inspection.

## Related
- [[fda-as-counterparty]]
- [[ind-submission-and-30-day-clock]]
- [[pre-ind-and-ind-preparation]]
- [[ind-application-312-23]]
- [[investigators-brochure]]
- [[safety-reporting-workflow]]
- [[expanded-access-coordination]]
- [[sponsor-investigator]]
- [[completeness-ledger]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 312.40 — General requirements for use of an investigational new drug in a clinical investigation](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.40)
- [21 CFR 312.42 — Clinical holds and requests for modification](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.42)
- [21 CFR 312.47 — Meetings](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.47)
- [21 CFR 312.82 — Early consultation (life-threatening / severely-debilitating illnesses)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-E/section-312.82)
- [FDA Guidance — Formal Meetings Between the FDA and Sponsors or Applicants of PDUFA Products](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/formal-meetings-between-fda-and-sponsors-or-applicants-pdufa-products)
- [FDA — Bioresearch Monitoring (BIMO) Compliance Programs](https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-program-guidance-manual-cpgm/bioresearch-monitoring)
- [FDA Compliance Program 7348.811 — Clinical Investigators and Sponsor-Investigators (PDF)](https://www.fda.gov/media/75927/download)
