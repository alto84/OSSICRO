---
title: "21 CFR Part 11 Compliance and the FDA AI-Credibility Framework"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "21 CFR Part 11 (Electronic Records; Electronic Signatures)"
  - "FDA Guidance: Part 11, Electronic Records; Electronic Signatures — Scope and Application (2003)"
  - "FDA Draft Guidance: Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making for Drug and Biological Products (2025, DRAFT)"
  - "ICH E6(R3) (data governance; computerized systems)"
tags: [ossicro/part11, ossicro/ai-credibility, ossicro/engine, cfr/11, ich/e6r3, status/confirmed, status/interpretive]
aliases: ["Part 11", "AI Credibility", "Part 11 and AI"]
updated: 2026-07-11
---

# 21 CFR Part 11 Compliance and the FDA AI-Credibility Framework

> [!authority] Governing authority
> [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) is a **binding rule** governing every electronic record OSSICRO creates, modifies, maintains, or transmits in satisfaction of an FDA predicate rule (Parts 50, 54, 56, 312) and every electronic signature applied to one, as narrowed in enforcement by FDA's 2003 [Scope and Application guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application). FDA's AI guidance ([FDA-2024-D-4689](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological), published 2025-01-07, comment period closed 2025-04-07) is **DRAFT and non-binding**; it states current thinking and may change. Status: **Mixed** — Part 11 obligations are confirmed; OSSICRO's context-of-use risk-tiering argument is interpretive.

Part 11 is the compliance boundary that makes OSSICRO's outputs admissible as regulatory records; the FDA AI-credibility framework is the emerging standard against which OSSICRO's AI components will be judged. This page maps the system to both. It is the compliance backbone referenced by [[architecture]], [[generate-check-validate-engine]], [[claude-sdk-ai-in-the-loop]], [[draft-provenance-model]], and [[verifiable-site-qualification-dossier]].

## Part 11 — scope and the predicate-rule trigger

Part 11 applies to "records in electronic form that are created, modified, maintained, archived, retrieved, or transmitted, under any records requirements set forth in agency regulations" ([21 CFR 11.1(b)](https://www.law.cornell.edu/cfr/text/21/11.1)). The trigger is always a **predicate rule**: Part 11 does not itself require any record to exist; Parts 312, 50, 54, and 56 do, and Part 11 governs the electronic form of those records. For OSSICRO the predicate-rule inventory includes, at minimum: IND content and amendments (21 CFR 312.23, 312.30-312.31), IND safety reports (312.32), annual reports (312.33), sponsor records and reports (312.57-312.58), investigator records (312.62), consent documentation (50.27), IRB records (56.115), and financial disclosure (Part 54). FDA's 2003 Scope and Application guidance narrows *enforcement discretion* — validation, audit trail, record retention, and record copying provisions are enforced with discretion for legacy and low-risk systems — but it does not repeal the rule, and OSSICRO builds to the full rule rather than to the enforcement floor.

## Part 11 — clause-by-clause mapping

### Subpart B — Electronic records (§11.10 controls for closed systems)

OSSICRO operates as a closed system (access controlled by the persons responsible for the records' content), so [§11.10](https://www.law.cornell.edu/cfr/text/21/11.10) is the operative control set. The **Status** column (added in the Overhaul P3 truth pass, M12) states what exists in the code today — BUILT (implemented and tested), PARTIAL (a real subset exists), NOT-YET-BUILT (design target only). The "implementation" column describes the design target; the Status column is the honest gap map, and nothing in it is a compliance certification:

| Clause | Requirement | OSSICRO implementation | Status |
|---|---|---|---|
| 11.10(a) | System validation for accuracy, reliability, consistent intended performance, and the ability to discern invalid/altered records | Versioned validation suite for the engine; the eligibility-matching subsystem additionally carries the public-benchmark harness of [[matching-evaluation-and-benchmarks]] | **PARTIAL** — the engine/app pytest suite runs versioned in-repo; the matching public-benchmark harness is NOT-YET-BUILT |
| 11.10(b) | Accurate and complete copies in human-readable and electronic form for FDA inspection | Every document state exportable with its full provenance manifest ([[draft-provenance-model]]) | **PARTIAL** — the package view exports rendered documents with a SHA-256 hash manifest and per-span provenance; a full-state inspection export is NOT-YET-BUILT |
| 11.10(c) | Record protection for accurate, ready retrieval through the retention period | Retention aligned to 21 CFR 312.57(c)/312.62(c) and E6(R3) ([[record-retention-and-archival]]) | **NOT-YET-BUILT** — no retention/archival machinery exists yet (single-machine JSON case store) |
| 11.10(d) | Access limited to authorized individuals | Role-scoped access mirroring the four personas ([[four-entry-points]]) and the oversight bodies ([[communication-hub]]) | **NOT-YET-BUILT** — persona authentication is explicitly deferred (INV-7); the pilot is single-user, loopback-only |
| 11.10(e) | Secure, computer-generated, time-stamped audit trails that independently record operator entries and actions; record changes must not obscure prior entries | The append-only audit spine; ALCOA++ per E6(R3); rendered as the provenance UX and hash-chained into the [[verifiable-site-qualification-dossier]] | **BUILT** — append-only, hash-chained trail (`ossicro.audit`) with tamper-evidence verification; `ai_review` / `ai_review_disposition` logging BUILT as of Overhaul P3 |
| 11.10(f)-(g) | Operational and authority checks enforcing permitted sequencing and authorized use | The gate machinery itself ([[non-delegable-functions-and-gates]]) — sequencing checks are how enrollment is blocked pending IRB approval | **PARTIAL** — sequencing checks are enforced fail-closed in the engine (`GateViolation`; `finalize()` is the only path to final); authority checks await the INV-7 auth layer |
| 11.10(k) | Controls over systems documentation | Versioned SOPs and system documentation under the same document-control scheme as study artifacts | **NOT-YET-BUILT** — repo docs are versioned in git, but no controlled SOP scheme exists |

### Subpart C — Electronic signatures (§11.50-11.300)

[§11.50](https://www.law.cornell.edu/cfr/text/21/11.50) requires each signed record to show the printed name of the signer, the date/time, and the **meaning** of the signature (review, approval, responsibility, authorship) — OSSICRO records the meaning explicitly at each gate (e.g., "sponsor attestation, Form FDA 1571"). [§11.70](https://www.law.cornell.edu/cfr/text/21/11.70) binds signatures to their records so they cannot be excised or transferred. §11.100-11.300 govern signature uniqueness, identity verification, the certification to FDA that e-signatures are the legally binding equivalent of handwritten signatures (§11.100(c)), and ID/password controls. Every gate signature in the [[non-delegable-functions-and-gates|master gating matrix]] runs on this machinery; eConsent signatures additionally follow the [2016 FDA/OHRP eConsent guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers).

**Status: NOT-YET-BUILT** (Overhaul P3 truth pass, M12). What exists today is a *record of a human act performed outside OSSICRO* — the sign-off endpoint stores signer name, role, date, and the committed-profile hash, and the audit trail chains it. The Part 11 **e-signature ceremony itself** — signature uniqueness and identity verification (§11.100(a)-(b)), the §11.100(c) certification letter to FDA, ID/password controls (§11.300), and §11.50/§11.70 display-and-binding on rendered records — is not yet built. Until it is, no sign-off recorded in OSSICRO is represented as a 21 CFR Part 11 electronic signature.

### AI authorship in the audit trail

AI-drafted content is treated as a distinct record event, not disguised as human work. For every AI-generated span the audit trail records: attribution (which agent), model and version, input hash, template and template version, generation timestamp, and — before the record can advance — the identity and signature of the qualified human reviewer ([[single-pass-review-ux]], [[claude-sdk-ai-in-the-loop]]). This is an OSSICRO design rule that exceeds the Part 11 text; it exists so that an FDA inspector (BIMO; see [[fda-as-counterparty]]) can reconstruct exactly what the machine drafted and what the human reviewed and signed.

**Status: PARTIAL — `ai_review` logging BUILT as of Overhaul P3.** Every LIVE concept review (document text sent to an external model, permitted only under the opt-in flag and the preconditions in `docs/deployment/AI-REVIEW-PRECONDITIONS.md`) now writes one `ai_review` audit record: `actor="system:concept-reviewer"`, model id and version, the committed-profile input hash, the reviewed document ids, the finding count, and the destination (`anthropic-api`) — never document text or finding spans (INV-8). The human reviewer's judgment on each finding is captured as an `ai_review_disposition` record (accepted/dismissed, under a named human), and the check screen discloses which reviewer ran — never silent either way. The offline stub reviewer writes no `ai_review` record because no egress happened. Per-span generation attribution (template + template version on each span) exists in the provenance stamps; the *pre-advance signature requirement* is the gate machinery above and inherits its e-signature status (NOT-YET-BUILT as a Part 11 signature; BUILT as a recorded human act).

## The FDA 2025 AI-credibility draft guidance

FDA's draft guidance *Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making for Drug and Biological Products* ([Federal Register 2025-01-07, Docket FDA-2024-D-4689](https://www.federalregister.gov/documents/2025/01/07/2024-31542/considerations-for-the-use-of-artificial-intelligence-to-support-regulatory-decision-making-for-drug); comments closed 2025-04-07; **still draft as of this writing**) applies when an AI model's output supports a regulatory decision about drug safety, effectiveness, or quality. Its core is a risk-based **credibility assessment framework** in seven steps:

1. **Define the question of interest** the model output will address.
2. **Define the context of use (COU)** — the specific role and scope of the model in answering that question, including what other evidence sits alongside it.
3. **Assess model risk** — the combination of **model influence** (how much the model output contributes to the decision relative to other evidence) and **decision consequence** (the severity of harm if the decision is wrong).
4. **Develop a credibility assessment plan** commensurate with that risk.
5. **Execute the plan.**
6. **Document results and deviations.**
7. **Determine the adequacy** of the model for the COU; if inadequate, adjust the COU, add controls, or increase evidence.

The guidance also emphasizes life-cycle maintenance — monitoring for data drift and re-assessing credibility as models change — which OSSICRO carries via versioned model records in the audit trail and the [[regulatory-change-log]] watch on the guidance itself.

> [!interpretive] OSSICRO position — differentiated COU risk tiers
> OSSICRO explicitly runs the seven-step analysis per subsystem rather than claiming a single blanket tier, and the results differ:
>
> - **Document drafting for qualified human review is a low-influence COU.** The model output never *is* the regulatory decision; a named qualified human reviews with full provenance ([[draft-provenance-model]]) and signs before any record advances ([[non-delegable-functions-and-gates]]). Model influence is low because the human gate is structural; decision consequence is bounded because the artifact is a draft until signed. This keeps the drafting engine in a defensible, lower-credibility-burden tier — with the credibility plan still documented, not waived.
> - **Patient-trial matching is a higher-influence COU and is engineered as one.** A matcher that can return "no eligible trial" can effectively gate a patient's access to therapy; its errors are silent by default. OSSICRO therefore treats matching under a stricter credibility plan: recall-first objective, never-silently-exclude design, three-valued per-criterion verdicts with citations, investigator adjudication of eligibility as the retained human decision, and a public-benchmark evaluation harness (CHIA, TREC Clinical Trials, n2c2) as the executed credibility assessment ([[matching-eligibility-adjudication]], [[matching-evaluation-and-benchmarks]]).
>
> Both positions are interpretive applications of a **draft** guidance. OSSICRO flags the draft status in-product wherever the argument is surfaced, and never asserts "automation-permitted" where the governing text supports only "human-sign-off-permitted."

> [!warning] Non-delegable
> No credibility tier, however low, converts a gated act into an automatable one. Even a fully validated, benchmark-proven model does not sign a 1571, determine causality, or adjudicate eligibility. The AI-credibility framework governs how much evidence the *drafting and retrieval* functions need; the [[non-delegable-functions-and-gates|gating matrix]] governs what may never be automated at all. AI-model reliance beyond a documented, human-reviewed COU is itself a gated act.

## Interaction of the two frameworks

Part 11 and the AI-credibility framework meet in the audit trail. Part 11 makes the record trustworthy (who did what, when, without obscuring history); the credibility framework makes the model trustworthy (is this output adequate for this use). OSSICRO's design fuses them: the credibility documentation for each model version — COU definition, risk assessment, plan, results — is itself a Part 11-controlled record set, producible at inspection alongside the study records the models helped draft. ICH E6(R3)'s computerized-systems and data-governance expectations (validation proportionate to risk; ALCOA++ data integrity) supply the GCP overlay on both.

## Related

- [[architecture]]
- [[generate-check-validate-engine]]
- [[claude-sdk-ai-in-the-loop]]
- [[draft-provenance-model]]
- [[single-pass-review-ux]]
- [[non-delegable-functions-and-gates]]
- [[matching-eligibility-adjudication]]
- [[matching-evaluation-and-benchmarks]]
- [[verifiable-site-qualification-dossier]]
- [[regulatory-change-log]]
- [[record-retention-and-archival]]
- [[confirmed-vs-interpretive]]
- [[regulatory-landscape]]

## Sources

- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [FDA Guidance: Part 11, Electronic Records; Electronic Signatures — Scope and Application (2003)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application)
- [FDA Draft Guidance: Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making for Drug and Biological Products (2025-01-07, DRAFT)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological)
- [Federal Register notice for the AI draft guidance (Docket FDA-2024-D-4689)](https://www.federalregister.gov/documents/2025/01/07/2024-31542/considerations-for-the-use-of-artificial-intelligence-to-support-regulatory-decision-making-for-drug)
- [ICH E6(R3) Good Clinical Practice — FDA final guidance (2025-09-09)](https://www.fda.gov/media/169090/download)
- [FDA/OHRP Guidance: Use of Electronic Informed Consent — Questions and Answers (2016)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers)
