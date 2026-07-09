---
title: "System Architecture — Components and the Part 11 Environment"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "21 CFR Part 11 (Electronic Records; Electronic Signatures)"
  - "21 CFR 312.52 (Transfer of obligations to a CRO)"
  - "ICH E6(R3) Good Clinical Practice (data governance; computerized systems)"
  - "45 CFR 164.512(i) (HIPAA — research provisions)"
tags: [ossicro/engine, ossicro/part11, ossicro/matching, ossicro/micro-cro, cfr/11, cfr/312, ich/e6r3, status/interpretive]
aliases: ["Architecture", "OSSICRO Architecture"]
updated: 2026-07-09
---

# System Architecture — Components and the Part 11 Environment

> [!authority] Governing authority
> [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) governs every electronic record OSSICRO creates, modifies, maintains, or transmits in satisfaction of an FDA predicate rule (Parts 50, 54, 56, 312), and every electronic signature applied to one; ICH E6(R3) supplies the data-governance and computerized-systems expectations; [45 CFR 164.512(i)](https://www.law.cornell.edu/cfr/text/45/164.512) constrains how the matching subsystem may touch PHI. Status: **Mixed** — the compliance constraints are confirmed; the five-component decomposition is the OSSICRO design position.

OSSICRO is five components over a shared, Part 11-compliant substrate. The decomposition follows the legal structure of the problem, not engineering convenience: each component corresponds to a distinct regulatory boundary — PHI handling, document generation, template provenance, inter-entity coordination, and legal accountability — and the boundaries between components are where the hard gates live. This page describes each component, the substrate they share, and the deployment posture.

## Component 1 — Program database and patient-trial matching

The discovery front-door for all four entry points ([[four-entry-points]]). Built on the [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api) (phase/status enumerations; no registration wall) with an OSSICRO adjudication layer on top, because the native API ranks by keyword relevance and cannot adjudicate eligibility ([[matching-engine]], [[matching-eligibility-adjudication]]). Chart data enters through [[smart-on-fhir-integration]] (SMART App Launch at point of care; Backend Services / Bulk `$export` for panel screening; US Core R4, mCODE, FHIR Genomics profiles).

The component sits entirely behind the [[privacy-state-machine]]: matching operates under the HIPAA *review-preparatory-to-research* provision ([45 CFR 164.512(i)(1)(ii)](https://www.law.cornell.edu/cfr/text/45/164.512)) — local-first, minimum-necessary, no PHI egress — and the transition to enrollment requires a signed authorization ([45 CFR 164.508](https://www.law.cornell.edu/cfr/text/45/164.508)) or a documented IRB/Privacy-Board waiver ([45 CFR 164.512(i)(1)(i)](https://www.law.cornell.edu/cfr/text/45/164.512)). The transition is a logged, code-enforced state change, not a policy statement. See [[hipaa-and-privacy-gating]].

## Component 2 — Generate/check/validate engine

The document pipeline: **generate** a draft from a template plus structured study data, **check** it for completeness and cross-document consistency (including an adversarial machine pre-review), and **validate** it against a rule engine in which every rule traces to a specific CFR/ICH subsection and every rule touching an accountable act fails to a human gate. Fully specified at [[generate-check-validate-engine]]; its output contract is the [[completeness-ledger]] and the span-level [[draft-provenance-model]]. The engine's AI implementation (drafting agents, QC agents, coordination agents behind permission modes) is documented at [[claude-sdk-ai-in-the-loop]].

## Component 3 — Template library

Seeded public-domain-first: the NIH-FDA Phase 2/3 protocol template, NIH-model DSMB charters, the official FDA forms (1571, 1572, 3454/3455, 3500A, 3926), and the ICH M11 harmonized protocol template (final template 2025-11-19; the CeSHarP structured representation is the priority generation target). Institutional libraries — Penn's numbered document-control library, Pitt's IND/amendment template set, UNC Lineberger, Stanford CRQ — are *schema-mirrored* (structure and taxonomy reimplemented) rather than copied, with reuse license verified before any verbatim adoption; provenance is recorded per template in [[external-templates-and-licenses]]. Consortium-gated IP (TransCelerate CPT) and proprietary templates (Advarra) are cross-checked but not reproduced.

## Component 4 — Pharma-style frontend

A milestone/deadline regulatory tracker across every counterparty — FDA (30-day clock, annual-report anniversary, safety-report clocks via the [[safety-clock-engine]]), IRB (approval expiration, continuing review), DSMB (meeting cadence), and the pharma partner. Each of the four personas gets a role-scoped portal view ([[06-personas/index|personas]]), and inter-actor traffic runs through the auditable [[communication-hub]], which respects both HIPAA scoping and the Medical Affairs / Clinical Development firewall ([[pharma-partner-interface-iis]]). Interoperation with sponsor stacks (CTMS, eTMF, EDC, IRT, safety databases, site portals) is on Part 11-conformant e-record conventions — OSSICRO exchanges records with those systems; it does not silently write into them.

## Component 5 — Micro-CRO service layer

The thin, named, legally accountable human entity that holds only the functions [21 CFR 312.52(b)](https://www.law.cornell.edu/cfr/text/21/312.52) requires an entity for, when the sponsor-investigator cannot personally hold them, under a written [[transfer-of-regulatory-obligations-toro|TORO]] instrument enumerating each assumed obligation. Service tiers run from open-source self-serve through paid human review at accountable gates to full enumerated-obligation assumption ([[micro-cro-operating-model]]). This component is people and an entity, not software; it appears in the architecture because the software routes work to it, produces its dossiers ([[verifiable-site-qualification-dossier]]), and records its sign-offs.

> [!warning] Non-delegable
> The architecture has no path by which software assumes a sponsor obligation. [21 CFR 312.52(b)](https://www.law.cornell.edu/cfr/text/21/312.52) makes a transferee "subject to the same regulatory action as a sponsor"; only a legal person or entity can be. Components 1–4 draft, check, route, time, and record. Component 5 — humans in an accountable entity — and the sponsor-investigator personally are the only parties in this architecture that can *own* a regulated act. See [[non-delegable-functions-and-gates]].

## The Part 11 substrate

All five components share one compliance substrate, mapped clause-by-clause to [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11):

| Part 11 requirement | Substrate implementation |
|---|---|
| §11.10(a) — system validation | Documented validation of the engine and rule sets; the rule engine's own test suite is a controlled record. |
| §11.10(b), (c) — accurate copies; record protection and retention | Export of any record in human-readable and electronic form for FDA inspection; retention aligned to [21 CFR 312.57(c)](https://www.law.cornell.edu/cfr/text/21/312.57) and [312.62(c)](https://www.law.cornell.edu/cfr/text/21/312.62) (see [[record-retention-and-archival]]). |
| §11.10(d), (g) — access and authority controls | Role-scoped access per persona; authority checks before any state-changing operation. |
| §11.10(e) — audit trail | Computer-generated, time-stamped, independent audit trail on every record creation/modification/deletion; prior entries are never obscured. The audit trail doubles as the [[draft-provenance-model]] and is hash-chained for the [[verifiable-site-qualification-dossier]]. Detailed in [[data-model]]. |
| §11.10(k) — documentation controls | The template library and rule sets are themselves version-controlled records with change history. |
| §11.50, §11.70 — signature manifestations; signature/record linking | Signed records display printed name, date/time, and meaning of the signature (review, approval, responsibility); signatures are cryptographically bound to their records and cannot be excised or transferred. |
| §§11.100–11.300 — electronic signature requirements | Identity verification before assignment; two-component non-biometric signatures; per-individual (never shared) credentials. |

Two interpretive layers condition this mapping. First, FDA's [Part 11 Scope and Application guidance (2003)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application) narrows enforcement discretion to records required by predicate rules — OSSICRO treats every record destined for the TMF, the IND, or an FDA form as in-scope rather than litigating the boundary. Second, ICH E6(R3)'s data-governance section layers ALCOA++ expectations (attributable, legible, contemporaneous, original, accurate — plus complete, consistent, enduring, available) and computerized-systems requirements over the CFR floor; the substrate is built to R3 as the forward standard (FDA final guidance 2025-09-09; no US compliance date set as of this writing).

**AI attribution.** Every AI-generated span is recorded in the audit trail with model identity/version, input hash, timestamp, and the identity of the human reviewer who accepted, modified, or rejected it ([[claude-sdk-ai-in-the-loop]]). An AI agent never holds a Part 11 signature credential; signatures belong exclusively to identified humans (§11.100(a) requires signatures to be unique to one *individual*).

> [!interpretive] OSSICRO position
> Treating the draft-generation function as a low-influence, low-consequence context of use under the FDA 2025 AI-credibility draft framework — because a qualified human reviews and signs every output before it becomes a regulatory record — is an OSSICRO risk-tiering argument, not an FDA determination. The guidance is draft (comments closed 2025-04-07). Matching, which can gate a patient's access to a trial, is deliberately classified as a *higher*-influence context of use and evaluated accordingly ([[matching-evaluation-and-benchmarks]], [[part-11-and-ai-credibility]]).

## Deployment posture

The reference deployment is **local-first**: a single-container installation inside the covered entity's boundary, so PHI never leaves the clinician's environment during matching and low-resource sites need no data-center dependency ([[offline-local-deployment]]). External calls (ClinicalTrials.gov, PubMed, openFDA — [[data-integrations-ctgov-pubmed]]) carry only de-identified query parameters outbound. The [[privacy-state-machine]] is enforced in the same container, which is what makes "no PHI egress" a code property rather than a policy promise.

## Related

- [[generate-check-validate-engine]]
- [[data-model]]
- [[part-11-and-ai-credibility]]
- [[privacy-state-machine]]
- [[hipaa-and-privacy-gating]]
- [[smart-on-fhir-integration]]
- [[matching-engine]]
- [[communication-hub]]
- [[micro-cro-operating-model]]
- [[offline-local-deployment]]
- [[claude-sdk-ai-in-the-loop]]
- [[non-delegable-functions-and-gates]]
- [[compliance-mapping]]

## Sources

- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [FDA Guidance — Part 11, Electronic Records; Electronic Signatures: Scope and Application (2003)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application)
- [21 CFR 312.52 — Transfer of obligations to a contract research organization](https://www.law.cornell.edu/cfr/text/21/312.52)
- [21 CFR 312.57 — Recordkeeping and record retention](https://www.law.cornell.edu/cfr/text/21/312.57)
- [45 CFR 164.512 — Uses and disclosures for which an authorization is not required (research provisions)](https://www.law.cornell.edu/cfr/text/45/164.512)
- [FDA — E6(R3) Good Clinical Practice (final guidance, Sept 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025, PDF)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA Draft Guidance — Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making for Drug and Biological Products (Jan 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological)
- [FDA Guidance — Conducting Clinical Trials With Decentralized Elements (final, Sept 2024)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/conducting-clinical-trials-decentralized-elements)
- [ClinicalTrials.gov API v2 documentation](https://clinicaltrials.gov/data-api/api)
