---
title: "Sponsor — Responsibilities under 21 CFR 312.50-312.59 and ICH E6(R3)"
section: "01-roles-responsibilities"
status: mixed
governing_authority:
  - "21 CFR 312.50-312.59"
  - "21 CFR 312.32-312.33"
  - "21 CFR Part 54"
  - "ICH E6(R3) Annex 1, Section 3 (Sponsor)"
tags: [role/sponsor, cfr/312, gcp/e6r3, lifecycle/conduct, lifecycle/safety, ossicro/gating]
aliases: ["sponsor responsibilities", "312.50"]
updated: 2026-07-09
---

# Sponsor — Responsibilities under 21 CFR 312.50-312.59 and ICH E6(R3)

> [!authority] Governing authority
> 21 CFR 312 Subpart D, §§312.50-312.59 (sponsor responsibilities); 21 CFR 312.32-312.33 (IND safety and annual reporting, Subpart B); 21 CFR Part 54 (financial disclosure); ICH E6(R3) Annex 1, Section 3 — Sponsor (Step 4 final 2025-01-06; adopted as FDA final guidance September 2025; corresponds to E6(R2) §5, the numbering still used in most institutional SOPs). Status: **Mixed** — CFR duties confirmed; OSSICRO automation-boundary claims marked interpretive.

A **sponsor** is "a person who takes responsibility for and initiates a clinical investigation" (21 CFR 312.3(b)). The sponsor may be an individual, a pharmaceutical company, a governmental agency, an academic institution, a private organization, or another organization; the sponsor does not actually conduct the investigation unless the same individual is a [[sponsor-investigator]]. The sponsor holds the IND, owns the regulatory relationship with FDA, and carries ultimate accountability for participant safety and data reliability across every site. This page enumerates the sponsor duty set that OSSICRO must track, document, and gate — for a pharma sponsor in Mode A ([[pharma-partner-sponsor]]) and, collapsed into one physician, in Mode B ([[two-modes-site-vs-sponsor-investigator]]).

## General responsibilities — 21 CFR 312.50

Section 312.50 is the umbrella: sponsors are responsible for (1) **selecting qualified investigators**, (2) **providing them the information they need** to conduct the investigation properly, (3) **ensuring proper monitoring** of the investigation(s), (4) **ensuring the investigation is conducted in accordance with the general investigational plan and protocols contained in the IND**, (5) **maintaining an effective IND**, and (6) **ensuring that FDA and all participating investigators are promptly informed of significant new adverse effects or risks** with respect to the drug. Each clause is elaborated by a later section: (1)-(2) by 312.53 and 312.55, (3) by 312.53(d) and 312.56, (5) by 312.30-312.33, (6) by 312.32 and 312.55(b).

## Transfer of obligations — 21 CFR 312.52

A sponsor may transfer responsibility for any or all Part 312 obligations to a contract research organization, but only **in writing**. A partial transfer must describe **each obligation** being assumed; a full transfer may use a general statement. **Any obligation not covered by the written description is deemed not to have been transferred** (312.52(a)). A CRO that assumes an obligation must comply with the corresponding regulations and "shall be subject to the same regulatory action as a sponsor" for failure to comply (312.52(b)). Because the transferee must be a person capable of bearing FDA enforcement, only a legal entity qualifies — this is the load-bearing fact of the OSSICRO legal frame ([[legal-thesis-3123-vs-31252]]): software can support compliance but can never *be* the transferee. The written instrument is documented at [[transfer-of-regulatory-obligations-toro]]; the accountable entity is the [[cro]] or, in the OSSICRO model, the [[micro-cro-accountable-layer]].

> [!warning] Non-delegable
> Ultimate accountability for participant safety and for the quality and integrity of trial data remains with the sponsor even after a 312.52 transfer, and always when duties are merely *supported* by software or service providers (312.52; ICH E6(R3) Annex 1 §3, service-provider oversight). OSSICRO is a compliance tool, not a transferee: it can never assume, hold, or discharge a sponsor obligation.

## Selecting investigators and monitors — 21 CFR 312.53

- **(a) Selecting investigators.** The sponsor shall select only investigators "qualified by training and experience as appropriate experts" to investigate the drug.
- **(b) Control of drug.** The sponsor shall ship investigational new drug only to investigators participating in the investigation.
- **(c) Obtaining information from the investigator.** Before permitting an investigator to begin participation, the sponsor shall obtain: **(c)(1)** a signed [[form-fda-1572-statement-of-investigator|Form FDA 1572]] containing the investigator's identifying information, facilities, IRB, subinvestigators, protocol reference, and the Field 9 commitments (protocol adherence, personal conduct or supervision, informed consent per Part 50, reporting per 312.64, IRB review per Part 56); **(c)(2)** a curriculum vitae or other statement of qualifications; **(c)(3)** the clinical protocol (an outline for Phase 1; a detailed protocol for Phase 2/3); and **(c)(4)** financial disclosure information sufficient to make complete and accurate Part 54 certification or disclosure ([[form-fda-3454-3455-financial-disclosure]]), plus the investigator's commitment to update it for one year after study completion.
- **(d) Selecting monitors.** The sponsor shall select a monitor "qualified by training and experience" to monitor the progress of the investigation ([[clinical-monitor-cra]]).

## Emergency research — 21 CFR 312.54

For investigations involving an exception from informed consent under 21 CFR 50.24 or emergency use under 50.23, the sponsor must monitor progress, promptly submit the required public-disclosure materials to the IND file and FDA, and — if an IRB determines it cannot approve such research — promptly notify FDA, other reviewing IRBs, and investigators of the same or a substantially equivalent investigation. This pathway is out of OSSICRO's Phase 0-6 scope but is included in the [[document-catalog]] for completeness.

## Informing investigators — 21 CFR 312.55

- **(a)** Before the investigation begins, the sponsor shall give each participating clinical investigator an [[investigators-brochure|investigator's brochure]] containing the information described in 21 CFR 312.23(a)(5).
- **(b)** The sponsor shall keep each participating investigator informed of new observations discovered by or reported to the sponsor, particularly with respect to adverse effects and safe use — via updated brochures, reprints, published studies, letters, or other appropriate means. Important safety information must be relayed per 312.32 ([[ind-safety-report]]).

## Review of ongoing investigations — 21 CFR 312.56

- **(a)** The sponsor shall **monitor the progress of all clinical investigations** conducted under its IND (implemented per the [[monitoring-plan]] and, under E6(R3), a risk-based strategy — [[risk-based-monitoring-e6r3]]).
- **(b)** A sponsor who discovers that an investigator is not complying with the signed 1572 agreement, the general investigational plan, or Part 312 requirements shall **promptly either secure compliance or discontinue shipments** of the drug and **end the investigator's participation**, require drug return or disposition per 312.59, and **notify FDA**.
- **(c)** The sponsor shall **review and evaluate the evidence relating to the safety and effectiveness of the drug** as obtained from the investigator, make the safety reports required by 312.32, and make annual reports per 312.33.
- **(d)** If the sponsor determines the drug **presents an unreasonable and significant risk to subjects**, it shall discontinue those investigations as soon as possible, and **no later than 5 working days** after making the determination; notify FDA, all reviewing IRBs, and all investigators; assure disposition of outstanding drug stocks; and furnish FDA a full report of its actions.

> [!warning] Non-delegable
> The 312.56(b) judgment to secure compliance or terminate a non-compliant investigator, and the 312.56(d) determination of unreasonable and significant risk with its 5-working-day discontinuation clock, are sponsor decisions. OSSICRO may surface the triggering evidence, compute the deadline ([[safety-clock-engine]]), and draft the notifications — a qualified human owns the determination and every resulting communication to FDA, IRBs, and investigators.

## Recordkeeping and retention — 21 CFR 312.57

- **(a)** Maintain adequate records of the **receipt, shipment, and other disposition** of the investigational drug — including the name of each investigator, and the date, quantity, and batch or code mark of each shipment ([[drug-accountability-log]]).
- **(b)** Maintain **complete and accurate records of financial interests** subject to Part 54 disclosure requirements.
- **(c)** **Retention:** records and reports required by Part 312 must be kept for **2 years after a marketing application is approved** for the drug; or, if no application is filed or approved, until **2 years after shipment and delivery of the drug for investigational use is discontinued and FDA has been so notified** ([[record-retention-and-archival]]).
- **(d)** Retain reserve samples of test article and reference standard used in bioequivalence/bioavailability studies, per the cross-referenced Part 320 requirements.

## Inspection — 21 CFR 312.58

Upon request of a properly authorized FDA officer or employee, at reasonable times, the sponsor shall permit access to, and copying and verification of, any records and reports relating to the clinical investigation (312.58(a)). For investigational substances controlled under the Controlled Substances Act, records must additionally be made available to DEA, and adequate storage precautions taken (312.58(b)). Inspection readiness is treated at [[fda-as-counterparty]].

## Disposition of unused supply — 21 CFR 312.59

The sponsor shall assure the **return of all unused supplies** of the investigational drug from each discontinued or terminated investigator, or authorize alternative disposition that does not expose humans to risks from the drug, and shall maintain written records of any disposition per 312.57.

## Cross-Subpart sponsor duties: safety and annual reporting

Two Subpart B duties are inseparable from the Subpart D set and are carried by every sponsor:

- **IND safety reports (21 CFR 312.32).** The sponsor must promptly review all safety information from any source (312.32(b)); notify FDA **and all participating investigators** of serious and unexpected suspected adverse reactions, qualifying findings from other studies or animal/in vitro testing, and clinically important increased occurrence rates, in a 15-calendar-day IND safety report (312.32(c)(1)); and notify FDA of unexpected fatal or life-threatening suspected adverse reactions within **7 calendar days** (312.32(c)(2)). Follow-up information is due within 15 calendar days of receipt (312.32(d)). See [[ind-safety-report]], [[form-fda-3500a-medwatch]], [[safety-reporting-lifecycle]].
- **Annual report (21 CFR 312.33).** Within **60 days of the anniversary date that the IND went into effect**, the sponsor must submit a brief report of progress — study status, summary safety information, IND safety reports, the coming year's general investigational plan, IB revisions, significant Phase 1 protocol modifications, and relevant foreign marketing developments. See [[ind-annual-report-dsur]], [[annual-reporting-and-amendments]].

## The ICH E6(R3) layer

E6(R3) Annex 1 §3 (Sponsor) overlays a quality-management framework on the CFR floor. The elements OSSICRO encodes:

- **Quality by design and risk-based quality management** — identify the factors critical to quality; manage risks proportionately to their importance to participant safety and result reliability; avoid disproportionate process and non-critical data collection.
- **Oversight of service providers** — the sponsor retains responsibility for, and must maintain documented oversight of, all delegated trial-related activities, including technology vendors. Delegation does not transfer accountability.
- **Risk-based monitoring** — a systematic, prioritized strategy combining centralized and on-site monitoring ([[risk-based-monitoring-e6r3]]).
- **Safety assessment and reporting** — ongoing safety evaluation, expedited and periodic reporting, and keeping the IB current ([[safety-management-plan]]).
- **Investigational product management** — manufacturing, labeling, coding, supply, and documented accountability and reconciliation.
- **Data governance (Annex 1 §4) and essential records (Appendix C)** — ALCOA-conformant data integrity across the lifecycle, validated systems with audit trails, and a trial master file sufficient to reconstruct the trial ([[document-catalog]], [[record-retention-and-archival]]).

> [!interpretive] OSSICRO position
> Within this duty set, OSSICRO classifies as automatable *coordination labor*: assembling and version-controlling the 312.53(c) investigator package, generating the monitoring plan and visit schedules, computing the 312.32 and 312.33 clocks, drafting safety reports and annual reports, maintaining drug-accountability and financial-interest records, and completeness-checking the TMF against E6(R3) Appendix C ([[completeness-ledger]]). Everything else — the qualification judgments, the compliance/termination decisions, the causality and risk determinations, and every FDA-facing signature and submission — stays behind human gates ([[non-delegable-functions-and-gates]]). OSSICRO drafts complete documentation for qualified human review; it never replaces the sponsor's judgment, IRB/ethics review, or DSMB oversight ([[dsmb-dmc]]).

## Related

- [[investigator]]
- [[sponsor-investigator]]
- [[cro]]
- [[micro-cro-accountable-layer]]
- [[transfer-of-regulatory-obligations-toro]]
- [[form-fda-1571-ind-cover]]
- [[form-fda-1572-statement-of-investigator]]
- [[form-fda-3454-3455-financial-disclosure]]
- [[ind-safety-report]]
- [[ind-annual-report-dsur]]
- [[monitoring-plan]]
- [[drug-accountability-log]]
- [[risk-based-monitoring-e6r3]]
- [[non-delegable-functions-and-gates]]
- [[legal-thesis-3123-vs-31252]]

## Sources

- [21 CFR 312.50 — General responsibilities of sponsors (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.50)
- [21 CFR 312.52 — Transfer of obligations to a contract research organization (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52)
- [21 CFR 312.53 — Selecting investigators and monitors (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53)
- [21 CFR 312.54 — Emergency research (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.54)
- [21 CFR 312.55 — Informing investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.55)
- [21 CFR 312.56 — Review of ongoing investigations (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56)
- [21 CFR 312.57 — Recordkeeping and record retention (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.57)
- [21 CFR 312.58 — Inspection of sponsor's records and reports (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.58)
- [21 CFR 312.59 — Disposition of unused supply of investigational drug (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.59)
- [21 CFR 312.32 — IND safety reporting (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
- [21 CFR 312.33 — Annual reports (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.33)
- [21 CFR Part 54 — Financial disclosure by clinical investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA — E6(R3) Good Clinical Practice guidance page (Sept 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
