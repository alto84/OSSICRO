---
title: "Single-Pass Review UX — Attention Triage Across Three Lanes"
section: "05-ossicro-system"
status: interpretive
governing_authority:
  - "21 CFR Part 11 (Electronic Records; Electronic Signatures — §11.10(e) audit trail; §11.70 signature/record binding; §§11.50–11.300 signatures)"
  - "ICH E6(R3) (quality by design, critical-to-quality factors, risk-proportionate oversight; Section 4 Data Governance)"
  - "FDA Guidance — Oversight of Clinical Investigations: A Risk-Based Approach to Monitoring (Aug 2013); Q&A (Apr 2023)"
  - "FDA Draft Guidance on AI to Support Regulatory Decision-Making (Jan 2025, FDA-2024-D-4689)"
tags: [ossicro/engine, ossicro/gating, ossicro/part11, ossicro/ai-credibility, cfr/11, ich/e6r3, status/interpretive]
aliases: ["Three Review Lanes", "Attention Triage", "Single-Pass HITL"]
updated: 2026-07-09
---

# Single-Pass Review UX — Attention Triage Across Three Lanes

> [!authority] Governing authority
> The records and signatures this review process produces are governed by [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) (audit trail §11.10(e); signature-to-record binding §11.70; electronic signatures §§11.50–11.300). The design principle — concentrate oversight attention where risk and judgment concentrate — is the same principle FDA confirmed for monitoring in the [2013 risk-based monitoring guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/oversight-clinical-investigations-risk-based-approach-monitoring) and ICH E6(R3) confirmed for trial quality (quality by design, critical-to-quality factors). Status: **Interpretive** — no regulation prescribes a review UX; this architecture is OSSICRO's mechanism for making the *confirmed* requirement of qualified human review real in a single pass.

Human sign-off gates ([[non-delegable-functions-and-gates]]) only protect subjects and trials if the human at the gate actually exercises judgment. A reviewer handed 200 undifferentiated pages of machine-generated text will rubber-stamp — the failure mode is not malice but attention exhaustion, and it converts every gate in the [[generate-check-validate-engine]] into theater. The single-pass review UX is OSSICRO's answer: every span of every draft is classified into one of **three review lanes** by the strength of its provenance, so that a reviewer's finite attention lands, in one pass, on exactly the spans that required judgment to produce and therefore require judgment to review.

## The failure mode this design targets

AI-assisted drafting changes the economics of document production but not the economics of review. If OSSICRO can generate a complete [[ind-application-312-23|IND package]] in an afternoon, the binding constraint becomes the sponsor-investigator's review attention — and an unstructured review of machine output is *worse* than an unstructured review of human output, because machine text is uniformly fluent and gives the eye no texture to catch on. The regulatory stakes are concrete: the [[sponsor-investigator]] who signs a [[form-fda-1571-ind-cover|1571]] or [[form-fda-1572-statement-of-investigator|1572]] attests to the content of the whole record ([21 CFR 312.23(a)(1)](https://www.law.cornell.edu/cfr/text/21/312.23); [312.53(c)(1)](https://www.law.cornell.edu/cfr/text/21/312.53)), and Part 11 [§11.70](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.70) binds that signature to the exact record signed. A review process that predictably produces unread signatures is a compliance defect, whatever the SOP says.

The design goal, stated precisely: **one qualified pass, with attention allocated by provenance strength, dispositions every span that embodies a judgment call, and produces audit-trail evidence that it did so.**

## The three lanes

Every span in a draft carries a (source datum → provenance → citation) triple per the [[draft-provenance-model]]. Lane assignment is a deterministic function of that triple:

| Lane | Definition | Default presentation | Review obligation |
|---|---|---|---|
| **Deterministic** | Machine-verifiable transcription of structured source data — a date copied from the `Site` record, an address from the investigator CV, an IND number from the `IND` entity, a lab certificate number. A checkable verification rule exists and has passed. | Collapsed, with the provenance triple and the passing verification rule one interaction away. | Spot-check at reviewer discretion; bulk verification already performed and cited. |
| **Boilerplate** | Unmodified text from a template of verified provenance and license ([[external-templates-and-licenses]]). The diff against the template source is empty. | Collapsed, with template identity, version, and license shown. | Confirm template selection is appropriate for the mode/phase; no line-by-line reading of unmodified text. |
| **Inferred / interpretive** | Everything else: AI-synthesized language, spans with no source datum, template text that was modified, any span instantiating a requirement whose satisfaction is a judgment call, and every **amber** item of the [[completeness-ledger]]. | **Foregrounded.** This lane *is* the review. | Mandatory per-span disposition — accept, edit, or reject — by a qualified reviewer. Dispositions enter the Part 11 audit trail. |

Lane assignment is **conservative by construction**. A span enters the deterministic lane only if a machine-checkable verification rule exists, ran, and passed — never on a drafting agent's self-assessment. A span enters the boilerplate lane only if a byte-level diff against the licensed template is empty. Anything unclassifiable defaults to the foregrounded lane. Demotion (foregrounded → collapsed) is never available to the AI; promotion (collapsed → foregrounded) is automatic on any of: template deviation detected, verification rule failure, cross-document inconsistency flagged by the adversarial check pass ([[generate-check-validate-engine]]), or reviewer request.

## Mechanics of the single pass

1. The reviewer opens the package with the [[completeness-ledger]] as the cover sheet: greens collapsed with citations, ambers enumerated as the gate list, reds blocking with their resolving questions.
2. The foregrounded lane presents each inferred/interpretive span **with its context, its provenance triple (or the explicit marker *no source — inferred*), the governing citation, and — where the adversarial QC agent flagged it — the machine critique**. The reviewer starts where the adversary found weakness.
3. Each foregrounded span requires an explicit disposition. There is **no bulk-accept for the foregrounded lane**; bulk operations exist only for the collapsed lanes, and even there they are recorded as the disposition they are ("accepted deterministic lane, n=214 spans, verification rules cited").
4. Every disposition — identity, timestamp, action, resulting text — is an Event in the [[data-model]] audit trail per [21 CFR 11.10(e)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10).
5. When every foregrounded span and every amber ledger item is dispositioned, the document transitions `checked → human-reviewed` in the state machine; gates then discharge by Part 11 signature or documented external event ([[non-delegable-functions-and-gates]]).

Indeterminate outputs from [[matching-eligibility-adjudication]] follow the same discipline: a criterion the matcher graded *indeterminate — needs data* arrives in the foregrounded lane with the exact missing datum named, because eligibility determination is the investigator's non-delegable call.

## What triage does not change

> [!warning] Non-delegable
> Attention triage narrows where review attention *goes*; it never narrows what the reviewer is *accountable for*. The signature at the end of the pass covers the entire record — [21 CFR 11.70](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.70) binds it to the whole document, and the 1571/1572 attestations run to the full content, collapsed lanes included. Collapsing a lane is a presentation choice backed by cited machine verification, not a waiver of review; the reviewer may expand and re-disposition any span at any time. No lane assignment, and no machine verification, ever substitutes for the human judgment reserved by [[non-delegable-functions-and-gates]] — consent, IRB approval, causality, statistical sign-off, and the signature attestations remain human acts regardless of lane.

## Regulatory grounding and precedent

The principle that oversight attention should be *proportionate to risk rather than uniform* is not an OSSICRO invention. FDA's 2013 monitoring guidance rejected 100% source-data verification in favor of concentrating monitoring on critical data and processes, and the [2023 Q&A](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/risk-based-approach-monitoring-clinical-investigations-questions-and-answers) reaffirmed it; ICH E6(R3) generalizes it to the whole trial through quality by design and critical-to-quality factors ([[risk-based-monitoring-e6r3]]). The three-lane UX applies the same confirmed logic to document review: deterministic transcriptions and unmodified licensed boilerplate are the low-risk strata; synthesized and judgment-bearing spans are the critical-to-quality strata.

> [!interpretive] OSSICRO position
> The regulations require *qualified* review and *attributable* records; they do not prescribe how a reviewer's attention is allocated. OSSICRO's position is that provenance-based attention triage is what makes one-pass qualified review achievable at machine drafting speed — and that the alternative, uniform review of uniform machine text, predictably degrades into the unread-signature failure mode. This also supports the engine's credibility argument under the FDA 2025 AI-credibility **draft** guidance ([[part-11-and-ai-credibility]]): drafting remains a low-influence context of use precisely because the review this page describes is real, evidenced, and audit-trailed — not asserted.

## Related

- [[draft-provenance-model]]
- [[completeness-ledger]]
- [[generate-check-validate-engine]]
- [[non-delegable-functions-and-gates]]
- [[data-model]]
- [[claude-sdk-ai-in-the-loop]]
- [[part-11-and-ai-credibility]]
- [[matching-eligibility-adjudication]]
- [[risk-based-monitoring-e6r3]]
- [[compliance-mapping]]
- [[external-templates-and-licenses]]

## Sources

- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [21 CFR 11.10 — Controls for closed systems (incl. §11.10(e) audit trail)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10)
- [21 CFR 11.70 — Signature/record linking](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.70)
- [21 CFR 312.23 — IND content and format](https://www.law.cornell.edu/cfr/text/21/312.23)
- [21 CFR 312.53 — Selecting investigators and monitors](https://www.law.cornell.edu/cfr/text/21/312.53)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025, PDF)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA Guidance — Oversight of Clinical Investigations: A Risk-Based Approach to Monitoring (Aug 2013)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/oversight-clinical-investigations-risk-based-approach-monitoring)
- [FDA Guidance — A Risk-Based Approach to Monitoring of Clinical Investigations: Questions and Answers (Apr 2023)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/risk-based-approach-monitoring-clinical-investigations-questions-and-answers)
- [FDA Draft Guidance — Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making for Drug and Biological Products (Jan 2025, FDA-2024-D-4689)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological)
