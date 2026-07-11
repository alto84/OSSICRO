# OSSICRO Master Build Plan — "build the whole vision"

**Authorized 2026-07-10 (Alton): full autonomy, build the entire remaining feature set as one
contiguous, dependency-ordered program.** Each unit is a build→adversarial-review→revise loop
(the discipline that caught real PHI-leak and patient-safety bugs in Phases 13–14). Fable reviews
this plan before execution and reviews each build. A **jargon-cleaning pass** (K) is deferred to
the end by explicit instruction — implement first, de-jargon after.

Governing hard lines hold throughout: synthetic data only, no PHI egress (HC2), nothing drives
generation before a named human commits (HC1/INV-3), statutory clocks computed never judged (HC3),
drafts only — OSSICRO never performs a non-delegable regulated act.

## The features (all discussed, none-to-partially built)

| Tag | Feature | Status entering this plan |
|-----|---------|---------------------------|
| **A** | INV-3 `commit_profile` (hard-gate, per-field re-confirmation) | **done** (built/reviewed/revised, 201 tests) |
| **I-audit** | Append-only, hash-chained audit log + persistence hardening | **done** (built/reviewed/revised, 239 tests) |
| **B** | INV-4 de-identified egress gateway | **done** (closed struct, allow-list, live path disabled, hash-chained egress audit; built/reviewed/revised) |
| **C** | Matching engine — registry-search organizer (trials + EA records) | **done** (criteria not scores, absence framing, mini-eval, /match gated; built/reviewed/revised, 282 tests) |
| **D** | Form FDA 3926 export — print-ready PDF (DRAFT watermark) + FDF field-map | **done** (pure-stdlib PDF, gated, human-verify FDF map; built/reviewed/revised) |
| **E** | Pharma persona — manufacturer view behind a named-human release gate | **done** (opaque release_id, snapshot view, audit-logged release; built/reviewed/revised, 311 tests) |
| **F** | Patient persona — tokenized, read-only plain-language status | **done** (opaque token, no enumeration, stage-correct notice; built/reviewed/revised) |
| **G** | Micro-CRO persona — read-only coordinator status board | **done** (GET-only, coded summaries; built/reviewed/revised) |
| **H** | INV-5 `promote()` — preparatory-review → enrollment legal transition | **done** (legal-basis gate, arms the 312.32/56.104(c)/312.310(d)/312.33 duty clocks; built/reviewed/revised, 336 tests) |
| **I** | Hardening — append-only audit log (GAP-3), case-persistence robustness (GAP-7), wire the last wiki rule (GAP-1) | not built |
| **J** | Timed pilot (HITL-3) — one real end-to-end run | gated by HITL-2 (Alton's hours) |
| **K** | Jargon-cleaning pass — plain reader-first prose for user-facing + outward text | **done** (UI copy + Constitution + README rewritten, measured by `tools/prose_lint.py`, fresh-reader verified; internal notes left as-is by design) |

## Dependencies (what must precede what)

- **B → C**: matching cannot query external registries (clinicaltrials.gov, openFDA, PubMed) until the
  egress gateway guarantees only de-identified predicates leave the machine. Build B first, always.
- **A → H**: enrollment (`promote()`) gates against a committed profile; INV-3 must exist first.
- **I-audit early**: the append-only audit log underpins commit, matching egress, and enrollment — build
  it in the foundation wave so later features write to it rather than retrofitting.
- **D independent**: the fillable PDF depends only on the existing intake→3926 field map.
- **E/F/G** need a stable backend; **E (Pharma)** is the most self-contained door (consumes the LOA
  request the physician flow already produces); **G (Micro-CRO)** ties E+F+physician together, so last.
- **J last**: the pilot is the evidence gate; it needs A, D, I and Alton's HITL-2 attestation.
- **K near-last, cross-cutting**: a single vocabulary pass over UI + docs once the surface area is stable.

## Execution waves (revised after Fable's plan review — see amendments log below)

**Wave 1 — Foundation.** A (INV-3, done) + **I-audit** (append-only `audit.py` + `/audit` read; every
commit / signoff / import / release / egress writes an immutable record) + **I-persistence moved here
from Wave 5** (durable case identity — the audit log and the multi-session personas both need it before
they exist, not after). Review, commit. *(HITL-2 attestation starts in parallel — the worksheet exists;
it needs a named attester now, not after Wave 5, because it is the pilot's long pole.)*

**Wave 2 — Safety + marquee.** **B (INV-4 gateway)** — `egress.py`: the single sanctioned outbound
constructor, a closed `DeidentifiedPredicates` struct (condition codes, drug/RxNorm, age-band, sex,
coded route — no names/dates/geography/free-text), destination allow-list (clinicaltrials.gov, NCBI
eutils, openFDA), every call audit-logged; `TestEngineEgressBoundary` extended to *enforce* it. **Against
inference (not just identifier) egress:** rare-code hierarchy roll-up, query decomposition (query the
condition alone; filter age/sex **locally**, never in the outbound query), and an honestly-documented
residual re-identification risk — expanded access skews rare-disease, where code+age-band+sex can be
nationally unique. Then **C (matching)** — `matching.py` + `/api/case/{id}/match`, built as a **registry-
search ORGANIZER, not a recommender** (this is the line between Non-Device CDS and a regulated device):
  - **FDA-2022 Non-Device CDS criterion 4 is a named design constraint** — the physician must be able to
    independently review the *basis* of every candidate.
  - Show **matched / unmatched criteria**, never an opaque confidence score ("matched: condition code,
    drug class; unverifiable from structured data: age criterion"). No manufactured certainty.
  - Absence renders **"no candidates found in the queried registries as of <date>"**, never "no options
    exist" — registry lag must never tell a physician nothing exists.
  - Ship a **mini eval fixture set** (mini GAP-6) alongside it — no unbenchmarked quality claims.
  - **v1 scope = open trials + expanded-access records only.** Defer diagnosis→drug ranking (the most
    CDS-shaped, riskiest third) until **GAP-4** (a human-confirmed manufacturer/drug registry) and the
    eval harness exist. Every candidate is a physician-confirmed proposal, never auto-acted. Review, commit.

**Wave 3 — Artifact + first door.** **D (3926 PDF)** — pure-stdlib AcroForm fill (or a faithful
print-ready layout), field-mapped from intake, **DRAFT watermark retained until the gates clear** (a
filled 3926 is one email from a submission), flagged for the one human field-map verification pass.
**E (Pharma persona)** — a manufacturer-facing view of incoming LOA requests (supply/authorize decision
stays the manufacturer's — FDCA 561A). **Cross-persona visibility is a SEND:** nothing the physician
produced becomes visible in any other persona without an **explicit named-human "release" act, audit-
logged, refused otherwise; synthetic-only through the pilot** — E/F/G together are an inter-party
transmission fabric and must not transmit without that gate (HC1-adjacent). **All UI strings move into a
single display-string table from this wave on** (so K becomes a data pass, not a six-wave code sweep).
Review, commit.

**Wave 4 — Remaining doors + enrollment.** **F (Patient persona)** — **minimal access model first**:
unguessable tokenized links, no case enumeration (auth proper is INV-7-deferred, but a patient surface
cannot ship with case-id-as-capability); **patient-facing vocabulary established at build time**, because
"understandable to the subject" is a 21 CFR Part 50 requirement, not cosmetic polish deferred to K.
**G (Micro-CRO)** — scoped to a **read-only status board**, not an acting coordinator, honoring its own
documented deferral trigger (no real counterparty exists yet). **H (INV-5 `promote()`)** — built **only
if Wave 4 actually produces an enrollment artifact for it to gate**; and if built, `promote()` **arms the
post-enrollment sponsor-investigator obligation clocks (21 CFR 312.32 safety reports, 312.310(d)
follow-up, 312.33 annual) and emits the obligations checklist** — the system must not walk a physician
into duties it then ignores. Otherwise post-enrollment is stated explicitly out of pilot scope. Review, commit.

**Wave 5 — Polish.** **K (jargon cleaning)** as a **data pass over the display-string table** (physician /
manufacturer registers; patient vocabulary already set in Wave 4) + **regulatory-content versioning** —
the Constitution §V regulatory-change log, load-bearing now that matching provenance, the PDF field map,
and the personas triple the citation-bearing surface. Review, commit.

**Wave 6 — Evidence.** **J (timed pilot)** once HITL-2 is done: one synthetic case end-to-end under time,
results written up against pre-registered success criteria.

## Fable review amendments (2026-07-10) — incorporated

Fable's outside review of this plan returned "proceed with the named changes." All are folded in above:

- **BLOCKER 1 (matching manufactures certainty / device-regulation line):** C reframed as a registry-search
  organizer with matched/unmatched criteria (no confidence scores), Non-Device CDS criterion 4 as a named
  constraint, absence-of-match framing, a mini eval fixture, and v1 scoped to trials/EA records.
- **BLOCKER 2 (cross-persona routing is a send):** E gains a named-human, audit-logged **release** gate;
  no cross-persona transmission without it; synthetic-only through the pilot.
- **SERIOUS 3:** I-persistence moved to Wave 1.
- **SERIOUS 4:** INV-4 gains rare-code roll-up + query decomposition + documented residual.
- **SERIOUS 5:** GAP-4 manufacturer registry named as C's prerequisite; C v1 cut to trials/EA meanwhile.
- **SERIOUS 6:** F gains a minimal tokenized-access model before any patient surface ships.
- **SERIOUS 7:** H arms post-enrollment obligation clocks + checklist, or post-enrollment is out of scope.
- **SERIOUS 8 (the eschaton pattern — matches a standing household directive):** G cut to a read-only
  status board; H built only if an enrollment artifact exists to gate. We do not resurrect features their
  own prior reasoning deferred just because the mandate is "build all."
- **WORTH-CONSIDERING 9/10/11:** HITL-2 starts parallel to Wave 1; display-string table from Wave 3 (F
  vocabulary at build time); regulatory-content versioning + DRAFT watermark on the filled PDF.

## Guardrails for the autonomous run

- Every wave commits its own artifacts with attributable messages; the phase log is the audit trail.
- Reviewer is always a standalone agent outside the build team; revisions by the orchestrator; re-review
  on every substantive round (the Phase-13/14 discipline).
- No file edited by two parallel agents in the same wave (server.py / index.html / registries serialize).
- The live server on 8765 is only restarted by the orchestrator at a wave boundary, never mid-build.
- Anything that would perform or enable a real regulated act (send, sign, submit, transfer) stays a
  DRAFT with a named-human gate — no exceptions, at any wave.
- Token spend is authorized ("build all"); correctness and the hard lines are the only ceilings.
