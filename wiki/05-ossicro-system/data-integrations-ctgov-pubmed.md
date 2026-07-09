---
title: "Data Integrations: ClinicalTrials.gov v2, PubMed, openFDA"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "ClinicalTrials.gov API v2 (public registry; FDAAA 801 / 42 CFR Part 11 data bank)"
  - "PubMed / NCBI E-utilities (public bibliographic + literature API)"
  - "openFDA (drug labels via SPL; FAERS adverse-event data)"
  - "HIPAA Privacy Rule — 45 CFR 164.512(i)(1)(ii) (outbound queries carry no PHI)"
  - "21 CFR 312.32 (safety literature supports, never replaces, causality judgment)"
tags: [ossicro/engine, ossicro/matching, cfr/312, cfr/11, usc/hipaa, lifecycle/safety, status/mixed]
aliases: ["Data Integrations", "External Data Sources", "CT.gov PubMed openFDA"]
updated: 2026-07-09
---

# Data Integrations: ClinicalTrials.gov v2, PubMed, openFDA

> [!authority] Governing authority
> Sources: [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api) (the FDAAA 801 registry under [42 CFR Part 11](https://www.ecfr.gov/current/title-42/part-11)), [PubMed / NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/), [openFDA](https://open.fda.gov/apis/) (drug labels and [FAERS](https://open.fda.gov/apis/drug/event/)). Privacy floor: [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512) — outbound queries carry **no PHI**. Safety frame: [21 CFR 312.32](https://www.ecfr.gov/current/title-21/section-312.32). Status: **Mixed** — the sources and their public terms are confirmed facts; how OSSICRO normalizes, caches, and interprets them (and the reliability limits it must flag) are interpretive engineering positions, marked inline.

This page specifies the external data layer that feeds three OSSICRO subsystems: the [[matching-engine]] (trial and therapy discovery, eligibility text), document drafting (auto-population of protocol, IB, and registration artifacts in the [[generate-check-validate-engine]]), and safety surveillance (supporting literature and adverse-event context for the [[safety-reporting-workflow]] and [[safety-clock-engine]]). Three public sources are integrated. None is a substitute for the primary regulatory record, and none carries PHI outbound.

## The PHI-egress invariant (confirmed)

> [!warning] Non-delegable
> Every call to CT.gov, PubMed, or openFDA is an **outbound query that must carry no protected health information**. Under [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512), the preparatory-review basis requires that **no PHI leave the covered-entity boundary**. Query construction therefore uses **de-identified or non-identifying terms only** (condition codes, drug names, biomarkers, phase/status filters) — never a patient identifier, never a free-text chart excerpt. The PHI-bearing side of matching (chart adjudication) stays local behind the [[privacy-state-machine]]; these integrations touch only the public knowledge side. This invariant is enforced in code, not documented as a hope.

## 1. ClinicalTrials.gov API v2

The [v2 REST API](https://clinicaltrials.gov/data-api/api) is the authoritative US trial registry surface — free, no registration wall — exposing structured study records under FDAAA 801 / [42 CFR Part 11](https://www.ecfr.gov/current/title-42/part-11) (see [[clinicaltrials-gov-registration]]).

**What OSSICRO consumes:**

- **Discovery filters** — condition, intervention, phase enum, overall status, study type, location/geography, sponsor.
- **Eligibility module** — inclusion/exclusion criteria (free text), sex, age bounds, healthy-volunteer flag. This is the input to computable-eligibility parsing in [[matching-eligibility-adjudication]].
- **Contacts & locations** — central and facility contacts, recruiting-status by site — used to route a candidate toward Mode A site enrollment.
- **Identifiers & metadata** — NCT number, protocol IDs, sponsor/collaborator, dates, and design fields used to de-duplicate and to link a registry record to its [[clinical-protocol-and-synopsis|protocol]] and [[investigators-brochure|IB]].

> [!interpretive] OSSICRO position
> The v2 API returns eligibility as **free text**, provides **no synonym or semantic expansion**, and has **no biomarker-to-trial reasoning**. Registry data quality is also uneven: criteria are authored by many sponsors to no fixed schema, statuses lag reality, and site-level recruiting flags are frequently stale. OSSICRO therefore treats CT.gov as a **discovery and eligibility-text source, not ground truth for enrollability** — the semantic/[[matching-mechanism-graph|mechanism]] layer sits on top for retrieval, and the [[matching-engine|retrieve→adjudicate]] step renders a cited, three-valued verdict rather than trusting a status flag. Records are cached with a fetch timestamp so staleness is visible and the [[regulatory-change-log|change-watch]] can re-pull.

## 2. PubMed / NCBI E-utilities

The [E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) provide programmatic access to PubMed and related NCBI databases (`esearch`, `esummary`, `efetch`, `elink`). OSSICRO uses them for two purposes:

- **Supporting evidence** — literature behind a candidate mechanism or therapy (for the mechanism-first matching direction and for the scientific-rationale sections a [[sponsor-investigator]] must draft in a [[pre-ind-and-ind-preparation|pre-IND package]] or an [[iis-request-workflow|IIS concept]]).
- **Safety literature** — published adverse-event and pharmacovigilance signal literature feeding safety surveillance context (see below).

Every retrieved reference is carried with its **PMID/DOI** so that any statement drafted from it in a downstream document is provenance-linked ([[draft-provenance-model]]) and independently verifiable. OSSICRO honors NCBI usage limits (rate limits; API-key tiering) and does not send PHI in query terms.

## 3. openFDA

[openFDA](https://open.fda.gov/apis/) exposes two datasets OSSICRO uses:

- **Drug labels (SPL)** — [structured product labeling](https://open.fda.gov/apis/drug/label/) for marketed drugs: indications, dosage, warnings, contraindications. Feeds the condition→therapy and medication→label matching directions, and supplies the [[investigators-brochure|IB]] "package-insert substitution" content when the investigational use is of a **marketed** drug ([21 CFR 312.55](https://www.ecfr.gov/current/title-21/section-312.55)).
- **FAERS adverse-event data** — the [FDA Adverse Event Reporting System](https://open.fda.gov/apis/drug/event/) as post-marketing safety context.

> [!interpretive] OSSICRO position
> FAERS is **spontaneous-report, non-denominator** data: it establishes neither incidence nor causation, is subject to reporting bias and duplication, and openFDA itself is not the system of record. OSSICRO surfaces FAERS strictly as **context** ("this event has been reported for this drug"), never as a rate and never as a causal statement. It is decision-support texture for a human safety review, not an input to any automated safety determination.

## Safety surveillance: support, never substitute (confirmed line)

> [!warning] Non-delegable
> Literature (PubMed) and spontaneous-report context (FAERS) may **inform** a human safety assessment. They do **not** make the [21 CFR 312.32](https://www.ecfr.gov/current/title-21/section-312.32) determination. **Seriousness, expectedness, and causality** — the judgments that turn an adverse event into a reportable SUSAR — are the [[medical-monitor]]'s non-delegable call (ICH E2A). The integration layer pre-populates and cites; the [[safety-clock-engine]] times; a qualified physician decides and signs. See [[pharmacovigilance-safety]] and [[safety-report-timelines-7-15-day]].

## Integration engineering (interpretive)

| Concern | OSSICRO approach |
|---------|------------------|
| **Normalization** | Map source vocabularies (MeSH, RxNorm/UNII, ICD/SNOMED where present) to a common concept layer feeding the [[matching-mechanism-graph]] |
| **Provenance** | Every ingested datum keeps source + record ID + fetch timestamp → the (datum → provenance → citation) triple in [[draft-provenance-model]] |
| **Caching & staleness** | Local cache with timestamps; the [[regulatory-change-log|living-compliance watch]] and re-pull cadence bound drift; stale flags shown to the reviewer |
| **Rate limits & availability** | Respect each API's published limits/keys; degrade to cached data, never to fabricated data — an unavailable source is reported as unavailable, not guessed |
| **Offline** | The [[offline-local-deployment|offline single-container deployment]] runs against a bounded local snapshot when a site has no outbound connectivity |
| **No fabrication** | If a datum is not returned, it is absent — the engine does not synthesize registry fields, PMIDs, or label text |

## Where the data goes

- → [[matching-engine]] and [[matching-eligibility-adjudication]] (discovery + eligibility text).
- → [[generate-check-validate-engine]] (auto-population of drafts, each span provenance-linked).
- → [[safety-reporting-workflow]] / [[safety-clock-engine]] (supporting evidence + FAERS context for human review).
- → [[communication-hub]] for routing of the resulting artifacts, after the applicable [[privacy-state-machine]] gate.

## Related
- [[matching-engine]]
- [[patient-trial-matching]]
- [[matching-eligibility-adjudication]]
- [[matching-mechanism-graph]]
- [[smart-on-fhir-integration]]
- [[privacy-state-machine]]
- [[safety-clock-engine]]
- [[pharmacovigilance-safety]]
- [[clinicaltrials-gov-registration]]
- [[draft-provenance-model]]
- [[regulatory-change-log]]

## Sources
- [ClinicalTrials.gov API v2 documentation](https://clinicaltrials.gov/data-api/api)
- [42 CFR Part 11 — ClinicalTrials.gov Data Bank (eCFR)](https://www.ecfr.gov/current/title-42/part-11)
- [NCBI E-utilities (Entrez Programming Utilities) — reference](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [openFDA APIs (overview)](https://open.fda.gov/apis/)
- [openFDA — Drug Label API (SPL)](https://open.fda.gov/apis/drug/label/)
- [openFDA — Drug Adverse Event API (FAERS)](https://open.fda.gov/apis/drug/event/)
- [45 CFR 164.512 — preparatory-to-research (eCFR)](https://www.ecfr.gov/current/title-45/section-164.512)
- [21 CFR 312.32 — IND safety reporting (eCFR)](https://www.ecfr.gov/current/title-21/section-312.32)
- [21 CFR 312.55 — Informing investigators / Investigator's Brochure (eCFR)](https://www.ecfr.gov/current/title-21/section-312.55)
