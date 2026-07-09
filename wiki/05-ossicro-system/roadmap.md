---
title: "Roadmap — Phased Build"
section: "05-ossicro-system"
status: interpretive
governing_authority:
  - "21 CFR 312.52 (constraint on every phase)"
  - "21 CFR Part 11 (substrate requirement from Phase 2 onward)"
  - "ICH E6(R3); ICH M11 (forward standards built to)"
tags: [ossicro/engine, ossicro/micro-cro, ossicro/matching, ossicro/part11, status/interpretive]
aliases: ["Roadmap", "Phased Build", "Build Plan"]
updated: 2026-07-09
---

# Roadmap — Phased Build

> [!authority] Governing authority
> The roadmap itself is an OSSICRO planning document (status: **Interpretive** throughout). The constraints it builds under are binding: [21 CFR 312.52](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52) forbids any phase from drifting toward software-as-transferee; [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) governs the substrate from the first generated record; ICH E6(R3) (FDA final 2025-09-09) and ICH M11 (final template 2025-11-19) are the forward standards every artifact is built to.

The build order follows dependency and risk, not ambition: the citation spine first (everything downstream validates against it), the narrowest provable engine loop second, breadth after correctness. Each phase has an explicit success criterion; a phase is done when its criterion is verifiably met, not when its features exist. The strategist improvements adopted 2026-07-09 (see `docs/strategy-review-fable-2026-07-09.md`) are threaded into the phases where they structurally belong rather than appended as a parallel track.

## Phase 0 — Regulatory wiki and citation map *(this deliverable)*

The exhaustively cited knowledge base: every page in this vault, the [[cfr-citation-map]], [[ich-guideline-map]], [[fda-guidance-map]], [[fda-form-index]], and the confirmed-vs-interpretive calibration standard ([[confirmed-vs-interpretive]]). This is the compliance-mapping spine everything else validates against — a validation rule that cannot cite a wiki page and its underlying authority does not ship.

**Success criterion:** complete IA per [[INDEX]]; every requirement claim carries a citation; interpretive positions labelled; reviewed by a qualified human.
**Also seeded here:** the [[regulatory-change-log]] change-watch (strategist item 7), because the wiki begins rotting the day it is finished — E6(R3) has no US compliance date yet, M11 is newly final, and the AI-credibility guidance is still draft.

## Phase 1 — Template library, public-domain first

Seed from unambiguous sources: the NIH-FDA protocol template, NIH-model DSMB charters, the official FDA forms (1571, 1572, 3454/3455, 3500A, 3926, 3674), ICH M11/E6(R3). Schema-mirror (structure, not text) the institutional libraries — Penn's numbered document-control scheme, Pitt's amendment taxonomy, UNC Lineberger, Stanford CRQ — with license status verified per template and recorded in [[external-templates-and-licenses]]. Consortium-gated IP (TransCelerate) is cross-checked, never reproduced.

**Success criterion:** every template in the library carries provenance, license status, and a mapping to the [[document-catalog]] rows it satisfies.

## Phase 2 — Form 1572 generate/check/validate

The deliberately narrow proof of the engine pattern: [[form-fda-1572-statement-of-investigator|Form FDA 1572]] has a fixed FDA schema, official field instructions, and a real non-delegable gate (the investigator's signature, [21 CFR 312.53(c)(1)](https://www.law.cornell.edu/cfr/text/21/312.53)). Build the full loop — generate from CV/site/IRB structured data, check fields 1-9, validate against the citation-traced rule set, fail to the human signature gate — end to end, on one document.

This phase also stands up the substrate the loop requires: the Part 11 audit trail and e-signature capture ([[part-11-and-ai-credibility]]), the [[draft-provenance-model]] (every generated span carries source→provenance→citation), the [[completeness-ledger]] (green/amber/red output contract), and the first [[single-pass-review-ux|attention-triaged review surface]] — strategist items 3 and 5, placed here because retrofitting provenance later would be structurally dishonest.

**Success criterion:** a qualified human can review and sign a generated 1572 in a single pass, with every field traceable to its source and the audit trail reconstructable.

## Phase 3 — IND assembly engine

The full [21 CFR 312.23](https://www.law.cornell.edu/cfr/text/21/312.23) package for Mode B ([[two-modes-site-vs-sponsor-investigator]]): 1571 cover, general investigational plan, [[investigators-brochure|IB]], protocol to the ICH M11 CeSHarP structured schema ([[clinical-protocol-and-synopsis]]), CMC, pharm/tox, prior human experience — plus the document state machine (draft → checked → human-reviewed → signed → filed → archived) and the six-amendment-type taxonomy ([[annual-reporting-and-amendments]]). The **adversarial machine pre-review and cross-document consistency engine** (strategist item 4) lands here: an independent QC agent, structurally separate from drafting, red-teams the package and verifies PI/site/IND-number/protocol-version identity across every document before the human sees it ([[generate-check-validate-engine]]).

**Success criterion:** a complete, internally consistent draft IND package with a fully green-or-explained [[completeness-ledger]], reviewed by a regulatory professional against the 312.23 checklist.

## Phase 4 — Coordination engine

Inter-entity document-flow routing per the [[inter-entity-document-flow-map]]; the milestone tracker across FDA/IRB/DSMB/pharma counterparties; IRB reliance via the SMART IRB/IREx pattern ([[prior-art-vcap-irex-smartirb]], [[single-irb-mandate-and-central-irbs]]); and the dedicated [[safety-clock-engine]] (strategist second tier) computing 7/15-day [21 CFR 312.32](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32) deadlines with escalation — computing and escalating only; the causality call and the filing act stay human ([[non-delegable-functions-and-gates]], gates G4/G11). The [[communication-hub]] ships here with role scoping and the Medical-Affairs/Clinical-Development firewall.

**Success criterion:** a simulated study run in which every document reaches every entitled counterparty, every deadline fires with correct lead time, and no gated act has an automated path.

## Phase 5 — Matching and frontend

The highest-risk COU, deliberately late: [[matching-engine]] over ClinicalTrials.gov API v2, PubMed/E-utilities, and openFDA ([[data-integrations-ctgov-pubmed]]); [[smart-on-fhir-integration|SMART-on-FHIR chart ingestion]] behind the code-enforced [[privacy-state-machine]] (strategist item 1); the retrieve→adjudicate [[matching-eligibility-adjudication]] layer with mechanism-aware expansion ([[matching-mechanism-graph]]) and three-valued per-criterion verdicts (item 2); and the [[matching-evaluation-and-benchmarks|evaluation harness]] on CHIA/TREC/n2c2 run **before** any patient-facing claim of matching quality. The pharma-style frontend with four persona portals ([[four-entry-points]]) completes the phase. [[offline-local-deployment|Single-container local deployment]] ships with it, because the preparatory-review privacy basis assumes PHI never leaves the covered entity ([[hipaa-and-privacy-gating]]).

**Success criterion:** benchmark recall/precision published; privacy state machine demonstrated to block PHI egress and to hard-gate the preparatory→enrollment transition; eligibility verdicts carry citations an investigator can check.

## Phase 6 — Micro-CRO service layer

Stand up the accountable entity itself: legal formation, SOPs and quality system ([[micro-cro]]), [[transfer-of-regulatory-obligations-toro|TORO]] tooling with per-obligation enumeration, the tiered service model (self-serve → automated triage → paid human review at gates → enumerated-obligation assumption; [[micro-cro-operating-model]]), and the [[verifiable-site-qualification-dossier]] (strategist item 6) as the pharma trust wedge. Counsel review of the service model precedes any assumption of obligations ([[risks-and-limitations]]).

**Success criterion:** the entity can lawfully execute a TORO for a defined obligation set and demonstrate, at audit, that it discharges what it assumed.

## Sequencing rationale and standing rules

- **Wiki → templates → engine → coordination → matching → entity** is a dependency chain: rules cite the wiki; generation instantiates templates; coordination routes what the engine produces; matching feeds the front of a pipeline that must already work; the entity assumes obligations only for a system proven to discharge them.
- **Matching after drafting**, although matching is the user-visible front door, because it is the higher-influence context of use under the FDA AI-credibility framework ([[part-11-and-ai-credibility]]) and must not launch ahead of its evaluation harness.
- **Standing rule for every phase:** no phase introduces an automated path through any gate in the [[non-delegable-functions-and-gates|master gating matrix]]; each phase's adversarial review explicitly attempts to find one, and finding one is a release blocker.
- The open-dataset publication of computable eligibility (strategist second tier) trails Phase 5 as a community deliverable once benchmark quality is demonstrated.

## Related

- [[what-is-ossicro]]
- [[architecture]]
- [[generate-check-validate-engine]]
- [[non-delegable-functions-and-gates]]
- [[part-11-and-ai-credibility]]
- [[hipaa-and-privacy-gating]]
- [[privacy-state-machine]]
- [[matching-eligibility-adjudication]]
- [[matching-evaluation-and-benchmarks]]
- [[completeness-ledger]]
- [[verifiable-site-qualification-dossier]]
- [[safety-clock-engine]]
- [[micro-cro-operating-model]]
- [[regulatory-change-log]]
- [[risks-and-limitations]]
- [[prior-art-vcap-irex-smartirb]]

## Sources

- [21 CFR 312.52 (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52)
- [21 CFR 312.23 — IND content and format (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23)
- [21 CFR Part 11 (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [ICH E6(R3) — FDA final guidance (2025-09-09)](https://www.fda.gov/media/169090/download)
- [ICH M11 Clinical Electronic Structured Harmonised Protocol (CeSHarP)](https://www.ich.org/page/multidisciplinary-guidelines)
- [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api)
- [FDA Draft Guidance: AI to Support Regulatory Decision-Making (2025, DRAFT)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological)
- [SMART IRB](https://smartirb.org/) · [IREx](https://www.irbexchange.org/)
