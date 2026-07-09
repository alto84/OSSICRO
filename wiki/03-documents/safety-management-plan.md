---
title: "Safety Management Plan — AE/SAE Workflow, Causality Routing, and 7/15-Day Timelines"
section: "03-documents"
status: mixed
governing_authority:
  - "21 CFR 312.32 (IND safety reporting)"
  - "21 CFR 312.64(b) (investigator SAE reporting to sponsor)"
  - "21 CFR 312.33 (annual reports)"
  - "ICH E2A; ICH E6(R3) Section 5 (safety assessment and reporting)"
tags: [role/pharmacovigilance-safety, role/medical-monitor, role/sponsor, cfr/312, ich/e2a, lifecycle/safety, ossicro/gating, ossicro/engine, status/mixed]
aliases: ["safety management plan", "SMP", "pharmacovigilance plan", "safety plan", "DSMP"]
updated: 2026-07-09
---

# Safety Management Plan — AE/SAE Workflow, Causality Routing, and 7/15-Day Timelines

> [!authority] Governing authority
> 21 CFR 312.32 (IND safety reporting — definitions, 7-day and 15-day expedited timelines); 21 CFR 312.64(b) (investigator reports SAEs to the sponsor immediately); 21 CFR 312.33 (IND annual report); ICH E2A (clinical safety data management — definitions and standards for expedited reporting); ICH E6(R3) §5 (sponsor safety assessment and reporting; investigator-brochure currency). Status: **Mixed** — the reporting obligations and timelines are **confirmed** black-letter law; the written safety management plan that operationalizes them is best practice; the causality/seriousness/expectedness determinations at the core of the workflow are **non-delegable** human medical judgments.

The **Safety Management Plan (SMP)** — also called the pharmacovigilance plan or Data Safety Monitoring Plan (DSMP) — is the written procedure by which a sponsor (here, typically a [[sponsor-investigator]]) collects adverse events, assesses them, determines expedited-reporting obligations, and discharges those obligations to FDA, investigators, the [[irb-iec|IRB]], and any [[dsmb-dmc|DSMB]]. It is the operating manual for the safety obligations of [21 CFR 312.32](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32) and the safety monitoring criterion the IRB checks under [21 CFR 56.111(a)(6)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-56/subpart-C/section-56.111).

OSSICRO drafts the SMP, computes the reporting clocks, pre-populates the [[form-fda-3500a-medwatch|3500A]]/[[ind-safety-report|IND safety report]], and routes cases to the qualified reviewer. It never adjudicates seriousness, causality, or expectedness, and it never files a report.

## Core definitions (21 CFR 312.32(a); ICH E2A)

The reporting obligation turns on four defined terms; getting them right is the whole game.

- **Adverse event (AE):** any untoward medical occurrence in a participant administered the drug, whether or not drug-related.
- **Serious adverse event (SAE):** an AE resulting in death, life-threatening event, inpatient hospitalization or prolongation, persistent/significant disability or incapacity, congenital anomaly/birth defect, or an important medical event requiring intervention to prevent one of these.
- **Suspected adverse reaction (SAR):** an AE for which there is a **reasonable possibility** the drug caused it — a causality standard less than "definite" but more than a mere temporal association.
- **Unexpected:** an AE not listed in the [[investigators-brochure|Investigator's Brochure]] (or, for a marketed drug, the labeling), or listed but more severe/specific than described.

The reportable event to FDA — a **SUSAR** in common usage — is one that is **serious AND unexpected AND a suspected adverse reaction** (all three). Each of the three is a human judgment.

## AE/SAE workflow

```
Site captures AE ──► Investigator assesses seriousness ──► SAE? ──► report to sponsor immediately (312.64(b))
        │                                                              │
        ▼                                                              ▼
   record in source/CRF                          Sponsor safety function intake + code (MedDRA)
                                                                       │
                                                                       ▼
                                          Medical monitor: seriousness · causality · expectedness  ◄── NON-DELEGABLE
                                                                       │
                                   ┌───────────────────┬───────────────┴───────────────┐
                                   ▼                   ▼                                ▼
                        serious+unexpected+SAR   fatal/life-threatening,        not all-three ⇒
                        (not fatal/LT)           unexpected, SAR                aggregate/annual only
                                   │                   │
                             15-day clock         7-day clock (+15-day
                             (312.32(c)(1))       written follow-up)
                                   │                   │
                                   ▼                   ▼
                    Draft 3500A / narrative ──► human authorizes ──► FDA submission (human act)
                                   │
                                   ▼
             Notify all participating investigators (312.32(c); 312.55(b)) ──► IRB (unanticipated problem) ──► DSMB
```

Every arrow after the medical-monitor node is gated on that human determination. OSSICRO drives the arrows; it does not make the node's decision.

## The two clocks (21 CFR 312.32(c))

| Trigger | Deadline | Basis | Follow-up |
|---------|----------|-------|-----------|
| Serious + unexpected + suspected adverse reaction (not fatal/life-threatening) | **15 calendar days** from the sponsor's determination it qualifies | 312.32(c)(1)(i) | Follow-up information reported as it becomes available |
| **Unexpected fatal or life-threatening** suspected adverse reaction | **7 calendar days** from the sponsor's initial receipt (by any means) | 312.32(c)(2) | Complete written **15-day** IND safety report thereafter |
| Aggregate findings (clinical/epidemiologic, pooled analyses, animal/in vitro showing risk; clinically important increased rate) | **15 calendar days** | 312.32(c)(1)(i)-(iv) | As applicable |
| Non-expedited events | **IND annual report** | [[ind-annual-report-dsur|312.33]] / ICH E2F DSUR | Annual rollup |

The clocks are arithmetic once the human determination is made; OSSICRO computes and escalates them (see [[safety-clock-engine]]). What starts a clock — the determination that an event is serious, unexpected, and a suspected adverse reaction — is not arithmetic.

## Causality routing

The SMP specifies the routing every SAE follows to reach the qualified reviewer:

1. **Intake** — the SAE arrives from the investigator (312.64(b), immediately) into the sponsor safety function; minimum ICSR elements confirmed (identifiable patient, identifiable reporter, suspect product, event).
2. **Coding** — the event is coded (MedDRA) and structured to the ICH E2B(R3) element set.
3. **Medical assessment** — the [[medical-monitor]] (a qualified physician) determines **seriousness**, **causality** ("reasonable possibility"), and **expectedness** against the IB. *This is the non-delegable node.*
4. **Classification** — the determination resolves the report type and clock (7-day / 15-day / aggregate / none-expedited).
5. **Drafting** — OSSICRO renders the [[form-fda-3500a-medwatch|3500A]] or narrative [[ind-safety-report]] from the structured case.
6. **Authorization and submission** — a human authorizes; submission to FDA is a human act.
7. **Distribution** — notify all participating investigators (312.32(c), 312.55(b)); the site notifies its IRB of unanticipated problems; feed the DSMB per the [[dsmb-workflow]].
8. **Reconciliation** — periodic reconciliation of the safety database against the partner's (see below) and against the [[clinical-study-report|CSR]]/annual-report line listings.

## Reconciliation with the pharma partner

Where a pharma partner supplies the investigational product — as an IIS supporter (Mode B) or as sponsor with the physician as a site (Mode A) — a **Safety Data Exchange Agreement (SDEA)** governs bidirectional SAE/SUSAR exchange, timelines, and reconciliation, and must respect the Medical-Affairs / Clinical-Development firewall ([[pharma-partner-sponsor]], [[pharma-partner-interface-iis]]). The SMP names the SDEA counterpart, the exchange timelines (tighter than the regulatory clock so each party can meet its own), and the periodic reconciliation cadence. OSSICRO tracks the exchange and flags reconciliation discrepancies; it does not negotiate or execute the SDEA.

## SMP section map

| # | Section | Contents |
|---|---------|----------|
| 1 | Scope, definitions, roles | AE/SAE/SAR/unexpected definitions; named medical monitor, safety function, investigators |
| 2 | AE/SAE collection | Capture at site; investigator-to-sponsor immediacy (312.64(b)); source/CRF |
| 3 | Assessment workflow | Seriousness, causality, expectedness routing to the medical monitor |
| 4 | Expedited reporting | 7-day / 15-day clock logic; report format (3500A / narrative / E2B) |
| 5 | Distribution | Investigator, IRB, DSMB notification obligations |
| 6 | Aggregate/annual | 312.33 annual report / ICH E2F DSUR rollup |
| 7 | Partner reconciliation | SDEA reference; exchange timelines; reconciliation cadence |
| 8 | IB currency | Updating the [[investigators-brochure]] as the safety profile evolves (E6(R3) §5) |
| 9 | Documentation / TMF | Where safety records live; audit trail (ALCOA++) |

## Non-delegable gate

> [!warning] Non-delegable
> The determinations of **seriousness, causality ("reasonable possibility"), and expectedness** — which decide whether and on which clock an IND safety report is owed — are medical judgments owned by the sponsor's qualified [[medical-monitor|medical monitor / safety physician]] under 21 CFR 312.32(a) and ICH E2A. OSSICRO must never auto-adjudicate causality, never machine-set seriousness, never machine-classify the report type, and never file a report to FDA. The engine performs intake, coding to the E2B(R3) structure, clock computation, draft rendering, and routing; a qualified human assesses, classifies, and authorizes; submission is a human act. The sponsor's ultimate accountability for safety review and reporting is not transferable to software (21 CFR 312.52; E6(R3) §5 oversight). See [[non-delegable-functions-and-gates]].

## OSSICRO engine behavior
- **Generate:** drafts the SMP from the protocol and study attributes; drafts individual 3500A/IND safety reports from structured cases.
- **Check:** verifies minimum ICSR elements; confirms the SMP names a medical monitor, the SDEA counterpart, and the distribution list; flags a missing IB-currency provision.
- **Validate:** holds each case in a gated state until the medical monitor sets seriousness, causality, and expectedness; only then does the [[safety-clock-engine]] resolve the report type and deadline and make the case authorizable. The engine computes and escalates the clock but never advances a case past the causality gate and never submits.

## Related
- [[ind-safety-report]]
- [[form-fda-3500a-medwatch]]
- [[safety-report-timelines-7-15-day]]
- [[safety-reporting-workflow]]
- [[safety-reporting-lifecycle]]
- [[pharmacovigilance-safety]]
- [[medical-monitor]]
- [[safety-clock-engine]]
- [[ind-annual-report-dsur]]
- [[dsmb-charter]]
- [[monitoring-plan]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 312.32 — IND safety reporting](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
- [21 CFR 312.64 — Investigator reports](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.64)
- [21 CFR 312.33 — Annual reports](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.33)
- [FDA — Safety Reporting Requirements for INDs and BA/BE Studies (guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-reporting-requirements-inds-and-babe-studies)
- [ICH E2A — Clinical Safety Data Management: Definitions and Standards for Expedited Reporting](https://www.ich.org/page/efficacy-guidelines)
- [ICH E6(R3) Good Clinical Practice — Step 4 Final Guideline (2025)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
