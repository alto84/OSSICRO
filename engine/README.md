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
| `ossicro/cli.py` | `python -m ossicro.cli demo` |
| `fixtures/sample_study.json` | synthetic single-patient (n-of-1) sponsor-investigator study — no real PHI |

This is a prototype of the design described in the wiki: [[generate-check-validate-engine]], [[completeness-ledger]], [[draft-provenance-model]], [[non-delegable-functions-and-gates]], [[data-model]]. Not medical, legal, or regulatory advice; every output is a draft for qualified human review.
