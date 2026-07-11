# OSSICRO MVP: Route 3926 (single-patient expanded access)

Reader: a developer or reviewer opening this project for the first time.

This directory holds a working full-stack prototype for the single-patient expanded-access pathway (21 CFR 312.310, Form FDA 3926). The backend is pure Python standard library and sits on top of the OSSICRO engine in `engine/`. The frontend is one interactive page. The prototype serves three audiences: the physician preparing the request, the FDA reviewer who receives it, and the manufacturer who acts on the letter-of-authorization request.

## Run it

```bash
cd OSSICRO
python app/server.py
```

The server uses only the standard library, so there is nothing to install. It listens on http://127.0.0.1:8765. Open that address in a browser and follow the flow: start a case, fill the intake, review the completeness ledger, then open the package view (regulator view, manufacturer view, and export).

Everything the software produces is a draft for qualified human review. Amber items in the ledger name the human who must act. The software does not submit or sign anything.

## What it does

**Intake.** 55 fields. Each field is labeled with the regulation that governs it and mapped to the documents it feeds.

**Generate.** 8 expanded-access documents: Form 3926, the treatment plan, a cover letter, the manufacturer letter-of-authorization (LOA) request, the IRB concurrence request, the informed-consent form, and a drug-accountability shell. Every filled span carries a provenance stamp recording which intake field it came from. Missing data does not stop generation; it becomes a red item in the ledger together with the exact question that would resolve it.

**Check.** `pipeline.run_check` produces the green/amber/red completeness ledger, cross-document consistency checks, and the gate packet for the three acts the software must never perform itself: `submission-to-fda`, `informed-consent`, and `irb-approval`. If a gate is unmet, the engine raises `GateViolation` rather than proceeding without it.

The check's concept (voice) review runs the **offline deterministic stub by default — nothing leaves the machine**. A deployment may opt in to the live model-backed reviewer by setting `OSSICRO_LIVE_CONCEPT_REVIEW` to an affirmative value (with `ANTHROPIC_API_KEY` present); that sends rendered document text to the Anthropic API and is a deployment decision with documented preconditions (BAA or de-identified projection, zero-retention configuration, and the named human recorded in the deployment log) — see [`docs/deployment/AI-REVIEW-PRECONDITIONS.md`](../docs/deployment/AI-REVIEW-PRECONDITIONS.md). Every live review writes one `ai_review` audit record (model, version, doc ids, finding count, destination — never text), the check screen discloses which reviewer ran, and `POST /api/case/{id}/review-disposition` records the named human's accepted/dismissed judgment on each finding (escalate-only; it never changes the ledger).

**Assemble.** The regulator-facing submission follows the eCTD module map: Module 1 holds the 3926, the cover letter, and the LOA; Module 5 holds the treatment plan; Modules 3 and 4 plus the investigator brochure are cross-references to the manufacturer's IND via the LOA. Assembly also produces a SHA-256 hash manifest and the manufacturer LOA packet. `submission_ready` stays False while any gate is unmet. The engine only assembles; filing is a human act.

**Clocks.** The deadlines differ between emergency and non-emergency use: the 15-working-day written submission (312.310(d)), the 5-working-day IRB notification (56.104(c)), and the 30-calendar-day IND wait (312.40(b)(1)).

## API

All endpoints are same-origin; the frontend consumes them. Several endpoints require a "committed profile" first. That is a project term: a named human commits the intake (`profile/commit`), the server records a hash of it, and generation is allowed only while the intake still matches that hash. This is invariant INV-3 in the engine; endpoints under it return 409 when the condition fails.

### Case setup and intake

- `GET /api/route/3926/schema` returns the route's field schema.
- `POST /api/case` creates a case.
- `GET /api/case/{id}` returns full case state: intake, sign-offs, revision counters, profile, and audit trail.
- `POST /api/case/{id}/intake` saves intake values. Any key outside the route schema is rejected.
- `POST /api/case/{id}/fhir/import` extracts field proposals from a FHIR bundle (or a built-in sample). It only proposes values; a human must accept them before they enter the intake.

### Profile commitment

- `POST /api/case/{id}/profile/commit` commits the intake profile under a named actor. The server stores only hashes of the values; the raw values are not written to the profile record (invariant INV-8).
- `POST /api/case/{id}/profile/confirm` records named per-field re-confirmation after the intake changes; once every pending field is confirmed, the profile recommits under a new hash.

### Generation and checking

- `POST /api/case/{id}/generate` generates the route documents. Requires a committed, current profile.
- `GET /api/case/{id}/check` returns the ledger (each question carries its field id), the clocks, and staleness flags.
- `POST /api/case/{id}/signoff` records that a named human performed a gate act outside the software; the role must match the gate. The sign-off is a record of a human act, and the engine's `has_signoff` check is what moves an amber item to green.
- `POST /api/case/{id}/match` runs a registry search. Requires a committed profile. Only de-identified predicates leave the case, through the egress gateway, to a mock registry adapter; live queries are disabled. The response lists which criteria matched and which did not. It does not compute a match score; the tool organizes registry results and makes no recommendation.

### Output

- `GET /api/case/{id}/package` returns a manifest over all route documents plus a package digest.
- `GET /api/case/{id}/form3926.pdf` returns the filled Form 3926 with a draft watermark. Requires a committed profile; the watermark stays until the gates clear.
- `GET /api/case/{id}/form3926.fdf` returns draft-marked FDF fill data under the same gate. The PDF field-name map is unverified; see `ossicro.pdf_3926.FDF_3926_FIELD_MAP`.
- `POST /api/case/{id}/export` with `{actor, format: "pdf"|"fdf"}` is the explicit export act: it returns the same draft bytes under the same committed-profile gate, and writes one `export` audit record naming the human and the format. One email separates an exported draft from a submission, so the export is on the record. The frontend's download buttons use this endpoint; the GET endpoints remain for direct browser use.

### Other personas

The manufacturer, the patient, and the coordinating physician each get a deliberately narrow view.

- `POST /api/case/{id}/release` lets a named human release a case to the manufacturer. It requires a committed profile and documents generated from it, writes one audit record, and is refused otherwise. Cross-persona visibility only happens through an explicit release; there is no default sharing.
- `GET /api/manufacturer/inbox` shows released cases only, as a snapshot taken at release time: the LOA request, the drug and indication, and the coded patient identifier. The supply decision and the LOA signature belong to the manufacturer alone (FDCA 561A); the software does not model either as an action it takes.
- `POST /api/case/{id}/patient-link` lets a named human mint and share an opaque status token for the patient. The token is the only way to reach the patient view; case ids do not work there, and cases cannot be enumerated.
- `GET /api/patient/{token}` is a read-only plain-language status page, written to the 21 CFR Part 50 standard of information "understandable to the subject": the current stage, what remains, and the standing draft notice. It exposes no case id and no clinical detail beyond the coded identifier and drug name. An unknown token returns 404 and is indistinguishable from any other not-found.
- `POST /api/case/{id}/promote` records the legal transition from preparatory review to enrollment (invariant INV-5); the HIPAA disclosure basis changes at this step. It requires a committed profile, a named actor, and a recorded `legal_basis`. It starts the post-enrollment sponsor-investigator obligation clocks (21 CFR 312.32, 312.310(d), 312.33) and returns the obligations checklist. Each clock is either computed from recorded dates or shown as not yet started; the engine does not invent dates. A repeat promote is refused with 409.
- `GET /api/cro/board` is a read-only status board summarizing every case's stage, for the physician coordinating multiple cases. It offers no actions; per-persona authentication is deferred (INV-7).
- `GET /` serves the frontend.

## Boundaries

Case data is stored on disk at `app/data/cases/{id}.json`. The store holds no real PHI; patients appear as coded identifiers only. Committed-profile hashes are HMAC-keyed under a server-side secret (`app/data/secret.key`, created on first run, never committed) so a hash of an enumerable value cannot be reversed offline. The software is not medical, legal, or regulatory advice. The submission spec that governs this MVP is `docs/route-3926-submission-spec.md`.

The server is a single-user loopback pilot and enforces that at startup: `main()` refuses to bind a non-loopback host, because no persona authentication exists (INV-7). The override (`OSSICRO_ALLOW_NONLOCAL_BIND=1`) additionally requires a configured authentication backend, which this build does not have, so the override cannot currently succeed. Everything a deployment must satisfy before any non-synthetic case — covered-entity boundary, encryption at rest, BAA inventory, retention, and the INV-7/keyed-hash preconditions — is in [`docs/deployment/DEPLOYMENT-COMPLIANCE.md`](../docs/deployment/DEPLOYMENT-COMPLIANCE.md).

At release and registry-match time, a naive deterministic lint sweeps the free-text intake fields for identifier-shaped content (SSN-shaped values, dates in narrative, date-of-birth labels, "name:"-labeled name pairs) and returns escalate-only warnings naming the field — never the matched text, never a block, never a rewrite.

Clock arithmetic has a single source. `ea_generators.py` delegates all working-day and deadline computation to `engine/ossicro/clocks.py`, and two test classes in `engine/tests/test_ea_features.py` (`ClockReconciliationTests` and `ComputeClocksCanonicalTests`) verify that the two stay in agreement.
