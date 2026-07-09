---
title: "The Verifiable Site-Qualification Dossier — Requirement → Artifact → Citation → Signer"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "21 CFR 312.53 (selecting investigators and monitors; Form FDA 1572; CV; financial disclosure)"
  - "21 CFR Part 54 (financial disclosure; Forms FDA 3454/3455)"
  - "21 CFR Part 11 (electronic records; electronic signatures; audit trails)"
  - "ICH E6(R3) (essential records; sponsor oversight of investigator/site selection)"
  - "FDA Compliance Program 7348.811 (BIMO clinical-investigator inspections)"
tags: [ossicro/micro-cro, ossicro/part11, ossicro/engine, cfr/312, cfr/54, cfr/11, gcp/e6r3, fda-form/1572, fda-form/3454, lifecycle/activation, role/pharma, role/investigator, status/interpretive]
aliases: ["Verifiable Dossier", "Site Qualification Dossier", "Qualification Manifest"]
updated: 2026-07-09
---

# The Verifiable Site-Qualification Dossier — Requirement → Artifact → Citation → Signer

> [!authority] Governing authority
> The *requirements the dossier evidences* are black-letter: [21 CFR 312.53](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53) (investigator selection, Form FDA 1572, CV, financial-disclosure collection), [21 CFR Part 54](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54) (Forms FDA 3454/3455), [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) (e-records, e-signatures, audit trails), and the essential-records framework of ICH E6(R3) Appendix C. The *dossier construct itself* — a complete, citation-mapped, signer-accountable qualification package with an internal integrity layer — is an OSSICRO design position. Status: **Mixed**; every interpretive claim is marked.

A new or small site's largest liability to a pharma sponsor is not incompetence — it is **unverifiability**: no trial history, no inspection record, no coordinator infrastructure a feasibility questionnaire can score. The verifiable site-qualification dossier is OSSICRO's answer, and its sponsor-facing substance is deliberately conventional: a **complete, internally consistent essential-document package in which every qualification requirement on the sponsor's own checklist maps to a concrete artifact, the artifact to its governing citation, and the artifact to the qualified, credentialed human who signed it** — delivered in the document conventions sponsor quality and clinical-operations functions already consume (TMF Reference Model–aligned naming and indexing; TransCelerate-style qualification and training artifacts). Underneath, the package is assembled on a Part 11 audit trail with a hash-chained manifest — an *internal* integrity and inspection-readiness mechanism, not something a sponsor reviewer is asked to operate. The dossier narrows the sponsor's trust decision from "do we believe this unknown site?" toward "is this package complete against our checklist, and are its signers qualified?" — the evidence-shaped part of a decision that remains, in substance, a judgment about future conduct. This is the pharma trust wedge described in [[single-patient-site-and-pharma-acceptance]] and the tangible service asset of the [[micro-cro-operating-model|Micro-CRO]].

## The trust problem the dossier solves — and the part it cannot

Sponsor site selection is a regulated judgment: the sponsor must select "only investigators qualified by training and experience" ([21 CFR 312.53(a)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53)) and, before shipping drug, must obtain the investigator's signed [[form-fda-1572-statement-of-investigator|Form FDA 1572]] (§312.53(c)(1)), a CV or equivalent statement of qualifications (§312.53(c)(2)), and sufficient financial-interest information for [[form-fda-3454-3455-financial-disclosure|Part 54 certification or disclosure]] (§312.53(c)(4)). In practice the sponsor's gate is wider than the regulation: feasibility questionnaires, a site-qualification visit (SQV), GCP-training evidence, pharmacy/storage capacity, IRB arrangements, inspection history (Form 483s, warning letters), and enrollment realism — because non-enrolling sites are the dominant cost sink in early-phase programs (see [[pharma-partner-interface-iis]] and [[site-activation]]).

Be precise about what the sponsor actually distrusts. It is not, primarily, that a new site's documents might be falsified or tampered with; it is **prospective operational conduct** — coordinator bandwidth, protocol-deviation risk, data-entry quality over time, monitoring-finding rates, inspection exposure. No document package can prove future performance. What a document package *can* do is exhaust the evidence-shaped portion of the gate: demonstrate that every checkable requirement is met, on its face and in substance, by named, credentialed, personally accountable signers, with the operational-capacity questions (staffing, delegation, storage, safety intake, coordinator coverage) answered by concrete artifacts rather than questionnaire self-report. An unproven site otherwise fails the gate by default, not on the merits; a complete, internally consistent, sponsor-convention-native package is the single most persuasive artifact such a site can produce, and the one thing a solo physician with software support can genuinely produce to sponsor standard. The residual — confidence earned through conduct — accrues only in operation, which is why the dossier is the instrument for winning the *first* trial and the [[micro-cro-operating-model|Micro-CRO's]] oversight and performance record is the instrument for the second (see [[micro-cro-accountable-layer]]).

## What the dossier contains

The dossier is the [[startup-tmf-checklist|before-trial essential-records set]] restructured as evidence. Representative rows (the full mapping lives in [[document-catalog]] and [[compliance-mapping]]):

| Requirement | Governing citation | Artifact in the dossier | Signer |
|---|---|---|---|
| Investigator statement and commitments | [21 CFR 312.53(c)(1)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53) | Signed [[form-fda-1572-statement-of-investigator|Form FDA 1572]] (or 1572-equivalent commitment for non-IND contexts) | Investigator |
| Qualification by training and experience | 21 CFR 312.53(a), (c)(2) | Current CV, medical license(s), board certification | Investigator attests; sponsor judges |
| Financial disclosure | [21 CFR Part 54](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54); 312.53(c)(4) | [[form-fda-3454-3455-financial-disclosure|Form 3454 or 3455]] + one-year update commitment | Each investigator/sub-investigator |
| GCP and protocol training | ICH E6(R3) §2/§3 | Training certificates, dated, per delegated person (TransCelerate mutual-recognition GCP training where the sponsor accepts it) | Trainee; PI countersigns delegation |
| Delegation of tasks | ICH E6(R3); FDA 2009 Investigator Responsibilities guidance | [[delegation-of-authority-log]] | PI |
| Adequate resources and staffing | ICH E6(R3) §2 (investigator responsibilities) | Staffing and coordinator-coverage plan; source-backed feasibility responses (patient-population basis, competing-study census) | PI |
| IRB of record | [21 CFR Part 56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56) | IRB registration, reliance/central-IRB agreement, approval letter when issued | IRB ([[irb-iec]]) |
| Laboratory capability | E6(R3) essential records | CLIA/CAP certificates, normal ranges | Lab director |
| Drug storage and accountability | [21 CFR 312.61](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.61), 312.62(a) | Storage SOP, temperature-monitoring evidence, [[drug-accountability-log]] procedures | PI / pharmacist |
| Safety-reporting capability | [21 CFR 312.64(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.64) | [[safety-management-plan]] excerpt; PV intake contact and escalation path ([[safety-clock-engine]]) | PI; medical monitor if distinct |
| Records environment | [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) | System description; audit-trail and access-control attestation ([[part-11-and-ai-credibility]]) | Deploying entity |
| Agreement and budget | contract law; AKS safe harbor; FMV | [[clinical-trial-agreement-and-budget|CTA + FMV-documented budget]] | Both parties |

The engine's [[generate-check-validate-engine|check pass]] verifies completeness of this set against the sponsor's requested scope and the E6(R3) risk-proportionate essential-records frame; open items appear on the [[completeness-ledger]] as amber (needs a human act, e.g., a signature) or red (missing datum, with the exact resolving question).

## How a sponsor reviewer actually consumes it

The dossier is designed for the review path sponsors already run, assuming the reviewer **never executes any OSSICRO tooling** — pharma IT security policy does not permit running third-party software from an unvetted source inside the network, and no sponsor QA SOP contemplates recomputing a vendor's hash chain. The sponsor-facing deliverable is therefore:

1. **Sponsor-native document conventions.** Artifacts arrive as individually filed documents with visible signatures and dates, named and indexed per TMF Reference Model conventions (CDISC), ready to file into the sponsor's eTMF or investigator portal without transformation. Qualification and training artifacts follow TransCelerate Site Qualification & Training patterns (mutual-recognition GCP training, standardized site-profile forms) where the sponsor participates in those programs.
2. **A cross-reference index, not a tool.** A human-readable index maps each item on the sponsor's own qualification checklist to the specific artifact, its governing citation, and its signer — so completeness review is a checklist join the reviewer performs in their ordinary workflow, not a reading exercise and not a software exercise.
3. **Substance review.** The human step, unchanged: judge the signers' qualifications, the CV, the training, the facilities, the enrollment basis. The dossier's contribution is that everything the reviewer wants to check is present, findable, signed, and internally consistent (names, dates, versions, and license numbers agree across documents — the check pass enforces this before export).

The cryptographic layer sits *behind* this, not in front of it, as described next.

## The integrity layer: manifest and hash chain (internal; Part 11 and inspection-readiness)

Internally, the dossier's spine is a machine-readable **manifest**: one entry per requirement, each entry a tuple —

- **`requirement`** — the qualification requirement, stated as text plus its citation key into [[cfr-citation-map]] / [[ich-guideline-map]] (e.g., `21 CFR 312.53(c)(1)`).
- **`artifact`** — the document satisfying it, identified by document-ID ([[data-model]] numbering) and content hash (SHA-256 of the canonical rendition).
- **`provenance`** — how the artifact came to exist: source data, template and version, generating agent (human or AI, per [[draft-provenance-model]] and [[claude-sdk-ai-in-the-loop]]), and review history.
- **`signer`** — the qualified human who executed it, with the Part 11 signature record ([§11.50 signature manifestations](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.50); [§11.70 signature/record linking](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.70)) and the signer's role and qualification reference.
- **`timestamp`** — from the system's time-stamped, computer-generated, independent audit trail ([§11.10(e)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10)).

Manifest entries are hash-chained: each entry's hash covers its own content **plus the hash of the prior entry**, and the chain head is committed into the same append-only Part 11 audit trail that records every document state transition (draft → checked → human-reviewed → signed → filed — the [[data-model]] state machine). Two properties follow:

1. **Tamper-evidence.** Altering any artifact, signature record, or manifest entry after the fact breaks every downstream hash. This is OSSICRO's implementation of record-integrity discipline under Part 11, and it is what makes the exported package a reliable record over its retention life.
2. **Completeness-evidence.** The manifest enumerates the requirement set *first* (from the citation map) and binds artifacts to it, so an absent artifact is a visible unfilled row — the package cannot silently omit a requirement it claims to cover. The sponsor-facing cross-reference index is generated *from* this manifest, which is why it can be trusted to be exhaustive.

The audience for the chain is not the sponsor's day-to-day reviewer. It is (a) OSSICRO's own quality system, continuously; (b) a sponsor's **vendor-qualification or GCP audit**, where an auditor may verify integrity on request — recomputation requires only a standard SHA-256 utility and the documented procedure, no OSSICRO software; and (c) an FDA inspection (site under [Compliance Program 7348.811](https://www.fda.gov/media/75927/download), or the records environment itself), where a demonstrably tamper-evident record set is an inspection-readiness asset. A dossier export accordingly bundles the artifacts (canonical renditions), the cross-reference index, the manifest, the relevant audit-trail extract, and the written verification procedure — available to any party that wants it, required of none.

## What the dossier does not prove

> [!warning] Non-delegable
> The dossier is **evidence, not a decision**. The sponsor's selection of a qualified investigator ([21 CFR 312.53(a)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53)) remains the sponsor's judgment — a complete package does not oblige acceptance. The PI's 1572 attestation is the investigator's **personal legal commitment**; the [[form-fda-3454-3455-financial-disclosure|financial disclosures]] are each investigator's own; the [[irb-iec|IRB]] approval judgment is the board's; and FMV/anti-kickback conclusions on the budget belong to qualified counsel/compliance. No manifest proves the truth of an attestation, the adequacy of a qualification, or — above all — **future operational performance**: coordinator bandwidth, deviation rates, and data quality are demonstrated in conduct, not in documents. OSSICRO assembles, checks, and chains; qualified humans attest, sign, and decide. See [[non-delegable-functions-and-gates]].

> [!interpretive] OSSICRO position
> The dossier is the **pharma trust wedge** and part of the Micro-CRO's tangible moat — and the wedge is the completeness, not the cryptography. The wedge claim: a sponsor's trust gate for an unknown site is entity-shaped and evidence-shaped, not software-shaped — so the persuasive deliverable is a complete, credentialed, internally consistent package in the sponsor's own document conventions, exhausting the checkable portion of the gate and leaving only the substantive judgment the sponsor was always going to make. The hash-chained manifest is supporting infrastructure — Part 11 integrity discipline and audit/inspection readiness — not the sponsor-facing pitch. The moat claim: producing complete, citation-mapped, signer-accountable dossiers repeatedly — and standing behind enumerated obligations as a real transferee where needed ([[transfer-of-regulatory-obligations-toro]], [21 CFR 312.52](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52)) — is an accumulating, reputation-bearing asset that pure coordination software structurally cannot hold (see [[failed-disintermediation-case-studies]]). No regulation requires cryptographic verifiability; it is a design position layered on confirmed Part 11 obligations, and this wiki labels it as such.

In [[two-modes-site-vs-sponsor-investigator|Mode A]] the dossier is the site-activation package presented to the pharma sponsor; in Mode B the [[sponsor-investigator]] presents it to the supporting pharma's IIS committee and holds it as their own sponsor-side selection record; in the [[single-patient-site-enrollment|n-of-1 site]] case it is the expedited-qualification package that makes a one-patient site acceptable at all.

## Related
- [[single-patient-site-and-pharma-acceptance]]
- [[site-activation]]
- [[startup-tmf-checklist]]
- [[pharma-partner-interface-iis]]
- [[form-fda-1572-statement-of-investigator]]
- [[form-fda-3454-3455-financial-disclosure]]
- [[delegation-of-authority-log]]
- [[clinical-trial-agreement-and-budget]]
- [[compliance-mapping]]
- [[completeness-ledger]]
- [[draft-provenance-model]]
- [[data-model]]
- [[part-11-and-ai-credibility]]
- [[micro-cro-operating-model]]
- [[micro-cro-accountable-layer]]
- [[transfer-of-regulatory-obligations-toro]]
- [[two-modes-site-vs-sponsor-investigator]]
- [[non-delegable-functions-and-gates]]
- [[generate-check-validate-engine]]

## Sources
- [21 CFR 312.53 — Selecting investigators and monitors (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53)
- [21 CFR Part 54 — Financial Disclosure by Clinical Investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54)
- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [21 CFR 312.52 — Transfer of obligations to a contract research organization (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52)
- [ICH E6(R3) Good Clinical Practice — FDA guidance page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
- [FDA — Frequently Asked Questions: Statement of Investigator (Form FDA 1572) (2010 guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/frequently-asked-questions-statement-investigator-form-fda-1572)
- [FDA Compliance Program 7348.811 — Clinical Investigators (BIMO)](https://www.fda.gov/media/75927/download)
- [FDA — Bioresearch Monitoring Program (BIMO)](https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-guides/bioresearch-monitoring-program-bimo)
- [TransCelerate BioPharma — Site Qualification and Training initiative](https://www.transceleratebiopharmainc.com/initiatives/site-qualification-and-training/)
- [CDISC — Trial Master File (TMF) Reference Model](https://www.cdisc.org/tmf)