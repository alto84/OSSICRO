---
title: "Safety Reporting Workflow — End-to-End PV Routing from Site AE Capture to FDA, Investigators, IRB, and DSMB"
section: "04-coordination"
status: mixed
governing_authority:
  - "21 CFR 312.32 (IND safety reporting)"
  - "21 CFR 312.64(b) (investigator SAE reporting to sponsor)"
  - "21 CFR 312.66; 21 CFR 56.108(b) (IRB reporting of unanticipated problems)"
  - "ICH E2A; ICH E6(R3) §5 (Safety Assessment and Reporting)"
tags: [role/pharmacovigilance-safety, role/medical-monitor, role/sponsor, role/investigator, cfr/312, cfr/56, ich/e2a, gcp/e6r3, lifecycle/safety, ossicro/gating, status/mixed]
aliases: ["safety reporting workflow", "PV workflow", "SAE routing", "SUSAR workflow", "pharmacovigilance workflow"]
updated: 2026-07-09
---

# Safety Reporting Workflow — End-to-End PV Routing

> [!authority] Governing authority
> The investigator reports serious adverse events to the sponsor immediately ([21 CFR 312.64(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.64)); the sponsor reviews all safety information ([21 CFR 312.32(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)) and submits expedited **IND safety reports** to FDA and all participating investigators ([21 CFR 312.32(c)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)); the investigator reports unanticipated problems to the reviewing IRB ([21 CFR 56.108(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-56/subpart-C/section-56.108); [312.66](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.66)). ICH E2A supplies the definitional framework; ICH E6(R3) §5 places safety assessment inside the sponsor's quality system. Status: **Mixed** — the routing and timelines are confirmed requirements; OSSICRO's boundary (capture, code, draft, time, and route — never adjudicate causality/seriousness/expectedness or file) is an interpretive position, marked inline.

This page is the **end-to-end pharmacovigilance (PV) routing map**: how a single adverse event captured at a site becomes, where warranted, an expedited IND safety report to FDA and a cascade of notifications to investigators, the [[irb-iec]], and the [[dsmb-dmc]]. The **definitions and the two clocks** (7-day and 15-day) are on [[safety-report-timelines-7-15-day]]; the **report format** is on [[form-fda-3500a-medwatch]]; this page is the *flow*. In the [[sponsor-investigator]] model the physician holds both the investigator's SAE-reporting duty *and* the sponsor's IND-safety-reporting duty — the two ends of this workflow collapse into one accountable person, which is exactly why OSSICRO's timing-and-routing support is load-bearing without ever touching the medical judgment.

## Stage 1 — Site capture (investigator → sponsor)

An adverse event (AE) is captured at the site during [[conduct-and-monitoring]]. When the event is a **serious** adverse event (SAE), the investigator must report it to the sponsor **immediately** per [21 CFR 312.64(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.64) and the protocol's safety-reporting section. The site's SAE report to the sponsor is the trigger event for the sponsor's clock. OSSICRO captures the AE/SAE into an ICH-E2B(R3)-structured case and starts the timing surveillance — but the **seriousness** flag at capture is a clinical determination the investigator makes.

## Stage 2 — Sponsor safety review and assessment

The sponsor must **promptly review all information relevant to the safety of the drug from any source, foreign or domestic** ([21 CFR 312.32(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)) — clinical and epidemiologic studies, literature, animal/in vitro data, and reports from foreign regulators or other manufacturers. For each case the sponsor's qualified [[medical-monitor|safety physician]] determines the three attributes that decide whether an expedited report is owed:

- **Serious** — death, life-threatening, hospitalization/prolongation, disability/incapacity, congenital anomaly, or a medically important event ([312.32(a)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)).
- **Unexpected** — not listed in the [[investigators-brochure]] / general investigational plan, or of greater severity/specificity than listed.
- **Suspected adverse reaction** — a **reasonable possibility** that the drug caused the event.

A case that is **serious + unexpected + suspected** is a SUSAR and is expedited-reportable. See [[safety-report-timelines-7-15-day]] for the full definitions and the two clocks.

> [!warning] Non-delegable
> **Causality, seriousness, and expectedness are medical judgments** owned by the sponsor's qualified [[medical-monitor|medical monitor / safety physician]] under [21 CFR 312.32(a)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32) and ICH E2A. OSSICRO must never auto-adjudicate "reasonable possibility of a causal relationship," never machine-set seriousness, and never machine-classify a case as a SUSAR. The engine assembles the case, computes and surfaces the deadline, and routes to the physician; the human assesses and classifies.

## Stage 3 — Expedited reporting (sponsor → FDA + all investigators)

When the safety physician classifies a case as expedited-reportable, the sponsor submits an **IND safety report** on [[form-fda-3500a-medwatch|Form FDA 3500A]] (or electronic E2B(R3)) to FDA within the applicable clock, and **notifies all participating investigators** of the new safety information ([312.32(c)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32); [312.55(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.55)):

- **7 calendar days** — unexpected **fatal or life-threatening** suspected adverse reaction (initial notification, with a 15-day written follow-up).
- **15 calendar days** — other **serious and unexpected** suspected adverse reactions, and certain aggregate/other-study findings and clinically important increased rates.

Notifying investigators is not a courtesy — it keeps every site's risk information current and feeds each investigator's own IRB-notification duty. The full clock mechanics are on [[safety-report-timelines-7-15-day]].

## Stage 4 — IRB and DSMB notification

Two further arrows run in parallel with the FDA submission:

- **Investigator → IRB.** The investigator reports **unanticipated problems involving risks to subjects or others** to the reviewing [[irb-iec]] per [21 CFR 56.108(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-56/subpart-C/section-56.108), [312.66](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.66), and IRB policy. Not every SAE is an unanticipated problem, and not every unanticipated problem is an SAE — the mapping is a human judgment, and it flows through the [[irb-review-workflow]].
- **Sponsor → DSMB/DMC.** Where the trial has a [[dsmb-dmc]], expedited safety information and the periodic safety rollup feed the committee's review per its [[dsmb-charter|charter]] and the [[dsmb-workflow]]. A DMC recommendation that changes the risk profile loops back to the sponsor and, through it, to the IRB and any [[annual-reporting-and-amendments|protocol amendment]].

## Stage 5 — Aggregate rollup

Individual expedited reports roll up annually into the [[ind-annual-report-dsur|IND annual report]] under [21 CFR 312.33](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.33) (satisfiable by the ICH E2F **DSUR**), which flows to FDA and informs the IRB and DMC. Emerging safety findings also drive [[investigators-brochure|Investigator's Brochure]] updates ([312.55(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.55)), which recalibrate "expectedness" for every subsequent case — closing the loop back to Stage 2.

## The full routing map

```
AE captured at site
   │  (investigator judgment: serious?)
   ▼
SAE ──immediately (312.64(b))──▶ SPONSOR safety review (312.32(b))
                                      │
                     safety physician: causal? unexpected? serious?   ◀── NON-DELEGABLE
                                      │
                            ┌─────────┴──────────┐
                        SUSAR / expedited     not expedited-reportable
                            │                     │
        7-day (fatal/LT) / 15-day (other)     logged; aggregated
        (312.32(c))                               │
            │                                     │
   ┌────────┼───────────────┐                     │
   ▼        ▼               ▼                      ▼
  FDA   all investigators  (site→IRB unanticipated-problem, 56.108(b))
                │                                  │
                ▼                                  ▼
         sponsor→DSMB (charter)          annual rollup: 312.33 / E2F DSUR
                │                                  │
        continue/modify/stop rec ──▶ sponsor ──▶ FDA + IRB + IB update (312.55(b))
```

Every node's *arrows* — timing and routing — are OSSICRO's coordination value; every node's *judgment* is a human's. See the canonical [[inter-entity-document-flow-map]].

> [!interpretive] OSSICRO position
> OSSICRO separates the **clerical/timeliness layer** it may automate from the **medical-judgment layer** it may not. It captures the case in E2B(R3) structure, codes descriptive fields (MedDRA-style term assignment surfaced for confirmation, not machine-final), drafts the [[form-fda-3500a-medwatch|3500A]] / narrative, runs the [[safety-clock-engine]] to compute and escalate the 7-/15-day deadline, and routes to every downstream recipient on the map. It holds each report in a gated state — "awaiting causality/seriousness determination by [named medical monitor]" — until the human closes the gate, and **submission to FDA is an explicit human act**. Provenance of every auto-populated field is recorded per the [[draft-provenance-model]] for the Part-11 audit trail.

## OSSICRO engine behavior

- **Generate:** builds the E2B(R3)-structured case from site capture; drafts the [[form-fda-3500a-medwatch|3500A]]/narrative and the investigator-notification and IRB/DMC cover artifacts.
- **Check:** verifies the minimum ICSR elements (identifiable patient, identifiable reporter, suspect product, event), the IND/protocol numbers, and the completeness of each downstream notification; flags gaps on the [[completeness-ledger]].
- **Validate:** holds the report behind the causality/seriousness/expectedness gate; on human classification as expedited-reportable, resolves the clock and report type, opens the FDA-submission (human-authorized), all-investigator, IRB, and DMC routing tasks, and escalates as the [[safety-clock-engine]] deadline runs — never filing and never making the causality call itself.

## Related
- [[safety-report-timelines-7-15-day]]
- [[form-fda-3500a-medwatch]]
- [[ind-safety-report]]
- [[safety-reporting-lifecycle]]
- [[pharmacovigilance-safety]]
- [[medical-monitor]]
- [[safety-clock-engine]]
- [[dsmb-workflow]]
- [[irb-review-workflow]]
- [[ind-annual-report-dsur]]
- [[investigators-brochure]]
- [[inter-entity-document-flow-map]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 312.32 — IND safety reporting](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
- [21 CFR 312.64 — Investigator reports (SAE to sponsor)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.64)
- [21 CFR 312.66 — Assurance of IRB review](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.66)
- [21 CFR 56.108 — IRB functions and operations (unanticipated problems)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-56/subpart-C/section-56.108)
- [21 CFR 312.33 — Annual reports](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.33)
- [FDA — Safety Reporting Requirements for INDs and BA/BE Studies (guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-reporting-requirements-inds-and-babe-studies)
- [ICH E2A — Clinical Safety Data Management: Definitions and Standards for Expedited Reporting](https://www.ich.org/page/efficacy-guidelines)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06, PDF)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
