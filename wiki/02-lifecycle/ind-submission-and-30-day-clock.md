---
title: "IND Submission & the 30-Day Clock"
section: "02-lifecycle"
status: confirmed
governing_authority:
  - "21 CFR 312.40 (conditions for use; when an IND goes into effect; the 30-day period)"
  - "21 CFR 312.42 (clinical holds and requests for modification)"
  - "21 CFR 312.20–312.23 (IND requirement, content, format)"
tags: [lifecycle/ind, cfr/312, fda-form/1571, role/fda, role/sponsor-investigator, status/confirmed]
aliases: ["30-Day Clock", "Safe to Proceed", "Clinical Hold", "IND Submission"]
updated: 2026-07-09
---

# IND Submission & the 30-Day Clock

> [!authority] Governing authority
> [21 CFR 312.40](https://www.ecfr.gov/current/title-21/section-312.40) (conditions for using an investigational new drug in a clinical investigation; when an IND goes into effect; the 30-day period); [21 CFR 312.42](https://www.ecfr.gov/current/title-21/section-312.42) (clinical holds and requests for modification); [21 CFR 312.20](https://www.ecfr.gov/current/title-21/section-312.20)–[312.23](https://www.ecfr.gov/current/title-21/section-312.23) (IND requirement, content, format). Status: **Confirmed** (citations re-verified against Cornell LII, 2026-07-09).

Submitting the IND starts a statutory waiting period. Under [21 CFR 312.40(b)](https://www.ecfr.gov/current/title-21/section-312.40), an IND goes into effect — and a clinical investigation may begin — either (1) **30 calendar days after FDA receives the IND**, unless FDA notifies the sponsor within that window that the investigations are subject to a **clinical hold** under [21 CFR 312.42](https://www.ecfr.gov/current/title-21/section-312.42); or (2) on **earlier notification** by FDA that the investigations may begin. This "safe-to-proceed by default" mechanism — silence-plus-30-days equals authorization — is the operative gate between IND preparation and site activation, and it is one of the two independent authorizations (the other being IRB approval) that must both clear before any subject is enrolled. OSSICRO computes and tracks this clock precisely; it never submits, and it never treats clock expiry as permission to dose without confirming the parallel IRB and site-activation gates.

## Submission and the IND number

The assembled IND package (see [[pre-ind-and-ind-preparation]] and [[ind-application-312-23]]) is submitted to the appropriate review center — **CDER** for most drugs, **CBER** for biologics — with a signed **Form FDA 1571** cover. Commercial INDs are filed electronically in **eCTD** format through the FDA Electronic Submissions Gateway; sponsor-investigator INDs may be accepted in alternative formats consistent with current FDA policy and the 2015 sponsor-investigator IND draft guidance. On receipt, FDA:

- assigns a **six-digit IND number**, which thereafter identifies every submission to that IND (amendments, safety reports, annual reports);
- sends an **acknowledgment letter** stating the IND number and the **date of receipt** — the date from which the 30-day clock is counted;
- routes the IND to the responsible review division for the 30-day safety review.

The IND number and the receipt date are load-bearing metadata: they anchor the clock, key every downstream submission, and must appear consistently across the [[document-catalog|TMF]]. See [[fda-as-counterparty]].

## The 30-day clock (312.40)

[21 CFR 312.40](https://www.ecfr.gov/current/title-21/section-312.40) sets the mechanics. Its subsections are frequently miscited; the accurate structure is:

- **312.40(a)** — *conditions for use.* An investigational new drug may be used in a clinical investigation only if (a)(1) the sponsor has submitted an IND that is **in effect** under paragraph (b) and complies with all applicable requirements of Part 312 and **Parts 50 and 56**, and (a)(2) each participating investigator conducts the investigation in compliance with Part 312 and Parts 50 and 56. IRB review and approval flow through Part 56; the **signed investigator agreement (Form FDA 1572)** is required separately under [21 CFR 312.53(c)](https://www.ecfr.gov/current/title-21/section-312.53), not under 312.40(a).
- **312.40(b)** — *when the IND goes into effect.* **(b)(1)** — 30 days after FDA receives the IND, **unless** FDA notifies the sponsor within that period that the investigations are subject to a clinical hold under 312.42; **(b)(2)** — on earlier FDA notification that the investigations may begin.
- **312.40(c)** — *shipment.* A sponsor may **ship** the investigational drug to named investigators once the IND is in effect (30 days after FDA receipt, or on earlier FDA authorization). This subsection governs shipment, **not** the clinical-hold power.
- **312.40(d)** — *administration bar.* An **investigator may not administer** the investigational drug to human subjects until the IND is **in effect** under paragraph (b).

The **clinical-hold power itself lives in [312.42](https://www.ecfr.gov/current/title-21/section-312.42)**; it enters the 30-day clock through the exception in 312.40(b)(1) (a hold prevents the IND from going into effect). The clock is measured from FDA's **receipt date**, not the sponsor's send date. During the 30 days FDA conducts its initial safety review; **silence is authorization** — if FDA imposes no hold, the IND goes into effect and the investigation may begin on day 31.

> [!warning] Non-delegable
> The decision to **begin dosing** — i.e., to treat the 30-day clock as satisfied and enrollment as authorized — is the sponsor-investigator's regulated act, and it is lawful only when the IND is in effect (no hold), IRB approval is documented ([[irb-submission-and-approval]]), and the site is activated ([[site-activation]]). OSSICRO computes the day-31 date and the state of every parallel gate and presents a consolidated "clear-to-enroll" view; it does **not** authorize enrollment. A qualified human confirms all gates and makes the call. See [[non-delegable-functions-and-gates]].

## The clinical hold (312.42)

A **clinical hold** is an FDA order to delay a proposed investigation or to suspend an ongoing one ([21 CFR 312.42(a)](https://www.ecfr.gov/current/title-21/section-312.42)). It may apply to the entire IND or to a specific protocol. The grounds are organized by study type under [312.42(b)](https://www.ecfr.gov/current/title-21/section-312.42):

- **Phase 1 studies — 312.42(b)(1).** FDA may impose a hold if (b)(1)(i) human subjects are or would be exposed to an **unreasonable and significant risk** of illness or injury; (b)(1)(ii) the clinical investigators are **not qualified** by scientific training and experience; (b)(1)(iii) the **investigator's brochure is misleading, erroneous, or materially incomplete**; or (b)(1)(iv) the IND **does not contain sufficient information** required under 312.23 to assess subject risk; or (b)(1)(v) the drug is intended to treat a life-threatening disease or condition and men or women with reproductive potential are excluded from eligibility solely because of a risk or potential risk of reproductive or developmental toxicity from the investigational drug.
- **Phase 2 or 3 studies — 312.42(b)(2).** Any of the Phase 1 grounds, **or** the plan or protocol is **clearly deficient in design** to meet its stated objectives.
- **Expanded-access / treatment protocols — 312.42(b)(3).** A hold may issue if the criteria of subpart I are not satisfied or the expanded-access submission fails to comply with subpart I.
- **Studies not designed to be adequate and well-controlled — 312.42(b)(4).** Distinct grounds including that the protocol would impede enrollment in, or otherwise interfere with, a concurrent controlled trial; insufficient drug supply; a demonstrated lack of effectiveness; a better benefit/risk alternative; or that the drug has already received marketing approval for the same indication and population.

Process ([312.42(c)–(e)](https://www.ecfr.gov/current/title-21/section-312.42)):

- **312.42(c)** — FDA ordinarily **discusses the deficiency** with the sponsor and attempts resolution before imposing the hold, except where subject safety requires immediate action.
- **312.42(d)** — as soon as possible, and **no more than 30 days** after imposing the hold, the Division Director provides the sponsor a **written explanation** of the basis for the hold.
- **312.42(e)** — when the sponsor submits, in writing, a **complete response** addressing every deficiency and requests removal of the hold, **FDA must respond in writing within 30 calendar days**; the hold is lifted only when FDA notifies the sponsor that the investigation may proceed.
- No subject may be enrolled or dosed under a held protocol until the hold is removed.

> [!warning] Non-delegable
> The **complete response** to a clinical hold is a substantive regulatory-scientific submission that resolves an FDA safety or adequacy concern; it is authored, reviewed, and submitted under the sponsor-investigator's accountability (ordinarily with regulatory counsel and the medical/scientific team). OSSICRO can assemble a response package mapped point-by-point to FDA's stated deficiencies and check it for completeness; the scientific content and the decision to submit are human. See [[fda-interactions-meetings-holds]].

## Interaction with the IRB clock (confirmed)

The 30-day FDA clock and IRB approval are **independent and both mandatory**. [312.40(a)](https://www.ecfr.gov/current/title-21/section-312.40) conditions use of the drug on compliance with **Part 56** (IRB review and approval) for each participating investigator, and [312.40(d)](https://www.ecfr.gov/current/title-21/section-312.40) bars administration until the IND is in effect; separately, [21 CFR 56.103](https://www.ecfr.gov/current/title-21/section-56.103) independently prohibits FDA-regulated research without prior IRB review and approval. Enrollment is gated on the **later** of: (a) day 31 (or earlier FDA "proceed" notice) with no hold in force, and (b) documented IRB approval. Neither clears the other. See [[irb-submission-and-approval]] and [[phase-model-overview]].

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
- [21 CFR 312.40 — Treatment of an investigational new drug; conditions for use and when an IND goes into effect (eCFR)](https://www.ecfr.gov/current/title-21/section-312.40) · [Cornell LII mirror](https://www.law.cornell.edu/cfr/text/21/312.40)
- [21 CFR 312.42 — Clinical holds and requests for modification (eCFR)](https://www.ecfr.gov/current/title-21/section-312.42) · [Cornell LII mirror](https://www.law.cornell.edu/cfr/text/21/312.42)
- [21 CFR 312.53 — Selecting investigators and monitors (signed Form FDA 1572) (eCFR)](https://www.ecfr.gov/current/title-21/section-312.53)
- [21 CFR 312.23 — IND content and format (eCFR)](https://www.ecfr.gov/current/title-21/section-312.23)
- [21 CFR 56.103 — Circumstances in which IRB review is required (eCFR)](https://www.ecfr.gov/current/title-21/section-56.103)
- [FDA — Clinical Holds and the IND process (FDA IND resources)](https://www.fda.gov/drugs/investigational-new-drug-ind-application/clinical-holds)
- [FDA Draft Guidance (2015) — INDs Prepared and Submitted by Sponsor-Investigators](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigational-new-drug-applications-prepared-and-submitted-sponsor-investigators)