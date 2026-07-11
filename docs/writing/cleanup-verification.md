# Cleanup verification — fresh-reader test (drift report §5.4)

Date: 2026-07-10. Reviewer: a fresh Claude session with no prior OSSICRO context, per the
reader-test requirement that the judge "has not been marinating in this repo's context."
Files reviewed: `app/static/index.html` (STRINGS tables + visible copy), `docs/OSSICRO-CONSTITUTION.md`,
`app/README.md`.

## Lint numbers (tools/prose_lint.py)

| file | words | em/1k (<=5) | not-never/1k (<=1.5) | honest/1k (<=0.3) | arrows (0) | lexicon (0) |
|---|---|---|---|---|---|---|
| docs/OSSICRO-CONSTITUTION.md | 2605 | 0.8 | 0.0 | **0.8 — MISS** | 0 | 0 |
| app/README.md | 1297 | 0.0 | 0.0 | 0.0 | 0 | 0 |
| corpus | 3902 | 0.5 | 0.0 | 0.5 (over) | 0 | 0 |

Aphorisms 0, maxim echoes 0, mid-caps 10 (all defined acronyms / DRAFT stamps — legitimate).
Every target is met except honest/1k in the Constitution (2 hits, analyzed below).

## Per-file verdicts

### app/static/index.html — RESIDUE-REMAINS (minor)

The reader test passes almost everywhere. The patient-view strings are the best writing in the
corpus: genuinely plain language ("Expanded access is a way to ask permission to use a medicine
that is still being studied"), no jargon, no project-private words, and the tone survives error
states ("We hit a snag."). Physician-facing copy defines its own terms in place (committed
profile, gate, ledger, stale drafts). Residue that remains:

1. **"Enrollment — INV-5"** (STRINGS.promote.eyebrow, ~line 1106). An internal invariant ID
   leaked into a physician-facing heading. A physician on first contact cannot state what
   "INV-5" tells them to know or do; it serves the writer's tracker, not the reader. Same
   class: **"Micro-CRO persona"** (STRINGS.cro.eyebrow) — "persona" is design-team vocabulary
   and "CRO" is never expanded anywhere the physician can see.
2. **armed / unarmed clock vocabulary** in physician-facing text: column headers "Clocks armed,"
   "Duties armed," "Armed," pill values "armed"/"unarmed," and "A clock with no trigger date
   stays unarmed." The drift report's own Tier-1 list flags "arms" for software events in
   user-facing text. It is defined once ("A clock shown as unarmed is waiting for its trigger
   date"), but the bare column header "Armed" travels without that definition.
3. **"Treatment, not research (21 CFR 312.305(a))"** (screen 1). The contrastive reflex shape —
   though this one is defensible as FDA's own framing of expanded access (treatment use vs.
   research), so it is a term of art rather than dialect. Borderline; acceptable.
4. **"FDF field-map"** — a physician downloading it will not know what FDF is; the caption says
   what to do with it but never what it is.

### docs/OSSICRO-CONSTITUTION.md — RESIDUE-REMAINS (minor; one lint target missed)

The reader test largely passes for all three named readers. Jargon is expanded at first use
(IND, Part 11, DSMB, QP, sponsor-investigator), "fails closed" is immediately defined in its own
sentence ("on violation it raises GateViolation and stops"), and the long deliberative passages
(the Section II discussion of when the value ordering binds) are the opposite of clipped dialect —
a regulator could restate them. What remains:

1. **honest/1k = 0.8 vs target 0.3.** Two hits: "Correctness and honesty" (value 2) and
   "CP4: Honesty about uncertainty." Both are honesty about *factual claims in documents* — the
   legitimate sense — not "honest" praise of a mechanism, which is what the Tier-1 rule targets.
   Judged: acceptable as-is, but if the number must clear the target, rename CP4 to something
   like "Uncertainty is stated once, precisely" and re-title value 2 "Correctness."
2. **Aphorism-shaped headings**: "Judgment escalates; it never clears" (CP5) and "Findings
   teach; they do not merely flag" (CP7), plus in-paragraph "Importance alone earns nothing."
   None *replaces* an explanation — each is immediately unpacked — so they head explanations
   rather than substitute for them. Kept-as-is is defensible; they are the last trace of the
   old cadence.
3. "condition 2, applied in reverse" (HC7) makes the reader compute the meaning, but the next
   two sentences do the computation for them. Passes.

### app/README.md — CLEAN

All lint targets met at zero. Every sentence tells a developer or reviewer something checkable:
what to run, what each endpoint does, what is refused and with what status code, where the
single source of clock arithmetic lives and which tests pin it. Project terms are defined at
first use ("committed profile" gets a full sentence: "That is a project term: ..."). Repeated
boundary statements ("The software does not submit or sign anything," "the engine does not
invent dates") are content, not tic — each states a distinct liability line. Minor notes only,
below the residue threshold: eCTD, FDF, and PHI are never expanded, but the named reader
(developer/reviewer in health-tech) plausibly knows PHI and FHIR, and eCTD/FDF are pointed at
the files that explain them.

## Over-correction check (the substitution failure)

**Not over-corrected.** Sentence shapes vary within and across all three files: the Constitution
keeps long multi-clause deliberation next to short rulings; the README mixes imperatives, lists,
and compound sentences; the UI ranges from two-word buttons to 40-word captions. No new fixed
palette detected, maxim echoes 0. One emerging pattern worth watching, not fixing: nearly every
success toast in STRINGS follows a two-beat "Act recorded. Boundary restated." shape ("Release
recorded. ... Nothing was sent." / "Enrollment recorded. ... performing the acts remains yours." /
"Patient status link ready. ... OSSICRO sent nothing."). Each boundary restatement carries real
content, so this is repetition of *meaning* rather than dialect — but if a Wave-5 pass adds more
toasts, vary the second beat.

## Sentences still needing work

1. `index.html` STRINGS.promote.eyebrow: "Enrollment — INV-5" → drop the invariant ID from the
   physician-facing string (keep it in the adjacent code comment). **Worst remaining item.**
2. `index.html` STRINGS.cro.eyebrow: "Micro-CRO persona" → "Coordinator view" or expand CRO.
3. `index.html` board/checklist column headers "Armed" / "Clocks armed" / "Duties armed" →
   consider "Running" / "Clocks running" or "Deadline set," and keep the one-line definition.
4. `docs/OSSICRO-CONSTITUTION.md` CP4 title, only if the honest/1k target is enforced
   numerically rather than by judgment: retitle to remove the "honesty" token.
