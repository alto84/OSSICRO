---
title: "Single-Patient (n-of-1) Site Enrollment — Three Routes, Documents, Pharma Acceptance"
section: "02-lifecycle"
status: mixed
governing_authority:
  - "21 CFR 312.310 (individual-patient expanded access) + Form FDA 3926"
  - "21 CFR 312.3(b), 312.20-312.23 (sponsor-investigator IND)"
  - "21 CFR 312.53, 312.62 (investigator selection, records) + Form FDA 1572"
  - "21 CFR 312.52 (transfer of obligations — accountability floor)"
  - "21 CFR Part 50; 45 CFR 46 (consent); 21 CFR Part 56 (IRB)"
tags: [lifecycle/expanded-access, lifecycle/ind, lifecycle/activation, role/sponsor-investigator, role/investigator, role/pharma, cfr/312, fda-form/3926, fda-form/1572, status/mixed]
aliases: ["n-of-1", "single-patient site", "one-patient site", "single patient enrollment"]
updated: 2026-07-09
---

# Single-Patient (n-of-1) Site Enrollment — Three Routes, Documents, Pharma Acceptance

> [!authority] Governing authority
> One physician, one patient, one pharma early-phase therapy resolves onto **three legally distinct routes**: (1) individual-patient **expanded access** (21 CFR 312.310, [[form-fda-3926-expanded-access]]); (2) a **one-patient site** added to an existing sponsor protocol (21 CFR 312.53/312.62, [[form-fda-1572-statement-of-investigator]]); (3) a **sponsor-investigator single-patient study** (own IND, 21 CFR 312.3(b)/312.23). Consent (21 CFR Part 50; 45 CFR 46) and IRB review (21 CFR Part 56) gate all three. The accountability floor is **21 CFR 312.52**: obligations transfer only to an accountable entity. Status: **Mixed** — the three routes are confirmed; the route-selection heuristics and OSSICRO acceptance-dossier are interpretive.

The single-patient case is OSSICRO's sharpest test and its clearest value: a practicing clinician has one specific patient with a serious condition and a specific early-phase therapy in mind, and no research office to navigate the paperwork. The clinical goal is the same across routes — get this patient this drug, lawfully and safely — but the **route determines who is accountable, what documents exist, how long it takes, and what legal exposure the physician assumes**. Choosing wrong is not a formatting error; it changes the regulatory basis for administering the drug. OSSICRO's job is to make the choice legible at triage, then generate the complete, cited document set for whichever route fits ([[the-three-pathways-triage]], [[two-modes-site-vs-sponsor-investigator]]).

> [!warning] Non-delegable
> Route selection is a clinical + regulatory judgment: is this **treatment** (expanded access) or **research** (site enrollment / sponsor-investigator study)? Is a fitting trial actually open? Can the patient realistically be enrolled? OSSICRO drafts the triage record and surfaces the trade-offs; the physician (with the IRB and, where applicable, the sponsor) owns the election. See [[expanded-access-workflow]] for the treatment/research bright line.

## The three routes at a glance

| Dimension | Route 1 — Expanded access | Route 2 — One-patient site on an existing protocol | Route 3 — Sponsor-investigator single-patient study |
|---|---|---|---|
| Legal character | **Treatment**, not research (312.305(a)) | **Research** — physician is a site investigator | **Research** — physician is sponsor-investigator |
| Who is sponsor / IND holder | Access-IND holder (treating physician or manufacturer) | **Pharma** company (existing IND) | **The physician** (own new IND, 312.3(b)) |
| Primary instrument | [[form-fda-3926-expanded-access]] + treatment plan | [[form-fda-1572-statement-of-investigator]] + site-activation package | Full 312.23 IND package + [[form-fda-1571-ind-cover]] |
| Manufacturer's role | Must agree to supply + issue LOA (FDCA §561A) | Provides drug under its protocol | Supplies drug + LOA to cross-reference IND ([[iis-request-workflow]]) |
| Generalizable data? | No (no efficacy endpoint, no randomization) | Yes (contributes to the sponsor's trial) | Yes (the physician's study objective) |
| Relative speed | Fastest (emergency: telephone auth, 312.310(d)) | Medium (site qualification + activation) | Slowest (30-day IND clock, full package) |
| Physician's obligation load | Lightest (treatment-use AE reporting, consent, IRB) | Investigator obligations (312.60-312.69) | **Both** sponsor (312.50-312.59) **and** investigator sets |

## Route 1 — Single-patient expanded access

The fastest path when the goal is **treatment** for one named patient and no fitting trial is open. The treating physician files **Form FDA 3926** (or the 1571/1572 route), obtains a **manufacturer Letter of Authorization** to supply and cross-reference the manufacturer's IND, and secures **IRB concurrence** (for individual/emergency use, chair or designated-member review is permitted; emergency use may proceed by telephone authorization with a written submission within **15 working days**, 312.310(d)). Full mechanics, criteria (312.305), and the safety/recordkeeping tail are on [[expanded-access-workflow]].

- **Document set:** Form 3926, treatment plan, manufacturer LOA, IRB concurrence, informed consent form, drug-accountability record.
- **Accountable parties:** treating physician (treatment + AE reporting), manufacturer (supply decision), IRB (concurrence).
- **When OSSICRO recommends surfacing it:** a serious/life-threatening condition, no comparable alternative therapy, no open trial the patient can join, and the objective is care rather than data.

## Route 2 — One-patient site on an existing sponsor protocol

When a fitting pharma trial **is** open and enrolling, the cleanest route is to add the physician as a **site** (even for a single patient). The pharma company remains the sponsor; the physician takes on the **investigator** obligation set (21 CFR 312.60-312.69). The barrier is not law but **site qualification**: a new site with no track record must produce, on an expedited timeline, the essential-document activation package the sponsor's standards demand.

- **Document set (site-activation essential records):** [[form-fda-1572-statement-of-investigator]]; PI/sub-I CVs and medical licenses; [[form-fda-3454-3455-financial-disclosure]] (Part 54); GCP training certificates; [[clinical-trial-agreement-and-budget]] (FMV-set); IRB approval; lab certifications/normal ranges; [[delegation-of-authority-log]]; drug-accountability SOPs; the [[regulatory-binder-isf-index]]. Mapped to ICH E6(R3) Appendix C ([[document-catalog]], [[startup-tmf-checklist]]).
- **Accountable parties:** pharma sponsor (IND, protocol, safety), physician-investigator (conduct, consent, drug control), IRB (approval).
- **The pharma-acceptance backend** — intake, lightweight feasibility, expedited site qualification, drug-supply authorization, and a safety-data exchange agreement — is detailed at [[single-patient-site-and-pharma-acceptance]]. This is where OSSICRO's "turn a new site's biggest liability (no track record) into a verifiable dossier" thesis operates (see [[verifiable-site-qualification-dossier]]).

> [!interpretive] OSSICRO position
> OSSICRO's wedge in Route 2 is the **verifiable site-qualification dossier**: a complete, internally-consistent, citation-carrying essential-records package that answers a skeptical sponsor's trust question before it is asked. The dossier is the single most persuasive artifact to a sponsor evaluating an unknown single-patient site. Flagged interpretive: the pharma's acceptance decision is theirs; OSSICRO makes the site *reviewable*, not *approved*.

## Route 3 — Sponsor-investigator single-patient study

When no trial fits, the therapy is investigational, and the objective is genuinely **research** (a defined study question, generalizable intent), the physician can hold their **own IND** as a sponsor-investigator (21 CFR 312.3(b)). This is the heaviest route: the physician carries **both** obligation sets and drives the full 312.23 package and the 30-day clock. In practice this is usually reached **through an IIS** — the pharma company supplies drug and often funding via its Medical Affairs IIS program, and the physician holds the IND ([[iis-request-workflow]]).

- **Document set:** full [[ind-application-312-23]] — [[form-fda-1571-ind-cover]], general investigational plan, [[investigators-brochure]] (or manufacturer package insert + LOA for CMC/pharm-tox cross-reference), [[clinical-protocol-and-synopsis]], [[form-fda-1572-statement-of-investigator]], [[form-fda-3674-clinicaltrialsgov-certification]], financial disclosure; then IND maintenance ([[ind-safety-report]] 312.32, [[ind-annual-report-dsur]] 312.33, amendments 312.30/312.31).
- **Accountable parties:** the physician as sponsor-investigator (everything), manufacturer (supply + LOA), IRB (approval).
- **When OSSICRO recommends it:** a research objective the other two routes cannot serve, and a physician willing (with the [[micro-cro-accountable-layer]] as backstop) to hold sponsor accountability.

> [!warning] Non-delegable
> In Route 3 the physician signs the 1571 (sponsor attestation) and 1572 (investigator statement) and **holds the IND** — accountability that cannot be transferred to software (21 CFR 312.52; [[legal-thesis-3123-vs-31252]]). Where a specific accountable function exceeds a solo physician's capacity, it transfers to the thin, human-staffed [[micro-cro-accountable-layer]] by a written [[transfer-of-regulatory-obligations-toro]] — an entity, never a script.

## The gates common to all three routes

Regardless of route, three non-delegable human functions gate the patient reaching the drug:

- **Informed consent** — the 21 CFR 50.25 elements are a document OSSICRO drafts; the consent **conversation** is a non-delegable human event ([[informed-consent-document-vs-event]], [[enrollment-and-consent]]).
- **IRB review/concurrence** — the ethics gate (21 CFR Part 56; 45 CFR 46). Treatment and enrollment are gated on documented IRB action ([[irb-iec]], [[irb-review-workflow]]).
- **Safety reporting + causality** — once the drug is administered, AE/SAE reporting attaches; seriousness/causality/expectedness is a medical judgment ([[safety-reporting-lifecycle]], [[medical-monitor]], [[safety-clock-engine]]).

## How OSSICRO drives the n-of-1 case

OSSICRO's [[generate-check-validate-engine]] takes the physician's de-identified clinical picture and intended therapy, runs matching to establish whether an open trial exists (Route 2 candidate) ([[patient-trial-matching]]), and presents the three routes with their trade-offs. On election, it **generates** the route-appropriate document set from structured data, **checks** completeness against the essential-records matrix (risk-proportionate, not a fixed checklist), and **validates** each artifact against its governing CFR/ICH subsection — routing every accountable act (signatures, FMV, manufacturer supply, IRB concurrence, consent, causality) to a human gate ([[non-delegable-functions-and-gates]]). The [[completeness-ledger]] reports the package as green (validated), amber (needs human judgment = a gate), or red (missing data + the exact resolving question). The result is a **complete draft for qualified human review** — the paperwork barrier removed, the judgment left where the law puts it.

## Related

- [[the-three-pathways-triage]]
- [[expanded-access-workflow]]
- [[iis-request-workflow]]
- [[single-patient-site-and-pharma-acceptance]]
- [[two-modes-site-vs-sponsor-investigator]]
- [[sponsor-investigator]]
- [[site-activation]]
- [[verifiable-site-qualification-dossier]]
- [[form-fda-3926-expanded-access]]
- [[form-fda-1572-statement-of-investigator]]
- [[ind-application-312-23]]
- [[legal-thesis-3123-vs-31252]]
- [[micro-cro-accountable-layer]]
- [[non-delegable-functions-and-gates]]

## Sources

- [21 CFR 312.310 — Individual patients, including for emergency use (via Part 312, eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312)
- [FDA — Expanded Access: How to Submit a Request (Forms), incl. Form FDA 3926](https://www.fda.gov/news-events/expanded-access/expanded-access-how-submit-request-forms)
- [FDA — Overview of Sponsor-Investigator Roles and Responsibilities](https://www.fda.gov/media/174660/download)
- [FDA — Investigational New Drug Applications Prepared and Submitted by Sponsor-Investigators (guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigational-new-drug-applications-prepared-and-submitted-sponsor-investigators)
- [FDA — Instructions for Filling Out Form FDA 1572](https://www.fda.gov/media/79326/download)
- [21 CFR Part 312 Subpart D — Responsibilities of Sponsors and Investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06, PDF)](https://database.ich.org/sites/default/files/ICH_E6(R3)_Step4_FinalGuideline_2025_0106.pdf)
