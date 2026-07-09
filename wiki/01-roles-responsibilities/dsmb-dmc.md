---
title: "DSMB / DMC — Data and Safety Monitoring Board / Data Monitoring Committee"
section: "01-roles-responsibilities"
status: mixed
governing_authority:
  - "FDA Guidance (2006): Establishment and Operation of Clinical Trial Data Monitoring Committees"
  - "FDA Draft Guidance (2024): Use of Data Monitoring Committees in Clinical Trials"
  - "21 CFR 50.24(a)(7)(iv)"
  - "21 CFR 56.111(a)(6)"
  - "ICH E6(R3); ICH E9 §4.5"
tags: [role/dsmb, cfr/50, cfr/56, ich/e6r3, ich/e9, lifecycle/conduct, lifecycle/safety, entity/dsmb]
aliases: ["DSMB", "DMC", "IDMC", "Data Monitoring Committee", "Data and Safety Monitoring Board"]
updated: 2026-07-09
---

# DSMB / DMC — Data and Safety Monitoring Board / Data Monitoring Committee

> [!authority] Governing authority
> FDA Guidance for Clinical Trial Sponsors, *Establishment and Operation of Clinical Trial Data Monitoring Committees* (final, 2006); FDA draft guidance, *Use of Data Monitoring Committees in Clinical Trials* (2024 — **draft**, not yet final; supersedes the 2006 guidance when finalized); 21 CFR 50.24(a)(7)(iv) (the one context where a DMC is required by regulation); 21 CFR 56.111(a)(6) (data-monitoring provision as an IRB approval criterion); ICH E6(R3); ICH E9 §4.5 (IDMC). Status: **Mixed** — the regulatory hooks are confirmed; most DMC practice is guidance-level recommendation, and OSSICRO's support boundary is an interpretive position, marked inline.

A Data Monitoring Committee (DMC; also DSMB, IDMC) is a group of individuals with pertinent expertise that reviews **accumulating unblinded safety — and, where chartered, interim efficacy — data** from an ongoing trial on a regular basis and **advises the sponsor** on the continuing safety of current and future subjects and on the continuing validity and scientific merit of the trial. Two structural facts define the role: the committee must be **independent** of the trial it monitors, and it is **advisory, not decisional** — it recommends; the [[sponsor]] (or [[sponsor-investigator]]) decides, and remains fully accountable for that decision.

## 1. When a DMC is required, recommended, or optional

- **Required by regulation in exactly one context:** research conducted under the exception from informed consent for emergency research must establish an independent data monitoring committee to exercise oversight (21 CFR 50.24(a)(7)(iv)). This is the only 21 CFR provision mandating a DMC.
- **An IRB approval criterion, indirectly:** the IRB must find that, where appropriate, the research plan makes adequate provision for monitoring the data collected to ensure subject safety (21 CFR 56.111(a)(6); 45 CFR 46.111(a)(6)). A data-safety-monitoring plan satisfies this for most early-phase studies; a formal DMC is one way to satisfy it for higher-risk designs. See [[irb-iec]].
- **Recommended by FDA guidance** particularly for: large, randomized, multi-site trials; trials with mortality or major-morbidity endpoints; trials enrolling vulnerable or fragile populations; trials of high-risk interventions or with a-priori safety concerns; and trials where interim analysis is planned for early stopping. Conversely, FDA acknowledges most trials — especially short, early-phase, single-site studies — do not need a formal DMC.
- **Institutional policy:** NIH requires a DSMB for the multi-site phase III clinical trials it funds, and requires a data-and-safety-monitoring plan for all NIH-funded trials — relevant context for federally funded sponsor-investigator studies.

> [!interpretive] OSSICRO position — risk-tiered monitoring bodies for the sponsor-investigator
> For the typical OSSICRO Mode B early-phase, single-site study, the proportionate structure is usually a **safety-monitoring plan with an independent safety reviewer or small safety committee**, escalating to a formal chartered DMC where the FDA-guidance risk factors are present. OSSICRO's engine drafts both variants (see [[dsmb-charter]]) and records the selection rationale in the study record; the selection itself is a design judgment made by the sponsor-investigator with the [[medical-monitor]] and, where engaged, the [[biostatistician]] — and the IRB independently judges adequacy under 56.111(a)(6).

## 2. The charter

The DMC operates under a **written charter, adopted before the committee's first substantive data review** (normally at an organizational meeting before enrollment). Per the 2006 guidance (and elaborated in the 2024 draft), the charter should specify:

- Purpose and scope; the trial(s) covered; the range of possible recommendations (continue; continue with modification; pause enrollment; terminate).
- Membership, roles, and the conflict-of-interest policy; procedures for assessing and disclosing COI on an ongoing basis.
- Meeting schedule and triggers (calendar cadence, enrollment or event milestones), and the organizational / open / closed session format.
- The statistical monitoring plan: planned interim analyses, stopping guidelines or boundaries, and their relationship to the trial's [[statistical-analysis-plan]].
- Data flow: who prepares the reports (an **independent, unblinded statistician** outside the sponsor's firewall), what the open-session (pooled/blinded) and closed-session (unblinded, by-arm) packets contain, and timelines.
- Confidentiality and firewall procedures protecting interim comparative data from the sponsor, investigators, and trial personnel.
- Format, addressee, and timing of recommendations and minutes (open and closed minutes; who holds the closed minutes until trial end).

See [[dsmb-charter]] for the template and section-by-section validator, and [[dsmb-workflow]] for the operating cadence.

## 3. Membership, independence, and conflicts of interest

Confirmed themes of both the 2006 guidance and the 2024 draft:

- **Expertise:** typically at least three members, including clinicians expert in the relevant specialty and at least one biostatistician experienced in sequential/interim analysis; an ethicist or patient/community representative is appropriate for some trials. Prior DMC experience in at least some members is strongly recommended.
- **Independence:** members must not be investigators in the trial, employees of the sponsor, or otherwise hold significant financial, intellectual, professional, or regulatory conflicts of interest with the trial's outcome. Compensation for DMC service itself is not disqualifying but must be disclosed and managed.
- **The unblinded statistician firewall:** the statistician preparing unblinded interim reports should be independent of the sponsor's trial team; in the sponsor-investigator setting this independence is structurally harder and must be deliberately constructed (an external statistician; never the S-I's own study staff).

The 2024 draft guidance updates the 2006 framework in light of the substantial growth in DMC use — including expanded discussion of charters, of DMCs monitoring multiple trials or an entire development program, of the interplay with other adaptive-design governance bodies, and of operational best practices. **It is a draft; where it and the 2006 final guidance diverge, the 2006 guidance remains the operative final statement until the draft is finalized.** OSSICRO templates track both and flag draft-sourced provisions (see [[regulatory-change-log]]).

## 4. Advisory role and the recommendation loop

The DMC transmits a written recommendation to the sponsor after each data review. The **sponsor decides** — continue, modify (protocol amendment via 21 CFR 312.30), pause, or terminate — and carries the regulatory consequences of the decision: notifying FDA and investigators of significant new risks (312.32; 312.55(b)), informing IRBs, and, on a determination of unreasonable and significant risk, discontinuing the investigation within five working days (312.56(d)). DMC recommendations and meeting outputs are essential records ([[document-catalog]]); safety data flows to the DMC through the safety function ([[pharmacovigilance-safety]]) and the independent statistician, as diagrammed in [[inter-entity-document-flow-map]].

> [!warning] Non-delegable
> Two human judgments anchor this page. (1) The **DMC's deliberation and recommendation** require an independent, conflict-free human committee reviewing unblinded data — no software, including OSSICRO, may generate, weight, or stand in for the recommendation. (2) The **sponsor's continue/modify/stop decision** in response is the sponsor's (or sponsor-investigator's) own accountable risk-benefit judgment (21 CFR 312.56(b)–(d)). OSSICRO schedules, assembles open-session materials, transmits, timestamps, and archives; it is architecturally excluded from the closed session: unblinded interim data are prepared by the independent statistician outside both the sponsor firewall and the OSSICRO drafting pipeline.

> [!interpretive] OSSICRO position — what the system does here
> OSSICRO drafts the charter from the risk-tiered template library, maintains the meeting calendar and packet-assembly deadlines, generates open-session (blinded/pooled) report shells for human completion, routes the DMC's written recommendation to the sponsor-investigator as a gated action item, and files minutes and recommendations to the TMF with full provenance ([[draft-provenance-model]]). It performs no interim analysis, holds no unblinded data, and never drafts the recommendation itself.

## Related

- [[dsmb-charter]] · [[dsmb-workflow]] · [[inter-entity-document-flow-map]]
- [[biostatistician]] · [[statistical-analysis-plan]] · [[medical-monitor]]
- [[pharmacovigilance-safety]] · [[safety-reporting-lifecycle]] · [[safety-report-timelines-7-15-day]]
- [[sponsor]] · [[sponsor-investigator]] · [[irb-iec]]
- [[non-delegable-functions-and-gates]] · [[entity-map]] · [[glossary]]

## Sources

- [FDA Guidance (2006) — Establishment and Operation of Clinical Trial Data Monitoring Committees](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/establishment-and-operation-clinical-trial-data-monitoring-committees)
- [FDA Draft Guidance (2024) — Use of Data Monitoring Committees in Clinical Trials](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-data-monitoring-committees-clinical-trials)
- [21 CFR 50.24 — Exception from informed consent for emergency research (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-B/section-50.24)
- [21 CFR 56.111 — Criteria for IRB approval of research (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56/subpart-C/section-56.111)
- [21 CFR 312.56 — Review of ongoing investigations (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56)
- [ICH E9 — Statistical Principles for Clinical Trials (PDF), §4.5](https://database.ich.org/sites/default/files/E9_Guideline.pdf)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06, PDF)](https://database.ich.org/sites/default/files/ICH_E6(R3)_Step4_FinalGuideline_2025_0106.pdf)
- [NIH — Policy for Data and Safety Monitoring (NOT-98-084)](https://grants.nih.gov/grants/guide/notice-files/not98-084.html)
