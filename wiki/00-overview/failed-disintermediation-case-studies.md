---
title: "Failed Disintermediation: Science 37 and TrialSpark → Formation Bio"
section: "00-overview"
status: interpretive
governing_authority:
  - "21 CFR 312.52 (legal backdrop: obligations transfer only to an accountable entity)"
  - "21 CFR 312.3(b) (definitions: CRO, sponsor-investigator)"
tags: [role/cro, cfr/312, ossicro/micro-cro, status/interpretive]
aliases: ["Science 37", "TrialSpark", "Formation Bio", "case studies"]
updated: 2026-07-09
---

# Failed Disintermediation: Science 37 and TrialSpark → Formation Bio

> [!authority] Governing authority
> Legal backdrop: 21 CFR 312.52 and 312.3(b) (see [[legal-thesis-3123-vs-31252]]). Status: **Interpretive.** The corporate events recounted here (SPAC valuation, delisting notice, take-private, rebrand, financing) are documented public record; the *lesson drawn from them* — that coordination-only trial software captures no durable value because value follows accountability and asset ownership — is an OSSICRO thesis position, not a regulatory requirement.

Two well-capitalized companies ran the experiment OSSICRO deliberately declines to run: sell clinical-trial coordination software as the product, without holding either the regulated accountable role or the drug asset. Both outcomes are matters of public record, and both point the same direction. This page documents the cases as market evidence for the design choices made in [[what-is-ossicro]] and [[micro-cro-operating-model]], and states honestly what the evidence does and does not prove.

## Why case studies appear in a regulatory wiki

The legal thesis ([[legal-thesis-3123-vs-31252]]) says software *cannot* be the § 312.52 transferee. That argument is doctrinal. These cases supply the economic corollary: because the enforceable role can never land on the software, sponsors pay for coordination tooling as a *tool* — a substitutable line-item — never as a *counterparty*. The market prices this correctly. A clinician or reviewer evaluating OSSICRO should understand that the system's architecture (sponsor-investigator core + thin accountable [[micro-cro-accountable-layer]] + open-source coordination engine) is a response to both the law and the demonstrated economics.

## Case 1 — Science 37

**What it sold.** Science 37, founded 2014, built decentralized-clinical-trial (DCT) software plus a "metasite" — a virtual site network of telehealth investigators, mobile nurses, and remote coordinators. It rode pandemic-era DCT demand into a SPAC merger (LifeSci Acquisition II Corp) that closed in October 2021 at a valuation of approximately $1 billion, listing on Nasdaq as SNCE.

**What happened.** Post-COVID, DCT demand receded: pandemic studies were cancelled, sponsor sales cycles lengthened, and quarterly net bookings collapsed (trade-press earnings coverage reported net bookings of roughly $4.7 million in a quarter against $35.9 million in the same quarter a year earlier). The stock fell below Nasdaq's $1.00 minimum-bid continued-listing standard, and in June 2023 the company disclosed a deficiency notice under Nasdaq Listing Rule 5450(a)(1) (Form 8-K). In January 2024, Science 37 agreed to be taken private by eMed, a digital diagnostics company, at approximately $38 million — a small fraction of its peak valuation.

**The reading.** Science 37 held real operational capability but neither the drug asset nor the durable accountable role. Its revenue was cyclical services demand mediated by software; when the demand cycle turned, there was no regulatory or asset moat underneath. Coordination tooling alone — however sophisticated — proved to be a thin, substitutable layer.

## Case 2 — TrialSpark → Formation Bio

**What it sold, and what it chose instead.** TrialSpark, founded 2016, began as trial-coordination software and expanded into a full tech-enabled CRO running end-to-end trials on its own platform — the closest real-world instantiation of "be the CRO via software." The company that best understood the economics of that model then abandoned it: from 2022 TrialSpark began acquiring and in-licensing drug assets to develop itself, and in December 2023 it rebranded as **Formation Bio**, an AI-native drug *developer* — a sponsor, not a service vendor (PR Newswire, December 2023). In 2024 it raised a $372 million Series D with Sanofi participation to license additional drug assets (Fierce Biotech).

**The reading.** This is revealed preference from the best-informed actor. Having operated the tech-enabled-CRO model at scale, TrialSpark's leadership concluded that durable value sits with whoever *owns the asset and holds the sponsor role* — the position § 312.52(b) makes enforceable — and re-founded the company around that position. The coordination layer they had built became internal tooling in service of the accountable role, not the product.

## The pattern

> [!interpretive] OSSICRO position
> The two cases, read together with 21 CFR 312.52, support one proposition: **in clinical trials, value follows accountability and asset ownership, not coordination tooling.** The law prevents software from ever holding the enforceable role; the market consequently refuses to pay software the margin that attaches to that role. Any business or system design premised on "software replaces the CRO" fights both the regulation and the demonstrated economics simultaneously.

OSSICRO's response inverts the failed play rather than repeating it:

| Failed play | OSSICRO design |
|---|---|
| Software vendor tries to occupy the CRO's economic position | Software is open-source and physician-operable; it occupies no regulatory position at all ([[what-is-ossicro]]) |
| Accountability nominally outsourced, actually nowhere | Accountability explicitly located: the [[sponsor-investigator]] personally, or a real [[micro-cro-accountable-layer]] entity via a written [[transfer-of-regulatory-obligations-toro]] |
| Value capture attempted at the coordination layer | Coordination labor is treated as cost-to-eliminate for the physician's benefit; the thin accountable layer and the [[verifiable-site-qualification-dossier]] are where trust (and any commercial value) concentrates |
| Sponsor trust sought through platform branding | Sponsor trust earned the way pharma actually grants it: a complete, internally consistent, credentialed document set ([[pharma-partner-sponsor]], [[single-patient-site-and-pharma-acceptance]]) |

## What the cases do and do not prove

Calibration per [[confirmed-vs-interpretive]]:

- **They are n = 2**, with confounders: COVID-era demand distortion, 2021 SPAC-vintage valuations, and the 2022-2023 rate environment all contributed to Science 37's collapse independent of any structural thesis. TrialSpark's pivot reflects one management team's judgment, not a controlled comparison.
- **They do not prove that trial-coordination software is worthless.** Sponsors buy CTMS, eTMF, EDC, and IRT systems continuously; those vendors persist as tooling businesses. The cases show that tooling revenue does not carry CRO-shaped margin or valuation, because it does not carry CRO-shaped accountability.
- **They are directional, not statistical.** OSSICRO treats them as corroboration of a conclusion reached independently on the regulatory text ([[legal-thesis-3123-vs-31252]]), not as a substitute for it. If the doctrinal argument were wrong, these cases alone would not establish the thesis.

> [!warning] Non-delegable
> The design lesson operationalized: OSSICRO never positions its software as the assuming party of any Part 312 obligation. Every accountable function identified in [[non-delegable-functions-and-gates]] — consent, IRB judgment, causality/expectedness, statistical sign-off, the 1571/1572 attestations, the § 312.52(b) transferee role itself — is held by a named, qualified human or a real legal entity. The software drafts complete documentation for their review; it never becomes the counterparty.

## Related

- [[legal-thesis-3123-vs-31252]]
- [[what-is-ossicro]]
- [[confirmed-vs-interpretive]]
- [[cro]]
- [[micro-cro-accountable-layer]]
- [[micro-cro-operating-model]]
- [[transfer-of-regulatory-obligations-toro]]
- [[non-delegable-functions-and-gates]]
- [[pharma-partner-sponsor]]
- [[verifiable-site-qualification-dossier]]
- [[sponsor-investigator]]

## Sources

- [eCFR — 21 CFR 312.52, Transfer of obligations to a contract research organization](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52)
- [Science 37 Form 8-K — Notice of Delisting or Failure to Satisfy a Continued Listing Rule (Nasdaq Rule 5450(a)(1), June 2023)](https://capedge.com/filing/1819113/0001819113-23-000057/SNCE-8K)
- [MedCity News — Science 37 to go private at a fraction of its $1B valuation (January 2024)](https://medcitynews.com/2024/01/decentralized-clinical-trials-software-mobile-app-science-37-covid-19/)
- [Endpoints News — Science 37 to go private in deal with diagnostics startup eMed](https://endpts.com/decentralized-trials-company-science-37-to-go-private-in-deal-with-diagnostics-startup-emed/)
- [PR Newswire — TrialSpark rebrands as Formation Bio (December 2023)](https://www.prnewswire.com/news-releases/trialspark-rebrands-as-formation-bio-continuing-its-commitment-to-advancing-drug-development-innovation-302006328.html)
- [Contrary Research — Formation Bio company report (founding story and pivot)](https://research.contrary.com/company/formation-bio)
- [Fierce Biotech — Formation Bio secures Sanofi-backed $372M Series D to license more drugs](https://www.fiercebiotech.com/biotech/ai-focused-formation-secures-sanofi-backed-372m-series-d-license-more-drugs)
