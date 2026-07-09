# OSSICRO Template Library

60 fillable regulatory document templates (markdown), one per entry in the engine's document registry (`engine/registry/documents.json`), organized by the 17 document categories.

Each template carries:
- **YAML frontmatter** — `doc_id`, `governing_citations`, `owner`, `receiver`, `gate`.
- A **governing-authority callout** with linked citations.
- A **fillable body** — correct regulatory form for the document type, using `{{snake_case_placeholders}}` for variable data and `[INSTRUCTION: …]` notes.
- A **non-delegable-gate warning** where the document is gated (consent, IRB, causality, signatures, submission) — OSSICRO drafts; a qualified human signs.
- A **fields table** mapping each placeholder to its study-record source and citation, and `## Related` wikilinks to the matching wiki page.

Every template produces a **DRAFT for qualified human review**. The engine (`../engine`) cannot finalize a gated document without a recorded human sign-off. Verify each form against its current OMB-approved FDA version before use. Not medical, legal, or regulatory advice.
