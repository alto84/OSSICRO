---
title: "Claude Agent SDK — AI-in-the-Loop Behind Human Gates"
section: "05-ossicro-system"
status: interpretive
governing_authority:
  - "21 CFR Part 11 (Electronic Records; Electronic Signatures)"
  - "FDA Draft Guidance — AI to Support Regulatory Decision-Making (Jan 2025)"
  - "21 CFR 312.52 (Transfer of obligations); 312.32 (safety reporting)"
  - "ICH E6(R3) Section 5 (computerized systems; service-provider oversight)"
tags: [ossicro/engine, ossicro/ai-credibility, ossicro/part11, ossicro/gating, cfr/11, gcp/e6r3, status/interpretive]
aliases: ["Claude Agent SDK", "AI-in-the-Loop", "AI Drafting Agents", "Part-11 Audit of AI Drafts"]
updated: 2026-07-09
---

# Claude Agent SDK — AI-in-the-Loop Behind Human Gates

> [!authority] Governing authority
> [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) (electronic records, signatures, audit trail); FDA draft guidance *Considerations for the Use of AI to Support Regulatory Decision-Making for Drug and Biological Products* (Jan 2025, docket FDA-2024-D-4689); [21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52) and [312.32](https://www.law.cornell.edu/cfr/text/21/312.32); ICH E6(R3) §5. Status: **Interpretive** — this page is entirely an OSSICRO design position. The Part 11 requirements it satisfies are black-letter; the AI-credibility framework it self-classifies under is **draft, non-binding** guidance subject to change.

The OSSICRO generate/check/validate engine ([[generate-check-validate-engine]]) is implemented with the **Claude Agent SDK**: drafting agents produce document drafts from structured study data plus templates, review/QC agents check completeness against the essential-records matrix and red-team the package for inconsistencies, and coordination agents route artifacts between entities. Every agent action is a **DRAFT behind a human sign-off gate**; permission modes enforce, in code, that non-delegable functions are never auto-executed; and every AI authorship event is recorded in the Part 11 audit trail. This page specifies the agent roles, the permission-mode enforcement, how the agents map onto the three-pass engine, and the audit treatment of AI-authored drafts.

## The hard principle, made mechanical

OSSICRO drafts complete, compliant documentation for qualified human review; it never replaces human-in-the-loop judgment, [[irb-iec|IRB/ethics review]], [[dsmb-dmc|DSMB oversight]], or medical/safety decisions. With an autonomous agent framework the temptation is precisely to let the agent *act* — file the report, sign the form, adjudicate the case. The whole point of this page's architecture is to make that impossible by construction, not by policy. The mechanism is three layers: (1) agent roles that are structurally scoped to *drafting and checking*; (2) permission modes that fail closed at every accountable act; (3) a Part 11 audit trail that attributes every AI contribution so a human reviewer and, ultimately, FDA can see exactly what the machine wrote and what the human owned.

> [!warning] Non-delegable
> No SDK agent — regardless of permission mode, model version, or confidence — may sign a [[form-fda-1571-ind-cover|Form 1571]] or [[form-fda-1572-statement-of-investigator|1572]], obtain [[informed-consent-form|informed consent]], render an [[irb-iec|IRB approval]], make the SAE **causality/expectedness** determination ([21 CFR 312.32](https://www.law.cornell.edu/cfr/text/21/312.32)), provide [[biostatistician|statistical sign-off]], submit to FDA, or assume a [21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52) obligation. Software cannot be a §312.52 transferee and cannot be subject to FDA enforcement. These acts are hard-coded as ungated-impossible in the [[data-model|Gate object]] and enforced by the permission modes below.

## Agent roles

The agents are structurally separated so that no single agent both writes and approves its own work — the same separation-of-duties principle that keeps a [[dsmb-dmc|DMC]] independent of the sponsor.

- **Drafting agents.** Instantiate a template from structured study data (CV/site/financial data auto-populate the forms; the ICH M11 CeSHarP structured protocol is the priority target schema). Output is always a draft *for qualified human review*, never a filed document. Drafting agents have **no** submission or signing capability.
- **Review / QC agents.** Check completeness against the essential-records matrix (ICH E6(R3) Appendix C, risk-proportionate — not a fixed checklist) and against form field-rules ([[form-fda-1572-statement-of-investigator|Form 1572]] fields 1-9; 3454-vs-3455 selection logic). This is the *check* pass.
- **Adversarial pre-review agent.** Structurally separate from the drafting agents, it red-teams the assembled package and runs cross-document consistency checks (PI name, address, dates, IND number, protocol version identical across the 1572, delegation log, and protocol). The human receives the draft **plus** the critique — an elevated *check* described in [[generate-check-validate-engine]].
- **Coordination agents.** Route artifacts between entities on the [[communication-hub]] with role-scoped access, respecting HIPAA and the Medical-Affairs/Clinical-Development firewall. They move documents and compute deadlines ([[safety-clock-engine]]); they do not author the underlying judgments.

## Permission modes and human-in-the-loop patterns

The SDK's permission system is the code-level enforcement of the gating matrix ([[non-delegable-functions-and-gates]]). OSSICRO runs agents in a **default-deny** posture for any tool that could effect an accountable act:

- **Read/draft tools** (retrieve structured data, fill a template, compute a completeness check) run in an automated mode — these are the ~90-95%-labor coordination surface the system is built to absorb (see [[micro-cro-operating-model]] and [[cro]]).
- **Any tool that writes a filing, applies a signature, or transitions a [[data-model|Document state]] past `human-reviewed`** is on a hard allow-list that no agent can satisfy; the transition requires an authenticated human e-signature under [21 CFR 11.100-11.300](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11). The agent's proposed action is surfaced to the responsible human as a gate, not executed.
- The document state machine — `draft → checked → human-reviewed → signed → filed → archived` (see [[data-model]]) — is the enforcement spine: agents may advance a document only to `checked`; the `human-reviewed → signed` transition is reserved to an authenticated human and is the point where the [[single-pass-review-ux|attention-triaged review]] concentrates the reviewer on the judgment calls.

This is the "gate fails closed" property: a validation rule that touches an accountable act carries disposition `fail-to-gate` ([[compliance-mapping]]) and can never auto-pass. A misconfiguration that removed a gate would leave the document *stuck* at `checked`, not silently filed — the safe-failure direction.

## Mapping onto the generate/check/validate engine

| Engine pass | Agent(s) | Output | Gate |
|---|---|---|---|
| **Generate** | Drafting agents | A draft artifact with [[draft-provenance-model|span-level provenance]] (source datum → provenance → citation). | None fires yet; output is a draft. |
| **Check** | Review/QC + adversarial pre-review agents | Completeness verdict against the essential-records matrix + cross-document consistency critique + [[completeness-ledger|green/amber/red ledger]]. | Amber items are surfaced as open gates. |
| **Validate** | Rule engine (deterministic, not a generative agent) | Per-rule `pass` / `fail-to-fix` / `fail-to-gate`, each traced to a CFR/ICH subsection ([[compliance-mapping]]). | `fail-to-gate` routes to the named human. |

The validate pass is deliberately **deterministic** where the check is a compliance judgment — a generative model ranks and drafts; a rule engine decides whether a citation-traced predicate is met. This keeps the load-bearing compliance decisions out of the probabilistic layer and inside auditable rules, which is also the argument that keeps most of the engine in a low-risk context of use (below).

## Part 11 audit of AI-authored drafts

Every AI action is recorded in the [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) audit trail — the ALCOA++ record required by ICH E6(R3) §5 rendered as the generation output contract. Each AI authorship event captures:

- **Attribution** — that the span/artifact was AI-generated (not human-authored), so a reviewer never mistakes machine text for human judgment.
- **Model and version** — the exact model identifier and SDK version, so a later reviewer can reconstruct which system produced the draft.
- **Input hash** — a hash of the structured input the draft was generated from, making the draft reproducible and tamper-evident.
- **Template and citation set** — which template instantiated and which authorities the [[compliance-mapping|manifest]] attached.
- **Human reviewer and disposition** — who reviewed, what they changed, and the timestamp of the `human-reviewed → signed` transition.

The audit trail is time-stamped and independent per [§11.10(e)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11), stored in the validated environment described in [[part-11-and-ai-credibility]]. The [[draft-provenance-model]] is the sentence-level face of this record: the audit trail is not a separate log bolted on after generation — it *is* the provenance the generation emits.

## The AI-credibility risk-tiering argument

The engine's AI outputs are risk-tiered under the FDA 2025 AI-credibility draft guidance's 7-step context-of-use / model-risk framework (define the regulatory question → define the COU → assess model risk as model-influence × decision-consequence → plan, execute, document the credibility assessment). OSSICRO's explicit argument:

- **Document drafting for human review is a low-influence, low-consequence context of use** — the software does not make the regulatory decision; a qualified human reviews, owns, and signs every artifact. This keeps most of the engine in a defensible, lower-credibility-burden tier.
- **Matching that can return "no eligible trial" is a *higher*-influence COU** and is designed and evaluated as one — recall-first, three-valued, with a public-benchmark eval harness (see [[matching-eligibility-adjudication]] and [[matching-evaluation-and-benchmarks]]). This page's low-risk argument applies to *drafting*, not to matching; the two are tiered separately, deliberately.

> [!interpretive] OSSICRO position
> The low-risk-COU classification is an OSSICRO argument, not an FDA determination, and the guidance it rests on is **draft** (docket FDA-2024-D-4689; comment period closed 2025-04-07). OSSICRO must (a) build the validation engine around the 7-step framework, (b) flag the draft status to users in-product, and (c) never assert "automation-permitted" where only human sign-off is lawful. The credibility-tiering claim is defended in [[part-11-and-ai-credibility]] and revisited by the [[references/regulatory-change-log|regulatory-change watch]] whenever the guidance moves.

## Service-provider oversight of the SDK itself

Under ICH E6(R3) §5, delegating a function to a technology vendor does not transfer accountability for the trial's quality and integrity — the sponsor (or [[micro-cro-operating-model|micro-CRO]]) retains documented oversight of the tool. OSSICRO's use of the Claude Agent SDK is exactly such a vendor relationship: the accountable entity retains oversight of the validated system, its change control, and its audit trail. The SDK is infrastructure under an accountable human; it is never itself an accountable party.

## Related

- [[generate-check-validate-engine]]
- [[part-11-and-ai-credibility]]
- [[non-delegable-functions-and-gates]]
- [[data-model]]
- [[draft-provenance-model]]
- [[single-pass-review-ux]]
- [[completeness-ledger]]
- [[compliance-mapping]]
- [[safety-clock-engine]]
- [[matching-eligibility-adjudication]]
- [[micro-cro-operating-model]]
- [[communication-hub]]

## Sources

- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [FDA Draft Guidance — Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making for Drug and Biological Products (Jan 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological)
- [21 CFR 312.32 — IND safety reporting (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.32)
- [21 CFR 312.52 — Transfer of obligations to a CRO (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.52)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025, PDF)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA — E6(R3) Good Clinical Practice (final guidance page, Sept 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
- [Claude Agent SDK documentation (Anthropic)](https://docs.anthropic.com/en/docs/claude-code/sdk)
