# OSSICRO Master Execution Plan

**Version 1.0 — 2026-07-09.** Subordinate to `docs/OSSICRO-CONSTITUTION.md`. Two parts: **Part I** is the concept-based validation architecture in implementable detail — the Constitution's Sections III and IV rendered as code structure. **Part II** is the sequenced roadmap from the current reviewable prototype (131-page wiki, 60 templates, runnable pure-stdlib engine, passed QA loop) to a working single-patient expanded-access product with counterparty hooks.

**Canonical naming (reconciled).** Earlier drafts diverged on names; these are canonical. Rule strategies: `deterministic | provenance-verified | concept-reviewed`. Deterministic check verbs: `field_nonempty`, `field_equals_study`, `enum_member`, `date_clock`, `human_determination_pending`. Reviewer modules: `review_port.py` / `review_stub.py` / `review_claude.py` (not a single `concept_review.py`). Registries: `rules.json`, `principles.json`; the existing `banned-constructions.json` splits into `hard-rules.json` (tier A) and `slop-examples.json` (tier B). The Constitution lives at `docs/OSSICRO-CONSTITUTION.md`; `docs/VALIDATION-PHILOSOPHY.md` is amended to defer to it for the boundary doctrine and the closed hard-rule list, retaining engine-level operational commentary.

---

# Part I — Concept-Based Validation Architecture

**Scope.** Wires the Constitution into the engine as its governing spine. Changes three modules (`validate.py`, `check.py`, `cli.py`), adds seven (`rules.py`, `provenance.py`, `review_port.py`, `review_stub.py`, `review_claude.py`, `pipeline.py`, `audit.py`), adds two registry files (`rules.json`, `principles.json`), splits one (`banned-constructions.json`), and adds a two-lane test harness. `gates.py` is untouched. Everything except the Claude adapter and the recall lane remains pure stdlib and offline.

**The one invariant that organizes everything:** the ledger status lattice is ordered `green > amber > red`, and every validation stage after generation is a monotone non-increasing fold over that lattice. Deterministic checks, provenance checks, the tripwire, and the concept reviewer can each only lower a document's status or leave it alone. Nothing but a recorded human sign-off moves a document upward past a gate, and nothing at all moves red to green except fixing the underlying defect and re-running the pipeline. This is CP5 ("escalate-only") expressed as a code property, enforced by `tests/test_pipeline_monotone.py`.

## 1. The deterministic spine

These checks stay deterministic because their targets are fact-shaped or legally non-delegable, per the Constitution's earned-rule test. This is the closed list; additions require the written three-condition argument. Each maps to a hard constraint (HC).

| # | Check | Where it lives | HC | Why legitimately deterministic |
|---|---|---|---|---|
| D1 | Gate enforcement: `finalize()` refuses ungated advancement; sign-off and causality records require named human + matching role + attestation; `GateViolation` on any programmatic attempt | `gates.py` (unchanged) | HC1 | Black-letter law; firmness is the protection |
| D2 | Verbatim-lock integrity: SHA-256 of each locked template span vs the registered hash; template-diff invariant | new `provenance.py` | HC4 | Byte identity is a fact |
| D3 | Statutory clocks: 7/15-day IND safety reports (312.32(c)), 30-day IND wait (312.40(b)(1)), annual-report window (312.33); later the working-day EA clocks (312.310(d), 56.104(c)) | `rules.py`, strategy `deterministic`, verb `date_clock` | HC3 | Calendar arithmetic against a regulation; AI judgment strictly worse |
| D4 | Citation presence and resolvability: every rule ships a citation; every generated span carries a `ProvenanceRecord` or is marked inferred | `rules.py` loader (refuses citation-less rules) + `provenance.py` | HC2 | Whether a citation exists and resolves is checkable fact |
| D5 | Ledger mechanics: required-document roster, required-field presence, green/amber/red tri-state, no gated doc green without recorded sign-off | `check.py` (unchanged core) | HC1 | Presence/absence is fact; the tri-state is the auditable spine |
| D6 | Cross-document identity comparison on canonical structured fields (`CONSISTENCY_KEYS`), after normalization, resolution routed to a human | `check.py::check_consistency` (unchanged) | HC2 | Conflicting IND numbers is a fact conflict |
| D7 | Tripwire hard tier: chat-transcript residue (unscoped) and 21 CFR 50.20 exculpatory-consent constructions (scoped `consent`) | `register_linter.py` (logic unchanged; loads split registries) | HC6, HC7 | Process leakage and a cited prohibition; never become legitimate |
| D8 | Part 11 audit trail: model, version, input hash, timestamp, reviewer identity for every AI contribution — including every concept-reviewer call | new `audit.py` | HC5 | The accountability substrate for the judgment layer itself |
| D9 | Field-value equality against the study record (e.g., delegation-log PI == PI of record) | `rules.py`, verbs `field_nonempty`, `field_equals_study` | HC2 | String equality on structured fields is fact |

Explicitly **not** on this list: the tripwire's example tier (advisory only, expected to decay — its density score is recorded, never gates), everything register- or adequacy-shaped, and the three rules migrated in §2.3.

## 2. Rules as data: the `validate.py` refactor

### 2.1 Schema

Rules move from a hardcoded Python list to `engine/registry/rules.json`, versioned like `documents.json` and `gates.json`. Each rule:

```json
{
  "id": "R-1572-IRB",
  "doc_id": "form-fda-1572-statement-of-investigator",
  "citation": "21 CFR 312.53(c)(1)(iv)",
  "principle_text": "Form 1572 item 5 must name the IRB responsible for review and approval of the study.",
  "strategy": "deterministic",
  "check": "field_nonempty",
  "params": {"field": "irb_name"},
  "resolving_question": "Which IRB (name and address) will review and approve this study? Enter it on Form 1572 item 5 (21 CFR 312.53(c)(1)(iv)).",
  "version": "2026-07-09"
}
```

`strategy` is the load-bearing field:

- **`deterministic`** — `check` names a function in the small closed vocabulary in `rules.py`: `field_nonempty`, `field_equals_study` (params: field, study path), `enum_member`, `date_clock` (params: anchor, days, direction, calendar: calendar|working), `human_determination_pending` (the SAE rule's shape). New check verbs require code review; new rules using existing verbs are data edits.
- **`provenance-verified`** — no `check` function. The generic verifier in `provenance.py` runs: the named span has a `ProvenanceRecord`, the record's source path matches `params.source`, and (for verbatim spans) SHA-256 of the rendered span equals `params.sha256`. The property is factual **by construction of generation**, not by inspecting prose.
- **`concept-reviewed`** — never executed deterministically. The loader compiles these rules into `Principle` objects handed to the reviewer port (§3). `principle_text` plus `citation` **is** the check.

The loader (`rules.py::load_rules`) enforces D4 at load time: a rule without a citation, or a deterministic rule whose `check` verb is not in the vocabulary, fails engine startup. `principle_text` is mandatory for all three strategies — for deterministic rules it is the labeled proxy statement the Constitution's amendment clause requires: the concept the check stands in for, adjacent to the mechanism, so a reviewer can see when the proxy has decayed.

### 2.2 `validate.py` after the refactor

```python
@dataclass
class Rule:
    id: str
    doc_id: Optional[str]
    citation: str
    principle_text: str
    strategy: str                     # deterministic | provenance-verified | concept-reviewed
    check: Optional[str] = None       # deterministic only
    params: dict = field(default_factory=dict)
    resolving_question: str = ""
    version: str = ""

def run_rules(study, documents) -> List[RuleResult]:
    # executes ONLY deterministic + provenance-verified rules
def concept_rules(doc_id=None) -> List[Rule]:
    # returns concept-reviewed rules for the reviewer port; run_rules never touches them
```

`RuleResult` keeps its shape (rule_id, doc_id, passed, message, citation, resolving_question) so `check.py::build_ledger` needs no change to consume it. The seven current rule functions collapse into check-verb instances; the three string-matchers are migrated as follows.

### 2.3 Migrating the three semantic-faking rules

**R-1571-30DAY** (currently: substring match on `"30 days"` and `"312.40"` in rendered text, `engine/ossicro/validate.py:67-76` — a lexical proxy the generator can satisfy by pasting the strings). Migration: the 1571 template's commitment sentence becomes a named verbatim-locked span, `commitment-30-day-wait`, with its canonical text and SHA-256 registered in `documents.json`. `generate.py` records `ProvenanceRecord(span="commitment-30-day-wait", source="template:form-fda-1571#commitment-30-day-wait", citation="21 CFR 312.40(b)(1)")`. The rule becomes `strategy: provenance-verified, params: {span_id, sha256}`. The substring match is deleted. The property is now deterministic **and true**: the exact sentence, byte-identical, is present because generation placed it and the hash proves nothing altered it.

**R-1572-PHASE** (currently: membership in a frozen whitelist `{"1","2","3","1/2",...}` — over-fires on legitimate labels like `4` or `2b/3`, and validates the string, not its origin). Migration: phase is already a structured field on `Study`. The rule becomes `strategy: provenance-verified, params: {field: "phase", source: "phase"}` — the 1572 item-8 value must carry a provenance record tracing to `study.phase` and equal it. Whether an unusual phase label is *appropriate* is a human intake question, surfaced at study-record intake, not a rendering-time whitelist. The whitelist is deleted; the check verifies origin and fidelity, which are facts.

**R-ICF-50.25** (currently: presence of the marker strings `"50.25(a)(1)"`…`"50.25(a)(8)"` in the rendered ICF — the canonical decay case: it trains the generator to paste citation strings, not to disclose risks). Migration splits it along the boundary doctrine:

- *Presence (fact-shaped, by construction):* the ICF template is restructured into eight named element sections (`icf-element-1` … `icf-element-8`), each registering a provenance record citing its `50.25(a)(n)` subsection when rendered non-empty. New rule `R-ICF-50.25-PRESENT`, `strategy: provenance-verified`: all eight section records present, sections non-empty. Marker-string matching deleted.
- *Adequacy (quality-shaped, judgment):* new rules `R-ICF-50.25-ADEQ-1` … `-8`, `strategy: concept-reviewed`, each with a principle like: *"21 CFR 50.25(a)(2): assess whether the risks section substantively discloses the reasonably foreseeable risks of this product for this population, in language the subject population can understand, without minimization."* These go to the reviewer and, when graded deficient, make the ICF red — exactly what the string match pretended to do and could not.

### 2.4 Two-tier registry split

`registry/banned-constructions.json` splits into `registry/hard-rules.json` (tier A: chat-transcript residue; 21 CFR 50.20 exculpatory constructions with citations; hard-fail, forever — HC6/HC7 made data) and `registry/slop-examples.json` (tier B: dated mannerism examples; findings are non-blocking ledger advisories; each entry labeled with the concept it proxies). `register_linter.py` logic is unchanged — its two-tier design already conforms — but it loads the two files, so the tier boundary is a file boundary mirroring the Constitution's Section III/IV boundary.

## 3. The concept-based reviewer: a pluggable port

### 3.1 Port and data types (`review_port.py`)

```python
@dataclass
class Principle:
    id: str; citation: str; text: str
    category: Optional[str]           # consent | fda-form | protocol | correspondence | None (all)
    source_rule_id: Optional[str]     # back-link into rules.json when derived from a rule

@dataclass
class ConceptFinding:
    finding_id: str
    doc_id: str
    field: Optional[str]              # field name when span-scoped to a filled field
    span_quote: str                   # verbatim quote from the document — deterministically verified
    principle_id: str
    citation: str
    grade: str                        # "deficient" | "advisory" | "adequate"
    rationale: str
    suggested_rewrite: Optional[str]  # a proposal; regeneration goes through generate.py, never a silent edit
    reviewer_id: str; model_version: str; input_hash: str; timestamp: str

@dataclass
class ReviewReport:
    doc_id: str
    findings: List[ConceptFinding]
    spans_reviewed: int
    spans_skipped_verbatim: int       # jurisdiction evidence for the audit trail
    reviewer_id: str; model_version: str; input_hash: str
    def deficient(self) -> List[ConceptFinding]: ...
    def advisories(self) -> List[ConceptFinding]: ...

class ConceptReviewer(Protocol):
    def review(self, doc: Document, principles: List[Principle],
               context: ReviewContext) -> ReviewReport: ...
```

`ReviewContext` carries the document's registry category, the study record (for contradiction-hunting), tripwire example-tier findings (as hints), and reference-exemplar paths from the source library.

Two invariants are enforced by the **port**, outside any adapter, in `review_port.py::validate_report`:

1. **Evidence is verbatim or the finding is void.** Every `span_quote` must appear character-for-character in the document's rendered text. Findings failing this are dropped and logged to the audit trail as reviewer errors — a deterministic backstop against a hallucinating judge.
2. **Jurisdiction.** No finding may land inside a verbatim-locked span (checked against provenance records). The reviewer judges filled fields and generated spans only.

### 3.2 Reference stub (`review_stub.py`)

`StubReviewer` is the deterministic offline implementation, used by all unit tests and by the engine when no adapter is configured. Behavior:

- Default: returns `adequate` for every reviewed span (zero findings), so the pipeline is a no-op pass-through offline.
- Sentinel mode: a span containing `[[STUB:DEFICIENT:<principle-id>]]` or `[[STUB:ADVISORY:<principle-id>]]` yields the corresponding finding with a canned rationale. This lets fixture documents exercise every escalation path — red-from-concept, advisory notes, gate critique packets — with zero network and full determinism.
- Replay mode: `StubReviewer(replay_dir=...)` loads canned `ReviewReport` JSON keyed by input hash, for regression fixtures captured from real Claude runs.

### 3.3 Claude SDK adapter (`review_claude.py`)

`ClaudeReviewer` implements the port with the critique-and-revise loop — Constitutional AI's training-time pattern applied at inference time:

1. **Packet assembly.** Strip verbatim-locked spans (jurisdiction is enforced before the model ever sees the text, not just after). Assemble: generated spans with field names, the document category, the applicable `Principle` list (writing principles from `principles.json` plus the category's concept-reviewed rules from `rules.json`), tripwire example-tier hints, and one or two reference exemplars.
2. **Critique call.** One structured request: *for each principle, quote the evidence, grade the span, state the rationale.* Response is schema-validated JSON; malformed responses retry once, then fail the review loudly — a failed review is a pipeline error, never a silent pass.
3. **Revise call** (deficient findings only): produce `suggested_rewrite` per finding, judged against the same principle text. Maximum two critique-revise iterations; rewrites remain proposals routed through `generate.py` regeneration and re-validation — the reviewer never edits a document.
4. **Deterministic post-filter.** `validate_report` (§3.1) runs; surviving findings get audit fields stamped.
5. **Audit.** `audit.py::log_review(report)` writes the Part 11 record: model id, version, prompt input hash, findings, and later the human disposition per finding.

Configuration (`ossicro.toml` or env): model id pinned, temperature 0, principle-registry version recorded per call. The Constitution's central design claim — the reviewer improves with model capability with no rule rewrite — falls out of this contract: upgrading the pinned model changes nothing in `rules.json`, `principles.json`, or the port. `review_claude.py` is the only module allowed a non-stdlib dependency, import-guarded so the engine runs pure-stdlib without it.

**Escalation semantics** (enforced where findings are consumed, §4): `deficient` → red with the finding's rationale as the resolving question; `advisory` → note on the ledger item, status unchanged; `adequate` → audit log only. There is no code path by which a `ReviewReport` raises a status, discharges a gate, or alters a deadline. `review_claude.py` has no import of `gates.py` and no write access to `Document.signoffs` — structural, not conventional.

## 4. Composition in the pipeline: cheapest-first, escalate-only

New orchestrator `pipeline.py::run_check`, which `cli.py` calls in place of its current hand-sequenced steps:

```python
def run_check(study, documents, doc_registry, gate_registry,
              reviewer: Optional[ConceptReviewer] = None,
              review_policy: str = "survivors") -> CheckResult:
```

Stage order, cheapest first; each stage folds monotonically downward:

| Stage | Cost | What it does | Can produce |
|---|---|---|---|
| 1. Structural | free | Roster presence, required fields (existing `build_ledger` logic) | red |
| 2. Deterministic + provenance rules | µs | `run_rules` over `rules.json` strategies 1–2, incl. clocks and span hashes | red |
| 3. Consistency | µs | `check_consistency` (unchanged) | red |
| 4. Tripwire | ms | `lint_document` per doc with registry category; hard-tier findings only are gating | red (hard tier); hints (example tier) |
| 5. Concept review | seconds + $ | `reviewer.review(...)` with category principles; skipped entirely when `reviewer is None` | red (deficient), notes (advisory) |
| 6. Ledger fold | free | `build_ledger` extended with `lint_reports` and `review_reports` params | final tri-state |
| 7. Human gate | human | unchanged `gates.py`; amber until sign-off | green |

`review_policy="survivors"` (default) sends only documents still clean after stages 1–4 to the model — a document already red gets fixed and re-run before spending judgment tokens on it. `review_policy="all"` reviews everything (useful when the human wants the full critique packet in one pass).

`build_ledger` changes (the only `check.py` edit):

- New parameters `lint_reports: Dict[str, LintReport]` and `review_reports: Dict[str, ReviewReport]`.
- Tripwire hard findings and deficient concept findings join the red-question set exactly where failed rule results do today — same resolving-question mechanics, same ledger row.
- Advisory concept findings and example-tier lint findings append to `LedgerItem.notes`.
- The ledger records which layers ran (deterministic / tripwire / concept); when the concept layer did not run, that absence is itself a recorded advisory — a silent skip is not a pass.
- Ordering already guarantees the composition property: red conditions are evaluated before the amber gate check, so **amber (awaiting a gate) is only reachable with zero unresolved concept deficiencies** — CP5's "structurally complete *and* no unresolved concept deficiency" holds by construction.

**The human gate interaction.** New helper `pipeline.py::gate_packet(doc, review_reports, lint_reports) -> GatePacket` returns everything outstanding on a gated document — deficient findings, advisories, lint hints, suggested rewrites — formatted for the signer. `cli.py`'s sign-off flow prints the packet before `record_signoff`. The packet informs; it never blocks. `gates.py` is deliberately untouched: the human's authority to sign is not conditioned on the machine critique, and the machine critique cannot substitute for the signature. Findings escalate *toward* the gate; they never operate the gate in either direction.

## 5. Test harness: two lanes

### Lane 1 — Golden corpus, zero-false-positive, CI-blocking, offline

`engine/fixtures/golden/` holds human-vetted professional regulatory prose: reference documents from the source library, real-register consent forms, FDA-style correspondence — text a careful regulatory professional actually wrote, including legitimate "shall", formal passives, and verbatim defined-term repetition (the known over-fire traps).

`tests/test_golden_zero_fp.py` asserts, per golden file:
- tripwire **hard-tier** findings == 0 (example-tier findings are permitted and reported, not asserted — advisory by design);
- deterministic and provenance rules produce zero failures on the golden fixture studies;
- pipeline stages 1–4 leave every golden document non-red.

Pure stdlib, no network, runs on every commit. A false positive here is a build break by policy: the deterministic layer's contract is *certainty*, and one over-fire on professional prose invalidates it.

Companion structural tests, same lane:
- `tests/test_pipeline_monotone.py` — property test: for random stage orderings and finding injections, no fold ever raises a status.
- `tests/test_reviewer_contract.py` — parametrized over `[StubReviewer, ClaudeReviewer if API key present]`: evidence-verbatim invariant, jurisdiction (seed a mannerism inside a verbatim-locked span; assert no finding lands there), report shape, audit fields present.
- `tests/test_stub_escalation.py` — sentinel-seeded fixtures drive deficient → red, advisory → note, gate-packet contents; assert the reviewer cannot green anything (inject an `adequate`-everything report on a red document; document stays red).
- `tests/test_rules_registry.py` — every rule in `rules.json` has a citation and a valid strategy; every deterministic `check` verb exists; every provenance-verified rule's span/hash resolves against `documents.json`; the three migrated rule ids exist with their new strategies and the old string-match code paths are gone.
- `tests/test_constitution_conformance.py` — fails if any rule record lacks `{citation, principle_text, strategy}`, if any tier-B pattern hard-fails, or if the hard-rule enumeration in the registries diverges from the Constitution's closed list (HC1 gate ids, HC6/HC7 tier-A entries).

### Lane 2 — Judge-evaluated recall over held-out slop, scheduled, non-blocking

`engine/fixtures/slop/` holds documents with **seeded, labeled defects**: LLM mannerisms current and older, inadequate or minimized risk disclosures, promotional consent language, payment-framed-as-benefit, stacked-modal hedging, internal contradictions — each defect annotated `{span, expected_principle_id, expected_grade}`. **Contamination rule:** slop-corpus content never appears in reviewer prompt exemplars, `principles.json` examples, or replay fixtures; it is held out permanently.

`eval/run_recall_lane.py` (network-requiring, scheduled — not CI-blocking):
1. Runs `ClaudeReviewer` over the slop corpus; scores **recall** = fraction of seeded defects flagged with the correct principle (grade agreement reported separately).
2. Runs the same reviewer over the golden corpus; **any deficient finding on golden is a precision alarm**, reported per principle.
3. Writes `eval/results/<date>-<model_version>.json` with per-principle recall, golden-deficient count, and diffs vs the previous baseline.

Policy: a recall regression on model upgrade, or a golden precision alarm, triggers a rubric review recorded in the principle registry's version history — the Constitution's hindsight feedback loop, mechanized. Downstream real-world failures (payer rejection, IRB return) are added to the slop corpus as new labeled cases, so the recall lane's coverage grows from actual failure, not speculation.

## 6. Build inventory

**New files**

| Path | Contents |
|---|---|
| `engine/registry/rules.json` | All validation rules as data (§2.1 schema); seeded with the 7 current rules, 3 migrated |
| `engine/registry/principles.json` | Writing principles (from `docs/WRITING-PRINCIPLES.md`, mechanically mirrored + versioned) and per-category regulatory-adequacy principles |
| `engine/registry/hard-rules.json`, `engine/registry/slop-examples.json` | Two-tier split of `banned-constructions.json` (§2.4) |
| `engine/ossicro/rules.py` | `load_rules()`, check-verb vocabulary, strategy dispatch, `concept_rules()` |
| `engine/ossicro/provenance.py` | `verify_span(doc, span_id, source, sha256)`, `verbatim_spans(doc)`, generic provenance-verified rule executor |
| `engine/ossicro/review_port.py` | `Principle`, `ConceptFinding`, `ReviewReport`, `ReviewContext`, `ConceptReviewer` protocol, `validate_report()` |
| `engine/ossicro/review_stub.py` | `StubReviewer` (default / sentinel / replay modes) |
| `engine/ossicro/review_claude.py` | `ClaudeReviewer` critique-and-revise adapter; the only non-stdlib module, import-guarded |
| `engine/ossicro/pipeline.py` | `run_check()`, `CheckResult`, `gate_packet()` |
| `engine/ossicro/audit.py` | `log_review()`, `log_disposition()` — Part 11 trail entries for the concept layer |
| `engine/fixtures/golden/`, `engine/fixtures/slop/` | Corpora per §5 |
| `eval/run_recall_lane.py`, `eval/results/` | Lane 2 |
| `engine/tests/test_golden_zero_fp.py`, `test_pipeline_monotone.py`, `test_reviewer_contract.py`, `test_stub_escalation.py`, `test_rules_registry.py`, `test_constitution_conformance.py` | Lane 1 |

**Modified files**

| Path | Change |
|---|---|
| `engine/ossicro/validate.py` | `Rule` gains `principle_text`/`strategy`/`params`; rule bodies replaced by registry load + dispatch; `RuleResult` unchanged; three string-matchers deleted |
| `engine/ossicro/check.py` | `build_ledger` gains `lint_reports` + `review_reports` params; deficient/hard findings → red questions, advisories → notes; layer-provenance recorded; nothing else |
| `engine/ossicro/generate.py` | Registers the `commitment-30-day-wait` verbatim span and the eight ICF element-section provenance records; renders phase from `study.phase` with provenance |
| `engine/registry/documents.json` | Verbatim-span text + SHA-256 for the 1571 commitment; ICF template section ids |
| `engine/ossicro/register_linter.py` | Loads `hard-rules.json` + `slop-examples.json` instead of `banned-constructions.json`; logic unchanged |
| `engine/ossicro/cli.py` | Calls `pipeline.run_check`; prints `gate_packet` before sign-off flow |
| `docs/VALIDATION-PHILOSOPHY.md` | Amended to defer to the Constitution for the boundary doctrine and closed hard-rule list; retains operational commentary |

**Untouched:** `gates.py`, `models.py` (existing `ProvenanceRecord` suffices; `span` field carries the span id).

**Build order:** (1) `rules.json` + `rules.py` + refactored `validate.py`, existing tests green with behavior preserved; (2) provenance migration of the three rules + `generate.py`/`documents.json` changes; (3) port + stub + pipeline + `check.py` fold + monotonicity tests; (4) golden corpus + zero-FP gate + conformance test; (5) Claude adapter + audit; (6) slop corpus + recall lane. Steps 1–4 are fully offline and independently shippable; the engine runs identically with `reviewer=None` throughout.

---

# Part II — Phased Roadmap

Five phases, each with goal, tasks, dependencies, verifiable acceptance, and effort. Effort figures are focused agent-assisted build-days; planning estimates, not commitments. **Total arc: roughly 7–10 focused weeks.**

## Ordering and the dependency spine

```
P1 (Constitution + validation architecture, Part I)
 └─ P2 (Route-3926 vertical)
     └─ P3 (real app around the vertical)
         └─ P4a (agentic intake + route classifier)
     └─ P5 (front-door registry + Say-Yes pack + verifier)
         [P5's registry-seeding data work can run parallel to P3/P4a]
```

The ordering is forced, not preferential:

- **P1 before P2.** The 3926 generators must emit through the rules-as-data engine, the two-tier tripwire, and the concept reviewer. Building them against the current hardcoded `validate.py` and single-file `banned-constructions.json` means rebuilding them weeks later. Retrofitting the philosophy after the second route ships is exactly the structural dishonesty the directive names.
- **P2 before P3.** There is nothing worth wiring behind the frontend until one route runs end-to-end.
- **P3 before P4a.** The extraction agent, the minimum-necessary loop, and the interview-mode Red-Resolver need an application shell to land in. P3 ships with a structured intake form; P4a replaces that form with agents.
- **P5 after P2, overlapping P3/P4a.** The Say-Yes pack and the verifier consume P2's LOA-request generator and hash manifest. The Manufacturer Front-Door Registry seed is data work with no code dependency and can start any time after P2.

## The single first step

**Create `engine/registry/rules.json` and port the seven `validate.py` rules into it, with `docs/OSSICRO-CONSTITUTION.md` committed in the same commit.**

The Constitution states the boundary doctrine; the rule-record schema is the doctrine made executable, and porting the existing rules through it immediately forces the first real classification decision: `R-1571-30DAY` currently passes if the rendered document contains the substrings `"30 days"` and `"312.40"` (`engine/ossicro/validate.py:67-76`). That is the exact anti-pattern the doctrine names — judgment smuggled into a lexical proxy — sitting in the shipped engine today. Reclassifying it (verbatim-locked template span verified by provenance) is the proof, in the first commit, that the philosophy governs the code rather than describing it.

## P1 — Build the philosophical basis in

**Goal.** The concept-over-rules philosophy becomes the system's governing spine: a Constitution the code demonstrably obeys, every validation rule carrying `{citation, principle_text, strategy}`, hard rules and judgment structurally separated, and a concept reviewer wired into the ledger with escalate-only authority. This phase executes Part I in its entirety.

**Tasks.**

1. Commit `docs/OSSICRO-CONSTITUTION.md`; wire references from `README.md`, `PROGRAM.md`, `engine/README.md`, and a wiki page so no entry point misses it; amend `docs/VALIDATION-PHILOSOPHY.md` to defer to it.
2. Part I build steps 1–2: rules-as-data refactor + the three rule migrations (R-1571-30DAY, R-1572-PHASE, R-ICF-50.25).
3. Part I §2.4: two-tier registry split; linter loads both files; density score recorded, never gates.
4. Part I build step 3: reviewer port + stub + `pipeline.py` + `check.py` fold + `audit.py`.
5. Part I build step 4: golden-corpus seed + zero-FP gate + monotonicity, escalation, registry, and constitution-conformance tests.
6. Part I build step 5: `ClaudeReviewer` adapter, `principles.json`, Part 11 audit logging.
7. Part I build step 6: slop-corpus seed + `eval/run_recall_lane.py` (scheduled, non-blocking). Steps 6–7 may trail into early P2 without blocking it — the engine runs with `reviewer=None`.
8. StudyFacts v0: extend `models.Study` toward the canonical fact spine — provenance-stamped fact entries (`source`, `attested_by`, `date`) keyed to the registry's required-field resolve-paths. Minimal now; the P2 generators consume it; full formalization waits for the IND program.

**Dependencies.** None. Everything needed exists in the repo.

**Acceptance.**
- Existing engine and linter test suites (16 tests) pass; new Lane-1 tests pass.
- `validate.py` contains no inline rule content; all rules load from `rules.json`; no string-match-for-semantics rule remains anywhere in the engine.
- `python -m ossicro.cli demo` runs pure-stdlib with the concept layer stubbed, and its ledger records that the concept layer was stubbed.
- A generated 1572 passes the template-diff invariant with zero tier-A findings and no unresolved concept deficiencies.
- `OSSICRO-CONSTITUTION.md` exists, is referenced from every entry-point document, and the conformance test enforces its hard-rule list in CI.

**Effort.** 4–6 days.

## P2 — Route-3926 Sprint Pack

**Goal.** The smallest complete rapid-access vertical: from a structured intake, emit the full individual-patient expanded-access package (21 CFR 312.310) — verifiable, provenance-carrying, ledger-fronted — with the emergency variant's clocks computed.

**Tasks.**

1. **Routes as a first-class registry concept.** `registry/routes.json`: a route = named subset of the 60-document registry + route-specific rules + route-specific clocks + gate set. `route-3926` (non-emergency) and `route-3926-emergency` are the first two entries. This is the extension point every later route reuses.
2. **Fixture.** `fixtures/ea_3926_case.json`: synthetic patient, drug, manufacturer, IRB, physician credentials — plus the emergency variant. Human-verified as the first golden-package pair.
3. **Six generators**, each fill-only-the-blanks against its template, emitting provenance triples, consuming StudyFacts v0: Form 3926 field fill with the 10.a/10.b waiver logic as deterministic branching; clinical-history and treatment-plan narrative (narrative spans are concept-reviewed field values, not free prose); manufacturer LOA-request letter; IRB chair-concurrence submission; drug-accountability record shell; 50.25-compliant ICF with EA-specific consent handling and the ClinicalTrials.gov statement treated per 42 CFR 11.10 applicability (citation-conditional logic as a deterministic rule with the citation on it).
4. **Clock engine.** Working-day arithmetic (federal-holiday table, versioned as data): the 312.310(d) 15-working-day written-follow-up clock and the 56.104(c) 5-working-day IRB-notification clock, both starting at recorded telephone authorization. Compute and surface only; no clock ever discharges anything.
5. **Route rules.** 312.305(a)/312.310(a) criteria coverage: presence checks deterministic; adequacy of the risk/benefit narrative is a `concept-reviewed` rule citing the criteria — the first live use of the P1 boundary.
6. **Gates.** Physician certification/signature, 312.310(a) risk determination, manufacturer LOA, IRB concurrence, consent event — all ambers only external humans discharge; `GateViolation` on any premature advance.
7. **Emergency mode.** The clock starts, plus the phone-authorization briefing sheet (what the physician says to FDA on the call) as a generated document.
8. **Verifiable package assembly.** Hash-chained manifest (every artifact, version, provenance index, ledger snapshot) with the completeness ledger rendered as the cover sheet.
9. **Harness fixture.** Both 3926 fixtures enter the golden-package harness and gate CI from this point on.

**Dependencies.** P1 complete (rules schema, tier split, concept reviewer, verbatim locks, StudyFacts v0).

**Acceptance.**
- The synthetic fixture reaches a green-or-explained ledger with only gate ambers (sign, consent, IRB, LOA) pending.
- Every generated field traces to a StudyFacts entry or renders `[[MISSING]]` → red; zero invented facts by construction, verified by the template-diff invariant on all six documents.
- Clock computations verified against a test table of dates spanning weekends and federal holidays.
- Tripwire and concept reviewer run over every generated span; tier-A findings zero; concept deficiencies resolved or surfaced.
- An independent script can verify the package manifest end-to-end.

**Effort.** 8–12 days. The generators are parallelizable across agents; the clock engine and route model are not.

## P3 — Real-app wiring

**Goal.** Replace the static landing page with the working flow: intake → route → generate → check → ledger → gated export. A physician-shaped user can run the app locally and drive the 3926 route through it.

**Tasks.**

1. **Backend decision and service.** Keep the engine pure-stdlib; allow the app layer one thin dependency tier (FastAPI + uvicorn is the pragmatic call; a stdlib `http.server` variant is defensible if the zero-dependency property matters for the local-first story — decide at phase start and record the decision). Endpoints: create case, submit intake, run generate, get ledger, get document with provenance spans, discharge-gate (records a named-human sign-off with attestation metadata), export package.
2. **Intake wizard.** Structured form for the 3926 route's fields — deterministic, no agents yet. Every field labeled with its citation, mirroring the templates' Fields tables.
3. **Ledger view.** Green/amber/red with each red's resolving question and each amber's named human act; layer-provenance visible (what the deterministic layer, tripwire, and concept reviewer each found).
4. **Red-Resolver v0 (deterministic).** The ledger-driven question queue in the UI: walk reds in dependency order (spine facts before consuming documents), recompute the ledger after each answer, write answers into StudyFacts provenance-stamped. No interview agent yet — the queue order and recompute loop are pure engine logic; P4a adds the agent on top of this exact loop.
5. **Document viewer.** Fixed template prose, filled spans, and inferred spans visually segregated; provenance on hover/demand.
6. **Gated export.** Export refuses while any gate is undischarged; the `GateViolation` surfaces in the UI as the feature it is, not as an error to suppress. Single-pass review surface: deterministic/boilerplate spans collapsed, interpretive spans foregrounded, amber list as an ordered signature-routing queue, gate packet shown before each sign-off.
7. **Local persistence and honesty.** SQLite or JSON-file store, local only; DRAFT — REQUIRES QUALIFIED HUMAN REVIEW watermarks on everything; no PHI-handling claims beyond what the local-first architecture actually delivers. Update README to stop calling the frontend a landing-page demo only when this is true.

**Dependencies.** P2 (a route worth wiring). No dependency on P4.

**Acceptance.**
- A user runs the app locally, enters the synthetic case through the UI, watches the ledger move red → amber via the Red-Resolver queue, and downloads the manifested package.
- Export with pending gates is refused, visibly, with the gate list.
- The wall-clock criterion becomes measurable here: intake-to-green-ledger under 24 hours with only gate actions pending, timed on the fixture.
- No API path exists that discharges a gate without a recorded named-human attestation — adversarial review explicitly hunts for one, and finding one blocks release.

**Effort.** 5–8 days.

## P4a — Patient intake and matching (scoped)

**Goal.** Replace the structured form with agentic intake: free-text and document extraction, a minimum-necessary question loop, and the route classifier that surfaces hard stops before any drafting. Scoped to what serves the 3926 route and route triage.

**The honest split.** Full trial matching — retrieve→adjudicate against live ClinicalTrials.gov data, mechanism-aware expansion, benchmarked on CHIA/TREC/n2c2 before any patient-facing quality claim — is a research-grade program measured in months. That is **P4b**, and it runs as its own program with its own evaluation harness. P4a below is the part that ships value into this arc.

**Tasks.**

1. **Extraction agent (Claude SDK).** Pasted chart snippet, free-text history, PDF path → structured profile with span-level provenance and per-field confidence. The invariant is contractual and tested: anything unmappable is `indeterminate`, never guessed, never a silent not-met. Adversarial fixtures (ambiguous labs, conflicting dates, missing units) verify it.
2. **Field-by-field confirmation UI.** The extracted profile is a draft the physician confirms before it drives anything; deterministic and inferred spans visually segregated; the confirmed profile is hashed as the generation input-of-record.
3. **Minimum-necessary loop.** The gap agent diffs required predicates against the profile and emits an ordered question list; every asked datum traces to a specific predicate or ledger red, making 45 CFR 164.502(b) minimum-necessary verifiable from the audit trail. For this arc the predicate universe is the 3926 route's requirements, not parsed trial-eligibility criteria.
4. **Route classifier with hard stops first.** Profile → draft route recommendation across Mode A / Mode B / 312.310 / no-suitable-option, with the four software-unfixable hard stops (central-IRB access and fee, research-liability indemnification, NCD 310.1 billing, site readiness) rendered as the first output, each a ledger item. Output is a draft recommendation, never an instruction; the pathway decision stays with the physician.
5. **Red-Resolver interview agent.** The agent layer on P3's deterministic queue: conversational resolution of reds in dependency order, each answer provenance-stamped `physician-attested, date, session`. The agent supplies data that makes predicates pass; it never grades, never dispositions a red, never touches amber.
6. **Privacy posture.** All extraction local, PREPARATORY-state semantics (no PHI egress, audited reads, ephemeral); the code-enforced privacy state machine in full is later scope, but the no-egress property is enforced and tested now.

**Dependencies.** P3 (the app shell), P1 (attribution plumbing for agent contributions).

**Acceptance.**
- Pasted chart snippet → confirmed profile → route recommendation with hard stops → 3926 intake pre-populated with zero re-keying.
- Adversarial extraction fixtures produce `indeterminate`, never fabricated values — tested, not asserted.
- The audit trail shows, for every question asked, the predicate or red that justified it.
- Every agent contribution carries the Part 11 attribution record; a named human confirmed every fact that entered StudyFacts.

**Effort.** 10–15 days. P4b explicitly excluded from this figure.

## P5 — CRO and pharma hooks (scoped)

**Goal.** The counterparty-facing layer for the expanded-access route: the manufacturer front-door registry, the router, the EA Say-Yes pack, and the standalone dossier verifier. The IIS pack, full activation binder, SDEA/TORO builders, and Checklist Join stay in the later program.

**Tasks.**

1. **Manufacturer Front-Door Registry — schema and seed.** Structured records: counterparty function, sanctioned intake point (§561A published expanded-access policy, medical-information contact), required intake fields, submission format, stated decision timelines; per-record source URL, retrieval date, content hash. Seed with 25–50 manufacturers of drugs plausibly requested via EA. An extraction agent drafts records from published policies; **every record that could drive a real submission is human-confirmed before first use** — a stale contact spends the patient's clock. A freshness job re-checks and diffs on a schedule. The registry is a public good in its own right and ships as data in the open repo. Data work; can start in parallel with P3/P4a.
2. **Route router.** Drug facts → manufacturer → front door → pre-mapped Say-Yes fields. Hard rail as a deterministic validation rule: routing to a sales contact is a validation error, never a fallback — Medical Affairs or Clinical Development only.
3. **EA Say-Yes pack.** The LOA-request export: 3926 draft, clinical narrative, monitoring plan, physician-qualification statement, consent form, IRB path, signature-ready LOA skeleton (the §312.305(b)(1) cross-reference letter drafted for the manufacturer's counsel to edit and sign) — professional cover letter, human-readable cross-reference index (requirement → artifact → citation → signer), visible-signature PDF renditions, hash manifest as an appendix. The ledger blocks export while any gate item is amber or red; release is an explicit physician action.
4. **Sponsor-side dossier verifier.** Free, standalone, no-install (single-file script or static HTML): confirms hash-chain integrity, checklist coverage, internal consistency, and open items without trusting OSSICRO's servers. Small build, disproportionate trust value — it converts "trust this one-physician site" into "verify this dossier in twenty minutes."

**Dependencies.** P2 (LOA-request generator, manifest); P3 (export surface). Task 1 has no code dependency.

**Acceptance.**
- Registry holds ≥25 human-confirmed records, each with source URL, retrieval date, and hash; the freshness job runs and reports diffs.
- The router resolves the fixture drug to the correct confirmed front door; a sales-contact route raises a validation error in tests.
- The Say-Yes pack renders complete from the fixture case and is blocked while any gate is open.
- The verifier confirms an untampered package and detects a single-byte tamper — both as tests.

**Effort.** 7–10 days for the scoped version. The full counterparty surface (SDEA, TORO, Checklist Join, micro-CRO entity formation with counsel review) is a separate program, not scheduled until a real counterparty interaction motivates it.

## Cross-phase obligations

- **Golden-package harness** gates CI from P2 onward; one human-verified fixture pair per route as each route ships. The red line at every merge: zero gate regressions.
- **Adversarial gate hunt.** Each phase's review explicitly attempts to find an automated path through any gate in the gating matrix; finding one is a release blocker. Standing policy, restated per phase because it is the one check that must never be assumed.
- **Days-to-Drug clock model.** Once P3 makes the flow drivable, instrument the decomposition: physician-side intervals (driven toward zero), cited statutory clocks, observed counterparty intervals (elapsed time only, no fabricated predictions). The measurement layer that proves "routine" is being achieved rather than claimed.
- **Constitution conformance** runs in CI from P1 onward: every new rule enters as data with `{citation, principle_text, strategy}`, and additions to the hard-rule list require the earned-rule test in writing.

## What this arc deliberately does not contain

Named so their absence is a decision, not an oversight: the full IND assembly swarm (needs the mature StudyFacts spine P2 only seeds); benchmarked trial matching (P4b); the safety-clock engine and E2B(R3) conduit (no live study exists yet to need it); the SDEA/TORO/Checklist-Join contract kit and micro-CRO entity formation (counsel review precedes any assumption of obligations). Each becomes schedulable the moment its predecessor in this arc is real.