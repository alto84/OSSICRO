---
title: "Annual Reporting and IND Amendments"
section: "02-lifecycle"
status: mixed
governing_authority:
  - "21 CFR 312.33 (annual reports)"
  - "21 CFR 312.30 (protocol amendments)"
  - "21 CFR 312.31 (information amendments)"
  - "ICH E2F (DSUR)"
tags: [lifecycle/annual, cfr/312, ich/e2f, fda-form/1571, ossicro/engine, ossicro/gating]
aliases: ["IND annual report", "DSUR", "protocol amendment", "information amendment"]
updated: 2026-07-09
---

# Annual Reporting and IND Amendments

> [!authority] Governing authority
> 21 CFR 312.33 (annual reports, due within 60 days of the IND anniversary); 21 CFR 312.30 (protocol amendments — new protocols, protocol changes, new investigators); 21 CFR 312.31 (information amendments); ICH E2F (Development Safety Update Report, accepted by FDA in lieu of the 312.33 annual report per the FDA E2F guidance); 21 CFR 56.108–56.109 (parallel IRB continuing-review and amendment-approval track). Status: **Mixed** — the filing obligations and content lists are confirmed; DSUR substitution mechanics and OSSICRO's assembly automation are marked where interpretive.

An effective IND is a living application. Between activation and [[closeout]], the [[sponsor]] (or [[sponsor-investigator]]) maintains it through three amendment channels — protocol amendments (312.30), information amendments (312.31), and IND safety reports (312.32, covered at [[safety-reporting-lifecycle]]) — plus one aggregate obligation, the annual report (312.33). 21 CFR 312.50 makes "maintaining an effective IND" an affirmative sponsor duty; a lapsed or unmaintained IND places every ongoing subject exposure outside its legal shelter. In parallel, the IRB runs its own continuing-review and amendment-approval clock under 21 CFR 56.108–56.109, which is independent of FDA's.

## 1. The annual report (21 CFR 312.33)

Within **60 days of the anniversary date that the IND went into effect**, the sponsor must submit a brief report of the progress of the investigation, containing:

### 1.1 Individual study information — 312.33(a)
For each study in progress or completed during the year: title, purpose, patient population, study status; total planned subjects, entered to date (by age group, sex, race), completed, and discontinued; and, for completed or interim-analyzed studies, a brief description of any available results.

### 1.2 Summary information — 312.33(b)
- Narrative or tabular summary of the **most frequent and most serious** adverse experiences by body system;
- Summary of **all IND safety reports** submitted during the year;
- List of **subjects who died** during participation, with cause of death for each;
- List of subjects who **dropped out in association with any adverse experience**, whether or not drug related;
- Description of what, if anything, was learned pertinent to an **understanding of the drug's action**;
- List of **preclinical studies** (including animal studies) completed or in progress during the year, with summary of major findings;
- Summary of significant **manufacturing or microbiological changes**.

### 1.3 Forward-looking and change-tracking content — 312.33(c)–(f)
- Description of the **general investigational plan for the coming year**, replacing the plan submitted the prior year (312.33(c));
- If the [[investigators-brochure]] was revised, a **description of the revision** and reference to the date of submission of the revised IB (312.33(d));
- For Phase 1, a description of any **significant Phase 1 protocol modifications** made during the year and not previously reported in a protocol amendment (312.33(e));
- A brief summary of significant **foreign marketing developments** (approval or withdrawal/suspension in any country) (312.33(f)).

FDA may also request a **log of outstanding business** with respect to the IND (312.33(g)).

### 1.4 DSUR substitution (ICH E2F)

FDA's guidance adopting ICH E2F permits sponsors to submit a **Development Safety Update Report** in place of the 312.33 annual report. The DSUR is anchored to the **Development International Birth Date** (DIBD) and its structure (interval line listings, cumulative summary tabulations of serious adverse reactions, benefit-risk evaluation) exceeds the 312.33 content floor. For a sponsor-investigator study with a pharma partner supplying drug, the DSUR is usually the better instrument: the partner's own DSUR cycle and reference safety information can be reconciled once per year. See [[ind-annual-report-dsur]] for the document explainer.

> [!interpretive] OSSICRO position
> OSSICRO assembles the annual report/DSUR from data it already holds — the safety database line listings, IND safety-report log, enrollment tallies, IB version history, and amendment log — so the annual filing is a compilation event, not an archaeology project. The compiled draft is presented against a [[completeness-ledger]] (every 312.33 element green/amber/red) for the sponsor-investigator's review and signature. The compilation is automation; the accuracy attestation and submission are not.

## 2. Protocol amendments (21 CFR 312.30)

Once an IND is in effect, the sponsor amends it as needed to ensure the clinical investigations are conducted according to protocols included in the application.

### 2.1 New protocol — 312.30(a)
A study not covered by a protocol already in the IND requires a protocol amendment containing the new protocol. The study may begin **once the protocol has been submitted to FDA and the IRB has approved it** (21 CFR 312.40(b)(2)–(3), 312.66) — there is no new 30-day wait for an already-effective IND.

### 2.2 Change in protocol — 312.30(b)
A protocol amendment is required for:
- **Phase 1:** any change that **significantly affects the safety of subjects**;
- **Phase 2/3:** any change that significantly affects **subject safety, the scope of the investigation, or the scientific quality of the study**.

The regulation's own examples: an increase in dose or duration of exposure; a significant increase in the number of subjects; a significant design change (e.g., adding or dropping a control group); adding a new test or procedure intended to improve monitoring for, or reduce the risk of, adverse events — or dropping a safety test. The change may be implemented **after the amendment is submitted to FDA and the IRB approves it**, with one exception: a change made to **eliminate an apparent immediate hazard to subjects** may be implemented immediately, with FDA and the IRB notified afterwards (312.30(b)(2)(ii); 21 CFR 56.108(a)(4) mirrors this on the IRB side).

### 2.3 New investigator — 312.30(c)
A new investigator may be added once the sponsor holds a completed [[form-fda-1572-statement-of-investigator|Form FDA 1572]] and qualification records; FDA must be **notified within 30 days** of the investigator being added.

### 2.4 Content, format, and timing — 312.30(d)–(e)
Every protocol amendment is submitted under a [[form-fda-1571-ind-cover|Form FDA 1571]] cover, prominently identified by type ("Protocol Amendment: New Protocol", "...Change in Protocol", "...New Investigator"). Where feasible, FDA asks that amendments be submitted **not more frequently than every 30 days**, and a protocol amendment may reference and rely on information already in the IND.

## 3. Information amendments (21 CFR 312.31)

Essential information about the IND that is **not** within the scope of a protocol amendment, an IND safety report, or the annual report is submitted as an information amendment: new toxicology, chemistry, or other technical information, or a report of the **discontinuation of a clinical investigation**. Same 1571 cover discipline, identified by subject ("Information Amendment: Chemistry, Manufacturing, and Control", "...Pharmacology-Toxicology", "...Clinical"); the same not-more-than-every-30-days feasibility request applies (312.31(c)). IB revisions travel here (with the annual report cross-referencing them under 312.33(d)) and must also be distributed to all investigators and the IRB per the sponsor's 312.55(b) duty to keep investigators informed.

## 4. The parallel IRB track

FDA's amendment channels do not discharge the ethics channel. The IRB must approve protocol and consent changes **before implementation** (except immediate-hazard changes), and conducts **continuing review** at intervals appropriate to risk, at least annually under 21 CFR 56.109(f). Approval lapses gate enrollment. OSSICRO tracks both clocks as separate deadlines with separate document packages; see [[irb-review-workflow]] and [[irb-submission-and-approval]].

> [!warning] Non-delegable
> Whether a protocol change "significantly affects" safety, scope, or scientific quality (312.30(b)) is the sponsor's scientific and medical judgment; the immediate-hazard determination is a clinical call; the annual report/DSUR is a signed sponsor attestation submitted under the 1571; and IRB approval of any amendment is the board's judgment alone. OSSICRO classifies a proposed change against the 312.30(b) criteria and drafts the package, but the classification decision, the signature, and the submission are human acts. See [[non-delegable-functions-and-gates]].

## 5. Timing summary

| Obligation | Clock | Authority |
|---|---|---|
| Annual report / DSUR | Within 60 days of IND anniversary | 312.33 |
| New protocol | Submit to FDA + IRB approval before study begins | 312.30(a) |
| Protocol change | Submit to FDA + IRB approval before implementation (immediate-hazard exception) | 312.30(b) |
| New investigator | Notify FDA within 30 days of adding | 312.30(c) |
| Information amendment | As needed; ≥30-day spacing where feasible | 312.31 |
| IRB continuing review | At least annually (risk-appropriate) | 56.109(f) |

## Related

- [[ind-annual-report-dsur]] — the document explainer
- [[safety-reporting-lifecycle]] — the expedited channel feeding the annual rollup
- [[ind-submission-and-30-day-clock]] — how the IND went into effect
- [[form-fda-1571-ind-cover]] · [[form-fda-1572-statement-of-investigator]] — the cover and investigator instruments
- [[investigators-brochure]] — IB revision mechanics
- [[irb-review-workflow]] · [[irb-submission-and-approval]] — the parallel ethics clock
- [[conduct-and-monitoring]] — where deviations that motivate amendments surface
- [[closeout]] — the final report and IND disposition
- [[completeness-ledger]] — OSSICRO's open-items contract for the filing package
- [[non-delegable-functions-and-gates]]

## Sources

- [21 CFR 312.33 — Annual reports (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.33)
- [21 CFR 312.30 — Protocol amendments (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.30)
- [21 CFR 312.31 — Information amendments (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.31)
- [21 CFR 312.55 — Informing investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.55)
- [21 CFR 56.109 — IRB review of research (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/56.109)
- [ICH E2F — Development Safety Update Report](https://database.ich.org/sites/default/files/E2F_Guideline.pdf)
- [FDA Guidance: E2F Development Safety Update Report](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e2f-development-safety-update-report)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
