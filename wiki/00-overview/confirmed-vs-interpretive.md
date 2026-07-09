---
title: "Confirmed vs. Interpretive: The Calibration Standard"
section: "00-overview"
status: confirmed
governing_authority:
  - "21 CFR 10.115 (FDA Good Guidance Practices — guidance documents are nonbinding)"
  - "21 CFR Parts 11, 50, 54, 56, 312; 45 CFR 46; 45 CFR 164 (the binding floor)"
  - "ICH guidelines as FDA-adopted guidance (E6(R3), E8(R1), E9/E9(R1), E2A, E3, M11)"
tags: [cfr/312, cfr/11, ich/e6r3, ossicro/ai-credibility, status/confirmed]
aliases: ["calibration standard", "status legend"]
updated: 2026-07-09
---

# Confirmed vs. Interpretive: The Calibration Standard

> [!authority] Governing authority
> This is a wiki-methodology page. The classification it defines rests on the legal hierarchy of the authorities themselves: statutes and codified regulations (21 CFR, 45 CFR) bind with the force of law; guidance documents — including ICH guidelines as adopted by FDA — "do not establish legally enforceable rights or responsibilities" ([21 CFR 10.115(d)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-10/section-10.115)). Status: **Confirmed** (the standard itself; the positions it registers as interpretive are, by definition, interpretive).

Every page in this wiki carries a `status` of `confirmed`, `interpretive`, or `mixed`. This page defines what those words mean, how they are assigned, and why the distinction is a safety property rather than an editorial nicety. A clinician relying on this wiki must always be able to tell whether a statement is a legal requirement FDA can enforce, or a defended OSSICRO design position that a reviewer, counsel, or FDA could reasonably contest.

## Why calibration is a safety property

OSSICRO's mission puts reference-grade documentation in front of physicians who do not have a regulatory affairs office behind them. Two failure modes follow from miscalibration, and both can harm a patient or sink a trial:

- **Understating a requirement** (marking a binding rule as optional or interpretive) produces a non-compliant submission, a clinical hold (21 CFR 312.42), or an unprotected subject.
- **Overstating a position** (presenting an OSSICRO thesis as settled law — e.g., asserting that AI-drafted regulatory text is FDA-accepted) invites a physician to rely on a claim FDA has never confirmed, discovers the gap during a BIMO inspection, and forfeits the trust the whole system depends on.

The calibration standard is therefore enforced mechanically: in page frontmatter, in inline callouts, and in the [[compliance-mapping]] manifest that traces every generated artifact to its authority.

## The three statuses

### `confirmed`
A black-letter requirement stated in, and directly cited to, a binding authority: the FD&C Act or PHS Act, 21 CFR (Parts 11, 50, 54, 56, 312 and others), the Common Rule (45 CFR 46), HIPAA (45 CFR 160/164), or FDAAA 801 / 42 CFR Part 11 (ClinicalTrials.gov). Criteria: the claim can be verified by reading the cited section; no inference beyond plain text is required. Load-bearing requirements are quoted verbatim, not paraphrased — as [[legal-thesis-3123-vs-31252]] quotes § 312.52 in full.

### `interpretive`
An OSSICRO design or thesis position: defensible, argued from cited authority, but not itself a requirement — and potentially contestable by FDA, an IRB, a sponsor, or counsel. Interpretive claims must be (a) labelled with the `> [!interpretive]` callout, (b) argued, not asserted, and (c) accompanied by the strongest known counter-consideration. An unlabelled interpretive claim is a defect to be corrected on review.

### `mixed`
A page containing both, with each interpretive claim marked inline. Most substantive pages are mixed: the regulatory floor is confirmed; the OSSICRO treatment of it is interpretive.

## The authority hierarchy behind the classes

In descending order of bindingness, with the classification each layer supports:

1. **Statute** (FD&C Act, PHS Act 351; FDAAA 801) — confirmed.
2. **Codified regulation** (21 CFR, 45 CFR, 42 CFR) — confirmed.
3. **Final FDA guidance and ICH guidelines as FDA-adopted** — nonbinding statements of current agency thinking (21 CFR 10.115). Statements *about what the guidance says* are confirmed; treating guidance as if it compelled or permitted a practice is interpretive. Examples: ICH E6(R3) GCP, the 2024 decentralized-elements guidance, the 2016 FDA/OHRP eConsent Q&A.
4. **Draft guidance** — cite only with an explicit draft flag and date. Currently load-bearing drafts: the 2025 AI-credibility draft (FDA-2024-D-4689; comments closed 2025-04-07, still draft), the 2015 sponsor-investigator IND draft (FDA-2015-D-1484), and the 2024 DMC draft. Any argument resting on a draft is interpretive by construction.
5. **Institutional practice and published precedent** (Vanderbilt V-CAP, Harvard Catalyst, SMART IRB/IREx, Penn/Pitt/Stanford libraries; see [[prior-art-vcap-irex-smartirb]]) — evidence of feasibility and convention, never of legal requirement. Interpretive when used to justify a design.
6. **Market evidence** ([[failed-disintermediation-case-studies]]) — corroboration only; interpretive.

## Marking mechanics

- **Frontmatter** `status:` field on every page.
- **Authority callout** under the H1 naming the governing authority and status.
- **Inline callouts**: `> [!interpretive] OSSICRO position` for thesis claims; `> [!warning] Non-delegable` for functions that must remain with a qualified human or entity.
- **Tags**: `status/confirmed`, `status/interpretive`.
- **Engine level**: every validation rule in the [[generate-check-validate-engine]] carries the same classification in [[compliance-mapping]]; rules resting on interpretive positions fail toward a human gate, never toward automatic pass.

## The canonical register of interpretive positions

The wiki's standing interpretive positions, each defended on its own page:

1. **Software may perform all coordination labor** provided every accountable act gates to a qualified human — supportable from Part 312's text; not a settled FDA position ([[legal-thesis-3123-vs-31252]], [[non-delegable-functions-and-gates]]).
2. **AI-drafted regulatory text for human review is a low-influence, low-consequence context of use** under the FDA 2025 AI-credibility draft framework — an argument made *under a draft guidance* ([[part-11-and-ai-credibility]]).
3. **The software-assisted monitoring boundary**: ICH E6(R3)'s risk-based and centralized monitoring provisions open room for automated scheduling, tracking, and centralized analytics, but do not eliminate the qualified-monitor judgment ([[risk-based-monitoring-e6r3]], [[clinical-monitor-cra]]).
4. **The coordination-vs-accountable classification** of the eight CRO functional streams and the margin map derived from industry disclosures ([[cro]]).
5. **The market lesson** of Science 37 and TrialSpark → Formation Bio ([[failed-disintermediation-case-studies]]).
6. **Risk-proportionate essential records**: reading ICH E6(R3) Appendix C as a proportionate matrix rather than a fixed checklist ([[document-catalog]]).
7. **Matching as preparatory-to-research**: the position that patient-trial matching operates under 45 CFR 164.512(i)(1)(ii) until the enrollment transition ([[hipaa-and-privacy-gating]], [[privacy-state-machine]]).

## Authorities in motion

The frame is not static; every citation carries its adoption date, and drafts are flagged in-page:

| Authority | Status as of 2026-07-09 |
|---|---|
| ICH E6(R3) GCP | FDA final guidance published 2025-09-09; no US compliance date set |
| ICH M11 protocol template | Final template 2025-11-19 |
| FDA decentralized-elements guidance | Final 2024-09-18 |
| FDA AI-credibility guidance | **Draft** (FR 2025-01-07; comments closed 2025-04-07) |
| FDA sponsor-investigator IND guidance | **Draft** (May 2015) — verify current status before citing |
| FDA DMC guidance | 2006 final; 2024 **draft** revision |

The [[regulatory-change-log]] watches these and flags every affected page and validation rule when an authority moves; a human curator confirms each propagated change.

## Decision rules

1. **Downgrade when in doubt.** If a claim cannot be verified against the plain text of a binding authority, mark it interpretive.
2. **Never assert automation-permitted where only human-sign-off is supportable.** The defensible claim is always "OSSICRO drafts; a qualified human reviews, decides, and signs" — the HARD PRINCIPLE of [[what-is-ossicro]].
3. **Distinguish unknown from ambiguous.** "FDA has not addressed this" (unknown) is different from "the text supports two readings" (ambiguous); pages say which.
4. **Quote load-bearing text verbatim.** Paraphrase invites drift; the exact words of § 312.52(a)'s final sentence, or § 50.20's consent requirement, are the requirement.
5. **Date every guidance citation** and re-verify draft status at each page update.

> [!warning] Non-delegable
> Calibration review is itself a human function. AI drafting agents in the [[claude-sdk-ai-in-the-loop]] pipeline may propose a status, but the assignment of `confirmed` to any claim — the assertion that a statement is enforceable law — is made or ratified by a qualified human reviewer, recorded in the Part 11 audit trail ([[part-11-and-ai-credibility]]).

## Related

- [[legal-thesis-3123-vs-31252]]
- [[failed-disintermediation-case-studies]]
- [[regulatory-landscape]]
- [[what-is-ossicro]]
- [[compliance-mapping]]
- [[non-delegable-functions-and-gates]]
- [[part-11-and-ai-credibility]]
- [[generate-check-validate-engine]]
- [[regulatory-change-log]]
- [[glossary]]

## Sources

- [eCFR — 21 CFR 10.115, Good Guidance Practices](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-10/section-10.115)
- [eCFR — 21 CFR Part 312, Investigational New Drug Application](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312)
- [FDA — E6(R3) Good Clinical Practice guidance](https://www.fda.gov/media/169090/download)
- [FDA Draft Guidance — Considerations for the Use of Artificial Intelligence To Support Regulatory Decision-Making for Drug and Biological Products (January 2025, FDA-2024-D-4689; draft)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological)
- [FDA Draft Guidance — Investigational New Drug Applications Prepared and Submitted by Sponsor-Investigators (May 2015; draft)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigational-new-drug-applications-prepared-and-submitted-sponsor-investigators)
- [FDA Final Guidance — Conducting Clinical Trials With Decentralized Elements (September 2024)](https://www.fda.gov/media/167696/download)
- [HHS — 45 CFR 164.512 (uses and disclosures for research)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512)
