# OSSICRO — Writing Principles

# OSSICRO Writing Principles

**Version 1.0 — 2026-07-09.** Applied with judgment by the voice-validation reviewer (plan §5.2) and by human reviewers. This is a rubric of principles, not a checklist of phrases: the operative question for any span is never "does it match a listed pattern" but "would a careful regulatory professional write this, for this reader, in this document." See `docs/VALIDATION-PHILOSOPHY.md` for why the principles govern and the examples merely illustrate.

## The principles

**1. Every sentence serves the reader's decision.**
A regulator, IRB member, or manufacturer reads this document to decide something. Write what that decision needs — the fact, the citation, the commitment — and nothing that exists to perform thoroughness. A sentence that could be deleted without changing what the reader can decide should be deleted.

**2. Evidence over emphasis.**
State facts plainly and let them carry their own weight. Importance claims without content ("plays a critical role"), promotional framing ("promising", "state-of-the-art"), and superlatives are defects everywhere in regulatory prose and severity-critical in consent and counterparty-facing text, where they can minimize risk or overstate benefit. Nothing in a filing is impressive; it is supported or it is not.

**3. Calibrated uncertainty, stated once.**
Where uncertainty is real, state it precisely, once, with its source ("response rates in the phase 1 cohort ranged 20–35%"), not as stacked modals ("may potentially"). False confidence is the same defect in the other direction. The hedge is information or it is noise.

**4. The document does not narrate itself.**
No metacommentary ("it is important to note", "in conclusion"), no framing of what the document is about to do, no summaries of what it just did. A regulatory document ends with the requirement, not a wrap-up.

**5. Register is per-document and per-audience.**
Consent: second person, plain language a subject population can understand, risks stated without minimization, payment never framed as a benefit. FDA forms: third person, factual, transcribable, no narrative or editorializing. Protocol: precise, cited, non-promotional. Correspondence: formal, non-speculative, comparable to a reference regulatory document. The same sentence can be correct in one register and a defect in another.

**6. Write as the signer.**
A licensed physician signs this document as their own professional work product and carries its accountability. The test for any generated span: would that signer, reading closely, adopt this sentence as their own — or wince.

**7. Precision beats variety.**
Defined terms repeat verbatim; elegant variation is a defect here, not a virtue. Formal passives, "shall", and boilerplate repetition are legitimate regulatory register — a reviewer that flags them has misjudged the domain. When in doubt, compare against the source library's reference documents, not against general prose norms.

**8. Nothing reveals the drafting process.**
No chat residue, no AI self-reference, no instruction leakage, no traces of the generation pipeline. (This class alone is enforced deterministically as a hard rule — see `docs/VALIDATION-PHILOSOPHY.md` §3 — because it is fact-shaped and never becomes legitimate.)

## Illustrative examples — non-exhaustive, dated, expected to decay

The following illustrate failure classes as of models circa 2023–2025. They seed the reviewer's judgment; they do not bound it. A span exhibiting none of them can still fail principle review, and several of these phrases are legitimate in the right context — the judgment is the check, not the match.

- *Metacommentary / filler* (principle 4): "it is important to note", "it should be noted that", "in conclusion", "needless to say".
- *Inflation mannerisms* (principle 2): "not just X but Y", "delve into", "a testament to", "rich tapestry", "navigate the complexities", "in today's landscape".
- *Promotional register* (principles 2, 5): "cutting-edge", "seamless", "game-changing", "leverage", "unlock", "empower".
- *Context-dependent terms* (principle 7 cuts both ways): "robust" is filler in marketing copy and precise in a statistics section; "synergy" is business slop except when pharmacological synergy is meant. A pattern-matcher cannot make these calls; the reviewer must.

When a listed example stops appearing in model output, or starts appearing in ordinary professional English, retire it. The registry entry was always a snapshot; these principles are the standard.

## Application

The voice reviewer judges only filled field values and generated spans; verbatim-locked and fixed template prose are outside its jurisdiction by construction. It returns structured findings — `{field, span, principle, severity, rationale, suggested_rewrite}` — that drive the flag-and-rewrite loop and fail toward the human gate. It never hard-fails a document alone and never silently passes one. Findings record the reviewing model's version for the audit trail.