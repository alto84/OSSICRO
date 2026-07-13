# OSSICRO — Open Source Sponsor-Investigator CRO

**A compliant, low-cost path for a physician who has the right patient but no way to run the trial.**

OSSICRO is open-source software that assembles, checks, and coordinates the FDA-grade regulatory documentation a clinician needs to get an investigational drug to a single patient — the expanded-access pathway (21 CFR 312.310, Form FDA 3926) — and, more broadly, to run an investigator-initiated study. It drafts every required document from the patient's intake, checks each one against the exact regulation that governs it, and **refuses, in code, to perform the acts only a human may perform** (consent, IRB judgment, causality, signing, submitting).

> Built for **Built with Claude: Life Sciences** (Anthropic × Gladstone Institutes), **Builder Track**. Built entirely with **Claude Code**, July 2026. MIT-licensed. Repo: **https://github.com/alto84/OSSICRO**.

## See it in 60 seconds

No dependencies — pure Python standard library.

```bash
python app/server.py            # serves the dashboard at http://127.0.0.1:8765
python tools/smoke_e2e.py       # in a second terminal: drives all 22 endpoints green
```

Open `http://127.0.0.1:8765/` and walk the physician flow, one button at a time:

1. **Start a case** → **Load example case** (the synthetic epilepsy patient).
2. **Save & continue**, then type your name and **Commit profile** — a named human commits the input of record (the INV-3 gate; nothing is drafted from unconfirmed data).
3. **Generate documents** — the 8 expanded-access drafts appear with the green/amber/red **completeness ledger**, each item mapped to its CFR citation.
4. **Assemble package**, then open the filled **Form 3926 PDF**.
5. Click **Micro-CRO** in the header, then **Try to transfer to CRO** on *informed consent* — OSSICRO refuses it, in code, with the citation.

**▶ Demo video: _[link on submission]_**

## The user, and the wall

A neurologist has a patient with refractory epilepsy who could benefit from an investigational drug — but there is no open trial. To treat that one patient legally, she must become an FDA sponsor-investigator and produce grade-A regulatory documentation. Standing up a compliant path is a median **~9.4 months and $30–200K** of coordination labor; commercial CROs broker that friction and monetize it. Most physicians simply give up.

OSSICRO makes the coordination labor cheap and the paperwork correct, so a clinician can operate as a **sponsor-investigator** (21 CFR 312.3) without a commercial intermediary — while a thin **micro-CRO** layer supplies *only* the legally-accountable functions that must sit with a real entity.

## What's in the box (current state)

| Area | State |
|---|---|
| **Dashboard** (`app/static/index.html`) | A working single-page clinician app served at `/`. Physician, FDA-reviewer, manufacturer, patient, and coordinator views. The full flow runs end to end. |
| **Engine** (`engine/ossicro/`) | 25 pure-stdlib modules — generation with per-field provenance, the green/amber/red completeness ledger, cross-document consistency, the federal working-day clock engine, the de-identified egress gateway, the FHIR intake mapper, the Form-3926 PDF, and the micro-CRO TORO generator. **593 tests pass.** |
| **Governance** | Enforced in code, not just documented: non-delegable gates (HC1), no fabrication (HC2), computed statutory clocks (HC3), provenance + a SHA-256 manifest (HC4), Part-11 AI attribution (HC5), an append-only hash-chained audit log, the commit-profile hard gate (INV-3), and no-PHI-egress (INV-8). See [`docs/OSSICRO-CONSTITUTION.md`](docs/OSSICRO-CONSTITUTION.md). |
| **Regulatory wiki** (`wiki/`) | 131 cross-linked, cited pages — roles, lifecycle, the essential-document set, coordination, and the micro-CRO model. Cited to 21 CFR / ICH E6(R3) / FDA guidance and verified against primary sources. |
| **Templates** (`templates/`) | 61 regulatory document templates across 17 categories (IND, IRB, safety, monitoring, consent, contracts, expanded access, …). |
| **Verification** | `tools/smoke_e2e.py` drives all 22 API endpoints; `docs/HANDOFF.md` is the reviewer's guide. |

## The one hard rule

OSSICRO produces **DRAFTS** for qualified human review. It never performs a **non-delegable** act: obtaining informed consent (21 CFR Part 50), IRB/IEC judgment (Part 56), safety/causality determination (312.32), or signing/submitting to FDA. Each is a **gate**: a step owned by a named human where the software stops and waits. This is enforced in code — the micro-CRO's TORO generator, for example, will refuse to draft a transfer of informed consent to a CRO, because that obligation is non-delegable under Part 50.

## How it was built with Claude Code

OSSICRO is a demonstration of what a domain expert plus Claude Code can build in a week:

- **Multi-agent authoring** — a 24-agent scrape assembled the cited source library; **30 agents authored the regulatory wiki** against a shared style constitution.
- **Adversarial self-review loops** — most subsystems were *built → reviewed by an independent adversarial agent → revised → re-reviewed* before landing, and a full overhaul closed 15 major findings with a written root-cause analysis (`docs/overhaul/`).
- **Governance as code** — a small enumerated set of hard constraints, each justified and enforced at a concrete point in the engine, not left as prose.
- **Citations verified against primary sources** — when a review flagged a Form-1571 field number, it was checked against the actual FDA instructions PDF (the original was right) rather than "corrected" on a guess.

## Repository layout

| Path | Contents |
|---|---|
| `app/` | The backend (`server.py`, pure stdlib) and the dashboard (`static/index.html`) |
| `engine/ossicro/` | The generate / check / validate / govern engine (25 modules) |
| `engine/registry/` | Document, gate, route, claim, and sponsor-obligation registries (JSON) |
| `engine/tests`, `app/tests` | 593 tests |
| `wiki/` | The regulatory knowledge base (Obsidian vault; cited, cross-linked) |
| `templates/` | 61 regulatory document templates |
| `docs/` | The Constitution, submission spec, deployment-compliance, `HANDOFF.md`, and the build/QA history |
| `tools/` | `smoke_e2e.py` (end-to-end check), `prose_lint.py`, the attestation worksheet |
| `sources/` | Local originals of cited public documents (CFR / ICH / FDA), gitignored |

## Boundaries and honesty

This is a **prototype over synthetic cases**, not a production or validated regulatory tool. The server is a **single-user loopback pilot** and program-enforces it — it refuses to bind a non-loopback host because no authentication backend exists yet (INV-7). Everything a real deployment must satisfy first — covered-entity boundary, encryption at rest, BAA inventory, retention, keyed profile hashes — is in [`docs/deployment/DEPLOYMENT-COMPLIANCE.md`](docs/deployment/DEPLOYMENT-COMPLIANCE.md). Regulatory content is researched and cited but **must be independently verified** before any real use. Not medical, legal, or regulatory advice.

## License

MIT (see `LICENSE`), with the non-delegable-function notice appended.
