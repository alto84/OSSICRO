---
title: "Patient–Trial Matching: Overview & HIPAA Gating"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "HIPAA Privacy Rule — 45 CFR 164.512(i)(1)(ii) (reviews preparatory to research)"
  - "45 CFR 164.508 (individual authorization); 45 CFR 164.512(i)(1)(i) (IRB/Privacy-Board waiver)"
  - "45 CFR 164.514(b) (de-identification); 45 CFR 164.514(e) (limited data set)"
  - "21 CFR 312.60 (investigator adherence; subject selection)"
  - "FDA Draft Guidance — AI to Support Regulatory Decision-Making (2025-01-07, FDA-2024-D-4689)"
tags: [ossicro/matching, ossicro/gating, usc/hipaa, cfr/312, lifecycle/feasibility, status/mixed]
aliases: ["Patient Trial Matching", "Matching Overview", "Matching and HIPAA"]
updated: 2026-07-09
---

# Patient–Trial Matching: Overview & HIPAA Gating

> [!authority] Governing authority
> HIPAA Privacy Rule [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512) (review preparatory to research), with the transition bases [45 CFR 164.508](https://www.ecfr.gov/current/title-45/section-164.508) (individual authorization) and [45 CFR 164.512(i)(1)(i)](https://www.ecfr.gov/current/title-45/section-164.512) (IRB/Privacy-Board waiver); [45 CFR 164.514(b)/(e)](https://www.ecfr.gov/current/title-45/section-164.514) (de-identification, limited data set); investigator subject-selection duty [21 CFR 312.60](https://www.ecfr.gov/current/title-21/section-312.60). Status: **Mixed** — the privacy boundary and the non-delegable eligibility determination are black-letter (confirmed); OSSICRO's semantic/adjudication design and its context-of-use risk tiering are interpretive positions, marked inline.

Patient–trial matching is OSSICRO's discovery front door. A clinician has a patient (or a screening panel) and needs to know whether an early-phase program — an open trial, an investigator-initiated study concept, or an expanded-access route — plausibly fits, *before* any regulated research relationship exists. This page is the umbrella: it states what matching is, where the privacy line sits, how matching outputs are classified, and how a match hands off to a lifecycle pathway. The mechanical multi-directional retrieval and adjudication live in the [[matching-engine]]; the underlying feeds live in [[data-integrations-ctgov-pubmed]]; the code-enforced privacy boundary lives in the [[privacy-state-machine]].

The single most consequential fact on this page is a privacy fact, not a search-quality fact: **identifying a candidate program from a patient's protected health information (PHI) is a review preparatory to research** — a use HIPAA permits without authorization, but which does **not** authorize enrollment, recruitment contact beyond the covered entity's existing treatment relationship, or any PHI leaving the covered entity. The boundary between "matching" and "enrolling" is a HIPAA boundary, and OSSICRO enforces it in code, not in policy prose.

## What matching is — and is not

Matching produces **draft, advisory candidate lists with cited rationale**. It is decision *support*, surfaced for a qualified human. It is never:

- an **eligibility determination** (the investigator's non-delegable call under [21 CFR 312.60](https://www.ecfr.gov/current/title-21/section-312.60));
- an **enrollment decision** or an offer of enrollment;
- a **treatment recommendation** or clinical advice;
- a basis to **contact** a patient for recruitment beyond what the covered entity's own treatment relationship already permits; or
- an act that **moves PHI** outside the covered-entity boundary.

Matching answers two feasibility questions kept explicitly separate (see [[feasibility-and-patient-matching]]): *trial/therapy feasibility* (is there a candidate program for this patient?) and *site feasibility* (could this physician/site run it?). Both are answered at draft status.

## The HIPAA preparatory-to-research boundary (confirmed)

[45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512) permits a covered entity to use or disclose PHI for activities **preparatory to research** upon representations that:

1. the use/disclosure is sought **solely to prepare a research protocol** or for similar preparatory purposes;
2. **no PHI will be removed** from the covered entity in the course of the review; and
3. the PHI is **necessary** for the research purposes.

Applied to OSSICRO, these three conditions dictate architecture. Because no PHI may be removed and only the minimum necessary may be touched, the matching computation runs **local-first, inside the covered-entity trust boundary, with no PHI egress**, reading the **minimum necessary** on an **ephemeral, audited** basis. That is precisely the design of the [[privacy-state-machine]] and the reason an [[offline-local-deployment|offline single-container deployment]] exists: the privacy rule, not a preference, drives the topology. Where a use can be satisfied by de-identified data ([45 CFR 164.514(b)](https://www.ecfr.gov/current/title-45/section-164.514)) or a limited data set under a data-use agreement ([45 CFR 164.514(e)](https://www.ecfr.gov/current/title-45/section-164.514)), OSSICRO prefers the least-identifiable form that answers the feasibility question.

> [!warning] Non-delegable
> The preparatory-review **representations** under [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512) are made by the covered entity / a responsible human — never by software. OSSICRO structures, minimizes, and logs the review; it does not "represent" anything to the covered entity, and it never removes PHI. The judgment that a given use is genuinely preparatory and minimum-necessary is the covered entity's.

## The transition gate: matching → enrollment (confirmed)

Preparatory review is a ceiling, not a runway. It does **not** authorize enrolling the patient, exporting PHI to a pharma sponsor or to the OSSICRO [[micro-cro-accountable-layer|Micro-CRO]], or recruitment contact beyond the treatment relationship. Crossing from matching to enrollment requires one of:

- **Individual authorization** under [45 CFR 164.508](https://www.ecfr.gov/current/title-45/section-164.508) — typically the HIPAA authorization bundled with the [[informed-consent-form|informed-consent]] process; or
- **IRB / Privacy-Board waiver** of authorization under [45 CFR 164.512(i)(1)(i)](https://www.ecfr.gov/current/title-45/section-164.512), with the three waiver criteria documented.

OSSICRO models this as a **hard, logged state transition** in the [[privacy-state-machine]]: enrollment-phase artifacts (final consent packet, screening-log creation, any PHI disclosure to a sponsor) remain unavailable until an authorization or waiver basis is recorded. See [[enrollment-and-consent]] and [[hipaa-and-privacy-gating]].

```
[ PREPARATORY REVIEW ]  164.512(i)(1)(ii)
   local-first · min-necessary · no PHI egress · ephemeral audited reads
          │
          │  hard, logged gate  ── requires ──▶ 164.508 authorization
          │                                  OR  164.512(i)(1)(i) waiver
          ▼
[ ENROLLMENT ]  consent event · screening log · sponsor disclosure
```

## Matching is a higher-influence context of use (interpretive)

> [!interpretive] OSSICRO position
> Document *drafting for human review* is a low-influence/low-consequence context of use (COU) under the FDA 2025 draft AI-credibility framework ([FDA-2024-D-4689](https://www.federalregister.gov/documents/2025/01/07/2024-31542/considerations-for-the-use-of-artificial-intelligence-to-support-regulatory-decision-making-for-drug)). **Matching is not.** A matcher that can return "no eligible trial" and thereby *gate a patient's access* has greater model influence and greater decision consequence, so OSSICRO designs and evaluates it as a higher-influence COU: (a) a **recall-first** objective so the system never silently excludes a patient; (b) a **three-valued** per-criterion verdict — met / not-met / **indeterminate-needs-data** — never a bare yes/no; (c) **cited rationale** (chart citation + eligibility-criterion citation) on every verdict; and (d) a **measured** performance claim on public benchmarks rather than an asserted one. See [[matching-eligibility-adjudication]] and [[matching-evaluation-and-benchmarks]]. The AI-credibility guidance is **draft** (comments closed 2025-04-07); this tiering argument is flagged interpretive and will be revisited when the guidance finalizes.

> [!warning] Non-delegable
> Eligibility **determination** — who actually enrolls — is the investigator's judgment ([21 CFR 312.60](https://www.ecfr.gov/current/title-21/section-312.60): adherence to protocol and its subject-selection criteria). An "indeterminate-needs-data" verdict is an invitation to a human to gather data, not a denial of access. Matching surfaces candidates with rationale; it does not adjudicate enrollment.

## Matching outputs and their status

| Output | Basis | Status | Downstream |
|--------|-------|--------|-----------|
| Candidate trial/therapy list + cited match rationale | CT.gov v2 + semantic/[[matching-mechanism-graph\|mechanism]] layer | Draft/advisory | [[the-three-pathways-triage]] |
| Per-criterion eligibility verdicts (met/not-met/indeterminate) | Retrieve→adjudicate over chart + criteria | Draft/advisory | Investigator eligibility call |
| Supporting-evidence / safety-signal digest | PubMed + openFDA ([[data-integrations-ctgov-pubmed]]) | Draft/advisory | Risk-benefit discussion (human) |
| Preparatory-review audit record | 164.512(i)(1)(ii) representations + ephemeral-read log | Confirmed record | [[privacy-state-machine]] audit trail |

## Where a match hands off

- Candidate on an **open pharma protocol** → Mode A site activation ([[site-activation]], [[single-patient-site-and-pharma-acceptance]]).
- No fitting trial, the physician will run one → Mode B ([[pre-ind-and-ind-preparation]], [[two-modes-site-vs-sponsor-investigator]]).
- No trial fits, single patient, drug exists → [[expanded-access-workflow]] / [[single-patient-site-enrollment]].

Each hand-off is a HIPAA state transition first and a document-generation event second. The [[communication-hub]] carries the resulting artifacts between actors only after the applicable gate is recorded.

## The hard principle, stated for matching

OSSICRO drafts complete, cited discovery output so a clinician is not defeated by not knowing a trial exists. It does not decide who is eligible, does not enroll, does not contact patients on its own authority, and does not move PHI. Every non-delegable act on this workflow — the preparatory-review representation, the authorization/waiver, the eligibility determination, the enrollment decision — is surfaced and gated to a qualified human (see [[non-delegable-functions-and-gates]]).

## Related
- [[matching-engine]]
- [[matching-eligibility-adjudication]]
- [[matching-mechanism-graph]]
- [[matching-evaluation-and-benchmarks]]
- [[data-integrations-ctgov-pubmed]]
- [[privacy-state-machine]]
- [[hipaa-and-privacy-gating]]
- [[feasibility-and-patient-matching]]
- [[enrollment-and-consent]]
- [[the-three-pathways-triage]]
- [[communication-hub]]
- [[non-delegable-functions-and-gates]]

## Sources
- [45 CFR 164.512 — Uses and disclosures for which authorization is not required (eCFR)](https://www.ecfr.gov/current/title-45/section-164.512)
- [45 CFR 164.508 — Uses and disclosures for which an authorization is required (eCFR)](https://www.ecfr.gov/current/title-45/section-164.508)
- [45 CFR 164.514 — De-identification and limited data sets (eCFR)](https://www.ecfr.gov/current/title-45/section-164.514)
- [21 CFR 312.60 — General responsibilities of investigators (eCFR)](https://www.ecfr.gov/current/title-21/section-312.60)
- [HHS OCR — Research and the HIPAA Privacy Rule (preparatory-to-research guidance)](https://www.hhs.gov/hipaa/for-professionals/special-topics/research/index.html)
- [FDA Draft Guidance — Considerations for the Use of AI to Support Regulatory Decision-Making for Drug and Biological Products (Federal Register, 2025-01-07)](https://www.federalregister.gov/documents/2025/01/07/2024-31542/considerations-for-the-use-of-artificial-intelligence-to-support-regulatory-decision-making-for-drug)
