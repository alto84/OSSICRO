# OSSICRO MVP — Route-3926 (single-patient expanded access)

A functioning full-stack prototype: a stdlib backend over the OSSICRO engine and an interactive frontend, for the single-patient expanded-access pathway (21 CFR 312.310, Form FDA 3926). It is organized around **what the FDA reviewer receives and what the manufacturer acts on** — not just the physician's documents.

## Run it

```bash
cd OSSICRO
python app/server.py        # serves on http://127.0.0.1:8765  (pure stdlib, no pip install)
```

Open **http://127.0.0.1:8765** in a browser and walk: **Start a case → Intake → Completeness ledger → Package** (Regulator view + Manufacturer view → Export). Everything produced is a **DRAFT for qualified human review**; amber items name the human who must act; nothing is submitted or signed by the software.

## What it does

- **Intake** — 55 fields, each labeled with its governing citation, mapped to the documents it feeds.
- **Generate** — 8 expanded-access documents (Form 3926, treatment plan, cover letter, manufacturer LOA request, IRB concurrence request, ICF, drug-accountability shell), every filled span provenance-stamped; missing data becomes an explicit red ledger item with the exact resolving question.
- **Check** — the green/amber/red completeness ledger + cross-document consistency + the non-delegable gate packet (`submission-to-fda`, `informed-consent`, `irb-approval`), via `pipeline.run_check`.
- **Assemble** — the regulator-facing submission (eCTD module map: Module 1 = 3926 + cover + LOA; Module 5 = treatment plan; Modules 3/4 + IB = cross-references to the manufacturer IND via the LOA), a SHA-256 hash-manifest, and the manufacturer LOA packet. `submission_ready` is False while any gate is unmet — the engine assembles, it never files.
- **Clocks** — emergency vs non-emergency: 15-working-day written submission (312.310(d)), 5-working-day IRB notification (56.104(c)), 30-calendar-day IND wait (312.40(b)(1)).

## API (same-origin; the frontend consumes these)

`GET /api/route/3926/schema` · `POST /api/case` · `POST /api/case/{id}/intake` · `POST /api/case/{id}/generate` · `GET /api/case/{id}/check` · `GET /api/case/{id}/package` · `GET /` (frontend)

## Boundaries

Cases are held in memory; no real PHI. Not medical, legal, or regulatory advice. The submission spec that governs this MVP is `docs/route-3926-submission-spec.md`. Known cleanup: `ea_generators.py` carries an inline clock; it should be reconciled to the canonical `engine/ossicro/clocks.py`.
