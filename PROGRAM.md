# OSSICRO — Program Frame & Phase Log

**OSSICRO — Open Source Sponsor-Investigator CRO**

## Frame (Phase 0)

**Problem.** The coming wave of early-phase drugs (FIH → Phase 2) will bottleneck not on molecules but on patient enrollment and site activation. Standing up a compliant trial site takes a median ~9.4 months and $30–200K, with contract/budget negotiation the dominant chokepoint; ~11% of activated sites enroll zero patients. Commercial CROs broker this coordination labor and monetize the friction. Meanwhile, a physician who has the right patient for an early-phase therapy has no low-cost, compliant path to become a site or run an investigator-initiated study.

**What OSSICRO is.** A holistic, open-source software package plus an exhaustively-researched regulatory documentation wiki that lets an enrolling clinician coordinate the full paperwork burden across every required entity — sponsor, CRO, investigator / sponsor-investigator, IRB / ethics, DSMB / patient-safety board, pharmacovigilance, and pharma partner — with all documentation **generated, checked, validated, and coordinated in adherence with policy**. A thin "micro-CRO" operating layer supplies the legally-accountable functions (the ~5% of CRO work that must sit with a real entity) when required; everything else is open source and physician-operable.

**Guiding scenario.** A clinician has a patient and wants a treatment available via a searchable database of early-phase (e.g., Phase 2) programs from a pharma sponsor. OSSICRO assembles, checks, and coordinates every document required to match the patient, activate the site, and reach enrollment — routed correctly to trial-monitoring entities, patient-safety boards, ethics/IRB committees, and pharma/CRO counterparties.

**Success criteria (reviewable state).**
1. A cross-referenced regulatory **wiki** (markdown) covering sponsor / CRO / investigator / sponsor-investigator / pharma responsibilities, the trial lifecycle, the full essential-document set, and coordination workflows — in regulatory register, comparable to reference documents, with internal cross-links and external citations.
2. A **template library** for the required documents (ICF, FDA 1572, delegation log, monitoring plan, safety management plan, DSMB charter, IRB submission package, regulatory binder index, CTA/budget, feasibility questionnaire, protocol synopsis, etc.).
3. A **generate/check/validate engine** (prototype): document schemas + validation rules mapping each artifact to its regulatory citation.
4. A **pharma-corporate-style frontend** demonstrating the clinician flow end-to-end.
5. A **detailed plan** (system architecture, micro-CRO operating model, roadmap).
6. **QA** from three personas (enrolling physician, CRO, pharma) + Fable second opinions, with a punch list and applied fixes.

**Scope — in.** Documentation, templates, validation logic, the coordination model, a demo frontend, the plan. US regulatory frame (21 CFR, ICH E6(R3), FDA guidances) primary; note EU/ICH where load-bearing.

**Scope — out (this pass).** Live trial conduct; any real IND/IRB submission; storing real PHI; legal advice. All generated artifacts are DRAFT — REQUIRES QUALIFIED HUMAN REVIEW. Non-delegable functions (informed consent, IRB judgment, SAE causality, sponsor/investigator legal obligations) are surfaced and gated, never automated.

**Constraints.** Open source (MIT). Regulatory accuracy is the first-order requirement — every substantive claim carries a citation; unverified content is flagged. Local-first architecture assumed (PHI never leaves the covered entity).

## Location & repository plan

All OSSICRO materials and code are centralized in this single folder (`ossicro/`), currently developed in-tree on the `ossicro` branch of the Sartor repo (in-tree so the autonomous authoring subagents write without sandbox friction). The folder is self-contained and split-ready (own `README.md`, `LICENSE`, `.gitignore`); after the first review passes it will be extracted to its own public GitHub repository (`git subtree split -P ossicro`, or a clean copy) — Alton creates that repo. Precursor exploration is preserved under `docs/exploration/`.

## Phase Log

| Phase | Status | Artifact |
|-------|--------|----------|
| 0 Frame | done | this file |
| 1 Explore (research + academic/institutional sweep) | in progress | `references/`, research corpus |
| 2 Plan (IA + detailed plan) | pending | `docs/detailed-plan.md`, `wiki/INDEX.md` |
| 3 Build (wiki, templates, engine, frontend) | pending | `wiki/`, `templates/`, `engine/`, `frontend/` |
| 4 Adversarial Review (3 personas + Fable) | pending | `qa/` |
| 5 Revise | pending | patches |
| 6 Re-Review | pending | `qa/` |
| 7 Reviewable state → hand to Alton | pending | `README.md` summary |

## Model-orchestration note
Per principal directive: Fable subagents author + give second opinions; a Sonnet 5 agent runs the exhaustive academic/publication/institutional sweep. Every subagent reports its actual model; Fable→Opus fallbacks are logged in `docs/model-fallback-log.md`.
