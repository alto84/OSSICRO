# OSSICRO Engine — generate / check / validate (prototype)

Pure Python 3 standard library. No external dependencies, no network. Runs anywhere.

```bash
cd engine
python -m ossicro.cli demo        # run the end-to-end demo on the sample study
python -m unittest tests.test_engine -v
```

## What it does

Given a structured `Study` record, the engine:

1. **Generate** (`generate.py`) — instantiates document templates by `{{field}}` substitution. **Every filled span emits a `ProvenanceRecord`** (source datum → governing citation). Missing source data becomes an explicit `[[MISSING: field]]` marker, never a silent blank. Output is always a **DRAFT** for human review.
2. **Check** (`check.py`) — the **completeness ledger**: each required document resolves to **green** (present, all required fields filled, rules pass, any gate signed), **amber** (complete but awaiting a non-delegable human gate), or **red** (missing document/field, failed rule, or inconsistency — each with the *exact resolving question*). Plus a **cross-document consistency** check on identity-critical fields (investigator, IND #, protocol #/version, title).
3. **Validate** (`validate.py`) — a small **rule engine** mapping document/field conditions to pass/fail + citation (e.g., "1572 must name the reviewing IRB", "ICF must carry the 8 basic elements of 21 CFR 50.25(a)", "serious SAEs require a human causality determination"). Rules **never** auto-resolve a gate.
4. **Compliance map** (`compliance.py`) — artifact → governing authority → validation results → the non-delegable human gate and its responsible role.

## The HARD LINE, enforced in code

`models.py` + `gates.py` make the non-delegable principle structural: a `Document` whose registry entry names a gate (informed consent, IRB approval, SAE causality, 1571/1572 signatures, financial-disclosure certification, submission-to-FDA, statistical sign-off) **cannot reach `final`** without a recorded human sign-off. Attempting it raises `GateViolation` — which is *correct behavior*, the engine refusing to cross the line. `gates.record_signoff` only **records** that a named human of the correct role executed the act (a Part-11 e-signature ceremony in production); it can never perform the act. The demo shows the engine refusing to sign a Form 1572, then finalizing only after the investigator's sign-off.

## Files

| File | Role |
|------|------|
| `registry/documents.json` | 60-document registry: citations, owner, required fields, gate |
| `registry/gates.json` | 8 non-delegable gates: responsible role + citation |
| `ossicro/models.py` | dataclasses, Document state machine, `GateViolation` |
| `ossicro/generate.py` | template fill + provenance (built-in template set) |
| `ossicro/check.py` | completeness ledger + consistency |
| `ossicro/validate.py` | rule engine |
| `ossicro/gates.py` | gate enforcement / human sign-off recording |
| `ossicro/compliance.py` | compliance map |
| `registry/rules.json` | the validation rules **as data**: each `{id, citation, strategy: deterministic\|provenance\|concept}` — the boundary doctrine made executable |
| `ossicro/rules.py` | rules-as-data loader; fails loudly at load on a missing citation or unknown strategy |
| `ossicro/review_port.py` | concept-reviewer **port**: `ConceptReviewer` protocol + deterministic offline stub + `validate_report` (drops any finding inside a verbatim-locked span or quoting absent text) |
| `ossicro/pipeline.py` | `run_check` composes deterministic rules → ledger → consistency → tripwire → concept reviewer → gate packet (cheapest-first, escalate-only; findings add reds/notes, never clear a gate) |
| `ossicro/register_linter.py` | **register tripwire** — fast, fallible, non-authoritative for voice (deterministic; `python -m ossicro.register_linter <file>`). A clean lint is not a voice claim; voice authority is the concept-based reviewer applying `docs/WRITING-PRINCIPLES.md`. Its chat-residue and (once built) 21 CFR 50.20 rules are genuine hard rules; the mannerism tier is a dated, non-blocking smoke signal |
| `registry/banned-constructions.json` | two-tier registry via a per-rule `tier` field: **hard-rule** (chat-transcript residue + 21 CFR 50.20 exculpatory-consent, `scope`-gated) hard-fails; **example** (dated mannerisms) is a non-blocking smoke signal that also seeds the concept-based voice reviewer's rubric |
| `ossicro/cli.py` | `python -m ossicro.cli demo` |
| `fixtures/sample_study.json` | synthetic single-patient (n-of-1) sponsor-investigator study — no real PHI |

This is a prototype of the design described in the wiki: [[generate-check-validate-engine]], [[completeness-ledger]], [[draft-provenance-model]], [[non-delegable-functions-and-gates]], [[data-model]]. Not medical, legal, or regulatory advice; every output is a draft for qualified human review.
