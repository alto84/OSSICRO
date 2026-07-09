---
title: "Site Activation"
section: "02-lifecycle"
status: mixed
governing_authority:
  - "21 CFR 312.53 (selecting investigators and monitors)"
  - "21 CFR 312.55 (informing investigators)"
  - "21 CFR Part 54 (financial disclosure)"
  - "ICH E6(R3) Annex 1 §3 (sponsor) and Appendix C (essential records)"
tags: [lifecycle/activation, cfr/312, fda-form/1572, fda-form/3454, fda-form/3455, ich/e6r3, status/confirmed, status/interpretive]
aliases: ["site initiation", "green light", "site readiness"]
updated: 2026-07-09
---

# Site Activation

> [!authority] Governing authority
> [21 CFR 312.53](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53) (selecting investigators and monitors; the 1572/CV/financial-disclosure package); 21 CFR 312.55(a) (Investigator's Brochure before start); [21 CFR Part 54](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54) (financial disclosure); ICH E6(R3) Annex 1 §3 and Appendix C. Status: **Mixed** — the sponsor-side prerequisites are confirmed; the composition of the activation "green-light package" as a single gated artifact is an OSSICRO operating convention built on the confirmed requirements.

Site activation is the green-light event between [[irb-submission-and-approval|IRB approval]] and first subject screening: the point at which every startup essential record exists, every accountable signature is in place, the site team is trained, and investigational product may lawfully be released to the site. No regulation names "activation" as such; the gate is the composite of 21 CFR 312.53's preconditions to an investigator's participation, 312.55(a)'s requirement that the Investigator's Brochure precede the investigation, and the E6(R3) essential-records framework. OSSICRO treats activation as a machine-checked completeness gate over the [[startup-tmf-checklist|startup TMF]] with human sign-offs at each accountable node.

## Sponsor-side preconditions (21 CFR 312.53 and 312.55)

Before permitting an investigator to begin participation, the sponsor (in Mode B, the [[sponsor-investigator]] as to themself) must — each a confirmed requirement:

- **Select qualified investigators.** Only investigators qualified by training and experience as appropriate experts to investigate the drug (312.53(a)). This selection judgment is the sponsor's.
- **Ship drug only to participating investigators** (312.53(b)). Drug release is therefore the *last* act of activation, never an early convenience.
- **Obtain the investigator's commitment package** (312.53(c)): a signed [[form-fda-1572-statement-of-investigator|Form FDA 1572]] with its Field 9 commitments; a curriculum vitae or other statement of qualifications (312.53(c)(2)); the clinical-protocol commitments; and sufficient financial-interest information to support complete and accurate Part 54 certification or disclosure ([[form-fda-3454-3455-financial-disclosure|Forms FDA 3454/3455]]), including the investigator's commitment to update that information for one year after study completion (312.53(c)(4)).
- **Select a qualified monitor** (312.53(d)) and stand up the [[monitoring-plan|risk-based monitoring plan]] — see [[conduct-and-monitoring]].
- **Furnish the [[investigators-brochure|Investigator's Brochure]]** to each participating investigator before the investigation begins (312.55(a)); for a marketed drug studied under an IND, the current package insert may serve (312.55, 312.23(a)(5)).

## The activation green-light package

The essential-records set that must be complete, current, and version-consistent before activation (ICH E6(R3) Appendix C, before-trial records; E6(R2) §8.2 cross-numbering; [[document-catalog]]):

| Record | Basis | Accountable signature |
|---|---|---|
| Executed [[clinical-trial-agreement-and-budget|CTA and budget]] (Mode A: sponsor–site; Mode B: any pharma support/supply agreement) | E6(R3) Appendix C; contract law | Contracting parties |
| Signed Form FDA 1572 | 21 CFR 312.53(c)(1) | Investigator |
| CV, medical license, GCP training certificates — PI, subinvestigators, key staff | 21 CFR 312.53(c)(2); E6(R3) Annex 1 §2 | Each individual |
| Financial disclosure (3454/3455) for PI and each subinvestigator | 21 CFR Part 54; 312.53(c)(4) | Each investigator |
| IRB approval letter + version-stamped approved protocol and ICF | 21 CFR 56.109, 312.66 | IRB issues |
| IRB roster / statement of Part 56 compliance | 21 CFR 56.107; E6(R3) Appendix C | IRB |
| FDA may-proceed status on the IND (30-day clock elapsed or FDA notification; no clinical hold) | 21 CFR 312.40, 312.42; [[ind-submission-and-30-day-clock]] | — |
| Laboratory certifications (CLIA/CAP) and current normal ranges | 42 CFR Part 493; E6(R3) Appendix C | Laboratory |
| [[delegation-of-authority-log|Delegation-of-authority log]] initialized with training evidence | E6(R3) Annex 1 §2; 21 CFR 312.60 | Investigator per line |
| IB receipt documented | 21 CFR 312.55(a) | Investigator |
| [[drug-accountability-log|Drug accountability log]] initialized; storage/temperature provisions verified; labeling per 21 CFR 312.6 | 21 CFR 312.57(a), 312.61, 312.62(a) | Pharmacy/investigator |
| Blank CRF/eCRF (version-controlled) and source-document worksheets | 21 CFR 312.62(b); E6(R3) Annex 1 §4 | Sponsor issues |
| Randomization/blinding materials and code-break procedure (where design requires) | E6(R3) Appendix C | Sponsor statistician |
| Site initiation visit (SIV) report | E6(R3) Annex 1 §3; [[monitoring-workflow-siv-imv-cov]] | Monitor |

> [!warning] Non-delegable
> Three signatures in this package are legal attestations no software may make and no other person may make for the signer: the investigator's **Form FDA 1572** (Field 9 commitments; signing without intending or being able to meet them is grounds for disqualification), each investigator's **financial disclosure**, and — in Mode B — the sponsor-investigator's qualification and selection judgments under 312.53(a) and (d). OSSICRO auto-populates every field from the structured study record and validates against the form's official instructions; a qualified human reads, confirms, and signs. See [[non-delegable-functions-and-gates]].

## The site initiation visit

The SIV is the monitor-conducted readiness verification that closes activation: protocol and IB training delivered and documented; consent process walked through; facilities, equipment, and drug-storage conditions inspected; source-document conventions and the ISF ([[regulatory-binder-isf-index]]) reviewed; delegation log confirmed against training records. The SIV produces a visit report filed to the TMF — an essential record evidencing sponsor oversight (ICH E6(R3) Annex 1 §3; FDA risk-based monitoring guidance 2013/2023). Under E6(R3)'s risk-proportionate frame, SIV depth scales with trial risk; for a single-site sponsor-investigator study the visit may be conducted by the micro-CRO's qualified monitor or structured as a documented self-qualification review — see [[micro-cro-accountable-layer]] and, for the n-of-1 case, [[single-patient-site-enrollment]].

## Drug release — the final act

Activation completes when investigational product ships. Shipment before the package is green violates 312.53(b)'s participating-investigator restriction in spirit and often in letter (no effective 1572, no IRB approval). Shipment records (name of investigator, date, quantity, batch or code mark) enter the sponsor's disposition records (21 CFR 312.57(a)); receipt at site opens the [[drug-accountability-log]]. In Mode A the pharma sponsor controls release; in Mode B, drug typically arrives from the pharma supplier under the support agreement, and the sponsor-investigator's own disposition recordkeeping begins at receipt.

## Mode A vs Mode B

- **Mode A (physician-as-site).** The pharma sponsor's activation checklist controls; OSSICRO's job is to make a new site's package indistinguishable in quality from an experienced site's — the [[verifiable-site-qualification-dossier]] renders the whole table above as a citation-complete, signature-complete, independently verifiable manifest. Site qualification and feasibility precede this stage ([[pharma-partner-interface-iis]], [[single-patient-site-and-pharma-acceptance]]).
- **Mode B (sponsor-investigator).** The documents that normally flow between two parties (1572 to sponsor, IB from sponsor) collapse into self-directed obligations — but none disappears. The S-I executes the 1572, self-collects financial disclosure, documents their own IB receipt, and appoints or contracts a qualified monitor (312.53(d)); monitoring one's own site is the structural weak point the [[micro-cro-accountable-layer|micro-CRO]] exists to shore up. See [[two-modes-site-vs-sponsor-investigator]].

## OSSICRO's function at this gate

The [[generate-check-validate-engine]] instantiates every template in the table from structured study data; the cross-document consistency engine verifies that PI name, addresses, IRB identity, IND number, and protocol version are identical across the 1572, delegation log, protocol, and CTA; and the [[completeness-ledger]] holds the activation state: green (validated), amber (awaiting a human judgment or signature — these are the gates), red (missing datum plus the exact resolving question). Activation is declared only when the ledger shows no red and every amber has a completed human sign-off, each captured in the Part-11 audit trail ([[part-11-and-ai-credibility]], [[draft-provenance-model]]).

> [!interpretive] OSSICRO position
> Treating activation as a single machine-gated ledger over the startup essential-records set is OSSICRO's operating convention, not a regulatory term of art. The underlying requirements (312.53, 312.55(a), 312.66, E6(R3) Appendix C) are confirmed; the packaging of them into one code-enforced green-light is the design position, chosen because dispersed checklists are where new sites fail sponsor audits.

## Related

- [[startup-tmf-checklist]] — the before-trial essential-records list this gate closes over
- [[form-fda-1572-statement-of-investigator]] · [[form-fda-3454-3455-financial-disclosure]]
- [[clinical-trial-agreement-and-budget]] · [[delegation-of-authority-log]] · [[drug-accountability-log]]
- [[irb-submission-and-approval]] — the preceding gate
- [[enrollment-and-consent]] — what activation unlocks
- [[monitoring-workflow-siv-imv-cov]] · [[monitoring-plan]] · [[clinical-monitor-cra]]
- [[verifiable-site-qualification-dossier]] — the pharma-facing rendering of this package
- [[two-modes-site-vs-sponsor-investigator]] · [[single-patient-site-enrollment]] · [[micro-cro-accountable-layer]]
- [[completeness-ledger]] · [[non-delegable-functions-and-gates]]

## Sources

- [21 CFR 312.53 — Selecting investigators and monitors (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53)
- [21 CFR 312.55 — Informing investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.55)
- [21 CFR Part 54 — Financial Disclosure by Clinical Investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54)
- [ICH E6(R3) Guideline for Good Clinical Practice, Step 4 Final (6 Jan 2025)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA Guidance — Frequently Asked Questions: Statement of Investigator (Form FDA 1572)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/frequently-asked-questions-statement-investigator-form-fda-1572)
- [FDA Guidance — Oversight of Clinical Investigations: A Risk-Based Approach to Monitoring (2013)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/oversight-clinical-investigations-risk-based-approach-monitoring)
- [FDA Forms index (1572, 3454, 3455)](https://www.fda.gov/about-fda/reports-manuals-forms/forms)
