# OSSICRO — Open Source Sponsor-Investigator CRO

> Open-source coordination software + an exhaustively-researched regulatory knowledge base that lets an enrolling clinician assemble, check, validate, and route **every document** required to match a patient to an early-phase trial, activate a site, and reach enrollment — across sponsor, CRO, investigator / sponsor-investigator, IRB/ethics, DSMB/safety, pharmacovigilance, and pharma partner.

**Status:** early build, in active autonomous development. This folder is the single source of truth for all OSSICRO materials and code; it is structured to be split into its own public GitHub repository after the first review passes.

---

## Why

The next wave of early-phase drugs will bottleneck on patient enrollment and site activation, not on molecules. Standing up a compliant trial site takes a median ~9.4 months and $30–200K; ~11% of activated sites enroll zero patients. Commercial CROs broker this coordination labor and monetize the friction. A physician with the right patient for an early-phase therapy has no low-cost, compliant path to become a site or run their own study.

OSSICRO makes the coordination labor cheap and the paperwork correct, so a clinician can operate as a site — or as a **sponsor-investigator** (21 CFR 312.3) — without a commercial intermediary, while a thin "micro-CRO" layer supplies only the legally-accountable functions that must sit with a real entity.

## Two supported modes

1. **Physician-as-site** — enroll your patients into a pharma sponsor's early-phase trial; OSSICRO generates and coordinates the site-activation and conduct paperwork.
2. **Sponsor-investigator** — run your own investigator-initiated study; OSSICRO absorbs the sponsor-side burden (IND assembly, safety reporting scaffolding, essential-document/TMF management) that normally makes this impractical for a working clinician.

## Repository layout

| Path | Contents |
|------|----------|
| `PROGRAM.md` | Program frame, success criteria, and phase log (audit trail) |
| `wiki/` | The regulatory knowledge base (markdown, cross-referenced, cited) |
| `templates/` | Document templates (ICF, FDA 1572 guide, DOA log, monitoring & safety plans, DSMB charter, IRB package, regulatory-binder index, CTA/budget, feasibility questionnaire, protocol synopsis, …) |
| `engine/` | Prototype generate/check/validate engine (document schemas + validation rules mapped to citations) |
| `frontend/` | Pharma-corporate-style demo frontend (clinician flow end-to-end) |
| `docs/` | Detailed plan, system architecture, frontend strategy, model-fallback log, exploration provenance |
| `qa/` | Adversarial QA memos (enrolling-physician / CRO / pharma personas + second opinions) |
| `references/` | Bibliography + academic/CRO/gov institutional resources |

## Hard line — not a substitute for qualified humans or oversight bodies

OSSICRO produces **DRAFT** documentation for review, editing, and approval by qualified humans and the appropriate oversight entities. It does not, and must not be configured to, perform **non-delegable regulated functions**: informed consent of a patient, IRB/IEC review, safety/causality determination, or the legal obligations of a sponsor or investigator. These are surfaced and gated, never automated. Not medical, legal, or regulatory advice.

## License

MIT (see `LICENSE`), with the non-delegable-function notice appended.
