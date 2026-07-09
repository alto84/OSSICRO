---
title: "IND Submission & the 30-Day Clock"
section: "02-lifecycle"
status: confirmed
governing_authority:
  - "21 CFR 312.40 (general requirements; the 30-day waiting period)"
  - "21 CFR 312.42 (clinical holds and requests for modification)"
  - "21 CFR 312.20–312.23 (IND requirement, content, format)"
tags: [lifecycle/ind, cfr/312, fda-form/1571, role/fda, role/sponsor-investigator, status/confirmed]
aliases: ["30-Day Clock", "Safe to Proceed", "Clinical Hold", "IND Submission"]
updated: 2026-07-09
---

# IND Submission & the 30-Day Clock

> [!authority] Governing authority
> [21 CFR 312.40](https://www.ecfr.gov/current/title-21/section-312.40) (general requirements for use of an investigational new drug in a clinical investigation; the 30-day waiting period); [21 CFR 312.42](https://www.ecfr.gov/current/title-21/section-312.42) (clinical holds and requests for modification); [21 CFR 312.20](https://www.ecfr.gov/current/title-21/section-312.20)–[312.23](https://www.ecfr.gov/current/title-21/section-312.23) (IND requirement, content, format). Status: **Confirmed**.

Submitting the IND starts a statutory waiting period. Under [21 CFR 312.40(b)](https://www.ecfr.gov/current/title-21/section-312.40), a sponsor may begin a clinical investigation only after (1) the IND has been submitted to FDA and (2) **30 calendar days have elapsed** from FDA's receipt of the IND — unless FDA notifies the sponsor earlier that studies may begin, or unless FDA imposes a **clinical hold** ([21 CFR 312.42](https://www.ecfr.gov/current/title-21/section-312.42)) that prohibits or restricts the investigation. This "safe-to-proceed by default" mechanism — silence-plus-30-days equals authorization — is the operative gate between IND preparation and site activation, and it is one of the two independent authorizations (the other being IRB approval) that must both clear before any subject is enrolled. OSSICRO computes and tracks this clock precisely; it never submits, and it never treats clock expiry as permission to dose without confirming the parallel IRB and site-activation gates.

## Submission and the IND number

The assembled IND package (see [[pre-ind-and-ind-preparation]] and [[ind-application-312-23]]) is submitted to the appropriate review center — **CDER** for most drugs, **CBER** for biologics — with a signed **Form FDA 1571** cover. Commercial INDs are filed electronically in **eCTD** format through the FDA Electronic Submissions Gateway; sponsor-investigator INDs may be accepted in alternative formats consistent with current FDA policy and the 2015 sponsor-investigator IND draft guidance. On receipt, FDA:

- assigns a **six-digit IND number**, which thereafter identifies every submission to that IND (amendments, safety reports, annual reports);
- sends an **acknowledgment letter** stating the IND number and the **date of receipt** — the date from which the 30-day clock is counted;
- routes the IND to the responsible review division for the 30-day safety review.

The IND number and the receipt date are load-bearing metadata: they anchor the clock, key every downstream submission, and must appear consistently across the [[document-catalog|TMF]]. See [[fda-as-counterparty]].

## The 30-day clock (312.40)

[21 CFR 312.40](https://www.ecfr.gov/current/title-21/section-312.40) sets the mechanics:

- **312.40(a)** — the sponsor must have submitted an IND meeting 312.23, and each participating investigator must have the necessary IRB approval and a signed agreement, before the drug is administered.
- **312.40(b)(1)** — the sponsor may **not** begin a clinical investigation until **30 days after FDA receives the IND**, except as provided in 312.40(b)(2).
- **312.40(b)(2)** — the sponsor **may** begin earlier if FDA notifies the sponsor that investigations may proceed.
- **312.40(c)** — FDA may, at any time during the 30 days, impose a clinical hold under 312.42.
- **312.40(d)** — the sponsor may not begin, and must continue to withhold or restrict, if FDA has imposed a hold.

The clock is measured from FDA's **receipt date**, not the sponsor's send date. During the 30 days FDA conducts its initial safety review; **silence is authorization** — if FDA does not act, the IND goes into effect and the investigation may begin on day 31.

> [!warning] Non-delegable
> The decision to **begin dosing** — i.e., to treat the 30-day clock as satisfied and enrollment as authorized — is the sponsor-investigator's regulated act, and it is lawful only when the IND is in effect (no hold), IRB approval is documented ([[irb-submission-and-approval]]), and the site is activated ([[site-activation]]). OSSICRO computes the day-31 date and the state of every parallel gate and presents a consolidated "clear-to-enroll" view; it does **not** authorize enrollment. A qualified human confirms all gates and makes the call. See [[non-delegable-functions-and-gates]].

## The clinical hold (312.42)

A **clinical hold** is an FDA order to delay a proposed investigation or to suspend an ongoing one ([21 CFR 312.42(a)](https://www.ecfr.gov/current/title-21/section-312.42)). It may apply to the entire IND or to a specific protocol. Grounds vary by phase; the principal statutory/regulatory grounds under [312.42(b)](https://www.ecfr.gov/current/title-21/section-312.42) include:

- **subjects would be exposed to an unreasonable and significant risk** of illness or injury;
- the clinical investigators are **not qualified** by training and experience;
- the **investigator's brochure is misleading, erroneous, or materially incomplete**;
- the IND **does not contain sufficient information** required under 312.23 to assess subject risk;
- (Phase 2/3) the plan or protocol is **clearly deficient** in design to meet its stated objectives;
- for certain expanded-access/treatment protocols, additional 312.42(b)(2)–(b)(4) grounds.

Process ([312.42(c)–(e)](https://www.ecfr.gov/current/title-21/section-312.42)):

- FDA ordinarily **discusses the deficiency** with the sponsor first (except where subject safety requires immediate action) and then issues the hold.
- FDA provides written notice of the hold, specifying the reasons, within **30 days** of imposition.
- The sponsor responds with a **complete response** addressing every deficiency.
- FDA must respond to a complete response within **30 days**; the hold is lifted only when FDA notifies the sponsor that the investigation may proceed.
- No subject may be enrolled or dosed under a held protocol until the hold is removed.

> [!warning] Non-delegable
> The **complete response** to a clinical hold is a substantive regulatory-scientific submission that resolves an FDA safety or adequacy concern; it is authored, reviewed, and submitted under the sponsor-investigator's accountability (ordinarily with regulatory counsel and the medical/scientific team). OSSICRO can assemble a response package mapped point-by-point to FDA's stated deficiencies and check it for completeness; the scientific content and the decision to submit are human. See [[fda-interactions-meetings-holds]].

## Interaction with the IRB clock (confirmed)

The 30-day FDA clock and IRB approval are **independent and both mandatory**. [312.40(a)](https://www.ecfr.gov/current/title-21/section-312.40) requires IRB approval for each participating investigator before administration; [21 CFR 56.103](https://www.ecfr.gov/current/title-21/section-56.103) independently prohibits FDA-regulated research without prior IRB review and approval. Enrollment is gated on the **later** of: (a) day 31 (or earlier FDA "proceed" notice) with no hold in force, and (b) documented IRB approval. Neither clears the other. See [[irb-submission-and-approval]] and [[phase-model-overview]].

## What OSSICRO tracks at this phase

- **Clock computation.** Receipt date → day-31 safe-to-proceed date; a live countdown surfaced in the milestone tracker.
- **Hold-state tracking.** Records any FDA communication and any hold; if a hold is in force, the "clear-to-enroll" state is forced red regardless of clock expiry.
- **Consolidated gate view.** The intersection of (IND in effect) × (IRB approved) × (site activated); enrollment is surfaced as authorized only when all three are green and a human confirms.
- **Safety-clock handoff.** Once dosing may begin, the [[safety-clock-engine]] takes over the 7-day/15-day IND-safety-report deadlines under [[safety-reporting-lifecycle]].

> [!interpretive] OSSICRO position
> Treating "clear-to-enroll" as the **logical AND of three independent authorizations** (FDA clock, IRB approval, site activation) — and forcing the state red on any hold or missing approval — is an OSSICRO design encoding of the regulatory dependencies. The individual authorizations are black-letter; the consolidated gate is OSSICRO's implementation and is flagged as such. It never substitutes for the human's own verification.

## Related
- [[index]]
- [[phase-model-overview]]
- [[pre-ind-and-ind-preparation]]
- [[ind-application-312-23]]
- [[irb-submission-and-approval]]
- [[site-activation]]
- [[fda-interactions-meetings-holds]]
- [[fda-as-counterparty]]
- [[safety-clock-engine]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 312.40 — General requirements for use of an investigational new drug in a clinical investigation (eCFR)](https://www.ecfr.gov/current/title-21/section-312.40)
- [21 CFR 312.42 — Clinical holds and requests for modification (eCFR)](https://www.ecfr.gov/current/title-21/section-312.42)
- [21 CFR 312.23 — IND content and format (eCFR)](https://www.ecfr.gov/current/title-21/section-312.23)
- [21 CFR 56.103 — Circumstances in which IRB review is required (eCFR)](https://www.ecfr.gov/current/title-21/section-56.103)
- [FDA — Clinical Holds and the IND process (FDA IND resources)](https://www.fda.gov/drugs/investigational-new-drug-ind-application/clinical-holds)
- [FDA Draft Guidance (2015) — INDs Prepared and Submitted by Sponsor-Investigators](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigational-new-drug-applications-prepared-and-submitted-sponsor-investigators)
