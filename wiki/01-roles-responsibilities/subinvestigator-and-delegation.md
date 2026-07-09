---
title: "Subinvestigator and Delegation of Authority"
section: "01-roles-responsibilities"
status: mixed
governing_authority:
  - "21 CFR 312.3(b) (definitions)"
  - "21 CFR 312.53(c) / Form FDA 1572 Field 9"
  - "21 CFR 312.60, 312.61"
  - "FDA Guidance, Investigator Responsibilities — Protecting the Rights, Safety, and Welfare of Study Subjects (2009)"
  - "ICH E6(R3) Annex 1 §2 (Investigator)"
tags: [role/investigator, cfr/312, ich/e6r3, fda-form/1572, lifecycle/conduct, status/confirmed]
aliases: [delegation-of-authority, subinvestigator]
updated: 2026-07-09
---

# Subinvestigator and Delegation of Authority

> [!authority] Governing authority
> 21 CFR 312.3(b) (definition of investigator and subinvestigator); 21 CFR 312.53(c) and Form FDA 1572 Field 9 (the "personally conduct or supervise" commitment); 21 CFR 312.60–312.61; FDA Guidance for Industry, *Investigator Responsibilities — Protecting the Rights, Safety, and Welfare of Study Subjects* (October 2009); ICH E6(R3) Annex 1 §2. Status: **Mixed** — the delegation framework and the accountability rule are confirmed; OSSICRO's automation of log maintenance is an interpretive position, marked below.

Delegation is how a single [[investigator]] runs a trial with a team: specific trial-related tasks are assigned to qualified subinvestigators and study staff, recorded on a signed, dated [[delegation-of-authority-log]]. The controlling rule is asymmetric and absolute: **tasks can be delegated; accountability cannot.** Every commitment the investigator signs on [[form-fda-1572-statement-of-investigator|Form FDA 1572]] remains the investigator's own regardless of who performs the underlying work. This page states what may be delegated, what may not, what the delegation log must contain, and why investigator-side delegation is legally different in kind from sponsor-side transfer under [[cro|21 CFR 312.52]].

## Definitions

21 CFR 312.3(b) defines the *investigator* as "an individual who actually conducts a clinical investigation (i.e., under whose immediate direction the drug is administered or dispensed to a subject). In the event an investigation is conducted by a team of individuals, the investigator is the responsible leader of the team." The same section defines the *subinvestigator* as "any other individual member of that team" ([21 CFR 312.3](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A/section-312.3)).

For Form FDA 1572 Field 6 purposes, FDA's [1572 instructions](https://www.fda.gov/media/79326/download) and the [1572 FAQ guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/frequently-asked-questions-statement-investigator-form-fda-1572) direct listing as subinvestigators those team members (e.g., research fellows, residents) who will make a **direct and significant contribution to the data**. The purpose of Field 6 is to capture the individuals for whom the investigator is answerable; routine ancillary personnel (e.g., a hospital pharmacist dispensing per protocol, a phlebotomist drawing samples) generally need not be listed, but a person performing protocol-required medical assessments does.

## The legal frame: personally conduct or supervise

Two provisions carry the whole structure:

1. **21 CFR 312.60** — the investigator is responsible for ensuring the investigation is conducted according to the signed investigator statement, the investigational plan, and applicable regulations; for protecting the rights, safety, and welfare of subjects; and for the control of the drug ([eCFR](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.60)).
2. **Form FDA 1572, Field 9** (executed under 21 CFR 312.53(c)) — the investigator commits, among other things, to "personally conduct or supervise the described investigation(s)" and to "ensure that all associates, colleagues, and employees assisting in the conduct of the study(ies) are informed about their obligations in meeting the above commitments."

21 CFR 312.61 reinforces the supervision chain for the investigational product itself: the drug may be administered "only to subjects under the investigator's personal supervision or under the supervision of a subinvestigator responsible to the investigator" ([eCFR](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.61)).

## What may be delegated

The 2009 FDA guidance ([*Investigator Responsibilities*](https://www.fda.gov/media/77765/download)) confirms that investigators are not expected to perform every trial task personally. The investigator may delegate specific trial-related tasks — visit scheduling, specimen collection and processing, vital signs, questionnaire administration, CRF data entry, drug accountability logging, non-judgment screening steps — to individuals who are **qualified by education, training, and experience** to perform them. ICH E6(R3) Annex 1 §2 carries forward the long-standing GCP expectations (stated in ICH E6(R2) §§4.1.5 and 4.2.5–4.2.6) that the investigator maintain a record of appropriately qualified persons to whom significant trial-related duties are delegated, ensure their qualification, and **supervise** any individual or party to whom duties are delegated at the trial site ([ICH efficacy guidelines](https://www.ich.org/page/efficacy-guidelines)).

Adequate supervision, per the 2009 guidance, is evaluated on the facts: staffing levels and turnover, the team's training and experience, the complexity and risk of the protocol, the medical fragility of the population, and whether the investigator has a documented plan for oversight (routine team meetings, review of staff work product, procedures for medical escalation).

## What may not be delegated

> [!warning] Non-delegable
> The following remain the investigator's personally regardless of any delegation entry, and OSSICRO must route each to the qualified human — it drafts, tracks, and flags; it never performs or absorbs these:
> - **Overall supervision of the investigation** and the Field 9 commitments themselves (21 CFR 312.53(c); Form FDA 1572).
> - **Tasks requiring medical judgment.** The 2009 guidance states FDA's expectation that protocol-required tasks involving clinical judgment — eligibility determinations that require medical assessment, evaluation and medical management of adverse events, informed-consent discussion of medical alternatives and risks — be performed by a qualified physician (or dentist, where appropriate) listed on the 1572.
> - **Informed consent accountability.** A trained designee may conduct parts of the consent process, but the investigator remains responsible that legally effective consent is obtained from every subject before participation (21 CFR 312.60; 21 CFR Part 50; see [[informed-consent-document-vs-event]]).
> - **The SAE assessment of causal possibility** the investigator reports to the sponsor under 21 CFR 312.64(b) (see [[safety-reporting-lifecycle]]).
> - **Records integrity and inspection duties** (21 CFR 312.62, 312.68).

Failure of supervision is enforceable against the investigator personally: inadequate supervision of a study team is a recurring FDA Form 483 and Warning Letter finding, and repeated or deliberate noncompliance can lead to disqualification under [21 CFR 312.70](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.70).

## The delegation-of-authority log

The delegation log is a GCP and inspection expectation rather than a named 21 CFR document — the CFR requires the supervision and the qualification; the log is how both are evidenced (2009 FDA guidance; ICH E6(R2) §4.1.5, carried into E6(R3) Annex 1 §2 essential-records expectations). A compliant log records, for each team member:

| Element | Content |
|---|---|
| Identity | Name, role/title, signature and initials exemplar |
| Delegated tasks | Specific tasks (coded or enumerated) — not "all study duties" |
| Qualification evidence | CV, licensure, GCP and protocol-specific training records on file |
| Effective dates | Start and stop date per person per task |
| Authorization | Investigator's dated signature authorizing each delegation |

The log must stay current: staff join and leave, licenses lapse, protocol amendments change task sets. A log signed once at start-up and never touched again is the classic inspection finding. See [[delegation-of-authority-log]] for the document-level explainer and template treatment, and [[site-activation]] for where the log sits in the start-up package.

## Delegation is not transfer: the 312.52 contrast

Investigator-side delegation and sponsor-side transfer are legally distinct mechanisms and must never be conflated:

- **Investigator → subinvestigator/staff (this page):** tasks move; accountability does not. There is no regulatory mechanism by which an investigator can shed the Subpart D investigator obligations (21 CFR 312.60–312.69). No writing, contract, or log entry changes who FDA holds responsible.
- **Sponsor → CRO (21 CFR 312.52):** enumerated *sponsor* obligations can actually transfer, but only in writing and only to a legally accountable entity that then becomes "subject to the same regulatory action as a sponsor" — see [[cro]], [[transfer-of-regulatory-obligations-toro]], and [[legal-thesis-3123-vs-31252]].

For the [[sponsor-investigator]], both frames apply to one person: as investigator they may delegate tasks (never accountability) to their team; as sponsor they may transfer enumerated sponsor obligations to a real entity such as the [[micro-cro-accountable-layer|micro-CRO]] — and everything not transferred in writing remains theirs.

> [!interpretive] OSSICRO position
> OSSICRO's [[generate-check-validate-engine]] maintains the delegation log as a living, validated artifact: it drafts entries from structured staff records, cross-checks each delegated task against licensure/training evidence and against the 2009 guidance's medical-judgment carve-outs, flags lapses (expired license, missing GCP certificate, task delegated to an unlisted person), and version-controls every change. The investigator reviews and signs every authorization; the software never approves a delegation. Whether automated cross-checking of delegation entries satisfies an inspector's expectation of investigator oversight *evidence* is an OSSICRO design thesis, not a settled FDA position — the signed log plus the investigator's actual supervision remain the compliance substance.

## Related

- [[investigator]]
- [[sponsor-investigator]]
- [[delegation-of-authority-log]]
- [[form-fda-1572-statement-of-investigator]]
- [[cro]]
- [[micro-cro-accountable-layer]]
- [[transfer-of-regulatory-obligations-toro]]
- [[non-delegable-functions-and-gates]]
- [[informed-consent-document-vs-event]]
- [[site-activation]]
- [[safety-reporting-lifecycle]]
- [[clinical-monitor-cra]]

## Sources

- [21 CFR 312.3 — Definitions (investigator, subinvestigator, sponsor-investigator)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A/section-312.3)
- [21 CFR 312.53 — Selecting investigators and monitors](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53)
- [21 CFR 312.60 — General responsibilities of investigators](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.60)
- [21 CFR 312.61 — Control of the investigational drug](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.61)
- [21 CFR 312.70 — Disqualification of a clinical investigator](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.70)
- [FDA Guidance for Industry — Investigator Responsibilities: Protecting the Rights, Safety, and Welfare of Study Subjects (2009)](https://www.fda.gov/media/77765/download)
- [FDA — Instructions for Filling Out Form FDA 1572](https://www.fda.gov/media/79326/download)
- [FDA Guidance — Frequently Asked Questions: Statement of Investigator (Form FDA 1572)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/frequently-asked-questions-statement-investigator-form-fda-1572)
- [ICH Efficacy Guidelines — E6(R3) Good Clinical Practice](https://www.ich.org/page/efficacy-guidelines)
