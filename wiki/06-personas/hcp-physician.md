---
title: "Persona: Enrolling HCP / Physician"
section: "06-personas"
status: mixed
governing_authority:
  - "21 CFR 312.60–312.69 (investigator obligations)"
  - "21 CFR 312.3(b); 312.50–312.59 (sponsor set, Mode B)"
  - "21 CFR 312.53(c) (Form FDA 1572); 21 CFR Part 54"
  - "ICH E6(R3) (investigator responsibilities, Annex 1)"
tags: [role/investigator, role/sponsor-investigator, cfr/312, fda-form/1572, lifecycle/activation, status/mixed]
aliases: ["HCP Persona", "Physician Persona", "Enrolling Clinician"]
updated: 2026-07-09
---

# Persona: Enrolling HCP / Physician

> [!authority] Governing authority
> [21 CFR 312.60–312.69](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D) (investigator obligation set); [21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3) and [312.50–312.59](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D) when the physician is a [[sponsor-investigator]]; [21 CFR 312.53(c)](https://www.law.cornell.edu/cfr/text/21/312.53) ([[form-fda-1572-statement-of-investigator|Form FDA 1572]]); [21 CFR Part 54](https://www.law.cornell.edu/cfr/text/21/part-54) (financial disclosure); ICH E6(R3) investigator responsibilities. Status: **Mixed** — the duties are confirmed; the burden-removal architecture is OSSICRO **interpretive** design.

The enrolling physician is OSSICRO's load-bearing human and its core user. Their entry question: *"My patient needs this therapy. Make me an accepted site — without a research office, a regulatory department, or a study coordinator."* This page maps what the physician needs, the start-up burden OSSICRO removes, and — with equal weight — the duties no software can remove.

## Which hat: the first decision

The HCP's obligations depend entirely on the pathway ([[the-three-pathways-triage]]):

- **Mode A — site [[investigator]]** on a pharma sponsor's protocol: the investigator set only (312.60–312.69), memorialized in the signed 1572.
- **Mode B — [[sponsor-investigator]]** ([21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3)): *both* the investigator set *and* the full sponsor set — IND submission ([312.20–312.23](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-B)), safety reporting ([312.32](https://www.law.cornell.edu/cfr/text/21/312.32)), annual reports ([312.33](https://www.law.cornell.edu/cfr/text/21/312.33)), monitoring, records, drug disposition. The two role-holders of a conventional trial collapse into one person; nothing is delegated away by the collapse.
- **Expanded-access treating physician** ([21 CFR 312.310](https://www.law.cornell.edu/cfr/text/21/312.310)): treatment, not research — [[form-fda-3926-expanded-access|Form 3926]], manufacturer letter of authorization, IRB review, consent.

## The intimidation points — why physicians don't enroll

Harvard Catalyst's consult-service literature states the problem plainly: investigator-sponsors "often do not fully appreciate their regulatory obligations nor have resources to ensure compliance" ([Kim et al. 2014, PMID 24455986](https://pubmed.ncbi.nlm.nih.gov/24455986/)). Concretely, the barriers are:

1. **The site-activation package** ([[site-activation]]): executed [[clinical-trial-agreement-and-budget|CTA and budget]]; IRB approval of protocol and ICF; signed 1572; current CV and license; [[form-fda-3454-3455-financial-disclosure|financial disclosure]]; GCP and protocol training records; lab certifications (CLIA/CAP) and normal ranges; [[delegation-of-authority-log]]; drug-accountability and storage SOPs — a dossier a hospital research office normally produces and a solo clinician has never assembled.
2. **Mode B multiplies it**: the full [[ind-application-312-23|312.23 IND package]] ([[form-fda-1571-ind-cover|1571]] cover, general investigational plan, [[investigators-brochure|IB]], protocol, CMC, pharm/tox, prior human experience), the 30-day clock, then perpetual IND maintenance.
3. **No track record**: pharma's feasibility screen weights prior GCP trial history and enrollment realism heavily; a new site starts at a structural disadvantage (see [[pharma]] and [[single-patient-site-and-pharma-acceptance]]).
4. **Fear of inspection**: [21 CFR 312.68](https://www.law.cornell.edu/cfr/text/21/312.68) FDA access to records; BIMO inspection exposure feels existential to a clinician without a quality system.
5. **Time**: the physician's clinical schedule does not include a paperwork department.

## The duties the physician keeps — the non-delegable floor

> [!warning] Non-delegable
> Everything in this section stays with the physician. OSSICRO drafts, checks, routes, and times; the physician judges, signs, and answers to FDA. Task **execution** is delegable to qualified staff via the [[delegation-of-authority-log]]; **accountability never transfers** ([[subinvestigator-and-delegation]]; FDA 2009 Investigator Responsibilities guidance).

| Duty | Authority |
|---|---|
| Sign the 1572 and honor its Section 9 commitments: conduct per protocol; **personally conduct or supervise**; ensure Part 50 consent and Part 56 IRB review; report AEs per 312.64; read and understand the IB; ensure staff are informed; maintain 312.62 records; not make protocol changes without IRB/sponsor approval except to eliminate immediate hazard | [21 CFR 312.53(c)(1)](https://www.law.cornell.edu/cfr/text/21/312.53); [Form FDA 1572](https://www.fda.gov/media/74036/download) |
| Protect subjects' rights, safety, and welfare; control the investigational drug | [21 CFR 312.60](https://www.law.cornell.edu/cfr/text/21/312.60) |
| Administer the drug only to subjects under the investigator's personal supervision or that of a responsible sub-investigator | [21 CFR 312.61](https://www.law.cornell.edu/cfr/text/21/312.61) |
| **Eligibility determination** for each subject, and the consent conversation | 21 CFR 312.60; Part 50; [[informed-consent-document-vs-event]] |
| Maintain drug-disposition records and adequate, accurate **case histories**; retain 2 years post-approval or post-discontinuation notice | [21 CFR 312.62(a)–(c)](https://www.law.cornell.edu/cfr/text/21/312.62) |
| Report **serious adverse events to the sponsor immediately**, with a causality assessment; non-serious AEs per protocol timelines | [21 CFR 312.64(b)](https://www.law.cornell.edu/cfr/text/21/312.64) |
| Assure initial and continuing IRB review; report changes and unanticipated problems | [21 CFR 312.66](https://www.law.cornell.edu/cfr/text/21/312.66) |
| Permit FDA inspection and copying of records | [21 CFR 312.68](https://www.law.cornell.edu/cfr/text/21/312.68) |
| Controlled-substance security | [21 CFR 312.69](https://www.law.cornell.edu/cfr/text/21/312.69) |
| Financial-interest self-disclosure, updated for 1 year post-study | [21 CFR Part 54](https://www.law.cornell.edu/cfr/text/21/part-54); [312.64(d)](https://www.law.cornell.edu/cfr/text/21/312.64) |
| **Mode B adds the sponsor floor**: hold and maintain the IND; sign the 1571; own causality/expectedness for [[ind-safety-report|7/15-day IND safety reports]]; the [[ind-annual-report-dsur|annual report]]; the 312.56(d) unreasonable-risk discontinuation decision | [21 CFR 312.50–312.59](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D), [312.32–312.33](https://www.law.cornell.edu/cfr/text/21/312.32) |

## The burden OSSICRO removes

> [!interpretive] OSSICRO position
> Everything below is coordination labor — the ~90–95% of CRO direct cost that is labor, and precisely what makes the dual role impractical for a solo clinician. OSSICRO automates the drafting and tracking; every output is a **draft for qualified human review**, span-cited to its source ([[draft-provenance-model]]) and gated ([[non-delegable-functions-and-gates]]).

- **Document assembly**: the entire Mode A activation dossier and the Mode B 312.23 IND package, generated from structured study/CV/site data by the [[generate-check-validate-engine]], with completeness checked against the essential-records matrix (ICH E6(R3) Appendix C; [[document-catalog]]) and open items tracked on the [[completeness-ledger]] (green/amber/red — amber and red always resolve to the physician or a qualified human).
- **Deadline machinery**: the 30-day IND clock ([[ind-submission-and-30-day-clock]]), IRB continuing-review dates, the [[safety-clock-engine|7/15-day safety clocks]] (computed and escalated; **never** the causality call and **never** auto-filed), annual-report anniversaries.
- **Trust manufacturing**: the [[verifiable-site-qualification-dossier]] — a citation-complete, hash-chained qualification package that converts "no track record" into verifiable evidence a sponsor can audit (see [[pharma]]).
- **Review economics**: the [[single-pass-review-ux]] triages the physician's attention to judgment calls only; deterministic and boilerplate spans are visually segregated from inferred/interpretive ones.
- **Escalation**: when a function legally requires an entity or capacity the physician lacks, tiered escalation to the [[micro-cro|Micro-CRO]] — up to formal assumption of enumerated sponsor obligations via a [[transfer-of-regulatory-obligations-toro|TORO]]. Investigator obligations are never escalatable; they attach to the human.

## What the HCP needs to bring

Qualification is the one input OSSICRO cannot generate: a medical license in good standing; training and experience appropriate to the investigational drug ([21 CFR 312.53(a)](https://www.law.cornell.edu/cfr/text/21/312.53) — the sponsor must select "qualified by training and experience"); current GCP training; access to the patient population; facilities adequate for the protocol (storage, labs — arranged, not necessarily owned); and the willingness to hold the signatures. OSSICRO surfaces gaps early (e.g., no temperature-monitored storage → resolve before the 1572 names the facility).

## Related

- [[investigator]]
- [[sponsor-investigator]]
- [[the-three-pathways-triage]]
- [[site-activation]]
- [[form-fda-1572-statement-of-investigator]]
- [[form-fda-1571-ind-cover]]
- [[ind-application-312-23]]
- [[delegation-of-authority-log]]
- [[subinvestigator-and-delegation]]
- [[enrollment-and-consent]]
- [[verifiable-site-qualification-dossier]]
- [[completeness-ledger]]
- [[micro-cro]]
- [[patient]]
- [[perspective-matrix]]

## Sources

- [21 CFR Part 312 Subpart D — Responsibilities of Sponsors and Investigators](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)
- [21 CFR 312.60 — General responsibilities of investigators](https://www.law.cornell.edu/cfr/text/21/312.60)
- [21 CFR 312.62 — Investigator recordkeeping and record retention](https://www.law.cornell.edu/cfr/text/21/312.62)
- [21 CFR 312.64 — Investigator reports](https://www.law.cornell.edu/cfr/text/21/312.64)
- [FDA — Investigator Responsibilities: Protecting the Rights, Safety, and Welfare of Study Subjects (2009 guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigator-responsibilities-protecting-rights-safety-and-welfare-study-subjects)
- [FDA — Frequently Asked Questions: Statement of Investigator (Form FDA 1572) (2010 guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/frequently-asked-questions-statement-investigator-form-fda-1572)
- [FDA — Investigational New Drug Applications Prepared and Submitted by Sponsor-Investigators (draft guidance, 2015)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigational-new-drug-applications-prepared-and-submitted-sponsor-investigators)
- [Kim et al., Clin Transl Sci 2014 — Harvard Catalyst regulatory support for investigator-sponsors (PMID 24455986)](https://pubmed.ncbi.nlm.nih.gov/24455986/)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025, PDF)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
