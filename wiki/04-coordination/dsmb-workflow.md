---
title: "DSMB/DMC Workflow — Charter Adoption, Cadence, Open/Closed Sessions, and the Statistician Firewall"
section: "04-coordination"
status: mixed
governing_authority:
  - "FDA Guidance (2006) — Establishment and Operation of Clinical Trial Data Monitoring Committees"
  - "FDA Draft Guidance (Mar 2024) — Use of Data Monitoring Committees in Clinical Trials"
  - "ICH E6(R3) §5 (Sponsor: quality management, safety assessment)"
  - "21 CFR 312.32; 21 CFR 312.56(d)"
tags: [role/dsmb, role/biostatistician, role/sponsor, gcp/e6r3, cfr/312, lifecycle/safety, lifecycle/conduct, ossicro/gating, status/mixed]
aliases: ["DSMB", "DMC", "data monitoring committee", "data safety monitoring board", "DSMB workflow"]
updated: 2026-07-09
---

# DSMB/DMC Workflow — Charter Adoption, Cadence, Sessions, and the Statistician Firewall

> [!authority] Governing authority
> The Data Monitoring Committee (DMC) / Data Safety Monitoring Board (DSMB) is an advisory body operating under a written charter, described in FDA's 2006 guidance *Establishment and Operation of Clinical Trial Data Monitoring Committees* (being revised by the March 2024 draft *Use of Data Monitoring Committees in Clinical Trials*). Its outputs feed the sponsor's non-delegable continue/modify/stop decision under [21 CFR 312.56(d)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56) and safety-evaluation obligation under [21 CFR 312.32(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32). ICH E6(R3) §5 places DMC oversight inside the sponsor's risk-based quality-management system. Status: **Mixed** — the DMC's charter, independence, and advisory role are confirmed requirements; OSSICRO's boundary (assemble/schedule/route, never author a recommendation or breach the firewall) is an interpretive position, marked inline.

A DMC/DSMB is an **independent group of experts** that reviews accumulating safety — and, where the design warrants, interim efficacy — data over the life of a trial and advises the [[sponsor]] (or the [[sponsor-investigator]]) whether to **continue, modify, or stop**. It is a recommending body, not a decisional one: the DMC advises, the sponsor decides, the [[irb-iec]] is informed of any change that alters the risk profile, and every arrow is traceable in the [[inter-entity-document-flow-map]]. The committee exists to protect participants and preserve trial integrity precisely by holding the unblinded accumulating data at arm's length from the people running and funding the study.

## When a DMC is warranted

FDA's 2006 guidance recommends a DMC especially for large, randomized, multi-site controlled trials with **mortality or major-morbidity endpoints**, vulnerable populations, or high a-priori risk. Early-phase studies — OSSICRO's core [[sponsor-investigator]] use case — more often rely on a simpler **safety-review mechanism** (a pre-specified internal safety review, a dose-escalation review committee, or a medical monitor's periodic review) rather than a full independent DMC. The 2024 draft guidance sharpens the "when and why" and cautions against instituting a DMC reflexively where a lighter mechanism suffices.

> [!interpretive] OSSICRO position
> OSSICRO does **not** decide whether a study needs a DMC — that is a design judgment for the sponsor, the [[biostatistician]], and the [[medical-monitor]], informed by the protocol's risk profile. OSSICRO surfaces the 2006/2024-guidance decision factors as a structured prompt, and — once the human decides a DMC (or a defined safety-review mechanism) is required — generates the charter draft and stands up the cadence and packet-assembly workflow. The [[safety-management-plan]] records which mechanism was chosen and why.

## Charter adoption

The DMC operates under a **written charter** adopted before the committee reviews any data (typically finalized at or before the organizational meeting). Per the 2006 guidance and the 2024 draft, the charter should specify:

- **Purpose and scope** — the questions the DMC will consider and the set of recommendations it can make.
- **Membership and roles** — named members, the chair, and the independent (unblinded) statistician who serves the committee.
- **Meeting schedule and structure** — organizational meeting, then periodic reviews; the open/closed/executive session model (below).
- **Statistical monitoring plan** — interim-analysis timing, group-sequential or other stopping guidelines, and the analyses the committee will see.
- **Data flow and the firewall** — how data reach the DMC and the independent statistician without unblinding the sponsor team.
- **Confidentiality and conflict-of-interest procedures.**
- **Format of recommendations to the sponsor** and record-keeping / minutes conventions.

The charter template and its required-section validator are covered on the [[dsmb-charter]] document page; risk-tiered variants (single-site low-risk safety review vs. multi-site high-risk independent DMC) are generated from the same skeleton.

## Membership and independence

Members must be **free of significant financial, scientific, and regulatory conflicts of interest**. A DMC typically has three or more members, including clinicians in the relevant specialties and **at least one qualified biostatistician**, with an ethicist added for higher-risk studies. Members may **not** be study investigators, sponsor employees, at the same institution as the investigators, or from a regulatory agency. Prior DMC experience is valued. Independence is the entire point: the committee's credibility, and the protection it affords participants, rests on its distance from the parties with an interest in the trial's outcome.

> [!warning] Non-delegable
> DMC **membership, independence, and the continue/modify/stop recommendation** are human functions that cannot be authored by software. OSSICRO does not populate a committee, does not assess a member's conflicts, and does not generate a recommendation. It assembles and routes the packets the committee reads and records the minutes and recommendation the committee produces. The recommendation is the committee's; the decision that follows it is the sponsor's.

## Meeting cadence

Cadence is set in the charter — commonly an **organizational meeting before enrollment**, then **periodic reviews** (e.g., every 3–6 months, or triggered by event-count or enrollment milestones). OSSICRO schedules the cadence, tracks the milestone triggers, and issues the packet-assembly and meeting-logistics tasks; it never advances or compresses the schedule on a safety signal without routing the signal to the [[medical-monitor]].

## Session structure — open, closed, executive

Each review is structured into sessions that manage who sees unblinded data:

| Session | Attendees | Data seen |
|---------|-----------|-----------|
| **Open session** | DMC + sponsor (may attend) | Blinded / pooled — enrollment, aggregate safety, conduct metrics |
| **Closed session** | DMC + independent unblinded statistician only | Unblinded, by-arm safety and (where applicable) efficacy |
| **Executive session** | DMC voting members only | Deliberation toward the recommendation |

The **open session** lets the sponsor present trial status without seeing unblinded comparisons. The **closed session** is where the committee and the independent statistician review the by-arm data behind the firewall. The **executive session** is the committee's private deliberation. Output is a **written recommendation and minutes** to the sponsor.

## The statistician firewall

The **independent (unblinded) statistician** prepares the closed-session data reports and sits **outside** the sponsor firewall — deliberately separated from the sponsor/study team, who remain blinded to protect the integrity of the ongoing trial. The sponsor's own [[biostatistician]] does **not** see the unblinded interim comparisons; the closed-session packets are produced by the independent statistician, not the sponsor team. This firewall is the structural mechanism that keeps the accumulating unblinded data from influencing trial conduct, endpoint adjudication, or enrollment behavior.

> [!warning] Non-delegable
> The **firewall itself is a control OSSICRO must enforce, not relax.** Unblinded, by-arm interim data routed to the independent statistician and the DMC's closed session must never flow to the sponsor/study-team surfaces, and OSSICRO must never synthesize or expose an unblinded interim comparison to a blinded party. Access control here is a [Part 11](../05-ossicro-system/part-11-and-ai-credibility.md) and trial-integrity requirement, and it is code-enforced, not policy-suggested.

> [!interpretive] OSSICRO position
> OSSICRO models the DMC firewall as a hard access-control boundary in the [[communication-hub]] and the [[data-model]]: closed-session artifacts and unblinded line-listings carry a firewall attribute; only the independent-statistician and DMC-member roles can read them; the sponsor/study-team role is denied by construction, and every access is written to the [[draft-provenance-model|ALCOA++ audit trail]]. OSSICRO assembles the **open-session** packet from blinded aggregate data and hands the **closed-session** packet to the independent statistician to complete — it does not manufacture the unblinded comparison. The recommendation letter is a template OSSICRO renders *after* the committee dictates its content; the engine never drafts the substance of a continue/modify/stop recommendation.

## From recommendation to decision — the downstream arrows

A DMC recommendation flows: **DMC → sponsor**. The sponsor makes the continue/modify/stop decision ([21 CFR 312.56(d)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56) for the unreasonable-risk case). If the decision changes the trial's risk profile, it flows onward: **sponsor → IRB** (and a [[annual-reporting-and-amendments|protocol amendment]] where the protocol changes) and, where a safety issue is expedited-reportable, into the [[safety-reporting-workflow]] to FDA and all investigators. A DMC-driven stop for unreasonable and significant risk triggers the [312.56(d)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56) five-working-day discontinuation-and-notification duty. OSSICRO's coordination value is timing, routing, and completeness across exactly these arrows — never the judgment at any node.

## OSSICRO engine behavior

- **Generate:** drafts the DMC charter (risk-tiered variant) and the meeting-packet skeletons (open-session from blinded aggregate data; closed-session shell for the independent statistician to complete).
- **Check:** validates the charter contains every required section (purpose/scope, membership/COI, cadence, statistical monitoring plan and stopping guidelines, firewall procedures, recommendation format, minutes convention); confirms the cadence and firewall roles are configured before first data review.
- **Validate:** enforces the firewall as a code-level access boundary; holds every continue/modify/stop artifact in a gated state authored by the committee, not the engine; on a recorded recommendation that changes risk, opens the downstream IRB-notification / amendment / safety-report tasks.

## Related
- [[dsmb-dmc]]
- [[dsmb-charter]]
- [[biostatistician]]
- [[medical-monitor]]
- [[safety-reporting-workflow]]
- [[safety-report-timelines-7-15-day]]
- [[risk-based-monitoring-e6r3]]
- [[inter-entity-document-flow-map]]
- [[safety-management-plan]]
- [[non-delegable-functions-and-gates]]
- [[communication-hub]]

## Sources
- [FDA — Establishment and Operation of Clinical Trial Data Monitoring Committees (2006 guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/establishment-and-operation-clinical-trial-data-monitoring-committees)
- [FDA — Use of Data Monitoring Committees in Clinical Trials (2024 draft guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-data-monitoring-committees-clinical-trials)
- [FDA Law Blog — analysis of the 2024 draft DMC guidance](https://www.thefdalawblog.com/2024/03/how-to-run-dmc-its-tricky-fdas-new-draft-guidance-provides-updated-recommendations-on-how-to-best-use-data-monitoring-committees-in-clinical-trials/)
- [21 CFR 312.56 — Review of ongoing investigations](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56)
- [21 CFR 312.32 — IND safety reporting](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06, PDF)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
