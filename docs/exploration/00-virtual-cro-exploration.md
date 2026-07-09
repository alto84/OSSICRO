# Virtual CRO / enrollment-bottleneck exploration

Four Fable-5 subagents (models: 3 confirmed `claude-fable-5`; 4th pending verification) explored Alton's pivot: away from wet-lab, toward a clinical, open-source "virtual CRO" that lets physicians enroll patients more directly.

## The thesis is validated (hard numbers)
- ~80–85% of trials miss initial enrollment timelines; poor accrual causes ~36% of NCI cooperative-group trial failures and ~55% of early terminations.
- ~11% of activated sites enroll **zero** patients; ~37% under-enroll. Median site activation **9.4 months**; per-site startup **$30–200K**; the specific chokepoint is **budget/CTA negotiation (~60–100+ days)**.
- Pipeline is enormous (~22,940 active drugs, 2026); molecule supply is not the constraint — enrollment capacity is.
- Regulatory tailwind is real and now: FDA final DCT guidance (Sept 2024); ICH E6(R3) (EMA Jul 2025, FDA adopted 2025).
- Screen-fail rates average ~60% (up to ~92% in rare disease); relaxing **3** eligibility criteria nearly **doubled** the eligible NSCLC pool (ASCO–Friends). Enrollability is a *design* variable set before any site opens.

## The key reframe: pure disintermediation is illegal — but the sponsor-investigator IND isn't
- The pure "skip the CRO" play has corpses: **Science 37** ($1B SPAC → $38M sale, 2024); **TrialSpark** abandoned it and became a sponsor (Formation Bio); CVS exited trials.
- The reason is legal, not technical: **21 CFR 312.52** lets a sponsor transfer obligations only to a legally accountable **CRO entity** — software cannot be a transferee of regulatory obligations.
- **The elegant legal path already exists:** the **sponsor-investigator IND (21 CFR 312.3)** — a physician can hold both sponsor and investigator roles today (every investigator-initiated trial does this). The blocker isn't legality; it's that the physician then carries the entire coordination burden (312.50 monitoring, IND maintenance, safety reporting). **That burden is exactly what an AI back-office compresses, and it is where CRO margin sits (~49% of trial budget, 15–25% markup).**
- So the vision sharpens from *"replace the CRO"* to *"make every physician able to be their own micro-site/sponsor-investigator,"* which is both legal today and precisely the paperwork-compression AI is good at.

## Non-negotiable regulatory lines (AI drafts; humans own)
Informed consent (non-delegable investigator duty; eConsent tooling ok, obtaining consent is not); IRB review (human board); sponsor/investigator obligations + IND safety reporting (attach to a legal person); final eligibility determination + SAE causality (investigator); Part 11/ALCOA+ (AI must never *be* the source record); HIPAA (screening own panel = review-preparatory-to-research, but PHI can't leave the covered entity → **local-first architecture**). FDA's 2025 AI draft guidance flags AI making final determinations without human review as high-risk.

## Two product centers of gravity emerged
**A — Site-side "Site-in-a-Box" activation copilot** (truest to the vision). Physician-facing agent: enter a de-identified patient sketch → match to ClinicalTrials.gov trials with a per-criterion meets/fails/unknown matrix → one click generates the site-activation packet (draft FDA 1572, delegation log, ICF localized to 8th-grade reading level, feasibility questionnaire, sIRB checklist, budget/coverage-analysis draft, regulatory binder). Local-first (PHI never leaves the practice); every artifact watermarked DRAFT–INVESTIGATOR REVIEW REQUIRED with hard refusal rails on non-delegable functions. Named user: a community specialist (neurologist). Demo: *"62F relapsing MS, failed two DMTs, Montclair NJ"* → ranked trials + eligibility matrix in 30s → "become a site" → binder ZIP. Attacks the 9-month/$30–200K wall directly; the site-side packet is the CRO-margin territory nobody open-sources.

**B — Sponsor-side "Enrollability Waterfall"** (fixes enrollment at the protocol-design source). A criteria-to-cohort linter for a medical monitor / translational lead: paste eligibility criteria (or a ClinicalTrials.gov ID) → NLP structures each criterion → executes against an OMOP EHR (MIMIC-IV/Synthea/All of Us) → returns a **per-criterion attrition waterfall** ("creatinine cutoff drops the pool 34%, brain-mets exclusion another 21%") + mechanism-aware relaxation suggestions with the ASCO–Friends evidence. Inverts existing patient→trial matchers (Criteria2Query Apache-2.0, TrialGPT) into design-time optimization. This is the direct "design trials that match a novel drug to interesting populations" framing.

A and B **share the eligibility-criteria parsing engine** — build once, point it at the patient (A) or the protocol (B).

## The buildable convergence (hackathon Builder slice + venture seed)
The strongest single hackathon vertical is **A's match→become-a-site agent**: vivid physician-facing demo, genuinely agentic, local-first, open-source, and it seeds the real venture. 6-day scope: D1–2 ClinicalTrials.gov v2 ingest + LLM criteria→structured-checks parser with per-criterion citations; D3 matching UI + evidence-linked eligibility report; D4–5 document generators (1572/ICF/feasibility) with hard human-review gates; D6 demo polish + refusal rails.

## Open question for Alton
Center of gravity: **A (physician/site-side "Site-in-a-Box")** — truest to the venture vision, most vivid demo — or **B (sponsor-side "Enrollability Waterfall")** — closest to "design trials that match a novel drug to interesting populations," different user (medical monitor)? They share the parsing core, so the first build can lean toward one while keeping the other reachable.
