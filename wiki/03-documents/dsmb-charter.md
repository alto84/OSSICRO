---
title: "DSMB Charter — Sections and Risk-Tiered Variants"
section: "03-documents"
status: mixed
governing_authority:
  - "FDA Guidance: Establishment and Operation of Clinical Trial Data Monitoring Committees (2006)"
  - "FDA Draft Guidance: Use of Data Monitoring Committees in Clinical Trials (March 2024)"
  - "ICH E6(R3) Section 5 (sponsor oversight)"
  - "21 CFR 312.23(a)(6)(iii)(g); 21 CFR 56.111(a)(6)"
tags: [role/dsmb, gcp/e6r3, lifecycle/conduct, lifecycle/safety, ossicro/engine, ossicro/gating, status/mixed]
aliases: ["DSMB charter", "DMC charter", "data monitoring committee charter", "DSMB"]
updated: 2026-07-09
---

# DSMB Charter — Sections and Risk-Tiered Variants

> [!authority] Governing authority
> FDA Guidance "Establishment and Operation of Clinical Trial Data Monitoring Committees" (2006), being revised by the FDA draft guidance "Use of Data Monitoring Committees in Clinical Trials" (March 2024); ICH E6(R3) §5 (sponsor quality management and oversight); 21 CFR 56.111(a)(6) (adequate provision for monitoring data for subject safety); 21 CFR 312.23(a)(6)(iii)(g) (monitoring described in the protocol). Status: **Mixed** — a written charter governing a DMC's operation is the confirmed standard of practice where a committee is used; *whether* a given early-phase study requires a DMC is a conditional, risk-based judgment (interpretive), and the DMC's recommendations are non-delegable human committee output.

The **Data Safety Monitoring Board (DSMB)** — equivalently the **Data Monitoring Committee (DMC)** in FDA's vocabulary — is an independent, multidisciplinary group of experts that reviews accumulating safety (and, in some designs, interim efficacy) data at intervals during a trial and advises the sponsor whether to **continue, modify, or stop**. The **charter** is the committee's written constitution: it defines the DMC's mandate, membership, meeting structure, data flow, statistical monitoring plan, confidentiality firewall, and the format of its recommendations. Because the DMC operates on unblinded interim data behind a firewall from the sponsor's operational team, the charter is the instrument that makes its independence auditable.

OSSICRO generates the charter from a template and validates that every required section is present and internally consistent. It never selects committee members, never sits on the committee, and never authors, influences, or substitutes for a DMC recommendation.

## When is a DMC warranted?

FDA does not mandate a DMC for every trial. The 2006 guidance recommends a DMC most strongly where risk to participants is high and where interim data could ethically compel a change: large, randomized, multi-site studies; endpoints of mortality or major morbidity; vulnerable populations; and studies with a high a-priori risk. Many early-phase (Phase 1/2) studies use a simpler internal **safety review** mechanism instead of a formal chartered DMC. The [[dsmb-dmc]] role page and the [[safety-management-plan]] carry the decision heuristics; the OSSICRO engine raises a **"DMC-warranted" flag** — a prompt for human decision, never an automated determination — when the study's structured attributes match the higher-risk profile.

## Charter section map

The following sections reflect the 2006 FDA guidance and the 2024 draft. A complete charter carries all of them; the OSSICRO validator checks each for presence and consistency.

| # | Section | Contents | Governing basis |
|---|---------|----------|-----------------|
| 1 | **Introduction / purpose and scope** | The DMC's mandate; the trial it serves; the possible recommendations (continue / modify / suspend enrollment / stop) | FDA 2006 §3; 2024 draft |
| 2 | **Membership and roles** | Named members; chair; specialties; the independent (unblinded) statistician; quorum | FDA 2006 §4 (membership) |
| 3 | **Conflict-of-interest and independence** | Financial/scientific/regulatory COI exclusions; members are not investigators, sponsor employees, at investigator institutions, or from regulators; disclosure/attestation | FDA 2006 §4.2 |
| 4 | **Responsibilities** | Safety review; benefit/risk monitoring; interim-efficacy review where applicable; protocol-adherence oversight scope | FDA 2006 §3 |
| 5 | **Meeting schedule and structure** | Organizational (pre-enrollment) meeting; periodic reviews (calendar- or event-driven); **open** (blinded, sponsor may attend) and **closed** (unblinded, DMC + independent statistician only) sessions | FDA 2006 §5 |
| 6 | **Statistical monitoring / interim-analysis plan** | Interim analyses; group-sequential or other stopping boundaries; the analyses the closed report will contain; who prepares them (the independent statistician, not the sponsor team) | FDA 2006 §5-6; [[statistical-analysis-plan]] |
| 7 | **Stopping guidelines** | Safety stopping rules; futility/efficacy boundaries where applicable; the distinction between a **guideline** (DMC judgment retained) and a mechanical rule | FDA 2006 §6 |
| 8 | **Data flow and firewall** | What data reaches the DMC, in what form, from whom; the firewall between the unblinded statistician and the sponsor's operational/analytic team; unblinding controls | FDA 2006 §5.4; ICH E6(R3) §5 |
| 9 | **Confidentiality** | Handling of interim/unblinded data and DMC deliberations; who may see minutes | FDA 2006 §7 |
| 10 | **Recommendation format and communication** | How recommendations are worded and transmitted to the sponsor; what the sponsor may/may not learn | FDA 2006 §7 |
| 11 | **Recordkeeping / minutes** | Open- and closed-session minutes; retention; the auditable trail | FDA 2006 §7; ICH E6(R3) essential records |
| 12 | **Charter amendment and approval** | Signature/adoption by members; version control | FDA 2006 |

## Risk-tiered variants

> [!interpretive] OSSICRO position
> A single fixed charter template is a poor fit for the range from an n-of-1 single-site early-phase study to a multi-site, blinded, mortality-endpoint trial. OSSICRO maintains **risk-tiered charter variants** — a proportionality expression of the same principle E6(R3) §5 applies to monitoring. The tier is a **human-confirmed** classification (the engine proposes; a qualified human sets it); it selects the template, not the oversight itself.

- **Tier A — single-site, low-risk, open-label early-phase / safety review.** Often no formal chartered DMC; an internal **safety review committee** with a lightweight terms-of-reference document. If a DMC is used, a minimal charter: purpose, small membership (≥3, ≥1 biostatistician), safety-only review, simple periodic cadence, safety stopping guidelines, minutes. No interim-efficacy machinery; firewall proportionate.
- **Tier B — multi-site or moderate-risk, possibly blinded.** Full charter: independent unblinded statistician and firewall; open/closed session structure; interim safety analyses on a defined cadence; formal COI attestations; documented recommendation channel.
- **Tier C — multi-site, high-risk, blinded, mortality/major-morbidity endpoint, and/or vulnerable population.** Full charter plus: pre-specified group-sequential stopping boundaries tied to the [[statistical-analysis-plan|SAP]]; ethicist membership; frequent event-driven reviews; rigorous firewall and unblinding controls; explicit coordination arrows to the IRB and to protocol amendments per the [[inter-entity-document-flow-map]].

The tier drives the template but not the substance of independence: in every tier the DMC's members, judgment, and recommendations are human and independent of OSSICRO.

## Non-delegable gate

> [!warning] Non-delegable
> A DMC **recommendation** to continue, modify, or stop a trial is the output of an **independent, conflict-free, human expert committee** deliberating on unblinded interim data (FDA 2006/2024 DMC guidance). OSSICRO must never author, predict, weight, or substitute for that recommendation; must never place itself or the sponsor's operational team inside the firewall; and must never machine-trigger a stop on a stopping boundary — a boundary informs the committee's judgment, it does not replace it. Membership selection and COI adjudication are likewise human. The engine assembles the charter, schedules the cadence, and organizes the open/closed report packets prepared by the independent statistician; it owns none of the committee's judgment. See [[non-delegable-functions-and-gates]] and [[dsmb-workflow]].

## OSSICRO engine behavior
- **Generate:** instantiates the tier-appropriate charter template from the study's structured attributes (design, blinding, sites, endpoint, population), populating purpose, cadence, and firewall sections; produces a draft for the sponsor and prospective members.
- **Check:** validates that all required sections (1-12) are present; that a biostatistician and an independent unblinded statistician are provided for; that COI-exclusion language is present; that the stopping guidelines reference the SAP; and that the meeting structure separates open and closed sessions.
- **Validate:** cross-checks the charter against the protocol's monitoring section (21 CFR 312.23(a)(6)(iii)(g)) and the [[safety-management-plan]] for consistency; holds the charter in a draft state pending member adoption. It never asserts a DMC exists, never fills member identities without human input, and never advances a recommendation.

## Related
- [[dsmb-dmc]]
- [[dsmb-workflow]]
- [[safety-management-plan]]
- [[monitoring-plan]]
- [[statistical-analysis-plan]]
- [[medical-monitor]]
- [[biostatistician]]
- [[inter-entity-document-flow-map]]
- [[irb-submission-package]]
- [[non-delegable-functions-and-gates]]

## Sources
- [FDA — Establishment and Operation of Clinical Trial Data Monitoring Committees (2006)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/establishment-and-operation-clinical-trial-data-monitoring-committees)
- [FDA — Use of Data Monitoring Committees in Clinical Trials (Draft, March 2024)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-data-monitoring-committees-clinical-trials)
- [21 CFR 56.111 — Criteria for IRB approval of research](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-56/subpart-C/section-56.111)
- [21 CFR 312.23 — IND content and format](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23)
- [ICH E6(R3) Good Clinical Practice — Step 4 Final Guideline (2025)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
