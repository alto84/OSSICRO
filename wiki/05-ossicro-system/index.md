---
title: "OSSICRO System — Overview and Reading Order"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "21 CFR Part 11 (Electronic Records; Electronic Signatures)"
  - "21 CFR 312.52 (Transfer of obligations to a CRO)"
  - "21 CFR 312.3(b) (Sponsor-investigator)"
  - "ICH E6(R3) Good Clinical Practice"
tags: [ossicro/engine, ossicro/part11, ossicro/micro-cro, ossicro/matching, ossicro/gating, status/interpretive]
aliases: ["OSSICRO System", "System Overview"]
updated: 2026-07-09
---

# OSSICRO System — Overview and Reading Order

> [!authority] Governing authority
> The system described in this section operates inside a binding legal frame: [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) (electronic records and signatures), [21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52) (obligations transfer only to an accountable entity), [21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3) (the sponsor-investigator construct), and ICH E6(R3) (FDA final guidance 2025-09-09). Status: **Mixed** — the constraints are black-letter law; the architecture that satisfies them is the OSSICRO design position, labelled interpretive throughout.

This section documents the OSSICRO software system itself: what the components are, how the generate/check/validate engine works, what the data model records, and how every design decision traces back to a regulatory constraint. Sections 00–04 of this wiki describe the *law*; this section describes the *machine built to operate lawfully inside it*. Nothing here modifies or relaxes any requirement stated elsewhere in the corpus.

## What the system is

OSSICRO is five components over a [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)-compliant substrate (see [[architecture]]):

1. **Searchable program database + patient-trial matching** — ClinicalTrials.gov API v2 plus an eligibility-adjudication layer, HIPAA-gated at the preparatory-review boundary ([[patient-trial-matching]], [[matching-engine]], [[hipaa-and-privacy-gating]]).
2. **Generate/check/validate engine** — the three-pass document pipeline with human sign-off gates and an adversarial machine pre-review ([[generate-check-validate-engine]]).
3. **Template library** — public-domain-first regulatory templates (NIH-FDA protocol template, FDA forms, ICH M11), schema-mirrored from institutional libraries with verified licensing.
4. **Pharma-style frontend** — milestone/deadline tracking across sponsor, IRB, DSMB, and pharma counterparties, plus the role-scoped [[communication-hub]].
5. **Micro-CRO service layer** — the thin, named, legally accountable human entity that holds the functions [21 CFR 312.52(b)](https://www.law.cornell.edu/cfr/text/21/312.52) requires an entity for ([[micro-cro-operating-model]]).

## The design principle every page repeats

OSSICRO drafts **complete, compliant documentation for qualified human review**. It never replaces human-in-the-loop judgment, IRB/ethics review, DSMB oversight, or medical/safety decisions. Every generated artifact is a draft; every accountable act routes to a named, qualified human through a hard gate. The master gating matrix is [[non-delegable-functions-and-gates]]; the legal argument for why this line exists is [[legal-thesis-3123-vs-31252]].

> [!warning] Non-delegable
> No component described in this section signs, consents, approves, adjudicates causality, files with FDA, or makes a medical decision. Software cannot be a [21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52) transferee and cannot be subject to FDA enforcement. Where a page in this section says the system "produces" a Form 1572 or an IND safety report, read: *produces a draft that a qualified human reviews, owns, and signs*.

> [!interpretive] OSSICRO position
> The specific architecture in this section — the three-pass engine, the completeness ledger, the provenance model, the privacy state machine, the verifiable dossier — is an OSSICRO design thesis, not a regulatory category. Each page defends its design against the cited authority; none of it claims regulatory endorsement. The FDA 2025 AI-credibility framework this system self-classifies under is **draft** guidance (see [[part-11-and-ai-credibility]]).

## Reading order

**For a clinician** (you want to know what the system does for you and what it will never do):

1. [[two-modes-site-vs-sponsor-investigator]] — which of the two operating modes (plus the expanded-access branch) fits your situation.
2. [[generate-check-validate-engine]] — how a draft becomes a reviewable, gated package.
3. [[non-delegable-functions-and-gates]] — the acts that remain yours, by law.
4. [[single-pass-review-ux]] and [[completeness-ledger]] — how your review time is spent only on judgment calls.
5. [[patient-trial-matching]] and [[matching-engine]] — how a patient is matched to candidate programs.

**For a regulatory reviewer** (you are auditing whether the system is lawful):

1. [[architecture]] — components and the Part 11 environment.
2. [[compliance-mapping]] — artifact → authority → validation rule → responsible human.
3. [[part-11-and-ai-credibility]] — e-records/e-signatures posture and the AI risk-tiering argument (draft status flagged).
4. [[hipaa-and-privacy-gating]] and [[privacy-state-machine]] — the PHI boundary, enforced in code.
5. [[data-model]] — the audit trail, document state machine, and gate objects that make the above inspectable.
6. [[risks-and-limitations]] — what can go wrong and what mitigates it.

**For an engineer** (you are building or extending the system):

1. [[data-model]] — entities, state machines, audit trail.
2. [[generate-check-validate-engine]] — the pipeline contract.
3. [[draft-provenance-model]] — the span-level generation output contract.
4. [[claude-sdk-ai-in-the-loop]] — agent roles, permission modes, AI attribution.
5. [[data-integrations-ctgov-pubmed]] and [[smart-on-fhir-integration]] — external data surfaces.
6. [[roadmap]] — build order and why Form 1572 is the first end-to-end target.

## What lives in this section

| Page | Purpose |
|---|---|
| [[architecture]] | The five components and the Part 11-compliant substrate. |
| [[generate-check-validate-engine]] | Three passes, adversarial pre-review, human sign-off gates. |
| [[data-model]] | Entities, document state machine, document-ID scheme, ALCOA++ audit trail. |
| [[patient-trial-matching]] | ClinicalTrials.gov v2 integration and the HIPAA matching/enrollment boundary. |
| [[matching-engine]] | Multi-directional trial/condition/medication discovery with cited rationale. |
| [[matching-eligibility-adjudication]] | Per-criterion three-valued eligibility verdicts; investigator keeps the call. |
| [[matching-mechanism-graph]] | Biomarker → pathway → target → trial candidate expansion. |
| [[matching-evaluation-and-benchmarks]] | Measured matching performance on public benchmarks. |
| [[smart-on-fhir-integration]] | Chart ingestion (SMART App Launch + Bulk export; US Core, mCODE). |
| [[privacy-state-machine]] | Code-enforced 45 CFR 164.512(i) preparatory→enrollment transition. |
| [[micro-cro-operating-model]] | The thin accountable layer and its service tiers. |
| [[two-modes-site-vs-sponsor-investigator]] | Mode A vs. Mode B vs. the expanded-access branch. |
| [[compliance-mapping]] | The citation-carrying manifest for every generated artifact. |
| [[non-delegable-functions-and-gates]] | The master gating matrix. |
| [[part-11-and-ai-credibility]] | Part 11 posture; FDA 2025 AI-credibility (draft) risk tiering. |
| [[hipaa-and-privacy-gating]] | The privacy fulcrum: matching vs. enrollment. |
| [[single-pass-review-ux]] | Attention-triaged review lanes. |
| [[draft-provenance-model]] | Span-level (source → provenance → citation) triples. |
| [[completeness-ledger]] | Green/amber/red open-items contract per package. |
| [[verifiable-site-qualification-dossier]] | Cryptographically verifiable site dossier. |
| [[safety-clock-engine]] | 7/15-day deadline computation and escalation (never files, never adjudicates). |
| [[claude-sdk-ai-in-the-loop]] | Agent implementation, permission modes, Part 11 treatment of AI drafts. |
| [[data-integrations-ctgov-pubmed]] | ClinicalTrials.gov v2, PubMed/E-utilities, openFDA. |
| [[communication-hub]] | Role-scoped, auditable inter-actor messaging. |
| [[offline-local-deployment]] | Single-container deployment inside the covered-entity boundary. |
| [[prior-art-vcap-irex-smartirb]] | V-CAP and SMART IRB/IREx as published design precedents. |
| [[roadmap]] | Phased build plan. |
| [[risks-and-limitations]] | Legal, regulatory-motion, liability, adoption, and technical risks. |

## Related

- [[what-is-ossicro]]
- [[legal-thesis-3123-vs-31252]]
- [[non-delegable-functions-and-gates]]
- [[architecture]]
- [[generate-check-validate-engine]]
- [[data-model]]
- [[compliance-mapping]]
- [[micro-cro-accountable-layer]]
- [[INDEX]]

## Sources

- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [21 CFR 312.52 — Transfer of obligations to a contract research organization](https://www.law.cornell.edu/cfr/text/21/312.52)
- [21 CFR 312.3 — Definitions (sponsor-investigator)](https://www.law.cornell.edu/cfr/text/21/312.3)
- [FDA — E6(R3) Good Clinical Practice (final guidance, Sept 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025, PDF)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA Draft Guidance — Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making for Drug and Biological Products (Jan 2025, docket FDA-2024-D-4689)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological)
