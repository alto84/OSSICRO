---
title: "Non-Delegable Functions and the Master Gating Matrix"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "21 CFR 312.52 (Transfer of obligations to a CRO)"
  - "21 CFR 312.50, 312.60 (sponsor and investigator general responsibilities)"
  - "21 CFR 50.20-50.27 (informed consent)"
  - "21 CFR 56.109-56.111 (IRB review and approval)"
  - "21 CFR 312.32, 312.64(b) (IND safety reporting)"
  - "21 CFR 54.4 (financial disclosure certification)"
  - "21 CFR 312.23(a)(1), 312.53(c)(1) (Forms 1571 and 1572)"
  - "ICH E6(R3); ICH E2A; ICH E9/E9(R1)"
tags: [ossicro/gating, ossicro/micro-cro, cfr/312, cfr/50, cfr/54, cfr/56, ich/e2a, ich/e9, fda-form/1571, fda-form/1572, fda-form/3454, fda-form/3455, status/confirmed, status/interpretive]
aliases: ["Gating Matrix", "Non-Delegable Functions", "Master Gating Matrix"]
updated: 2026-07-09
---

# Non-Delegable Functions and the Master Gating Matrix

> [!authority] Governing authority
> [21 CFR 312.52](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52) (obligations transfer only to a legally accountable entity), [21 CFR Part 50](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50) (consent), [21 CFR Part 56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56) (IRB), [21 CFR 312.32/312.64](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32) (safety judgment), [21 CFR Part 54](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54) (financial disclosure), ICH E6(R3)/E2A/E9. Status: **Mixed** — each listed function is non-delegable under black-letter law or FDA-adopted guidance (confirmed); the gate mechanism that enforces the list in software is the OSSICRO design position (interpretive).

This page is the master gating matrix for the entire OSSICRO system: the exhaustive enumeration of regulated functions that must remain with a qualified human or legally accountable entity, the authority that makes each one non-delegable, and the code-level gate behavior that enforces the boundary. Every other system page ([[generate-check-validate-engine]], [[claude-sdk-ai-in-the-loop]], [[matching-eligibility-adjudication]], [[safety-clock-engine]], [[communication-hub]]) references this matrix; a validation rule that touches any row on it fails to a human gate rather than proceeding. The design principle it operationalizes: OSSICRO drafts COMPLETE documentation for qualified human review; it never replaces human-in-the-loop judgment, IRB/ethics review, DSMB oversight, or medical/safety decisions.

## Why the matrix exists — the §312.52 foundation

[21 CFR 312.52(a)](https://www.law.cornell.edu/cfr/text/21/312.52) permits a sponsor to transfer any or all of its obligations to a contract research organization only in a signed writing that describes each obligation assumed; §312.52(b) makes the transferee "subject to the same regulatory action as a sponsor." Only a legal person or entity can be subject to FDA regulatory action. Software therefore cannot be a transferee, cannot hold a sponsor obligation, and cannot own any accountable act — regardless of how capable it is at drafting the documentation that surrounds the act. The lawful architecture is the [[sponsor-investigator]] holding both obligation sets under [21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3), with the [[micro-cro-accountable-layer|micro-CRO]] as a written [[transfer-of-regulatory-obligations-toro|TORO]] transferee where an entity is required (see [[legal-thesis-3123-vs-31252]]). The matrix below is the operational consequence: the complete list of acts the software must surface, route, and record — but never perform.

## Gate semantics

A **gate** in OSSICRO is a fail-closed control point with four properties, all recorded in the [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) audit trail (see [[part-11-and-ai-credibility]] and [[draft-provenance-model]]):

1. **Block.** The workflow cannot advance past the gate by any automated path. There is no configuration flag, permission mode, or API call that executes the gated act. (In the [[claude-sdk-ai-in-the-loop|Claude Agent SDK implementation]], gated tools are denied at the permission layer, not merely discouraged by prompt.)
2. **Route.** The gate names the *specific qualified human role* responsible (sponsor-investigator, IRB, medical monitor, biostatistician, micro-CRO officer, manufacturer) and delivers the complete draft package, the [[completeness-ledger]], and the machine pre-review critique to that person.
3. **Record.** The human's decision, identity, signature meaning, and timestamp are captured per [21 CFR 11.50](https://www.law.cornell.edu/cfr/text/21/11.50), linked to the exact document version reviewed.
4. **Verify.** Downstream steps check for the *documented evidence* of the human act (e.g., enrollment logic verifies documented IRB approval exists in the TMF per [21 CFR 312.66](https://www.law.cornell.edu/cfr/text/21/312.66)), not for a workflow flag.

## The master gating matrix

| # | Non-delegable function | Authority | Accountable human/entity | What OSSICRO does (and stops at) |
|---|---|---|---|---|
| G1 | Obtaining informed consent — the consent conversation and voluntary agreement | [21 CFR 50.20](https://www.law.cornell.edu/cfr/text/21/50.20), 50.25, 50.27; 45 CFR 46.116-46.117 | Investigator or qualified designee | Drafts/version-controls the ICF, checks §50.25 elements, runs eConsent mechanics per the [2016 FDA/OHRP guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers); never conducts consent ([[informed-consent-document-vs-event]]) |
| G2 | IRB review and approval determination | [21 CFR 56.109-56.111](https://www.law.cornell.edu/cfr/text/21/56.111); 45 CFR 46.109-46.111 | Constituted IRB/IEC | Assembles the [[irb-submission-package]], pre-checks against §56.111 criteria; the approval judgment is the IRB's; enrollment is blocked until documented approval exists |
| G3 | Subject eligibility determination and all dosing/treatment decisions | Protocol; 21 CFR 312.60; practice-of-medicine | Investigator | Per-criterion adjudication with citations and three-valued verdicts ([[matching-eligibility-adjudication]]); the eligibility *determination* is the investigator's |
| G4 | SAE seriousness, expectedness, and causality assessment | [21 CFR 312.32](https://www.law.cornell.edu/cfr/text/21/312.32), 312.64(b); ICH E2A | Medical monitor / qualified safety physician | Intake, coding, narrative drafting, 3500A pre-population, 7/15-day clock computation and escalation ([[safety-clock-engine]]); never adjudicates causality |
| G5 | DSMB/DMC continue/modify/stop recommendation | FDA DMC guidance (2006; 2024 draft) | Independent, conflict-free committee | Assembles open/closed reports, tracks cadence ([[dsmb-workflow]]); the recommendation is the committee's |
| G6 | Sponsor's risk-benefit response to a DSMB recommendation (continue/modify/terminate) | 21 CFR 312.50, 312.56(d) | Sponsor / sponsor-investigator | Drafts the response documentation and amendment package; the decision is human |
| G7 | Form FDA 1571 signature — sponsor legal attestation | [21 CFR 312.23(a)(1)](https://www.law.cornell.edu/cfr/text/21/312.23) | Sponsor(-investigator) | Generates and completeness-checks the [[form-fda-1571-ind-cover|1571]]; the signature commits the human to statutory sponsor responsibility |
| G8 | Form FDA 1572 signature — investigator commitments (Field 9) | [21 CFR 312.53(c)(1)](https://www.law.cornell.edu/cfr/text/21/312.53) | Investigator | Auto-populates from CV/site data, validates fields 1-9 ([[form-fda-1572-statement-of-investigator]]); the signature is a personal legal commitment |
| G9 | Financial-disclosure certification/disclosure | [21 CFR 54.4](https://www.law.cornell.edu/cfr/text/21/54.4) | Each covered investigator | Collects attestations, selects [[form-fda-3454-3455-financial-disclosure|3454 vs 3455]]; the attestation itself is a signed representation to FDA the physician cannot delegate — including self-disclosure in the S-I model |
| G10 | Transfer of sponsor obligations (the transferee function itself) | [21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52) | Micro-CRO entity or the S-I personally | Drafts the [[transfer-of-regulatory-obligations-toro|TORO]] enumerating each obligation; only a legal entity signs and holds it |
| G11 | Final release of any submission to FDA (IND, amendment, safety report, annual report, 3926) | 21 CFR 312.23, 312.30-312.33; Subpart I | Sponsor(-investigator) or authorized micro-CRO officer | Assembles, validates, and stages the package; transmission is an explicit human-authorized action |
| G12 | Statistical sign-off — SAP approval, estimand selection, unblinded analysis | ICH [E9/E9(R1)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e9r1-statistical-principles-clinical-trials-addendum-estimands-and-sensitivity-analysis-clinical) | Qualified biostatistician | Structures the [[statistical-analysis-plan|SAP]]; analytic decisions and sign-off are the biostatistician's ([[biostatistician]]) |
| G13 | Fair-market-value determination and anti-kickback (AKS) anti-inducement judgment | 42 USC 1320a-7b(b); safe harbors | Counsel / compliance officer | Structures the [[clinical-trial-agreement-and-budget|CTA/budget]] with FMV documentation fields; the FMV/AKS judgment is human |
| G14 | Manufacturer's decision to supply investigational drug (trial, IIS, or expanded access) | FDCA §561A; [21 CFR 312 Subpart I](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I) | Manufacturer | Prepares the request and letter-of-authorization workflow ([[expanded-access-workflow]], [[form-fda-3926-expanded-access]]); the supply decision is the counterparty's |
| G15 | Investigational-product final disposition/destruction authorization | 21 CFR 312.59 | Sponsor(-investigator) | Maintains the [[drug-accountability-log]] and reconciliation; destruction is authorized by the human |
| G16 | Investigator conduct-of-trial obligations (supervision, drug control, records) | 21 CFR 312.60-312.62 | Investigator — non-transferable to any vendor or software | Tracks the [[delegation-of-authority-log]]; task delegation never transfers accountability ([[subinvestigator-and-delegation]]) |
| G17 | CSR scientific conclusions; QA release of protocol/IB/CSR | ICH E3; E6(R3) | Qualified human author/approver | Drafts to [[clinical-study-report|E3 structure]]; conclusions and release are signed human acts |
| G18 | EU/ICH named-person functions — QPPV; QP release of IMP | EU CTR 536/2014; GVP Module I | Named accountable individuals | Surfaces the requirement where the EU frame applies ([[qualified-person-qppv-eu]]); never substitutes |
| G19 | Any money movement, or any communication sent in a named person's name | Contract law; OSSICRO operating rule | The named human | Drafts for review; no autonomous send, no autonomous payment |

> [!warning] Non-delegable
> Every row above is a control point, not a convenience. G1 (consent), G2 (IRB approval), and G4 (causality) are the archetypal cases: [21 CFR 50.20](https://www.law.cornell.edu/cfr/text/21/50.20) requires that consent be *obtained*, [21 CFR 56.111](https://www.law.cornell.edu/cfr/text/21/56.111) vests the approval criteria judgment in the IRB, and [21 CFR 312.32(c)](https://www.law.cornell.edu/cfr/text/21/312.32) makes the sponsor's causality/expectedness evaluation the trigger for a 15-day IND safety report. OSSICRO drafts; a qualified human owns and signs, in every case, with no automated bypass.

## Grouping and cross-cutting behavior

The nineteen gates cluster into five families, which is how the [[generate-check-validate-engine]] organizes its rule failures:

- **Subject-protection gates (G1-G3):** enrollment of any subject is structurally blocked until documented IRB approval (G2) and a completed consent event (G1) exist as records in the TMF, and eligibility (G3) carries an investigator sign-off. The [[privacy-state-machine]] adds the HIPAA analogue: the preparatory→enrollment transition requires authorization or waiver ([[hipaa-and-privacy-gating]]).
- **Safety-judgment gates (G4-G6):** the [[safety-clock-engine]] computes deadlines and escalates, but the clock *starts* from a human causality/expectedness determination it can never make. See [[safety-reporting-lifecycle]] and [[ind-safety-report]].
- **Legal-attestation gates (G7-G11):** signatures and submissions. These are the gates the Part 11 e-signature machinery exists to serve ([[part-11-and-ai-credibility]]); each signature's meaning is recorded per [21 CFR 11.50](https://www.law.cornell.edu/cfr/text/21/11.50).
- **Financial/counterparty gates (G13-G15, G19):** judgments that belong to counsel, the manufacturer, or the paying human; OSSICRO structures the paperwork around them.
- **Scientific-accountability gates (G12, G16-G18):** qualified-professional sign-offs that ICH guidance vests in named roles.

> [!interpretive] OSSICRO position
> The *floor* of this matrix is black-letter law — no regulator has to accept OSSICRO's framing for G1-G11 to bind. The *enumeration as a closed, code-enforced list* (including G19's no-autonomous-send/no-money-movement rule, which is an OSSICRO operating rule stricter than any single regulation requires) is the OSSICRO design position. Where a new function is proposed for automation, the burden is on the proposer to show it appears on no row of this matrix; ambiguity resolves toward gating. The matrix is versioned, and the [[regulatory-change-log]] flags any authority change that touches a row.

## What is delegable — the complement

The matrix is meaningful because everything *not* on it is fair territory for the engine: document drafting and assembly, completeness checking against the essential-records matrix (ICH E6(R3) Appendix C; [[document-catalog]]), cross-document consistency verification, deadline computation, routing and notification, version control, audit-trail maintenance, template instantiation, form field population, literature and trial retrieval, and TMF filing ([[startup-tmf-checklist]], [[conduct-tmf-checklist]], [[closeout-tmf-checklist]]). This is precisely the coordination labor where CRO cost concentrates (~90-95% of direct cost is labor; see [[cro]]) — the removable burden — while the matrix rows are the irreducible accountable core the [[micro-cro-operating-model|micro-CRO]] and the sponsor-investigator retain.

## Related

- [[legal-thesis-3123-vs-31252]]
- [[micro-cro-accountable-layer]]
- [[micro-cro-operating-model]]
- [[transfer-of-regulatory-obligations-toro]]
- [[generate-check-validate-engine]]
- [[claude-sdk-ai-in-the-loop]]
- [[informed-consent-document-vs-event]]
- [[irb-review-workflow]]
- [[safety-clock-engine]]
- [[safety-reporting-lifecycle]]
- [[part-11-and-ai-credibility]]
- [[hipaa-and-privacy-gating]]
- [[completeness-ledger]]
- [[subinvestigator-and-delegation]]
- [[medical-monitor]]
- [[dsmb-dmc]]

## Sources

- [21 CFR 312.52 — Transfer of obligations to a contract research organization (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52)
- [21 CFR Part 312 Subpart D — Responsibilities of Sponsors and Investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D)
- [21 CFR Part 50 — Protection of Human Subjects (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50)
- [21 CFR Part 56 — Institutional Review Boards (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56)
- [21 CFR Part 54 — Financial Disclosure by Clinical Investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54)
- [21 CFR 312.32 — IND safety reporting (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
- [FDA Guidance: Investigator Responsibilities — Protecting the Rights, Safety, and Welfare of Study Subjects (2009)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigator-responsibilities-protecting-rights-safety-and-welfare-study-subjects)
- [FDA Guidance: Establishment and Operation of Clinical Trial Data Monitoring Committees (2006)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/establishment-and-operation-clinical-trial-data-monitoring-committees)
- [ICH E6(R3) Good Clinical Practice — FDA final guidance (2025-09-09)](https://www.fda.gov/media/169090/download)
- [ICH E2A — Clinical Safety Data Management: Definitions and Standards for Expedited Reporting](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e2a-clinical-safety-data-management-definitions-and-standards-expedited-reporting)
- [FDA/OHRP Guidance: Use of Electronic Informed Consent — Questions and Answers (2016)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers)
