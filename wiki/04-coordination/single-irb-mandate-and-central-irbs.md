---
title: "Single-IRB Mandate and Central IRBs"
section: "04-coordination"
status: mixed
governing_authority:
  - "45 CFR 46.114 (revised Common Rule)"
  - "NIH Policy NOT-OD-16-094"
  - "21 CFR 56.114 (current FDA rule); FDA proposed rule 87 FR 58752 (2022)"
tags: [role/irb, lifecycle/irb, cfr/56, entity/wcg, entity/advarra, entity/smart-irb, ossicro/engine, ossicro/micro-cro]
aliases: [sirb, single-irb, central-irb]
updated: 2026-07-09
---

# Single-IRB Mandate and Central IRBs

> [!authority] Governing authority
> 45 CFR 46.114(b) (single-IRB mandate for federally supported cooperative research; compliance date January 20, 2020); NIH sIRB Policy NOT-OD-16-094 (effective January 25, 2018); 21 CFR 56.114 (FDA rule — currently *permits* but does not compel joint/central review; harmonizing sIRB requirement proposed at 87 FR 58752, September 28, 2022, not final as of this page's update). Status: **Mixed** — mandates and their scope are confirmed; the applicability analysis for OSSICRO's modes is interpretive.

"Which IRB reviews this study?" has different answers depending on funding source, number of sites, and whether the enrolling physician has an institutional IRB at all. This page states the mandate landscape, the reliance mechanics that implement it, and the central-IRB route that is usually the practical answer for an OSSICRO [[sponsor-investigator]].

## The mandate landscape — three regimes

### 1. Revised Common Rule — 45 CFR 46.114(b)

For **cooperative research** (research covered by the Common Rule involving more than one institution), any U.S. institution must rely on approval by a **single IRB** for the portion of the research conducted in the United States. The reviewing IRB is identified by the supporting federal agency or, by agreement, proposed by the lead institution subject to agency acceptance (46.114(b)(1)). Compliance date: **January 20, 2020**. Exceptions (46.114(b)(2)): (i) cooperative research for which more than single-IRB review is required by law, including tribal law passed by the official governing body of an American Indian or Alaska Native tribe; and (ii) research for which any federal department or agency supporting or conducting it determines and documents that single-IRB review is not appropriate.

### 2. NIH single-IRB policy — NOT-OD-16-094

For NIH-funded **multi-site** studies conducting the **same protocol** of non-exempt human-subjects research at domestic sites, a single IRB of record is expected; effective for applications and proposals on/after **January 25, 2018** (implementation guidance in NOT-OD-20-058). The NIH policy predates and is narrower than 46.114(b) but drove the reliance infrastructure now in general use.

### 3. FDA-regulated studies — 21 CFR 56.114 (current) and the 2022 proposed rule

FDA's current regulation only *permits* cooperative arrangements: institutions involved in multi-institutional studies "may use joint review, reliance upon the review of another qualified IRB, or similar arrangements aimed at avoidance of duplication of effort" (21 CFR 56.114). There is **no FDA sIRB mandate in force**. Under the 21st Century Cures Act §3023 harmonization directive, FDA proposed in September 2022 to require sIRB review for FDA-regulated cooperative research ([87 FR 58752](https://www.federalregister.gov/documents/2022/09/28/2022-21089/institutional-review-boards-cooperative-research), with a companion human-subjects harmonization proposal at [87 FR 58733](https://www.federalregister.gov/documents/2022/09/28/2022-21088/protection-of-human-subjects-and-institutional-review-boards)). **Verify finalization status before advising on a specific study**; a dual-regulated study (FDA + federal funding) must already satisfy 46.114(b) regardless.

## Central / independent IRBs — WCG and Advarra

The two dominant U.S. commercial ("independent" or "central") IRBs are **WCG IRB** (WIRB-Copernicus Group, successor to Western IRB) and **Advarra** (formed from Chesapeake IRB and Schulman IRB). Both are AAHRPP-accredited, registered under 21 CFR 56.106 / 45 CFR 46, operate standing master reliance agreements with sponsors and institutions, and offer review turnarounds (frequently one to two weeks for initial full-board review) far faster than typical academic IRB queues. They function as the sIRB of record for most multi-site industry trials.

For OSSICRO's core user the central IRB solves a more basic problem: **a community physician typically has no institutional IRB at all.** A registered independent IRB is the standard, fully compliant route to Part 56 review for a sponsor-investigator study or a community site joining a pharma protocol. The review fee is a real cost (initial full-board review commonly runs low four figures; budget for it in the [[clinical-trial-agreement-and-budget|study budget]]).

## Reliance mechanics — SMART IRB and IREx

When the reviewing IRB is not the enrolling institution's own, the relationship is formalized by a **reliance (authorization) agreement** between the **reviewing IRB** (IRB of record) and each **relying institution**. The national infrastructure:

- **SMART IRB** — the NCATS-funded national reliance platform built on a master common reciprocal **Authorization Agreement** joined (via a Joinder Agreement) by more than a thousand U.S. institutions. Once both institutions are joined, per-study reliance is documented through SMART IRB's online reliance system rather than negotiating a bespoke agreement per study.
- **IREx (IRB Reliance Exchange)** — the web platform (Vanderbilt-hosted, used across the CTSA Trial Innovation Network) that operationalizes single-IRB review: capturing local-context surveys, tracking site approvals under the sIRB, and disseminating the sIRB's determinations to relying sites. IREx is direct published prior art for programmatic reliance coordination — see [[prior-art-vcap-irex-smartirb]].

### What stays local even under an sIRB

Reliance transfers the **IRB review** function only. The relying institution/site retains: local-context input (state and local law — e.g., consent age of majority, LAR rules), ancillary reviews (conflict-of-interest committee, radiation safety, institutional biosafety, pharmacy), HIPAA privacy-board functions unless expressly ceded ([[hipaa-and-privacy-gating]]), and all investigator obligations under 21 CFR 312.60-312.69 — which are never transferable ([[subinvestigator-and-delegation]]).

> [!warning] Non-delegable
> The reliance decision is institutional and the review judgment is the reviewing IRB's. OSSICRO drafts reliance packages, local-context worksheets, and submission materials, and tracks reliance status; it cannot execute an authorization agreement (that is an institutional official's signature) and it cannot substitute any prediction for the sIRB's approval ([[non-delegable-functions-and-gates]]).

## Applicability to OSSICRO's modes

> [!interpretive] OSSICRO position
> - **Mode B, single-site sponsor-investigator study:** not "cooperative research" — the sIRB *mandates* are not triggered. The operative question is access to *any* qualified IRB; the answer is almost always a central IRB (WCG/Advarra) engagement, which OSSICRO's engine assembles to the chosen IRB's submission checklist ([[irb-submission-package]]).
> - **Mode A, physician-as-site on a multi-site pharma protocol:** the sponsor has usually already designated a central sIRB; the new site executes reliance (or is added to the sponsor's central-IRB protocol file) and supplies local-context information. OSSICRO's job is the site-side reliance paperwork and local-context worksheet — see [[site-activation]] and [[single-patient-site-and-pharma-acceptance]].
> - **Federally funded multi-site work:** 46.114(b) and the NIH policy govern; SMART IRB/IREx is the expected machinery.
> These routing rules are encoded as a decision table in the [[generate-check-validate-engine]]; the output names the reviewing IRB candidate and the exact document set, and a human confirms the selection.

## Related

- [[irb-review-workflow]] — what the reviewing IRB does once selected
- [[irb-iec]] — IRB composition and authority
- [[site-activation]] — where reliance execution sits in startup
- [[prior-art-vcap-irex-smartirb]] — IREx/SMART IRB as design precedent for OSSICRO
- [[sponsor-cro-site-coordination]] — the contractual layer around reliance
- [[regulatory-landscape]] — where the 2022 FDA proposed rules sit among authorities in motion

## Sources

- [45 CFR 46.114 — Cooperative research (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.114)
- [HHS OHRP — Single IRB Exception Determinations](https://www.hhs.gov/ohrp/regulations-and-policy/single-irb-exception-determinations/index.html)
- [NIH NOT-OD-16-094 — Final NIH Policy on the Use of a Single IRB for Multi-Site Research](https://grants.nih.gov/grants/guide/notice-files/NOT-OD-16-094.html)
- [NIH NOT-OD-20-058 — sIRB implementation guidance](https://grants.nih.gov/grants/guide/notice-files/NOT-OD-20-058.html)
- [NIH — Single IRB Policy for Multi-Site Research (policy page)](https://grants.nih.gov/policy-and-compliance/policy-topics/human-subjects/single-irb-policy-multi-site-research)
- [21 CFR 56.114 — Cooperative research (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/56.114)
- [FDA Proposed Rule — Institutional Review Boards; Cooperative Research, 87 FR 58752 (Sept. 28, 2022)](https://www.federalregister.gov/documents/2022/09/28/2022-21089/institutional-review-boards-cooperative-research)
- [FDA Proposed Rule — Protection of Human Subjects and Institutional Review Boards, 87 FR 58733 (Sept. 28, 2022)](https://www.federalregister.gov/documents/2022/09/28/2022-21088/protection-of-human-subjects-and-institutional-review-boards)
- [SMART IRB](https://smartirb.org/)
- [IREx — IRB Reliance Exchange](https://www.irbexchange.org/)
- [NCATS — Trial Innovation Network](https://ncats.nih.gov/ctsa/projects/network)
- [WCG Clinical](https://www.wcgclinical.com/) · [Advarra](https://www.advarra.com/)
- [Advarra — Beginner's Guide to Single IRB Mandates](https://www.advarra.com/blog/beginners-guide-to-single-irb-mandates/)
