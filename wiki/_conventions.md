---
title: Wiki Conventions
section: _meta
status: confirmed
tags: [meta/conventions]
updated: 2026-07-09
---

# OSSICRO Wiki Conventions (Obsidian vault)

The `wiki/` folder is an **Obsidian vault** and the canonical source of truth for formatting. Every page follows these rules so the corpus stays consistent, portable, and machine-checkable.

## 1. YAML frontmatter (required on every page)

```yaml
---
title: "Human-readable page title"
section: "01-roles-responsibilities"     # the IA section folder
status: confirmed                         # confirmed | interpretive | mixed
governing_authority:                      # the binding law/guidance this page rests on
  - "21 CFR 312.50-312.59"
  - "ICH E6(R3) Section 5"
tags: [role/sponsor, cfr/312, gcp/e6r3]
aliases: []                               # optional alternate names for [[links]]
updated: 2026-07-09
---
```

`status` legend:
- **confirmed** — black-letter regulatory requirement, directly cited.
- **interpretive** — an OSSICRO design/thesis position (e.g., AI-drafted regulatory text, software-assisted monitoring boundary). Must be labelled and defended.
- **mixed** — page contains both; each interpretive claim is marked inline.

## 2. Page body structure

1. **Authority callout** immediately under the H1:
   ```
   > [!authority] Governing authority
   > 21 CFR 312.50-312.59 (sponsor responsibilities); ICH E6(R3) §5. Status: **Confirmed**.
   ```
2. **Lede** — 2-4 sentences in regulatory register orienting the reader.
3. **Body** — sections with `##`/`###`. Regulatory register throughout: precise, cited, non-promotional. Comparable to a reference regulatory document.
4. **Non-delegable gates** (where relevant) in a warning callout:
   ```
   > [!warning] Non-delegable
   > Causality/expectedness determination triggering a 15-day IND safety report is the sponsor's judgment (21 CFR 312.32). OSSICRO drafts; a qualified human owns and signs.
   ```
5. **Interpretive positions** in their own callout:
   ```
   > [!interpretive] OSSICRO position
   > ... (clearly separated from black-letter requirements)
   ```
6. **## Related** — near the bottom, a bullet list of `[[wikilinks]]` to adjacent pages.
7. **## Sources** — external citations as markdown links (eCFR / FDA / ICH / DOI), and links to any downloaded local original under `../sources/...`.

## 3. Internal links — Obsidian wikilinks

- Link by filename stem: `[[sponsor]]`, `[[transfer-of-regulatory-obligations-toro]]`.
- With display text: `[[sponsor-investigator|the sponsor-investigator]]`.
- Link generously — every role/document/workflow mentioned that has its own page gets a wikilink on first mention. A `[[link]]` to a not-yet-authored page is acceptable (it marks intended coverage).

## 4. External citations

- Regulations: link to eCFR (`https://www.ecfr.gov/...`) or Cornell LII; cite as `21 CFR 312.32(c)(1)`.
- ICH: cite guideline + section, link the ICH database PDF.
- FDA guidance/forms: link the FDA page; where a local original is stored, also link `../sources/...`.
- Publications: cite with PMID/DOI.

## 5. Tag taxonomy

`role/{sponsor,investigator,sponsor-investigator,cro,irb,dsmb,monitor,pharma,medical-monitor,biostatistician,fda}` ·
`cfr/{11,50,54,56,312}` · `usc/*` · `ich/{e6r3,e8r1,e9,e2a,e2b,e2d,e2f,e3,m11}` ·
`fda-form/{1571,1572,3454,3455,3500a,3926,3674}` ·
`lifecycle/{feasibility,ind,irb,activation,conduct,safety,annual,closeout,retention,expanded-access,iis}` ·
`entity/*` · `ossicro/{engine,micro-cro,matching,gating,part11,ai-credibility}` ·
`status/{confirmed,interpretive}`

## 6. Filenames

Kebab-case stems matching the information architecture in [[INDEX]]. One concept per page. Section folders: `00-overview/`, `01-roles-responsibilities/`, `02-lifecycle/`, `03-documents/`, `04-coordination/`, `05-ossicro-system/`, `references/`.

## 7. Not legal/medical/regulatory advice

Every page is reference material and produces DRAFT artifacts for qualified human review. Non-delegable regulated functions are surfaced and gated, never automated (see [[non-delegable-functions-and-gates]]).
