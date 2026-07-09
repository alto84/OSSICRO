---
title: "Risks and Limitations"
section: "05-ossicro-system"
status: interpretive
governing_authority:
  - "21 CFR 312.52 (the structural legal risk)"
  - "FDA Draft Guidance: AI to Support Regulatory Decision-Making (2025, DRAFT)"
  - "ICH E6(R3); ICH M11 (regulatory motion)"
  - "45 CFR 164.512(i) (privacy exposure)"
tags: [ossicro/gating, ossicro/ai-credibility, ossicro/part11, ossicro/micro-cro, cfr/312, status/interpretive]
aliases: ["Risks", "Limitations", "Risk Register"]
updated: 2026-07-09
---

# Risks and Limitations

> [!authority] Governing authority
> This page is OSSICRO's own risk register (status: **Interpretive** — it is analysis, not regulation). The authorities that define the risk surface are binding or near-binding: [21 CFR 312.52](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52) (the illegality of software-as-transferee), the [FDA 2025 AI draft guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological) (unsettled AI acceptance), ICH E6(R3)/M11 (standards in motion), and [45 CFR 164.512(i)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512) (privacy exposure at matching).

A system that drafts regulatory documentation a clinician will rely on, for trials in which patients receive investigational drugs, must be honest about its failure modes. This page enumerates them, ranked, with the mitigation each one carries and — where a risk cannot be mitigated to zero — the residual limitation stated plainly. It is the counterpart to [[what-is-ossicro]]: that page says what the system is; this page says where it can fail.

## 1. Legal risks (highest severity)

**1a. Drift toward software-as-transferee.** The controlling constraint is [21 CFR 312.52(b)](https://www.law.cornell.edu/cfr/text/21/312.52): sponsor obligations transfer only to a legally accountable entity. Any feature that lets the software *own* an accountable act — auto-filing a safety report, auto-signing a form, auto-adjudicating causality — is not a compliance gap but an illegal structure ([[legal-thesis-3123-vs-31252]]). *Mitigation:* the [[non-delegable-functions-and-gates|master gating matrix]] is code-enforced and fail-closed; every phase's adversarial review attempts to find an automated path through a gate, and finding one blocks release ([[roadmap]]); the [[micro-cro-accountable-layer|micro-CRO]] is a real entity holding real obligations under a written [[transfer-of-regulatory-obligations-toro|TORO]]. *Residual:* a determined operator misusing a self-hosted deployment could bypass local gates; OSSICRO's answer is that the legal obligation then rests where it always did — on the human sponsor-investigator — and the audit trail records what happened.

**1b. Product liability and unauthorized-practice exposure.** A system whose outputs touch medical and legal decisions attracts product-liability and unauthorized-practice-of-law/medicine theories. *Mitigation:* strict draft-for-qualified-human-review framing on every artifact; no clinical recommendation function (eligibility verdicts cite evidence for the investigator's determination — they do not recommend treatment; [[matching-eligibility-adjudication]]); counsel review of the micro-CRO service model before it assumes obligations. *Residual:* framing does not immunize; this exposure is managed, not eliminated, and is a standing item for entity counsel.

**1c. Template and content licensing.** TransCelerate's clinical protocol template is consortium IP behind a membership gate; Advarra and similar templates are proprietary. *Mitigation:* public-domain-first seeding (NIH-FDA protocol template, NIH DSMB charters, FDA forms, ICH M11); schema-mirroring rather than copying for institutional libraries; per-template provenance and license verification in [[external-templates-and-licenses]].

## 2. Regulatory-motion risks

The frame is moving under the system. As of this writing: ICH E6(R3) — FDA final guidance published 2025-09-09, **no US compliance date set**; ICH M11 — final template 2025-11-19, ecosystem tooling immature; FDA DCT guidance — final 2024-09-18; FDA AI-credibility guidance — **still draft** (published 2025-01-07, comments closed 2025-04-07); the 2015 sponsor-investigator IND guidance — still draft after a decade. A wiki page, template, or validation rule citing any of these can silently rot. *Mitigation:* build to E6(R3)/M11 as forward standards; version every citation with its adoption date and status; flag draft guidances in-page wherever relied on ([[confirmed-vs-interpretive]]); and run the [[regulatory-change-log]] change-watch, which diffs FDA/ICH/eCFR sources on a cadence and flags every affected page, template, and rule through the citation-dependency graph, with a human curator confirming each change. *Residual:* the watch reduces detection latency; it does not remove the window between an authority changing and the corpus catching up. Users are told to verify load-bearing citations at point of use.

## 3. AI-acceptance risk

FDA acceptance of AI-drafted regulatory text is not a settled position; the governing guidance is draft ([[part-11-and-ai-credibility]]). *Mitigation:* the explicit low-influence-COU argument for drafting (human review is structural, the model output is never the decision), the stricter credibility treatment of matching as a higher-influence COU with a public-benchmark evaluation harness ([[matching-evaluation-and-benchmarks]]), full AI-authorship attribution in the Part 11 audit trail, and the discipline of never asserting "automation-permitted" where only "human-sign-off-permitted" is supportable. *Residual:* FDA could finalize the guidance in a form that imposes heavier burdens on document-drafting COUs than OSSICRO's tiering argument assumes; the argument is flagged interpretive everywhere it appears, and the [[regulatory-change-log]] watches the docket.

## 4. Privacy risk

The highest-severity technical failure mode is silent PHI egress at the matching layer — a HIPAA breach at scale that would also destroy clinician trust. The lawful basis for matching ([45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512) preparatory review) is conditioned on PHI not leaving the covered entity ([[hipaa-and-privacy-gating]]). *Mitigation:* the boundary is architectural, not procedural — local-first processing inside the covered entity ([[offline-local-deployment]]), the code-enforced [[privacy-state-machine]] with a hard logged preparatory→enrollment transition gated on authorization or waiver, minimum-necessary reads, and ephemeral audited access. *Residual:* misconfiguration by a deploying institution remains possible; the deployment defaults fail closed and the audit trail is designed to make any egress visible after the fact.

## 5. Adoption and trust risks

**5a. Pharma's trust gate is entity-shaped.** A sponsor deciding whether to accept a new, small, or single-patient site is evaluating an accountable counterparty, not a software stack ([[pharma-partner-interface-iis]], [[single-patient-site-and-pharma-acceptance]]). Coordination-only software has already failed in the market twice — Science 37 (~$1B SPAC valuation to a ~$38M take-private) and TrialSpark (pivoted into Formation Bio, a drug developer) — which OSSICRO reads as structural, not incidental ([[failed-disintermediation-case-studies]]). *Mitigation:* OSSICRO's unit of persuasion is the complete, internally consistent, credentialed dossier — the [[verifiable-site-qualification-dossier]], verifiable without trusting OSSICRO — plus a real micro-CRO entity where an entity is what the counterparty requires. *Residual:* some sponsors will decline new sites regardless of dossier quality; OSSICRO cannot manufacture counterparty willingness (gate G14, [[non-delegable-functions-and-gates]]).

**5b. Clinician overreliance.** The subtler adoption risk is the opposite of rejection: a clinician who trusts drafts too much and reviews too little, hollowing out the human-in-the-loop the whole legal architecture depends on. *Mitigation:* the [[single-pass-review-ux]] triages attention to exactly the spans that need judgment (inferred/interpretive lanes foregrounded, deterministic lanes collapsed but inspectable); the [[completeness-ledger]] makes open judgment items (amber) impossible to overlook; gate signatures record the meaning of what was attested. *Residual:* no UX can compel diligence; the signature's legal weight rests, as it always has, on the signer.

## 6. Technical limitations (stated as limitations, not risks to argue away)

- **Eligibility matching has a recall/precision ceiling on free-text criteria.** Ranking is not adjudication; even the three-valued adjudication layer will emit *indeterminate* verdicts wherever chart data or criterion semantics are insufficient. This is by design — indeterminate routes to a human with the exact resolving question — but it means OSSICRO's matching is a screening aid, never an eligibility determination, and its measured performance is published rather than asserted ([[matching-evaluation-and-benchmarks]]).
- **Generative drafting can fabricate.** Language models produce fluent, wrong text. Every generated span therefore carries source→provenance→citation triples ([[draft-provenance-model]]), unsourced spans are flagged as such, and the adversarial pre-review agent is structurally separate from the drafting agent ([[generate-check-validate-engine]]). The residual hallucination rate is nonzero; the human reviewer is the control of record.
- **Model and data drift.** Model versions change; ClinicalTrials.gov records are uneven in quality; eligibility text is inconsistent across registries ([[data-integrations-ctgov-pubmed]]). Versioned model records, re-run benchmarks per model change, and the change-watch cadence are the controls.
- **Coverage limits.** The corpus and engine are US-frame first (21 CFR, HIPAA, Common Rule); EU/ICH obligations are mapped where load-bearing ([[qualified-person-qppv-eu]]) but the system does not claim EU CTR operational coverage. Pediatric (21 CFR 50 Subpart D), prisoner, and other special-population overlays are surfaced as requirements, not fully templated in early phases.

> [!warning] Non-delegable
> The deepest limitation is the intended one. OSSICRO cannot obtain consent, approve a protocol, judge causality, sign a 1571 or 1572, determine fair market value, decide to supply drug, or release a submission to FDA — and it is built so that it never appears to. Where this page says "mitigation," the mitigation is in every case a qualified human or accountable entity in the loop ([[non-delegable-functions-and-gates]]). A user seeking a system that removes the human owns a different risk register than this one.

> [!interpretive] OSSICRO position
> Ranking legal risk above technical risk is itself a design judgment: a hallucinated draft caught by a structurally required reviewer is a recoverable error; an architecture that quietly assumes an obligation software cannot hold is not. Every mitigation above therefore resolves to the same two instruments — the gating matrix and the audit trail — and the honest summary of this page is that OSSICRO's safety case rests on their integrity.

## Related

- [[non-delegable-functions-and-gates]]
- [[legal-thesis-3123-vs-31252]]
- [[failed-disintermediation-case-studies]]
- [[part-11-and-ai-credibility]]
- [[hipaa-and-privacy-gating]]
- [[privacy-state-machine]]
- [[matching-evaluation-and-benchmarks]]
- [[draft-provenance-model]]
- [[single-pass-review-ux]]
- [[completeness-ledger]]
- [[verifiable-site-qualification-dossier]]
- [[regulatory-change-log]]
- [[micro-cro-operating-model]]
- [[external-templates-and-licenses]]
- [[roadmap]]
- [[confirmed-vs-interpretive]]

## Sources

- [21 CFR 312.52 — Transfer of obligations to a contract research organization (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52)
- [FDA Draft Guidance: Considerations for the Use of AI to Support Regulatory Decision-Making for Drug and Biological Products (2025, DRAFT)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological)
- [ICH E6(R3) — FDA final guidance (2025-09-09)](https://www.fda.gov/media/169090/download)
- [FDA Guidance: Conducting Clinical Trials With Decentralized Elements (final, 2024-09-18)](https://www.fda.gov/media/167696/download)
- [45 CFR 164.512 — research provisions (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512)
- [21 CFR Part 11 (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [Kim MJ, et al. Harvard Catalyst IND/IDE Consult Service. Clin Transl Sci. 2014. PMID 24455986](https://doi.org/10.1111/cts.12146)
