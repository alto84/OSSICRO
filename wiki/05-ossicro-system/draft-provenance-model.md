---
title: "Draft Provenance Model — (Source Datum → Provenance → Citation) Triples"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "21 CFR Part 11 (§11.10(a) validation; §11.10(b) human-readable copies; §11.10(e) audit trail; §11.70 signature/record binding)"
  - "ICH E6(R3) Section 4 (Data Governance — ALCOA++ data-integrity characteristics)"
  - "21 CFR 312.57, 312.62 (sponsor and investigator records)"
  - "FDA Draft Guidance on AI to Support Regulatory Decision-Making (Jan 2025, FDA-2024-D-4689)"
tags: [ossicro/engine, ossicro/part11, ossicro/ai-credibility, cfr/11, cfr/312, ich/e6r3, status/interpretive]
aliases: ["Provenance Triples", "Span Provenance", "Provenance Model"]
updated: 2026-07-09
---

# Draft Provenance Model — (Source Datum → Provenance → Citation) Triples

> [!authority] Governing authority
> [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) requires a secure, computer-generated, time-stamped audit trail for electronic records (§11.10(e)), validated systems (§11.10(a)), human-readable copies for inspection (§11.10(b)), and signatures bound to their exact records (§11.70). ICH E6(R3) Section 4 (Data Governance) requires data that are attributable, legible, contemporaneous, original, accurate, complete, consistent, enduring, available, and traceable (ALCOA++). Status: **Mixed** — those requirements are confirmed; the span-level triple contract that satisfies them is an interpretive OSSICRO construction.

Every span of text OSSICRO generates carries a machine-readable triple: **(source datum → provenance → citation)**. The triple is simultaneously three things: the *generation output contract* that a drafting agent must satisfy for its output to enter the pipeline at all; the *Part 11 / ALCOA++ audit trail* for the draft, produced at generation time rather than reconstructed afterward; and the *review interface*, because the [[single-pass-review-ux]] lanes are computed directly from the triples. Provenance and audit trail are one structure viewed from two directions — the same hash-chained Event record that satisfies an FDA inspector is what the reviewer clicks on.

## Anatomy of the triple

**1. Source datum.** The upstream fact the span expresses. Permitted sources are enumerated, not open-ended:

- a field of a structured entity in the [[data-model]] (`Study`, `IND`, `Site`, `Investigator`, `Document`, `SafetyReport`) — e.g., the investigator address on a draft [[form-fda-1572-statement-of-investigator|1572]] traces to `Investigator.address`;
- a chart element lawfully in scope under the [[privacy-state-machine]], ingested via [[smart-on-fhir-integration]], identified by FHIR resource and element;
- template text of verified provenance and license ([[external-templates-and-licenses]]), identified by template ID, version, and span offsets;
- a prior controlled document (protocol version, [[investigators-brochure|IB]] edition) identified by document ID and version in the Penn-style numbering scheme;
- an explicit human input, attributed to the person who supplied it;
- **or nothing** — in which case the span is marked `inferred`, and that marker is load-bearing: inferred spans are always foregrounded in review and can never enter a collapsed lane.

**2. Provenance.** The causal chain from source datum to rendered span: which agent or human produced it, by what transformation, when. For AI-generated spans this is the attribution record required for the engine's credibility posture ([[part-11-and-ai-credibility]], [[claude-sdk-ai-in-the-loop]]): model identity and version, input hash, generation timestamp, and — appended as review occurs — the reviewing human's identity and per-span disposition. For transcribed spans it is the verification rule that checked the transcription. For template spans it is the diff result (empty, for the boilerplate lane). Provenance entries are Events in the [[data-model]] — computer-generated, time-stamped, append-only, hash-chained, per [21 CFR 11.10(e)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10).

**3. Citation.** Where the span exists because a regulation or guideline requires it, the triple names the authority — the specific CFR or ICH subsection from [[compliance-mapping]]. The eligibility-criteria section of a protocol cites [21 CFR 312.23(a)(6)](https://www.law.cornell.edu/cfr/text/21/312.23); a 1572 field cites [312.53(c)](https://www.law.cornell.edu/cfr/text/21/312.53) and the FDA field instructions; an essential-record's presence in the package cites its ICH E6(R3) Appendix C row ([[document-catalog]]). Spans that serve no cited requirement are permissible (connective prose exists), but a *requirement* with no span pointing at it is a [[completeness-ledger]] red — the citation layer runs both directions.

## The generation output contract

The triple is enforced at the pipeline boundary: **a drafting agent's output that lacks triples is rejected before it becomes a `Document` at all.** This is the mechanism that prevents the classic LLM failure — fluent, unsourced assertion — from ever reaching a reviewer disguised as fact. The agent cannot claim a source it was not given; the pipeline verifies that each claimed source datum exists and (for transcriptions) that the span matches it, and everything unverifiable is downgraded to `inferred` and foregrounded. Fabricated citations are structurally excluded for the same reason: the citation element must resolve against [[compliance-mapping]], whose entries are human-curated with their authorities — a rule or citation absent from the map cannot be attached to a span.

## ALCOA++ satisfied by construction

| ALCOA++ characteristic | How the triple discharges it |
|---|---|
| Attributable | Provenance names the producing agent/model/human and every subsequent disposer. |
| Legible / Enduring / Available | Append-only store; human-readable export of any document *with its triples* per [§11.10(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10); retention per [312.57(c)](https://www.law.cornell.edu/cfr/text/21/312.57) / [312.62(c)](https://www.law.cornell.edu/cfr/text/21/312.62). |
| Contemporaneous | Provenance Events are written at generation/disposition time, UTC-stamped, by the system rather than the operator. |
| Original | The source datum element points at the original record; the span is explicitly a derivation, never a silent replacement. |
| Accurate | Transcription spans carry a passed verification rule; unverifiable spans are marked inferred rather than presumed accurate. |
| Complete / Consistent / Traceable | Hash-chaining makes omission or reordering detectable; the citation layer plus [[completeness-ledger]] make coverage checkable; every span is traceable to source in one hop. |

Because Events are hash-chained (each commits to its predecessor's hash), the [[verifiable-site-qualification-dossier]] can prove to a pharma counterparty — without trusting OSSICRO — that no record was altered after signature. Versioning follows the [[data-model]] discipline: a signed or filed document is never edited in place; changes spawn a new version with lineage, so §11.10(e)'s rule that changes shall not obscure previously recorded information holds structurally, and [§11.70](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.70) keeps every signature bound to the exact version signed.

## Provenance as UX

The [[single-pass-review-ux]] lanes are a pure function of the triples: passed-verification transcriptions → deterministic lane; empty-diff template spans → boilerplate lane; everything else, including all `inferred` spans, → foregrounded lane. The reviewer inspecting a span sees its triple — source, chain, citation — in place. This is the sense in which the strategy holds that *provenance is the Part-11 audit trail rendered as UX*: there is no separate compliance artifact to maintain, and no way for the review interface and the inspection record to disagree, because they are reads of the same structure.

> [!warning] Non-delegable
> Provenance **attributes**; it does not transfer responsibility. Recording that a span was AI-generated does not make the model accountable for it — no software can hold a regulatory obligation ([[legal-thesis-3123-vs-31252|21 CFR 312.52 forecloses it]]). The human who signs the document owns its entire content, triples included, under [§11.70](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.70) and the 1571/1572 attestations. Likewise, a span's citation is a claim that a requirement is *addressed*, never a machine determination that it is *satisfied* — satisfaction judgments route to the gates in [[non-delegable-functions-and-gates]].

> [!interpretive] OSSICRO position
> Part 11 requires an audit trail for operator entries and actions on electronic records; it does not require span-level provenance triples, and no regulation does. The triple contract is OSSICRO's construction, defended on two grounds: (1) it satisfies the confirmed Part 11 and E6(R3) data-governance requirements *by schema rather than by operator discipline*; (2) it is what makes AI drafting auditable at all — under the FDA 2025 AI-credibility **draft** guidance, the transparency of a model's contribution to a regulatory record is central to its credibility assessment, and span-level attribution is the strongest transparency OSSICRO can offer. Flagged interpretive; the guidance is draft (comments closed 2025-04-07).

## Related

- [[single-pass-review-ux]]
- [[completeness-ledger]]
- [[data-model]]
- [[generate-check-validate-engine]]
- [[compliance-mapping]]
- [[part-11-and-ai-credibility]]
- [[claude-sdk-ai-in-the-loop]]
- [[verifiable-site-qualification-dossier]]
- [[smart-on-fhir-integration]]
- [[privacy-state-machine]]
- [[external-templates-and-licenses]]
- [[non-delegable-functions-and-gates]]
- [[document-catalog]]

## Sources

- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [21 CFR 11.10 — Controls for closed systems (§§11.10(a), (b), (e))](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10)
- [21 CFR 11.70 — Signature/record linking](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.70)
- [21 CFR 312.57 — Recordkeeping and record retention (sponsor)](https://www.law.cornell.edu/cfr/text/21/312.57)
- [21 CFR 312.62 — Investigator recordkeeping and record retention](https://www.law.cornell.edu/cfr/text/21/312.62)
- [21 CFR 312.23 — IND content and format](https://www.law.cornell.edu/cfr/text/21/312.23)
- [21 CFR 312.53 — Selecting investigators and monitors](https://www.law.cornell.edu/cfr/text/21/312.53)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025, PDF) — Section 4 Data Governance; Appendix C](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA Guidance — Part 11, Electronic Records; Electronic Signatures: Scope and Application (Aug 2003)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application)
- [FDA Draft Guidance — Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making for Drug and Biological Products (Jan 2025, FDA-2024-D-4689)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological)
