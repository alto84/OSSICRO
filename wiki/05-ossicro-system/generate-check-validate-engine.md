---
title: "The Generate / Check / Validate Engine"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "21 CFR 312.23 (IND content and format)"
  - "21 CFR 312.53(c) (Form FDA 1572; investigator information)"
  - "ICH E6(R3) Appendix C (Essential Records)"
  - "21 CFR Part 11 (Electronic Records; Electronic Signatures)"
  - "FDA Draft Guidance on AI to Support Regulatory Decision-Making (Jan 2025)"
tags: [ossicro/engine, ossicro/gating, ossicro/ai-credibility, cfr/312, cfr/11, ich/e6r3, ich/m11, status/interpretive]
aliases: ["Generate/Check/Validate", "GCV Engine", "The Engine"]
updated: 2026-07-09
---

# The Generate / Check / Validate Engine

> [!authority] Governing authority
> The engine's outputs are governed by the predicate rules they instantiate — [21 CFR 312.23](https://www.law.cornell.edu/cfr/text/21/312.23) for IND content, [21 CFR 312.53(c)](https://www.law.cornell.edu/cfr/text/21/312.53) for the 1572 package, [21 CFR Part 54](https://www.law.cornell.edu/cfr/text/21/part-54) for financial disclosure, ICH E6(R3) Appendix C for essential records — and by [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) as electronic records. The engine's AI implementation is risk-tiered under the FDA 2025 AI-credibility **draft** guidance. Status: **Mixed** — the requirements each pass checks against are confirmed; the three-pass architecture and its risk-tiering are interpretive OSSICRO positions.

The engine is the operating version of the HARD LINE: OSSICRO drafts complete documentation for qualified human review and never owns a non-delegable act. Mechanically, every document moves through three passes — **generate**, **check**, **validate** — and cannot exit the pipeline except through a **human sign-off gate**. Each pass carries citations; each gate names its responsible human. The passes are described here in order, followed by the gate mechanics and the credibility tiering of the engine's own AI.

## Pass 1 — Generate

A drafting agent instantiates a template from structured study data. Inputs are the template (with verified provenance, [[external-templates-and-licenses]]), the structured `Study`/`IND`/`Site`/`Investigator` entities from the [[data-model]], and — where chart data is lawfully in scope under the [[privacy-state-machine]] — clinical facts from [[smart-on-fhir-integration]]. The ICH M11 CeSHarP structured protocol representation is the priority target schema for protocol generation (final M11 template 2025-11-19); FDA forms auto-populate from CV, site, and financial-disclosure data.

Two contracts bind the output:

1. **Provenance.** Every generated span carries a (source datum → provenance → citation) triple per [[draft-provenance-model]]. A sentence in a draft 1572 traces to the CV field or site record it came from; a protocol eligibility criterion traces to its template origin or its investigator-supplied input. Spans with no source are marked *inferred* and routed to the foregrounded review lane ([[single-pass-review-ux]]).
2. **Draft status.** The output is a DRAFT for qualified human review, watermarked as such in the document state machine ([[data-model]]). No generate-pass output is ever a filed or signed record.

## Pass 2 — Check

The check pass answers two questions: *is the package complete?* and *is it internally consistent?*

**Completeness** is validated against the essential-records matrix — ICH E6(R3) Appendix C (with E6(R2) §8 cross-numbering; see [[document-catalog]]) — applied *risk-proportionately*, not as a fixed checklist: E6(R3) makes the nature and extent of essential records depend on trial design and materiality, so the matrix is parameterized by mode ([[two-modes-site-vs-sponsor-investigator]]), phase, and risk assessment. Form-level field rules run in the same pass: the Form 1572's fields 1–9 against FDA's official completion instructions, the 3454-versus-3455 selection logic under [21 CFR Part 54](https://www.law.cornell.edu/cfr/text/21/part-54) (a disclosable interest under §54.2 forces a 3455 disclosure — it cannot be certified away on a 3454), the 1571 content-item checklist against [21 CFR 312.23(a)](https://www.law.cornell.edu/cfr/text/21/312.23). The published precedent is Vanderbilt's V-CAP, which generates a personalized required-approvals checklist from structured study inputs ([PMC3767144](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3767144/)); OSSICRO reimplements the pattern independently ([[prior-art-vcap-irex-smartirb]]).

**Adversarial pre-review and cross-document consistency** elevate the check pass beyond a checklist. An independent QC agent — structurally separate from the drafting agent, with no shared working context — red-teams the package before any human sees it: it hunts for internal contradictions, unsupported spans, stale versions, and missed conditional requirements. A deterministic consistency engine verifies that facts asserted in more than one document are identical everywhere they appear: PI name and address, IND number, protocol version and date, site identity, and sub-investigator lists must agree across the 1572, the [[delegation-of-authority-log]], the protocol signature page, and the IRB submission. The human reviewer receives the draft *and* the machine critique together — the reviewer's attention starts where the adversary found weakness.

**Output contract.** The check pass emits the [[completeness-ledger]]: every requirement in the applicable matrix graded **green** (machine-validated, with the validating rule cited), **amber** (requires human judgment — i.e., a gate), or **red** (missing data, with the exact question whose answer resolves it). "Complete documentation" in OSSICRO always means *this ledger with no unexplained reds*, never an unaudited pile of files.

## Pass 3 — Validate

A rule engine in which **every rule traces to a specific CFR or ICH subsection** — the trace is part of the rule's definition, surfaced in [[compliance-mapping]], and a rule without a citation does not ship. The encodable model is the report-type × trigger × deadline table (the pattern published by Mayo's IND/IDE office): for example, *unexpected fatal or life-threatening suspected adverse reaction* → 7-calendar-day notification under [21 CFR 312.32(c)(2)](https://www.law.cornell.edu/cfr/text/21/312.32); *serious and unexpected suspected adverse reaction* → 15-calendar-day IND safety report under [312.32(c)(1)](https://www.law.cornell.edu/cfr/text/21/312.32); *IND anniversary* → annual report within 60 days under [312.33](https://www.law.cornell.edu/cfr/text/21/312.33). Deadline computation and escalation for the safety clocks is delegated to the dedicated [[safety-clock-engine]]. Recurring compliance checks (the MD Anderson annual-audit-per-IIT-IND cadence is the model) run on schedule, not only at document creation.

The defining behavior: **every rule that touches an accountable act fails to a human gate rather than proceeding.** The validate pass can conclude "the 15-day clock would start *if* this event is a serious, unexpected, suspected adverse reaction"; it cannot conclude that it *is* one. That determination belongs to the [[medical-monitor]] under [21 CFR 312.32](https://www.law.cornell.edu/cfr/text/21/312.32), and the rule's failure mode is to open the gate and start the escalation timer, never to file.

## Human sign-off gates

A gate is a first-class object in the [[data-model]]: it names the non-delegable act, the qualified human responsible, the authority that reserves the act to them, and the evidence of discharge (a Part 11 signature per §§11.50–11.300, or a documented external event such as an IRB approval letter). No document transitions past `human-reviewed` in the state machine without its gates discharged. The master matrix is [[non-delegable-functions-and-gates]]; the gates the engine most frequently opens are:

| Gate | Responsible human | Authority |
|---|---|---|
| 1571 signature (sponsor attestation) | Sponsor / [[sponsor-investigator]] | [21 CFR 312.23(a)(1)](https://www.law.cornell.edu/cfr/text/21/312.23); Form FDA 1571 |
| 1572 signature (investigator commitment) | [[investigator]] | [21 CFR 312.53(c)(1)](https://www.law.cornell.edu/cfr/text/21/312.53) |
| Informed consent (the event, not the form) | Investigator or qualified designee | [21 CFR 50.20](https://www.law.cornell.edu/cfr/text/21/50.20); see [[informed-consent-document-vs-event]] |
| IRB approval | [[irb-iec|IRB/IEC]] | [21 CFR 56.111](https://www.law.cornell.edu/cfr/text/21/56.111) |
| Seriousness / causality / expectedness | [[medical-monitor]] | [21 CFR 312.32](https://www.law.cornell.edu/cfr/text/21/312.32); ICH E2A |
| Statistical sign-off (SAP, analyses) | [[biostatistician]] | ICH E9 / E9(R1) |
| Submission to FDA (any filing) | Sponsor / sponsor-investigator | 21 CFR Part 312; explicit human-authorized action |

> [!warning] Non-delegable
> The engine drafts the 1572; the investigator signs it. The engine pre-populates the 3500A and computes the deadline; the medical monitor makes the causality call that determines whether a report is due at all. The engine assembles the IRB package and pre-checks it against [21 CFR 56.111](https://www.law.cornell.edu/cfr/text/21/56.111); the IRB alone approves. Automating past any of these gates is not a product decision available to OSSICRO — it is foreclosed by the cited regulations. See [[non-delegable-functions-and-gates]].

## Review ergonomics

Gates only protect if humans actually exercise judgment at them; a reviewer facing 200 undifferentiated pages will rubber-stamp. The engine therefore triages reviewer attention through [[single-pass-review-ux]]: deterministic spans (machine-verifiable transcriptions of source data) and boilerplate spans (unmodified template text) are presented collapsed with their provenance available, while inferred or interpretive spans — the judgment calls — are foregrounded. The amber items of the [[completeness-ledger]] are exactly the gate list for the package. This is an interpretive design position: the regulations require qualified review, and this architecture is OSSICRO's mechanism for making one-pass qualified review real.

## Credibility tiering of the engine's own AI

The engine's AI outputs are risk-tiered under the FDA draft guidance *Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making for Drug and Biological Products* (published 2025-01-07, docket FDA-2024-D-4689; comments closed 2025-04-07; **still draft**), which defines a 7-step credibility assessment around a stated context of use (COU) and a model-risk judgment of model influence × decision consequence.

> [!interpretive] OSSICRO position
> Document *drafting for mandatory qualified human review* is a low-influence, low-consequence COU: the model does not make the regulatory decision, a named human does, with the machine critique and provenance in front of them. This keeps the generate and check passes in a defensible lower-credibility-burden tier. Two deliberate exceptions: (1) **matching** can gate a patient's access to a trial and is classified as a higher-influence COU, with a measured evaluation harness ([[matching-evaluation-and-benchmarks]]); (2) the deterministic validate rules are not AI at all and are validated as conventional software under Part 11 §11.10(a). This tiering is OSSICRO's argument under a draft guidance, flagged as such wherever it appears. See [[part-11-and-ai-credibility]].

Every AI contribution is attributed in the Part 11 audit trail — model and version, input hash, timestamp, human reviewer identity and disposition ([[claude-sdk-ai-in-the-loop]], [[data-model]]).

## Related

- [[architecture]]
- [[data-model]]
- [[non-delegable-functions-and-gates]]
- [[completeness-ledger]]
- [[draft-provenance-model]]
- [[single-pass-review-ux]]
- [[compliance-mapping]]
- [[safety-clock-engine]]
- [[part-11-and-ai-credibility]]
- [[claude-sdk-ai-in-the-loop]]
- [[document-catalog]]
- [[form-fda-1572-statement-of-investigator]]
- [[form-fda-3454-3455-financial-disclosure]]
- [[prior-art-vcap-irex-smartirb]]

## Sources

- [21 CFR 312.23 — IND content and format](https://www.law.cornell.edu/cfr/text/21/312.23)
- [21 CFR 312.32 — IND safety reporting](https://www.law.cornell.edu/cfr/text/21/312.32)
- [21 CFR 312.33 — Annual reports](https://www.law.cornell.edu/cfr/text/21/312.33)
- [21 CFR 312.53 — Selecting investigators and monitors](https://www.law.cornell.edu/cfr/text/21/312.53)
- [21 CFR Part 54 — Financial disclosure by clinical investigators](https://www.law.cornell.edu/cfr/text/21/part-54)
- [21 CFR 56.111 — Criteria for IRB approval of research](https://www.law.cornell.edu/cfr/text/21/56.111)
- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025, PDF) — Appendix C, Essential Records](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [ICH M11 — Clinical Electronic Structured Harmonised Protocol (CeSHarP)](https://www.ich.org/page/multidisciplinary-guidelines)
- [FDA Draft Guidance — Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making for Drug and Biological Products (Jan 2025, FDA-2024-D-4689)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological)
- [Form FDA 1572 — Statement of Investigator (official form)](https://www.fda.gov/media/78830/download)
- [FDA — Instructions for Filling Out Form FDA 1572](https://www.fda.gov/media/79326/download)
- Byrne DW et al., "Vanderbilt Customized Action Plan (V-CAP)" — rules-driven personalized regulatory checklist ([PMC3767144](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3767144/))
