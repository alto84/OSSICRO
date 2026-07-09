---
title: "Regulatory Change Log — Living-Compliance Change Watch over the Citation Graph"
section: "references"
status: mixed
governing_authority:
  - "eCFR (official, continuously updated edition of the CFR)"
  - "Federal Register (rulemaking and guidance-availability notices)"
  - "ICH guidelines database (Step 4 texts and revisions)"
  - "FDA guidance portal (final/draft status of guidance documents)"
tags: [ossicro/engine, ossicro/gating, ich/e6r3, ich/m11, cfr/312, cfr/11, status/interpretive]
aliases: ["Change Log", "Regulatory Change Watch", "Living Compliance"]
updated: 2026-07-09
---

# Regulatory Change Log — Living-Compliance Change Watch over the Citation Graph

> [!authority] Governing authority
> This page's authority *is the watched corpus*: the [eCFR](https://www.ecfr.gov/) (the continuously updated official CFR edition), the [Federal Register](https://www.federalregister.gov/) (rules and guidance-availability notices), the [ICH guidelines database](https://database.ich.org/), and the [FDA guidance search portal](https://www.fda.gov/regulatory-information/search-fda-guidance-documents). Status: **Mixed** — the statuses recorded below are confirmed facts as of their as-of dates; the change-watch process itself is an OSSICRO design position.

A regulatory reference that is not maintained is a regulatory hazard: the corpus OSSICRO rests on is in **active motion** (ICH E6(R3) newly FDA-adopted with no US compliance date; ICH M11 newly final; the FDA AI-credibility guidance still draft), and a clinician acting on a stale citation can inherit a real defect into a real study. The regulatory change log is the wiki's anti-rot mechanism: a **change watch** that diffs the watched sources on a cadence, maps every detected change through the **citation-dependency graph** to the wiki pages, document templates, and validation rules that cite the changed authority, and records the disposition — with a **human curator confirming every change** before anything propagates. This page is both the specification of that process and the log itself. It operationalizes rule 4 of [[index|the citation conventions]] ("date every status claim; never silently upgrade a draft") and closes the loop that [[compliance-mapping]] opens: if every artifact carries its citations, then a changed citation identifies every artifact that must be re-verified.

## Watched sources and cadence

| Source | What is watched | Mechanism | Cadence |
|---|---|---|---|
| [eCFR](https://www.ecfr.gov/) | Every CFR section in [[cfr-citation-map]] (21 CFR 11, 50, 54, 56, 312; 45 CFR 46, 160/164; 42 CFR 11) | Section-level content retrieval and diff against the stored snapshot (the eCFR publishes point-in-time versions) | Weekly |
| [Federal Register](https://www.federalregister.gov/) | Proposed/final rules and guidance-availability notices on relevant dockets (e.g., FDA-2023-D-1955 E6(R3); FDA-2024-D-4689 AI credibility; FDA-2015-D-1484 sponsor-investigator IND) | [FR API](https://www.federalregister.gov/developers/documentation/api/v1) queries by docket and agency/topic | Weekly |
| [ICH database](https://database.ich.org/) | Step/revision status of every guideline in [[ich-guideline-map]] (E6, E8, E9, E2A/E2B/E2D/E2F, E3, M11) | Page and document-version checks; checksum of guideline PDFs | Monthly |
| [FDA guidance portal](https://www.fda.gov/regulatory-information/search-fda-guidance-documents) | Final/draft status and withdrawal of every guidance in [[fda-guidance-map]] | Search-result and document-page diff; checksum of guidance PDFs | Monthly |
| [FDA forms](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-forms-and-instructions) | Edition dates and OMB renewals of every form in [[fda-form-index]] (1571, 1572, 3454/3455, 3500A, 3926, 3674) | Form-page and PDF checksum | Monthly |
| ClinicalTrials.gov / NIH policy | Registration/results requirements (FDAAA 801, 42 CFR Part 11); API deprecations affecting [[data-integrations-ctgov-pubmed]] | Release notes and policy pages | Monthly |

Detection is automatable; **interpretation is not** — a diff says *something changed*, never *what it means for a trial*. That asymmetry drives the lifecycle below.

## The citation-dependency graph

Every wiki page declares its authorities in frontmatter and its `## Sources`; every validation rule in the [[generate-check-validate-engine]] carries its authority key; every template records the authorities it instantiates; and the maps in this section ([[cfr-citation-map]], [[ich-guideline-map]], [[fda-guidance-map]], [[fda-form-index]]) record the reverse index — *which pages cite which authority*. Together these form a queryable graph: **authority → {pages, templates, validation rules, generated-artifact manifests}**. When the watch detects a change to `21 CFR 312.32(c)`, the graph returns, mechanically, every page (e.g., [[safety-report-timelines-7-15-day]], [[ind-safety-report]], [[safety-clock-engine]]), every safety-report template, and every deadline-computation rule that must be re-verified — so the review burden of a change is bounded and enumerable instead of "re-read everything."

## Change-item lifecycle

| Stage | Actor | Output |
|---|---|---|
| 1. **Detected** | Watch job | Diff record: source, authority, before/after, detection date |
| 2. **Triaged** | Curator (human) | Classification: substantive / editorial / false positive; urgency |
| 3. **Impact-mapped** | Graph query + curator | The enumerated set of affected pages, templates, validation rules |
| 4. **Confirmed** | Curator (human) | The interpretation: what the change means, what edits are required |
| 5. **Propagated** | Editors / engine maintainers | Versioned edits to each affected item, each citing this log entry |
| 6. **Verified** | Second reviewer | Confirmation that every impact-mapped item was addressed or explicitly deferred |

Two standing rules from [[index|the citation conventions]] bind stages 4–5: a **draft guidance that finalizes is never silently upgraded** — the finalization is a logged change item with its own review — and every status claim in the corpus carries its as-of date so a reader can tell what the page knew and when.

> [!warning] Non-delegable
> The watch **detects**; a qualified human **decides**. Whether a regulatory change is substantive, what it requires of a live study, and whether a validation rule's logic must change are regulatory judgments owned by the human curator (and, for anything touching a live study's obligations, the accountable [[sponsor-investigator]] or [[micro-cro-accountable-layer|Micro-CRO]] with qualified regulatory counsel where warranted). The change watch never auto-edits a page, template, or rule — least of all a rule that guards a gate in [[non-delegable-functions-and-gates]]. An unreviewed diff is a *flag*, not a *fact about compliance*.

> [!interpretive] OSSICRO position
> Living compliance is a durable moat precisely because it is unglamorous: any actor can copy a snapshot of this wiki; keeping a citation corpus *continuously true* against four moving sources, through a disciplined human-confirmed process, is an accumulating asset that decays immediately when neglected. It is also a safety property — the failure mode it prevents (a clinician relying on a superseded requirement) is exactly the class of harm this project exists to avoid. The cadence and mechanisms above are design choices, not requirements; what is non-optional is that every status claim in the corpus be dated and every change be human-confirmed.

## The log

Entries in reverse-chronological order of last status change. "Affected" lists principal wiki dependencies; the full impact map is the graph query. All statuses **as of 2026-07-09**.

| # | Authority | Status (as of 2026-07-09) | Watching for | Affected (principal) | Disposition |
|---|---|---|---|---|---|
| CL-008 | **ICH M11** (Clinical Electronic Structured Harmonised Protocol) | Final template dated 2025-11-19; FDA implementation in progress | FDA adoption notice; template/technical-spec revisions | [[clinical-protocol-and-synopsis]], protocol templates, [[generate-check-validate-engine]] protocol schema | Open — corpus built to M11 as the forward standard |
| CL-007 | **ICH E6(R3)** (GCP) | Step 4 adopted Jan 2025; EU effective 2025-07-23; FDA final guidance published 2025-09-09 (FR docket FDA-2023-D-1955); **no US compliance date set** | A US compliance-date announcement; Annex 2 progress | [[document-catalog]], [[startup-tmf-checklist]]/[[conduct-tmf-checklist]]/[[closeout-tmf-checklist]], [[risk-based-monitoring-e6r3]], [[monitoring-plan]], essentially all GCP-citing pages | Open — corpus built to R3 with E6(R2) §8 cross-numbering retained as bridge |
| CL-006 | **FDA draft guidance — AI to Support Regulatory Decision-Making** (FDA-2024-D-4689) | Draft, published 2025-01-07; comment period closed 2025-04-07; **still draft** | Finalization or revision | [[part-11-and-ai-credibility]], [[claude-sdk-ai-in-the-loop]], [[generate-check-validate-engine]], [[matching-eligibility-adjudication]] (COU risk-tiering argument) | Open — draft status flagged in-page everywhere the 7-step framework is cited |
| CL-005 | **FDA final guidance — Conducting Clinical Trials With Decentralized Elements** | Final, 2024-09-18 (finalizes May 2023 draft) | Revision; related FDORA §3606 actions | [[regulatory-landscape]], remote-conduct aspects of [[conduct-and-monitoring]], [[two-modes-site-vs-sponsor-investigator]] | Stable — monitored |
| CL-004 | **FDA guidance — Data Monitoring Committees** | 2006 guidance + 2024 update; controlled status in [[fda-guidance-map]] | Status changes; charter-expectation deltas | [[dsmb-dmc]], [[dsmb-charter]], [[dsmb-workflow]] | Open — verify current final/draft status before citing the 2024 document as final |
| CL-003 | **FDA draft guidance — INDs Prepared and Submitted by Sponsor-Investigators** (FDA-2015-D-1484) | Draft since May 2015; never finalized | Finalization or withdrawal | [[sponsor-investigator]], [[pre-ind-and-ind-preparation]], [[ind-application-312-23]] | Open — most on-point FDA document for the core user; draft status flagged |
| CL-002 | **21 CFR Parts 50/56 vs. revised Common Rule** harmonization rulemaking | FDA alignment actions partial (2018–2023); further harmonization anticipated under 21st Century Cures §3023 | Proposed/final rules on FDA dockets aligning Parts 50/56 with 45 CFR 46 | [[informed-consent-form]], [[irb-iec]], [[single-irb-mandate-and-central-irbs]], [[irb-submission-and-approval]] | Open — dual-regime pages state both frameworks explicitly |
| CL-001 | **eCFR watch baseline** — 21 CFR 11, 50, 54, 56, 312; 45 CFR 46, 160/164; 42 CFR 11 | Snapshot taken 2026-07-09; no undispositioned diffs | Any amendment to a mapped section | Everything via [[cfr-citation-map]] | Baseline established |

### Log-entry conventions

Each entry carries: an immutable ID (`CL-###`), the authority (cited per [[index|the conventions]]), the dated status, the watched-for event, the principal affected dependencies (with the graph as the complete record), and the disposition (`Baseline` / `Open` / `Stable — monitored` / `Closed`, with closure requiring the stage-6 verification record). When a change item closes, the entry is retained — the log is append-only history, not a to-do list — and every page edited in consequence cites the entry ID in its change note.

## Related
- [[index|References — How to Cite in OSSICRO]]
- [[cfr-citation-map]]
- [[ich-guideline-map]]
- [[fda-guidance-map]]
- [[fda-form-index]]
- [[bibliography]]
- [[compliance-mapping]]
- [[confirmed-vs-interpretive]]
- [[regulatory-landscape]]
- [[generate-check-validate-engine]]
- [[non-delegable-functions-and-gates]]
- [[risks-and-limitations]]
- [[roadmap]]

## Sources
- [eCFR — Electronic Code of Federal Regulations (official, continuously updated)](https://www.ecfr.gov/)
- [eCFR — Recent Changes](https://www.ecfr.gov/recent-changes)
- [Federal Register](https://www.federalregister.gov/) · [Federal Register API v1](https://www.federalregister.gov/developers/documentation/api/v1)
- [ICH Guidelines Database](https://database.ich.org/)
- [FDA — Search for FDA Guidance Documents](https://www.fda.gov/regulatory-information/search-fda-guidance-documents)
- [FDA — E6(R3) Good Clinical Practice guidance page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
- [FDA — Considerations for the Use of Artificial Intelligence To Support Regulatory Decision-Making for Drug and Biological Products (draft, Jan 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological)
- [FDA — Conducting Clinical Trials With Decentralized Elements (final, Sept 2024)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/conducting-clinical-trials-decentralized-elements)
- [ICH M11 — Clinical Electronic Structured Harmonised Protocol (CeSHarP)](https://database.ich.org/sites/default/files/ICH_M11_Guideline_Step4_2025.pdf)
- [FDA — IND Forms and Instructions](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-forms-and-instructions)
