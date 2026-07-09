---
title: "Guiding Scenario — A Clinician Has a Patient"
section: "00-overview"
status: mixed
governing_authority:
  - "21 CFR Part 312 (IND); 21 CFR 312.3(b)"
  - "21 CFR 50 (informed consent); 21 CFR 56 (IRB)"
  - "45 CFR 164.512(i) (HIPAA preparatory-to-research)"
  - "ICH E6(R3) Good Clinical Practice"
tags: [ossicro/engine, lifecycle/feasibility, lifecycle/ind, lifecycle/irb, lifecycle/activation, status/mixed]
aliases: ["Guiding Scenario", "End-to-End Walkthrough"]
updated: 2026-07-09
---

# Guiding Scenario — A Clinician Has a Patient

> [!authority] Governing authority
> This walkthrough threads the binding requirements of [21 CFR Part 312](https://www.law.cornell.edu/cfr/text/21/part-312), [Part 50](https://www.law.cornell.edu/cfr/text/21/part-50) (consent), [Part 56](https://www.law.cornell.edu/cfr/text/21/part-56) (IRB), [Part 54](https://www.law.cornell.edu/cfr/text/21/part-54) (financial disclosure), the [HIPAA preparatory-to-research provision (45 CFR 164.512(i)(1)(ii))](https://www.ecfr.gov/current/title-45/section-164.512), and [ICH E6(R3)](https://www.fda.gov/media/169090/download). Status: **Mixed** — every regulatory step is confirmed and cited; the narrative sequencing and the points at which OSSICRO acts are **interpretive** design.

A concrete story makes the architecture legible. It is the spine that connects every downstream page: at each step, this page names the OSSICRO action, the governing authority, and the human gate that OSSICRO must not cross — including the gate OSSICRO controls least, the sponsor's decision to say yes.

## The setup

Dr. A is a practicing oncologist at a small community clinic with no dedicated research office. She has a patient, Mr. B, with a molecular subtype for which she recalls a mechanism-matched early-phase (Phase 2) program. Mr. B is out of standard options. Dr. A has never held an IND, never signed a [Form FDA 1572](https://www.fda.gov/media/79326/download), and has no idea whether she needs one. This is precisely the clinician OSSICRO is built for.

## Step 1 — Matching (preparatory to research)

Dr. A enters a **de-identified** clinical picture. OSSICRO's [[patient-trial-matching|matching engine]] queries the [ClinicalTrials.gov v2 API](https://clinicaltrials.gov/data-api/api) with a semantic + [[matching-mechanism-graph|mechanism-aware]] layer and returns candidate early-phase programs with a cited, per-criterion [[matching-eligibility-adjudication|adjudication]] (met / not-met / indeterminate-needs-data).

- **Authority:** This is a *review preparatory to research* under [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512) — permitted without authorization only if no PHI leaves the covered entity and the review is necessary to prepare the protocol. OSSICRO enforces this in code via the [[privacy-state-machine]] (local-first, minimum-necessary, no PHI egress, ephemeral audited reads).

> [!warning] Non-delegable
> Matching **ranks and adjudicates candidates and cites its reasoning; it does not determine eligibility.** The eligibility determination is the investigator's judgment. Matching that returns "no eligible trial" is a higher-influence context of use than drafting and is designed and evaluated as one ([[matching-evaluation-and-benchmarks]]); it never silently excludes a patient.

## Step 2 — Triage to a pathway

OSSICRO routes Dr. A through the [[the-three-pathways-triage|three-pathway decision tree]]:

- **(A) Site** on the pharma sponsor's existing protocol — the fastest route if the program is enrolling and the sponsor will accept a new site.
- **(B) Sponsor-investigator IND** — if Dr. A wants to run her own investigation and hold the IND ([[sponsor-investigator]], [21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3)).
- **(C) Expanded access** — if no trial fits and the need is single-patient treatment ([[expanded-access-workflow]], [Form 3926](https://www.fda.gov/media/162793/download)).

Mode A is the target — but it is contingent on a counterparty decision that no document set can compel. The accountable parties, document sets, and legal exposure differ entirely across the three; see [[two-modes-site-vs-sponsor-investigator]].

## Step 2.5 — Sponsor engagement (the gate OSSICRO cannot draft through)

> [!interpretive] OSSICRO position
> This step is where most one-patient site requests die, and the wiki treats it honestly: **a sponsor is under no legal obligation to add a site.** Investigator selection is the sponsor's own responsibility and discretion under [21 CFR 312.53(a)](https://www.law.cornell.edu/cfr/text/21/312.53), and a company's standard site-onboarding machinery is economically disproportionate for a single-patient engagement. Many sponsors decline such requests for exactly that reason. No validated refusal-rate statistic exists for one-patient site additions; the base rate should be assumed unfavorable and planned around, not argued with.

What actually happens, and who does it:

1. **Outreach** — Dr. A (or the [[micro-cro-accountable-layer|micro-CRO]] acting on her behalf, with her named as the contact) approaches the sponsor's medical affairs / clinical operations function. OSSICRO drafts the inquiry; a human sends it under their own name.
2. **CDA and feasibility questionnaire** — if the sponsor engages, the customary sequence is a confidentiality agreement followed by a site feasibility questionnaire. OSSICRO pre-populates the questionnaire from the [[verifiable-site-qualification-dossier|site qualification dossier]] so the response goes back in days, not weeks — the one cycle-time lever the physician side actually controls.
3. **Sponsor-side qualification and negotiation** — site qualification review, then [[clinical-trial-agreement-and-budget|CTA and budget]] negotiation with the sponsor's legal function. This is a bilateral negotiation; industry experience puts contract/budget cycle times at months, and OSSICRO's drafted, FMV-benchmarked, safe-harbor-structured CTA template shortens Dr. A's side of the exchange but cannot shorten the sponsor's. What the manufacturer needs to say yes — and the minimal-but-compliant package that makes a one-patient site acceptable — is worked through from the pharma side in [[single-patient-site-and-pharma-acceptance]].

**What OSSICRO does while waiting:** it does not idle on the sponsor's clock. In parallel, it keeps **pathway (C)** warm — assembling the [[expanded-access-workflow|individual-patient expanded access]] package ([21 CFR 312.310](https://www.law.cornell.edu/cfr/text/21/312.310), [Form 3926](https://www.fda.gov/media/162793/download)) so that if the sponsor declines the site, Mr. B's treatment request is days from submission rather than starting from zero. Expanded access still requires the manufacturer's agreement to supply, but it asks the company for far less than site activation does.

For this walkthrough, assume the sponsor engages and accepts: **Mode A proceeds.** The remaining steps are what that yes unlocks.

## Step 3 — Assemble the site-activation package

OSSICRO's [[generate-check-validate-engine|engine]] assembles the mode-appropriate essential-document set to sponsor standard, with a live [[communication-hub|milestone tracker]]:

- **[[form-fda-1572-statement-of-investigator|Form FDA 1572]]** (Statement of Investigator), auto-populated from Dr. A's CV, license, and site data ([312.53(c)](https://www.law.cornell.edu/cfr/text/21/312.53)).
- **[[form-fda-3454-3455-financial-disclosure|Financial disclosure]]** (Form 3454 certification / 3455 disclosure), by [Part 54](https://www.law.cornell.edu/cfr/text/21/part-54) thresholds.
- CV, medical license, GCP training certificates, lab certifications and normal ranges.
- **[[clinical-trial-agreement-and-budget|CTA and budget]]** — FMV-set, [Anti-Kickback](https://www.law.cornell.edu/uscode/text/42/1320a-7b) safe-harbor-structured.
- **[[delegation-of-authority-log|Delegation-of-authority log]]** and **[[drug-accountability-log|drug-accountability]]** SOPs.
- The **[[irb-submission-package|IRB submission package]]**, pre-checked against the [56.111](https://www.law.cornell.edu/cfr/text/21/56.111) approval criteria.

Every artifact is a **draft** carrying a citation-to-authority manifest ([[compliance-mapping]]) and ships with a [[completeness-ledger|completeness ledger]]: green (validated) / amber (needs human judgment) / red (missing data + the exact resolving question). A new site's biggest liability — no track record — becomes a [[verifiable-site-qualification-dossier|verifiable, citation-complete dossier]] that a skeptical sponsor can accept.

## Step 4 — The gates (where OSSICRO stops)

> [!warning] Non-delegable
> At each gate, Dr. A (or the [[micro-cro-accountable-layer|micro-CRO's]] qualified human) reviews, judges, and signs. OSSICRO cannot cross any of these:
> - **1572 signature** — the investigator's personal legal attestation ([312.53(c)](https://www.law.cornell.edu/cfr/text/21/312.53); [[form-fda-1572-statement-of-investigator]]).
> - **IRB approval** — the ethics body's independent judgment ([21 CFR 56.109](https://www.law.cornell.edu/cfr/text/21/56.109); [[irb-iec]]). Enrollment is gated on documented approval.
> - **Informed consent** — the human conversation with Mr. B and his signature ([21 CFR 50.20–50.27](https://www.law.cornell.edu/cfr/text/21/50.25); [[informed-consent-document-vs-event]]). OSSICRO drafts the *document*; it never conducts the *event*.
> - **PI qualification attestation** — Dr. A's own representation that she is qualified.

## Step 5 — Enrollment (the HIPAA transition)

Once the IRB has approved and Mr. B has consented, the [[privacy-state-machine]] executes a hard, logged transition from *preparatory review* to *enrollment*: PHI use now rests on [164.508 authorization](https://www.ecfr.gov/current/title-45/section-164.508) or a [164.512(i)(1)(i)](https://www.ecfr.gov/current/title-45/section-164.512) IRB/Privacy-Board waiver. Mr. B is enrolled per the protocol's [[enrollment-and-consent|eligibility and consent]] procedures — the eligibility determination remaining Dr. A's non-delegable call.

## Step 6 — Conduct, safety, closeout

OSSICRO tracks the remainder against deadlines:

- **Conduct/monitoring** — source data, CRFs, [[conduct-and-monitoring|monitoring visits]], deviations, drug accountability, under a risk-based [[risk-based-monitoring-e6r3|E6(R3)]] [[monitoring-plan]] (sponsor monitoring obligation, [312.53(d)](https://www.law.cornell.edu/cfr/text/21/312.53)).
- **Safety** — the [[safety-reporting-lifecycle|AE→SAE→SUSAR]] flow, with the [[safety-clock-engine|7-day/15-day clocks]] computed and escalated by OSSICRO under [312.32](https://www.law.cornell.edu/cfr/text/21/312.32).

> [!warning] Non-delegable
> Causality and expectedness — whether an event is a *suspected* adverse reaction and *unexpected* — is the [[medical-monitor|medical monitor's]] judgment ([312.32(a)/(c)](https://www.law.cornell.edu/cfr/text/21/312.32); [ICH E2A](https://www.ich.org/page/efficacy-guidelines)). OSSICRO computes the deadline, drafts the [[form-fda-3500a-medwatch|MedWatch 3500A]] narrative, and escalates — but never makes the causality call and never files.

- **Closeout** — final monitoring visit, drug reconciliation/destruction, final IRB notice, and record retention ([[closeout]], [[record-retention-and-archival]]).

## What the scenario demonstrates

Every step has the same shape: OSSICRO removes the coordination burden that would otherwise stop Dr. A cold, and stops precisely at the acts the law reserves to a human. One step is different in kind: the sponsor's yes (Step 2.5) is a counterparty's business decision that OSSICRO can make cheaper to grant but cannot manufacture — which is why the architecture always carries the expanded-access hedge in parallel. The paperwork barrier falls; the accountable human stands. Read the same story from each actor's vantage in [[four-entry-points]] and the [[06-personas/index|persona pages]].

## Related

- [[the-three-pathways-triage]]
- [[four-entry-points]]
- [[two-modes-site-vs-sponsor-investigator]]
- [[single-patient-site-and-pharma-acceptance]]
- [[site-activation]]
- [[informed-consent-document-vs-event]]
- [[safety-reporting-lifecycle]]
- [[non-delegable-functions-and-gates]]
- [[privacy-state-machine]]

## Sources

- [21 CFR Part 312 — Investigational New Drug Application](https://www.law.cornell.edu/cfr/text/21/part-312)
- [21 CFR 312.53 — Selecting investigators and monitors](https://www.law.cornell.edu/cfr/text/21/312.53)
- [21 CFR 312.310 — Individual patients, including for emergency use](https://www.law.cornell.edu/cfr/text/21/312.310)
- [21 CFR 56.111 — Criteria for IRB approval of research](https://www.law.cornell.edu/cfr/text/21/56.111)
- [21 CFR 312.32 — IND safety reporting](https://www.law.cornell.edu/cfr/text/21/312.32)
- [45 CFR 164.512 — Uses and disclosures for which authorization is not required (preparatory to research)](https://www.ecfr.gov/current/title-45/section-164.512)
- [FDA — Instructions for Filling Out Form FDA 1572](https://www.fda.gov/media/79326/download)
- [FDA — Form FDA 3926 (Individual Patient Expanded Access)](https://www.fda.gov/media/162793/download)
- [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api)
