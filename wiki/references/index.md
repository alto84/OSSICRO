---
title: "References — How to Cite in OSSICRO"
section: "references"
status: confirmed
governing_authority:
  - "21 CFR (binding regulations, cited per eCFR current edition)"
  - "ICH guidelines (non-binding, as adopted by FDA)"
  - "FDA guidance documents (non-binding; final vs. draft status controlled)"
tags: [status/confirmed, ossicro/engine, ossicro/gating]
aliases: ["citation conventions", "how to cite"]
updated: 2026-07-09
---

# References — How to Cite in OSSICRO

> [!authority] Governing authority
> This page governs the citation register of the OSSICRO wiki itself. The authorities it teaches you to cite are: the Federal Food, Drug, and Cosmetic Act and Public Health Service Act (statute); 21 CFR, 42 CFR, and 45 CFR (binding regulation); ICH guidelines as adopted by FDA; and FDA guidance documents (non-binding). Status: **Confirmed** (these are conventions, but the authority hierarchy they encode is black-letter administrative law).

Every claim in this wiki that a clinician might act on must trace to a specific, current, verifiable authority. This page defines how citations are written, how binding and non-binding sources are distinguished, and how citation rot is prevented. It is the operating manual for the `## Sources` section of every page and for the citation-carrying manifest in [[compliance-mapping]]. A wrong citation in a regulatory document is not a typo — it is a defect a real study can inherit.

## 1. The hierarchy of authority

Cite the highest applicable authority, and never present a lower tier as if it bound like a higher one.

| Tier | Authority | Force | Example |
|---|---|---|---|
| 1 | **Statute** (FDCA, PHS Act, U.S. Code) | Binding law | 21 U.S.C. § 355(i); 42 U.S.C. § 282(j) |
| 2 | **Regulation** (CFR) | Binding law (force and effect of statute) | 21 CFR 312.32(c)(1)(i) |
| 3 | **Federal Register rulemaking** (final-rule preambles) | Binding as promulgated; preamble is authoritative interpretation | 75 FR 59935 (Sept. 29, 2010) |
| 4 | **ICH guidelines as adopted by FDA** | Non-binding; states FDA's current thinking | ICH E6(R3) § 3.16.1 |
| 5 | **FDA guidance (final)** | Non-binding; states current thinking | eConsent Q&A (Dec. 2016) |
| 6 | **FDA guidance (draft)** | Non-binding and *not yet* current thinking; may change | AI credibility draft (Jan. 2025) |
| 7 | **Institutional practice / published precedent** | Persuasive only | Vanderbilt V-CAP (PMC3767144) |

Tiers 4–7 never satisfy a requirement that a tier 1–3 source imposes; they explain *how* to satisfy it. When a wiki page rests on tier 6 or 7, its frontmatter `status` is `interpretive` or `mixed` and the draft status is flagged inline — see [[confirmed-vs-interpretive]].

## 2. Citation forms

**CFR.** Cite to the smallest unit that carries the requirement: `21 CFR 312.32(c)(1)(i)`, not "Part 312." Link the section (not the part) to the [eCFR](https://www.ecfr.gov/), which is the continuously updated official edition; Cornell LII is an acceptable alternate. Every CFR section used anywhere in the wiki is enumerated with its URL in the [[cfr-citation-map]].

**U.S. Code.** `21 U.S.C. § 355(i)`; link Cornell LII (`https://www.law.cornell.edu/uscode/text/21/355`). Where an FDCA section number is the term of art (e.g., FDCA § 561A for expanded-access policies), give both: "FDCA § 561A (21 U.S.C. § 360bbb-0)."

**Federal Register.** Volume FR page (date), with the document number where useful: `89 FR 76983 (Sept. 18, 2024)` or `FR Doc. 2024-21078`. Link `federalregister.gov` or `govinfo.gov`.

**ICH.** Guideline, revision, section: `ICH E6(R3) § 6.9`, `ICH E2A § III.B`. Always state Step 4 (adoption) date and the FDA adoption status/date, because ICH text is only tier-4 authority *in the US* once FDA publishes it as guidance. Link the ICH database PDF (`database.ich.org`). Statuses live in the [[ich-guideline-map]].

**FDA guidance.** Full title, center(s), month/year, and **final or draft** — always: *Conducting Clinical Trials With Decentralized Elements* (FDA, final, Sept. 2024). Draft guidances additionally carry "draft — subject to change" in the citing sentence, never only in a footnote. Statuses live in the [[fda-guidance-map]].

**FDA forms.** Form number + OMB control number + edition date where known: `Form FDA 1572 (OMB No. 0910-0014)`. Forms and download URLs live in the [[fda-form-index]].

**Publications.** Author, year, journal, and PMID or DOI: `Kim et al. 2014, PMID 24455986`. The deduplicated master list is the [[bibliography]].

**Institutional resources and templates.** Institution, resource name, URL, and license status. Never cite an institutional template as if it were authority; it is precedent. Provenance and license status live in [[institutional-resources]] and [[external-templates-and-licenses]].

## 3. Link conventions

- **Internal:** Obsidian `[[wikilinks]]` by filename stem, generously — every role, document, or workflow with its own page gets a link on first mention (see `_conventions.md`).
- **External:** markdown links to eCFR / FDA / ICH / DOI. Prefer the issuing body's own domain over mirrors.
- **Local originals:** where a source PDF is preserved under `sources/` (1,015 documents; see `sources/MANIFEST.md`), the `## Sources` entry also links the local path (e.g., `../sources/fda-form/FDA_Form-1572.pdf`). The local copy is the inspection-stable snapshot; the URL is the living source.

## 4. Versioning and citation rot

The regulatory frame is in active motion: ICH E6(R3) was FDA-adopted 2025-09-09 with no US compliance date yet set; ICH M11's final template is dated 2025-11-19; the FDA AI-credibility guidance is still draft. Three rules keep the corpus honest:

1. **Date every status claim.** "Final as of 2026-07-09" beats "final."
2. **Never silently upgrade a draft.** A draft guidance that finalizes gets an explicit edit, logged in the [[regulatory-change-log]].
3. **The citation-dependency graph is maintained.** Each map page in this section records *which wiki pages cite which authority*, so a change in the authority identifies every page, template, and validation rule that must be re-verified.

> [!interpretive] OSSICRO position
> The generate/check/validate engine treats these conventions as machine-enforceable rules: every generated artifact carries its governing-authority citations in a manifest ([[compliance-mapping]]), every validation rule traces to a CFR/ICH subsection, and a citation to a superseded or draft authority is a checkable defect. Drafting the citation is automatable; *judging* whether an authority governs a live case is not — that stays with the qualified human reviewer, consistent with [[non-delegable-functions-and-gates]].

## 5. Pages in this section

| Page | Contents |
|---|---|
| [[cfr-citation-map]] | Every 21/42/45 CFR section (and U.S.C. section) used in the wiki, with eCFR/LII URLs and principal citing pages |
| [[ich-guideline-map]] | ICH guidelines with Step 4 dates, FDA adoption status, and supersession notes |
| [[fda-guidance-map]] | FDA guidance documents with final/draft status, dates, and URLs |
| [[fda-form-index]] | FDA forms with OMB control numbers, authorities, and download URLs |
| [[bibliography]] | Consolidated deduplicated bibliography (regulatory + peer-reviewed, PMID/DOI) |
| [[institutional-resources]] | Academic/CRO/government resource table with reuse-license status |
| [[external-templates-and-licenses]] | Provenance and license status of every seed template |
| [[regulatory-change-log]] | Living-compliance change watch across FDA/ICH/eCFR |

## Related
- [[confirmed-vs-interpretive]]
- [[regulatory-landscape]]
- [[compliance-mapping]]
- [[non-delegable-functions-and-gates]]
- [[generate-check-validate-engine]]
- [[regulatory-change-log]]
- [[what-is-ossicro]]

## Sources
- [eCFR — Electronic Code of Federal Regulations (official, continuously updated)](https://www.ecfr.gov/)
- [Cornell Legal Information Institute — U.S. Code](https://www.law.cornell.edu/uscode/text)
- [Federal Register](https://www.federalregister.gov/)
- [ICH Guidelines Database](https://database.ich.org/)
- [FDA Search for Guidance Documents](https://www.fda.gov/regulatory-information/search-fda-guidance-documents)
- [FDA — IND Forms and Instructions](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-forms-and-instructions)
- Local source library manifest: `../sources/MANIFEST.md`
