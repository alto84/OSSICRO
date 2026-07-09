---
title: "FDA as Counterparty — CDER/CBER, the 30-Day Clock, Clinical Hold, and BIMO"
section: "01-roles-responsibilities"
status: mixed
governing_authority:
  - "21 CFR 312.40 (treatment may begin — 30-day rule)"
  - "21 CFR 312.42 (clinical holds)"
  - "21 CFR 312.44 (termination)"
  - "21 CFR 312.58 (FDA inspection of sponsor records)"
  - "21 CFR 312.68 (inspection of investigator records)"
  - "FDA Compliance Program 7348.811 (BIMO — Clinical Investigators/Sponsors)"
tags: [role/fda, cfr/312, lifecycle/ind, status/mixed, ossicro/gating]
aliases: ["FDA", "CDER", "CBER", "the Agency", "BIMO"]
updated: 2026-07-09
---

# FDA as Counterparty — CDER/CBER, the 30-Day Clock, Clinical Hold, and BIMO

> [!authority] Governing authority
> FDA's counterparty role over an IND is defined by 21 CFR Part 312: the 30-day review clock (312.40), clinical hold authority (312.42), termination (312.44), and inspection (312.58, 312.68); BIMO inspections run under FDA Compliance Program 7348.811/7348.810. Status: **Mixed** — the regulatory mechanics are confirmed; what OSSICRO *submits vs. surfaces* and its inspection-readiness role are interpretive, marked inline.

FDA is not a party OSSICRO coordinates *between* — it is the regulator on the other side of the IND. The [[sponsor-investigator]] holds a direct, non-transferable relationship with the Agency: submissions, safety reports, and annual reports go from the sponsor to FDA, and FDA's authorities (hold, termination, inspection) act on the sponsor and investigator. Software neither submits to FDA in its own name nor receives FDA's determinations; it assembles the package a human authorizes and files, and it maintains the state that makes the sponsor-investigator inspection-ready.

## Which center: CDER vs. CBER

An IND is reviewed by the FDA center whose product class it falls in:

- **CDER (Center for Drug Evaluation and Research)** reviews small-molecule drugs and most therapeutic biologics (monoclonal antibodies, many recombinant proteins) — the majority of early-phase INDs.
- **CBER (Center for Biologics Evaluation and Research)** reviews vaccines, blood products, cellular and gene therapies, and certain other biologics.

The center assignment determines the review division, the reviewers (medical officer, pharm/tox, chemistry/CMC, clinical pharmacology, statistics), and the relevant guidance corpus. OSSICRO's [[pre-ind-and-ind-preparation]] workflow should route product class to the correct center so that the 312.23 package meets that center's expectations.

## The 30-day clock (21 CFR 312.40)

Filing an IND does not, by itself, permit dosing. Under **21 CFR 312.40**, a sponsor may begin a clinical investigation **30 days after FDA receives the IND**, unless FDA notifies the sponsor sooner that studies may begin, *or* places the study on **clinical hold** (312.42). The 30-day window is FDA's initial safety review — the Agency reads the protocol, the [[investigators-brochure]], the CMC and pharm/tox packages, and the [[form-fda-1571-ind-cover]] commitment, and decides whether it is safe to proceed.

> [!warning] Non-delegable
> **Beginning dosing is gated on the 30-day clock elapsing without a hold (or on affirmative FDA "may proceed").** OSSICRO computes and displays the day-30 date and blocks the enrollment/dosing gate until the clock is satisfied *and* documented IRB approval exists in the TMF — but the decision to dose the first subject is the sponsor-investigator's accountable act (see [[ind-submission-and-30-day-clock]] and [[non-delegable-functions-and-gates]]).

## Clinical hold (21 CFR 312.42)

A **clinical hold** is an FDA order to delay a proposed investigation or suspend an ongoing one. It may apply to the entire IND or to a specific protocol. The grounds (312.42(b)) include: unreasonable and significant risk to subjects; investigators not qualified; a misleading, erroneous, or materially incomplete [[investigators-brochure]]; or insufficient information to assess risk (and, for Phase 2/3, a deficient protocol design). On hold, **no new subjects may be enrolled and subjects already enrolled may not receive the investigational drug** unless FDA permits it for safety. FDA provides the reasons (initially by telephone, then in a written hold letter within 30 days), and the sponsor responds with a **complete response** addressing every deficiency; FDA has 30 days from a complete response to act. See [[fda-interactions-meetings-holds]].

> [!warning] Non-delegable
> **The clinical-hold response is a substantive regulatory and medical rebuttal authored and signed by the sponsor-investigator (with medical/CMC input).** OSSICRO can assemble the response package, track the deficiency-by-deficiency closure, and manage the 30-day clocks, but the scientific answers and the attestation are human. A hold is lifted only by FDA.

## Termination and inactivation

Beyond hold, FDA may **terminate** an IND (312.44) for serious deficiencies or noncompliance, following (except in emergencies) a proposal-and-comment process. The sponsor may separately request **inactivation** (312.45) or FDA may inactivate an inactive IND; a completed or discontinued IND is handled under [[closeout]] (312.38 withdrawal). These are FDA-side determinations OSSICRO surfaces and tracks, never issues.

## BIMO inspection (Bioresearch Monitoring)

FDA's **Bioresearch Monitoring (BIMO)** program inspects clinical investigators, sponsors, monitors, and IRBs to verify data integrity and human-subject protection. The operative authorities are **21 CFR 312.58** (sponsor must permit FDA access to, and copying/verification of, records and reports relating to the investigation) and **21 CFR 312.68** (investigator must make records available for inspection). Inspections run under FDA compliance programs **7348.811** (clinical investigators / sponsors-monitors-CROs) and **7348.810** (IRBs). Outcomes are classified **NAI** (no action indicated), **VAI** (voluntary action indicated), or **OAI** (official action indicated); a **Form FDA 483** lists inspectional observations, and serious findings may escalate to a Warning Letter or, for investigators, disqualification (312.70).

> [!interpretive] OSSICRO position
> Inspection-readiness is where OSSICRO's dossier discipline pays off. A complete, internally-consistent, citation-carrying essential-records set — the [[verifiable-site-qualification-dossier]] hash-chained to the [[part-11-and-ai-credibility|Part 11]] audit trail — is precisely what a BIMO inspector reconstructs the trial from. OSSICRO maintains the [[regulatory-binder-isf-index]] in a continuously audit-ready state so that a 312.58/312.68 request is answered from an assembled TMF, not a scramble. This inspection-readiness claim is an OSSICRO design position; the underlying access obligations are confirmed black-letter law.

## What OSSICRO submits vs. surfaces

> [!warning] Non-delegable
> **OSSICRO never transmits a submission to FDA in its own name.** Filing the IND, filing [[ind-safety-report|safety reports]] (7-day/15-day, 312.32), filing the [[ind-annual-report-dsur|annual report]] (312.33), and responding to a hold are **human-authorized actions**: the sponsor-investigator (or an authorized submitter) releases the package. OSSICRO **assembles, checks, validates, times, and version-controls**; the human **authorizes and submits**. This is the operational form of the hard line and of 21 CFR 312.52's rule that only an accountable person/entity — not software — carries a Part 312 obligation.

| FDA-facing action | OSSICRO role | Human accountable act |
|---|---|---|
| IND submission (312.23) | Assemble & completeness-check the package | Sign 1571; authorize submission |
| 30-day clock (312.40) | Compute day-30; hold the dosing gate | Decide to dose subject 1 |
| Clinical hold response (312.42) | Assemble response; track deficiencies | Author scientific rebuttal; attest |
| IND safety reports (312.32) | Compute 7/15-day clocks; draft report | Causality/expectedness call; submit |
| Annual report / DSUR (312.33) | Assemble from safety line-listings | Review; authorize submission |
| BIMO inspection (312.58/312.68) | Keep the TMF audit-ready | Grant access; respond to 483 |

## Related

- [[sponsor-investigator]]
- [[ind-submission-and-30-day-clock]]
- [[pre-ind-and-ind-preparation]]
- [[fda-interactions-meetings-holds]]
- [[form-fda-1571-ind-cover]]
- [[ind-safety-report]]
- [[ind-annual-report-dsur]]
- [[closeout]]
- [[regulatory-binder-isf-index]]
- [[verifiable-site-qualification-dossier]]
- [[non-delegable-functions-and-gates]]
- [[part-11-and-ai-credibility]]

## Sources

- [21 CFR 312.40 — General requirements for use of an investigational new drug in a clinical investigation (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.40)
- [21 CFR 312.42 — Clinical holds and requests for modification (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.42)
- [21 CFR 312.44 — Termination (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.44)
- [21 CFR 312.58 — Inspection of sponsor's records and reports (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.58)
- [21 CFR 312.68 — Inspection of investigator's records and reports (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.68)
- [eCFR — 21 CFR Part 312 (Investigational New Drug Application)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312)
- [FDA — Compliance Program 7348.811 (Bioresearch Monitoring: Clinical Investigators and Sponsor-Investigators)](https://www.fda.gov/media/75927/download)
- [FDA — Bioresearch Monitoring Program (BIMO)](https://www.fda.gov/drugs/guidances-drugs/bioresearch-monitoring-program-bimo)
