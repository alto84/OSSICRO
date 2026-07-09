---
title: "Data Model — Entities, Document State Machine, and Audit Trail"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "21 CFR 11.10(e) (audit trail); 11.50-11.300 (electronic signatures)"
  - "21 CFR 312.57, 312.62 (records and retention)"
  - "ICH E6(R3) (data governance / ALCOA++; Appendix C essential records)"
  - "45 CFR 164.514 (de-identification; limited data sets)"
tags: [ossicro/engine, ossicro/part11, ossicro/gating, cfr/11, cfr/312, ich/e6r3, status/interpretive]
aliases: ["Data Model", "Document State Machine"]
updated: 2026-07-09
---

# Data Model — Entities, Document State Machine, and Audit Trail

> [!authority] Governing authority
> The audit-trail and e-signature requirements are [21 CFR 11.10(e)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10) and [21 CFR 11.50–11.300](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11); record content and retention follow [21 CFR 312.57](https://www.law.cornell.edu/cfr/text/21/312.57) and [312.62](https://www.law.cornell.edu/cfr/text/21/312.62); data-integrity expectations follow ICH E6(R3) data governance (ALCOA++). Status: **Mixed** — those constraints are confirmed; the entity decomposition, state machine, and numbering scheme are interpretive OSSICRO design positions built to satisfy them.

The data model is where the wiki's legal analysis becomes machine state. Its design rule: **every regulated fact is an entity, every regulated transition is an event, and every event is attributable** — so that an FDA inspector, an IRB, or a skeptical pharma partner can reconstruct exactly who did what, when, on what basis, and under what authority ([21 CFR 312.58](https://www.law.cornell.edu/cfr/text/21/312.58) makes sponsor records inspectable on request; E6(R3) requires records sufficient to permit reconstruction and evaluation of the trial).

## Core entities

| Entity | What it records | Anchoring authority |
|---|---|---|
| **Study** | Protocol identity, phase, design, mode (A / B / expanded access — [[two-modes-site-vs-sponsor-investigator]]), risk assessment, critical-to-quality factors | [21 CFR 312.23(a)(6)](https://www.law.cornell.edu/cfr/text/21/312.23); ICH E6(R3) §7, E8(R1) |
| **IND** | IND number, holder, effective date, 30-day clock, status (active / clinical hold / inactive / withdrawn), annual-report anniversary | [21 CFR 312.20–312.45](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B); [312.33](https://www.law.cornell.edu/cfr/text/21/312.33) |
| **Site** | Facility, IRB of record, lab certifications, activation status, port of the [[verifiable-site-qualification-dossier]] | [21 CFR 312.53](https://www.law.cornell.edu/cfr/text/21/312.53); Form FDA 1572 fields |
| **Investigator / Sponsor-Investigator** | Qualifications (CV), 1572 status, financial-disclosure status (3454/3455), delegation log linkage, training evidence | [21 CFR 312.53(c)](https://www.law.cornell.edu/cfr/text/21/312.53); [Part 54](https://www.law.cornell.edu/cfr/text/21/part-54); [312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3) |
| **Subject (coded)** | Study-assigned code, enrollment status, consent status and version, privacy-state ([[privacy-state-machine]]). **Identities never appear in this entity or in any log** — the code-to-identity key stays with the site per E6(R3) confidentiality requirements | [21 CFR 50](https://www.law.cornell.edu/cfr/text/21/part-50); [45 CFR 164.514](https://www.law.cornell.edu/cfr/text/45/164.514) |
| **Document** | A versioned regulatory record with document-ID, template provenance, state (below), gates, and provenance spans | [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11); E6(R3) Appendix C |
| **Obligation** | A discharged-or-open regulatory duty, keyed to its CFR/ICH subsection and to its owner (sponsor-investigator or micro-CRO transferee under a [[transfer-of-regulatory-obligations-toro|TORO]]) | [21 CFR 312.50–312.69](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D); [312.52](https://www.law.cornell.edu/cfr/text/21/312.52) |
| **Gate** | A non-delegable act: the act, the responsible qualified human, the reserving authority, discharge evidence (Part 11 signature or documented external event) | [[non-delegable-functions-and-gates]] |
| **Event** | Any state transition: document moves, gate discharges, deadline starts, privacy-state changes, AI generations, human dispositions | [21 CFR 11.10(e)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10) |
| **SafetyReport** | AE/SAE intake, seriousness/expectedness/causality *fields awaiting human determination*, the applicable clock (7-day / 15-day / none), submission evidence | [21 CFR 312.32](https://www.law.cornell.edu/cfr/text/21/312.32); ICH E2A; [[safety-clock-engine]] |
| **Milestone** | Tracked deadlines and counterparty commitments feeding the frontend tracker | [21 CFR 312.33](https://www.law.cornell.edu/cfr/text/21/312.33), [312.40](https://www.law.cornell.edu/cfr/text/21/312.40); IRB expiration dates |

The **Obligation** entity is the model's legal spine: in Mode B every sponsor obligation (312.50–312.59) and every investigator obligation (312.60–312.69) instantiates against the same physician per [21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3); a TORO reassigns enumerated sponsor obligations to the micro-CRO entity, and — mirroring [312.52(a)](https://www.law.cornell.edu/cfr/text/21/312.52) — any obligation not named in the instrument remains with the sponsor-investigator. The model cannot represent an obligation owned by software; the owner field admits only natural persons and legal entities. That is a schema-level encoding of the wiki's central legal thesis ([[legal-thesis-3123-vs-31252]]).

## Document state machine

Every Document moves through one canonical lifecycle:

```
draft → checked → human-reviewed → signed → filed → archived
```

- **draft** — output of the generate pass; watermarked DRAFT; carries provenance spans ([[draft-provenance-model]]).
- **checked** — passed the check pass (completeness + adversarial pre-review + cross-document consistency); the [[completeness-ledger]] is attached. Red ledger items block this transition.
- **human-reviewed** — a qualified human has dispositioned every foregrounded span and every amber ledger item ([[single-pass-review-ux]]). The reviewer's identity and per-span dispositions enter the audit trail.
- **signed** — all gates attached to the document are discharged with Part 11 signatures ([21 CFR 11.50](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.50), [11.70](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.70), [11.100–11.300](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-C)). Signing is always a human act; the state machine has no automated path into this state.
- **filed** — transmitted to its receiving counterparty (FDA, IRB, sponsor, DSMB) as an explicit human-authorized action; the transmission evidence (submission receipt, acknowledgment letter) is itself a Document.
- **archived** — retained per [21 CFR 312.57(c)](https://www.law.cornell.edu/cfr/text/21/312.57) / [312.62(c)](https://www.law.cornell.edu/cfr/text/21/312.62) (2 years past approval, or 2 years past discontinuation-and-notification) and E6(R3) essential-records expectations; see [[record-retention-and-archival]].

Transitions are monotonic within a version. A change to a signed or filed document never edits in place: it spawns a **new version** linked to its predecessor, restarting the lifecycle, so that no signed record is ever altered after signature (Part 11 §11.10(e) requires that audit-trail changes "shall not obscure previously recorded information"; §11.70 binds the signature to the exact record signed).

**Amendment taxonomy.** For IND-bound documents the versioning layer distinguishes the six amendment types in Pitt's published template taxonomy, mapped to their CFR triggers: new protocol, protocol change, new investigator ([21 CFR 312.30](https://www.law.cornell.edu/cfr/text/21/312.30)(a)/(b)/(c)), information amendment ([312.31](https://www.law.cornell.edu/cfr/text/21/312.31)), change of sponsor, and change of sponsor-investigator. Each type prescribes its own document set and validation rules in the [[generate-check-validate-engine]].

## Document-ID numbering

Document IDs follow the Penn Office of Clinical Research numbered document-control pattern (e.g., `03.01.01`): a stable hierarchical identifier of section → document class → instance, independent of title or version. Version and date are separate fields, so `03.01.01 v2.0` unambiguously names one record. The scheme is interpretive (no regulation prescribes a numbering system) but it operationalizes E6(R3)'s expectation that essential records be organized, retrievable, and reconstructable, and it gives the [[completeness-ledger]] and [[compliance-mapping]] a stable join key. The TMF/ISF binder index ([[regulatory-binder-isf-index]]) renders directly from it.

## Audit trail — ALCOA++ as schema

The Event entity is the audit trail, engineered to [21 CFR 11.10(e)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10): computer-generated, time-stamped (UTC plus local offset), independent of the operator, append-only, and never obscuring prior entries. Each ALCOA++ property is a schema-enforced field, not a policy aspiration:

| ALCOA++ property | Schema enforcement |
|---|---|
| Attributable | Every event carries an actor: a named human, or an AI agent identity (model, version, input hash) *paired with* the human reviewer who dispositioned its output. |
| Legible / Enduring / Available | Append-only store; human-readable export for inspection per §11.10(b); retention per 312.57(c)/312.62(c). |
| Contemporaneous | Events are written at the moment of the transition by the system, not reconstructed later. |
| Original | The signed record and its hash are preserved; copies are marked as copies. |
| Accurate / Complete / Consistent | The cross-document consistency engine ([[generate-check-validate-engine]]) validates asserted facts against the entity store; discrepancies block state transitions. |

Events are **hash-chained**: each event commits to the hash of its predecessor, which is what allows the [[verifiable-site-qualification-dossier]] to prove to a pharma counterparty — without trusting OSSICRO — that no record in the dossier was altered after signature. The same chain, rendered span-by-span in the review UI, *is* the [[draft-provenance-model]]: provenance and audit trail are one structure viewed from two directions.

**AI attribution.** An AI generation is an Event like any other: model identity and version, input hash, output hash, timestamp, and — before the affected document can leave `draft` — the reviewing human's identity and disposition (accepted / modified / rejected, per span). AI agents hold no signature credentials; [21 CFR 11.100(a)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-C/section-11.100) requires each electronic signature to be unique to one individual, and OSSICRO reads "individual" as a human. See [[claude-sdk-ai-in-the-loop]].

> [!warning] Non-delegable
> The Gate entity is the data model's hard floor. A gate's discharge evidence must be a qualified human's Part 11 signature or a documented act of an external accountable body (an IRB approval letter under [21 CFR 56.109](https://www.law.cornell.edu/cfr/text/21/56.109), an FDA safe-to-proceed notice under [312.40](https://www.law.cornell.edu/cfr/text/21/312.40), a manufacturer's letter of authorization). No system process, scheduled job, or AI agent can write a gate-discharge event. Consent status on the Subject entity records that a qualified human conducted the consent event ([[informed-consent-document-vs-event]]) — it is evidence *about* a human act, never a substitute for one.

> [!interpretive] OSSICRO position
> The entity decomposition, the six-state lifecycle, the Penn-style numbering, and hash-chaining are OSSICRO design positions. The defended claim is narrower than "this is required": it is that this model satisfies the confirmed requirements (Part 11 audit trail and signatures, 312.57/312.62 retention, E6(R3) ALCOA++ and reconstructability) by construction, so that compliance properties are consequences of the schema rather than of operator discipline.

## Privacy posture of the model

PHI is not a first-class citizen of the data model. Subjects are coded; free-text fields destined for logs or documents are screened for identifiers; chart data ingested for matching lives inside the [[privacy-state-machine]]'s preparatory scope (ephemeral, audited reads; no egress) and never persists into the entity store unless the subject's privacy state has lawfully transitioned to enrollment ([45 CFR 164.508](https://www.law.cornell.edu/cfr/text/45/164.508) authorization or [164.512(i)(1)(i)](https://www.law.cornell.edu/cfr/text/45/164.512) waiver). The audit trail records *that* a preparatory read occurred and its minimum-necessary scope — never the clinical content read. See [[hipaa-and-privacy-gating]].

## Related

- [[architecture]]
- [[generate-check-validate-engine]]
- [[draft-provenance-model]]
- [[completeness-ledger]]
- [[non-delegable-functions-and-gates]]
- [[part-11-and-ai-credibility]]
- [[privacy-state-machine]]
- [[verifiable-site-qualification-dossier]]
- [[safety-clock-engine]]
- [[record-retention-and-archival]]
- [[document-catalog]]
- [[regulatory-binder-isf-index]]
- [[transfer-of-regulatory-obligations-toro]]

## Sources

- [21 CFR 11.10 — Controls for closed systems (incl. §11.10(e) audit trail)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10)
- [21 CFR Part 11 Subpart C — Electronic Signatures (§§11.100–11.300)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-C)
- [21 CFR 312.57 — Recordkeeping and record retention (sponsor)](https://www.law.cornell.edu/cfr/text/21/312.57)
- [21 CFR 312.62 — Investigator recordkeeping and record retention](https://www.law.cornell.edu/cfr/text/21/312.62)
- [21 CFR 312.58 — Inspection of sponsor's records and reports](https://www.law.cornell.edu/cfr/text/21/312.58)
- [21 CFR 312.30 — Protocol amendments](https://www.law.cornell.edu/cfr/text/21/312.30) · [312.31 — Information amendments](https://www.law.cornell.edu/cfr/text/21/312.31)
- [21 CFR 312.32 — IND safety reporting](https://www.law.cornell.edu/cfr/text/21/312.32)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025, PDF) — data governance; Appendix C](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [45 CFR 164.512 — Research provisions (preparatory review; waiver)](https://www.law.cornell.edu/cfr/text/45/164.512) · [164.514 — De-identification; limited data sets](https://www.law.cornell.edu/cfr/text/45/164.514)
- [Penn Medicine Office of Clinical Research — Forms, Tools & Templates (numbered document-control library)](https://www.med.upenn.edu/clinicalresearch/forms-tools-templates.html)
- [University of Pittsburgh ECS-HSR — IND templates (six protocol-amendment types)](https://www.ecshsr.pitt.edu/ind-ide-support/investigational-new-drug-ind-templates)
