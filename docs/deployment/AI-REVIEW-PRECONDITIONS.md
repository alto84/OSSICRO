# AI-Review Preconditions — turning on the live concept reviewer

**Reader:** the person deciding whether a deployment may set
`OSSICRO_LIVE_CONCEPT_REVIEW`, and any reviewer auditing that decision.
**Governed by:** `docs/OSSICRO-CONSTITUTION.md` (HC5 attribution; the no-PHI-egress
hard line) and review finding **B1** (full remediation shipped in Overhaul Package 3).
**This document states requirements. It does not certify that any deployment meets
them — that certification is a human act, recorded per §3 below.**

## What the flag does

OSSICRO's concept (voice) review has two interchangeable reviewers behind one port
(`ossicro.review_port.ConceptReviewer`):

- **Offline deterministic stub** (`DeterministicStubReviewer`) — the shipped default.
  Runs in-process. Nothing leaves the machine. Selected whenever the flag is unset,
  non-affirmative, the API key is absent, or live construction fails (honest fallback).
- **Live Claude reviewer** (`ossicro.review_claude.ClaudeConceptReviewer`) — sends the
  **rendered document text** to the Anthropic API and returns findings. For an n-of-1
  rare-disease case, rendered text is realistically identifiable even with coded IDs:
  **this is PHI-relevant egress and is treated as such.**

The live reviewer is selected only when **both** hold at request time
(`app/server.py:_select_reviewer`, read at call time, never cached):

1. `OSSICRO_LIVE_CONCEPT_REVIEW` is set to an affirmative value (`1`/`true`/`yes`/`on`);
2. `ANTHROPIC_API_KEY` is present.

A key alone never triggers egress — the flag is a deliberate, separate act.

## Preconditions for setting the flag

Setting `OSSICRO_LIVE_CONCEPT_REVIEW` is a **deployment decision**, not a developer
convenience. Before any deployment sets it where real (non-synthetic) case data can
exist, ALL of the following must be true:

**(a) A Business Associate Agreement (BAA) with the model provider is signed and in
force** covering the API traffic this feature generates, **or** the deployment has
implemented and documented a de-identified projection (a reviewed transformation that
removes the identifying content *before* the text reaches the reviewer port) and a
qualified person has signed off that the projection meets the deployment's HIPAA
de-identification standard. "We only use coded IDs" is NOT such a documentation —
n-of-1 narrative text can identify by content.

**(b) Zero-retention configuration is in effect** on the provider account used by
`ANTHROPIC_API_KEY` (the provider does not retain or train on the submitted content),
and that configuration is verified against the provider's current terms, not assumed.

**(c) The named human who flipped the flag is recorded in the deployment log** —
name, date, and the statement that (a) and (b) were verified. The flag must never be
enabled by an unattributed config change.

## What the system does on every live review (built, not promised)

- **One `ai_review` audit record per live review** (HC5):
  `actor="system:concept-reviewer"`, `action="ai_review"`, the committed-profile input
  hash, and a flat, value-free detail — model id, model version, reviewed doc ids,
  finding count, `destination: "anthropic-api"`. Never document text, never finding
  spans (INV-8). The stub writes nothing, because no egress happened.
- **UI disclosure on the check screen**, composed from the claim registry
  (`engine/registry/claims.json`: `ai-review-live` / `ai-review-offline`): the screen
  states either that drafts were reviewed by the named external model and text left
  the machine under the deployment's BAA, or that the offline checker ran and nothing
  left the machine. Never silent either way.
- **Human disposition capture**: each concept finding carries a stable `finding_id`;
  `POST /api/case/{id}/review-disposition` records the named human reviewer's
  accepted/dismissed judgment as an `ai_review_disposition` audit record.
  Escalate-only — a disposition never changes ledger state, never clears a gate.
- **Authority boundary unchanged**: either reviewer can only FLAG. The escalate-only
  coupling in `ossicro.pipeline` means a finding can add a red or a note but can never
  clear a gate, edit a locked span, or advance a document.

## What this document does not do

It does not weaken any hard line. Drafts remain drafts; nothing is auto-decided or
auto-sent; a live review adds judgment input for the human reviewer, nothing more.
And it does not make the flag safe by itself: a deployment that cannot satisfy
(a)–(c) keeps the shipped default — the offline stub — and loses nothing but model
judgment on voice.
