# Why these errors happened — a process root-cause analysis

**Reader:** Alton, deciding how OSSICRO (and projects like it) get built from here.
**Written:** 2026-07-11, alongside `OVERHAUL-PLAN.md`. The plan fixes the defects; this
document asks why a project with five adversarial wave reviews, 337 passing tests, mutation
testing, and an unusually honest QA record still shipped 1 blocker and 15 majors that a
seven-persona outside review found in one pass.

The short version: the defects were not random. Almost every MAJOR traces to one of eight
process causes, and the strongest evidence for each cause is that the wave-review loop —
which was genuinely rigorous — was structurally incapable of seeing it.

---

## RC-1. The build→review loop was Claude reviewing Claude — same model, same blind spots

**Evidence.**
- Every wave review (waves 1–4, the INV-3 review, both EHR reviews) was a "standalone
  adversarial agent (not the builder)" — a different *session* of the same model. They were
  real reviews: mutation tests, injection attacks, parser validation (wave 3 validated the
  hand-built PDF in three independent parsers). And every one returned FIRE-after-patching.
- None of them flagged B1. The reviewer read `egress.py`'s docstring naming `review_claude.py`
  as "the only other module permitted to import an outbound HTTP client" and accepted the
  sanction — because the builder had written the sanction. The engine egress-boundary test
  literally allow-listed the leak. It took the ethics and compliance *personas* — prompts that
  forced an outside frame ("an IRB's first question is: what leaves the machine, when, and who
  consented?") — to see that a sanctioned outbound module with no greenlight, no audit record,
  and no BAA is the hard-line violation, not an exemption from it.
- The false "Still in draft." at the enrolled stage (BLOCKER-severity per the patient review)
  survived a *targeted fix of exactly that bug* (wave-4 MAJOR-2 made the notice
  stage-conditional in two places) and six other reviewers. It was caught only by the persona
  that actually *reads the page as its reader*: a frightened patient.
- The language-drift analysis documents the mechanism in its own domain: "the adversarial
  reviewers are also Claude. A dialect is never challenged by a reviewer who natively speaks
  it" — and the wave-3 review contributed some of the purest specimens of the house register
  while approving the work. Blind spots in style and blind spots in substance have the same
  cause: the reviewer shares the builder's priors, context, and definition of done.

**Why this produces exactly these bugs.** A same-model reviewer verifies that the code does
what the design says. It does not re-derive the design from the outside world. Every MAJOR
that survived is a *design-level* wrongness (wrong anchor, wrong frame, missing model of an
external party), not an implementation bug — implementation bugs got caught.

**Improvement (working agreement, partially tooled).**
1. **Persona review is a standing pre-"done" gate**, not a one-time event. No surface is
   "done" until at least one review has read it from outside the build frame: the affected
   persona for user surfaces, an egress-enumeration ("list everything that can leave the
   machine, from the network's point of view") for privacy claims, a primary-source check for
   regulatory claims. The `/complex-project` structural-separation pattern is the house
   mechanism; the casting must include at least one reviewer whose *prompt frame* is outside
   the build (a persona, a hostile auditor, ideally a human for hard-line surfaces).
2. **The tooled part:** the whole-app egress-boundary test (plan **[PT-5]**, Package 3) makes
   "what can leave the machine" a computed answer instead of a docstring's claim, so a future
   sanctioned-module blind spot fails a test instead of needing a lucky reviewer.

## RC-2. Citations were asserted "computed, not guessed" but never checked against the primary source at build time

**Evidence.**
- M8: every 312.305(b)(2) roman-numeral pinpoint in the system is off by one — ~20 sites,
  consistent with a single early transcription that omitted "(i) cover sheet (Form 1571)" and
  was then *propagated confidently* through five waves of templates, registries, and reviews.
  The regulator persona found it in one afternoon by reading eCFR.
- The 56.104(c) family: the clocks.py docstring misattributed the 5-working-day report to the
  expedited/less-than-quorum path; the anchor itself was wrong in the obligations checklist
  (M1); 312.310(d) vs (d)(2) granularity drifted between files (F4).
- The project had already been burned once and *re-committed the same class of error*: the
  Form 1571 item-15 correction was verified in `qa/REVISE-LOG.md`, and README then re-asserted
  the superseded wrong number as the fix (compliance F2). The correction lived in one file;
  the claim lived in another; nothing bound them.
- The one place a verification discipline existed — `TODO(HUMAN-VERIFY)` on the FDF field map —
  worked exactly as designed (nobody trusted the FDF names). But the discipline was applied at
  one site and never made systematic: the text 3926 template, the PDF layout, and the spec
  carried the same unverified numbering with no marker (M6).

**Why.** "Computed, not guessed" was true of the *arithmetic* (HC3's clocks are genuinely
computed) and silently extended to the *inputs* of the arithmetic — the pinpoints and anchors —
which were typed once from memory or a secondary summary and then trusted because they were in
the registry. A registry canonizes whatever is put in it.

**Improvement (tooling now, plan Package 1 [PT-2], plus a working agreement).**
- **Single-source citation table** (`engine/ossicro/citations.py`): every pinpoint has one
  authored copy, a status (`HUMAN-VERIFIED` / `PENDING-HUMAN-VERIFICATION`), and a named
  verifier+date. A generated `CITATION-INVENTORY.md` is the thing a human signs. Documents
  render a pending marker while any of their citations are unverified.
- **Working agreement:** a statutory citation or official-form structure enters the code only
  (a) verified against the primary source in the same session, with the check recorded, or
  (b) explicitly `PENDING-HUMAN-VERIFICATION`, surfaced on the rendered artifact. There is no
  third state. This is the generalization of the FDF map's one good habit.

## RC-3. Cross-cutting user-facing claims were COPIED, not sourced once

**Evidence.**
- "Nothing has been submitted to the FDA / still in draft" lived in three places: the
  server's stage-conditional notice, the physician draft bar, and a hardcoded bold lead in the
  patient render path (`index.html:3218`). Wave 4's careful MAJOR-2 fix updated two and missed
  the third — the classic copy-fix failure. A fourth copy existed as a *dead string*
  (`patientView.draftBar`) that the patient reviewer flagged as "re-arms the fixed bug if a
  future dev wires it back."
- "Never leaves this machine" (index.html:585) was written for chart import and silently
  overclaimed the whole deployment — including the concept-reviewer path its own author later
  added (B1).
- README's HC1–HC5 (the Constitution says HC7) and "9/9 tests pass" (suite was 336): the shop
  window drifted from the product because nothing regenerated it.

**Why.** Each claim was written where it was needed, in the flow of the wave that needed it.
Nothing made the second author aware the first copy existed; nothing made a fixer's grep
authoritative. In a system whose product *is* calibrated claims, claim text is data and was
treated as prose.

**Improvement (tooling now, plan Package 2 [PT-3]).** A claim registry
(`engine/registry/claims.json`) for cross-cutting claims — canonical text plus the conditions
under which the claim is true — rendered into both server STRINGS and the SPA from one copy,
with a duplication-grep test that fails when a registered claim's distinctive text appears
outside the render path. Stale-count claims (test counts, HC ranges) either become computed or
get a test pinning them to the source of truth.

## RC-4. External-party documents were modeled identically to physician documents — no "who authors/signs this" model existed

**Evidence.**
- M2: `manufacturer-letter-of-authorization` has `gate: null` and three physician-entered
  required fields, so the manufacturer's own letter goes GREEN ("complete") the moment the
  physician types the IND number, feeds `submission_ready`, and is listed as an enclosure. The
  spec (§4.1) even promised an "LOA-acceptance record" — the model was *designed* and never
  built, and no review noticed the promise was unkept because nothing in the registry said
  "this document is not the physician's to complete."
- The same missing dimension explains M13 (recording the IRB's act needs no evidence — the IRB
  is an author the data model can't represent, so its act degrades to a checkbox-shaped
  sign-off with server-synthesized attestation) and part of M4 (FDA's authorization had no
  fact-slot at all until this plan adds one).
- The registry has rich per-document metadata (gates, required_fields, categories, ectd slots)
  — authorship was simply not one of the axes, so the ledger's green/amber/red vocabulary had
  no way to say "waiting on someone who isn't the user."

**Why.** The document registry was built from the FDA package outward ("what must the filing
contain"), not from the actors outward ("who must do what"). Every document that had to exist
became a template the physician fills; the four-decisions/four-owners framing lived in prose
and gates, but never in the data model that drives the completeness ledger.

**Improvement (tooling now, plan Packages 2+4 [PT-4]).** `author_party` becomes a required,
validated field on every registry document; documents whose author is not the current persona
can never be green from that persona's typing alone — they sit in a first-class
`awaiting-external-party` state keyed to recorded receipt facts (`loa_received_date`,
signatory, optional document hash). The working-agreement half: any new document enters the
registry with its author declared, and any promised record (an "acceptance record" in a spec)
gets a registry/schema slot in the same wave or an explicit deferral marker.

## RC-5. Wave-by-wave building let later waves contradict earlier registry facts

**Evidence.**
- M1 is the type specimen: `routes.json` (early) anchored the 56.104(c) clock correctly on
  `submission.first_treatment_date`; the spec agreed; `gen_irb_request` agreed. Wave 4 then
  built the obligations checklist against the *convenience function*
  (`expanded_access_emergency_deadlines`) whose signature only offered one anchor — and wrote
  new help text teaching the physician the wrong trigger. Four artifacts asserted the anchor;
  the newest one contradicted the other three, and the same case could show two due dates for
  one statutory duty. The most-corroborated finding in the whole review (4 personas) was a
  *self-consistency* failure, not a knowledge failure — the correct fact was already in the
  repo.
- Smaller instances of the same shape: the annual-report clock re-implemented in the app
  instead of `clocks.py` (m16); the template corpus's dotted paths diverging from the engine
  schema (m5); the spec's 3926 field numbers vs the template's (M6's internal half); the eCTD
  map disagreeing with regional practice its own docs describe (m7).

**Why.** Each wave's definition of done was "this wave's tests pass and its reviewer fires."
No check ever asked "does this wave's output agree with every earlier assertion of the same
fact?" Registries were treated as append-only context, not as constraints on later code. And
convenience functions (one anchor for two clocks) baked an early simplification into an API
that later callers inherited without re-deriving.

**Improvement (tooling now, plan Package 1 [PT-6], plus a working agreement).**
Cross-artifact reconciliation tests: for every statutory duty, one test feeds the same facts to
every code path that renders that duty (route clock, generator paragraph, obligations row) and
asserts a single due date and a single trigger field. Same pattern extends to any fact asserted
in more than one artifact. Working agreement: a wave that touches a fact already asserted
elsewhere must either consume the existing single source or migrate all assertions in the same
wave — adding a second source is the defect.

## RC-6. Templates were generic where the pathway demanded a profile

**Evidence.**
- M3: the ICF a desperate expanded-access patient would sign opens "You are being asked to take
  part in a research study" while screen 1 of the same product says "Treatment, not research."
  The generic Part-50 trial ICF was reused via `gen_icf` because it satisfied the
  heading-verbatim rule — structure was checked, framing was not, and 50.25(a)(6) was
  structurally unsatisfiable because intake never asked for the whether-statement. The green
  `R-ICF-50.25` row certified compliance over non-compliant content.
- M14: the IRB request's fixed sentence "consent will be obtained before treatment begins" is
  false on the emergency pathway *that the same document's computed `pathway_statement`
  describes two lines earlier* — a fixed literal beside a computed one.
- m9: the patient page's "what still has to happen" list is route-blind and misdescribes the
  emergency pathway to the patient living it.

**Why.** Templates were authored once against the common case and parameterized by field
values, not by pathway. The rules layer verified the invariant parts (verbatim headings,
banned constructions) — which taught everyone the templates were "checked" — while everything
pathway-conditional stayed fixed prose. Deterministic checks certified the checkable and the
green bled onto the uncheckable (the same overclaim shape as m12's HC6 note).

**Improvement (tooling in plan Packages 5+6, plus a working agreement).** Pathway-conditional
statements become computed literals keyed to recorded facts/attestations (`pathway_statement`
was already the right pattern — extend it: the consent-timing sentence, the EA ICF variant,
the emergency patient lists). Working agreement: every template declares which route variants
it serves, and a test renders it under *each* variant asserting the pathway-conditional spans
differ correctly; any deterministic rule that verifies part of a document states in its
resolving text what it does NOT verify.

## RC-7. Honest deferral drifted into unguarded assumption

**Evidence.**
- The codebase is exemplary at *documenting* limits: unkeyed hashes (profile.py docstring),
  INV-7 deferral, egress residual risk, the FDF TODO. But M9 shows what documentation without
  a tripwire is worth: the entire access-control posture was `HOST = "127.0.0.1"` — a module
  constant every review memo *restated as a standing rule* and no code enforced. One token
  edit or a future env-var convenience silently converts a safe pilot into an open PHI-class
  surface.
- Same shape: "no real PHI" was a pilot *assumption* while the intake help invited initials
  into a cleartext store; the deferred adequacy rule (`R-ICF-50.25-ADEQ`) deferred silently —
  nothing running even said "adequacy was not evaluated."

**Why.** The house culture rewarded honest labeling (rightly), and honest labels came to feel
like mitigations. A deferral that costs nothing to violate is a wish. The reviews kept
"ACKNOWLEDGED, deferred" items scattered across five memos with no owner and no failing
condition.

**Improvement (tooling now, plan Packages 3+9 [PT-7], plus a working agreement).** Every
deferral gets a tripwire that fails loudly when the deferred assumption is violated: the
non-loopback bind guard, the stub-reviewer-by-default env test, the pending markers on
unverified artifacts. Working agreement: a deferral is only accepted with (a) the condition
under which it becomes unsafe, and (b) a test or guard that fires at that condition. "We wrote
it down" stops counting as a control.

## RC-8. The definition of done measured internal consistency, not outside ground truth

**Evidence.**
- 337 green tests pin expectations the same model authored; the match mini-eval computed
  recall/precision *on top of an assertEqual that forces 1.0* (m19) — a green number that
  could not say anything. The wave reviews measured "does the code do what the design says,"
  never "is the design right against eCFR / the OMB form / a real Medical Affairs intake /
  a real patient's reading."
- The language-drift analysis found the same in prose: a register optimized for the writer's
  own context, with the project's writing principles applied to generated documents and
  exempted from the project's own docs. The banned-constructions linter targeted the previous
  model generation's tics and caught none of the current dialect — controls tuned to
  yesterday's failure mode.
- Where outside ground truth WAS imported, it worked immediately: wave 3 validated the PDF in
  three independent parsers (real defects found); the regulator persona read eCFR (M8 found);
  the patient persona read the page as a patient (the false bold lead found).

**Why.** Ground truth is expensive and the loop was optimized for velocity; internal
consistency is what a model can verify without leaving its context. Every mechanism that
imported an external reference caught real defects, and there were only three such mechanisms
in five waves.

**Improvement (working agreement, with the plan's tooling as carriers).** Each wave's
definition of done names its external references and how they were consulted: primary
regulation text for citations (RC-2's table is the ledger), the official instrument for forms
(Package 8 is the model), independent parsers/tools for formats, a persona or human for each
user surface. Evals must be able to fail: no metric computed downstream of an assertion that
forces it (fix or delete the decorative ones). And per the drift analysis: every artifact
declares its named outside reader, and the jargon pass (BUILD-PLAN item K) enforces the §5
density metrics so the register serves that reader.

---

## Summary table

| # | Root cause | Produced | Improvement | Nature |
|---|---|---|---|---|
| RC-1 | Same-model build→review loop | B1, the enrolled-stage falsehood, every design-level MAJOR surviving 5 waves | Persona/outside-frame review as a standing pre-done gate; whole-app egress test | Working agreement + **tooling (P3, PT-5)** |
| RC-2 | Citations never checked against primary source at build time | M8, M1's docstring, F4, the 1571 relapse, M6 | Single-source citation table + human-signed inventory + pending markers | **Tooling now (P1, PT-2)** + agreement |
| RC-3 | Cross-cutting claims copied, not sourced once | 3-copy "nothing submitted" (fix missed one), "never leaves this machine", README drift | Claim registry + duplication test | **Tooling now (P2, PT-3)** |
| RC-4 | No author/signer model on documents | M2, M13, part of M4; the unbuilt "LOA-acceptance record" | `author_party` on every document + `awaiting-external-party` state + receipt facts | **Tooling now (P2+P4, PT-4)** |
| RC-5 | Wave-by-wave building without cross-wave fact reconciliation | M1 (4-persona finding), m16, m5, m7, M6-internal | Cross-artifact reconciliation tests; one-owner rule for repeated facts | **Tooling now (P1, PT-6)** + agreement |
| RC-6 | Generic templates on a profiled pathway | M3, M14, m9; green rules certifying past their scope | Computed pathway literals; per-variant render tests; rules state their non-scope | **Tooling (P5+P6)** + agreement |
| RC-7 | Deferrals documented but unguarded | M9, initials-into-cleartext, silent adequacy deferral | Every deferral gets a failing condition (guards, markers) | **Tooling now (P3+P9, PT-7)** + agreement |
| RC-8 | Done = internal consistency, not outside ground truth | m19's decorative eval; five FIRE verdicts over 15 majors; the register drift | Named external references per wave; evals that can fail; named-reader declarations + drift metrics | Working agreement (tooling carriers: P1, P8; jargon pass K) |

The through-line: **OSSICRO's engineering controls were excellent at enforcing what the
builder knew to enforce.** All eight causes are variants of one gap — no step in the loop was
structurally positioned to know something the builder didn't. The durable fix is not more
rigor of the same kind; it is importing outside frames (personas, primary sources, official
instruments, real readers) as *standing gates with tripwires*, which is exactly what the
plan's PT packages make cheap enough to be routine.
