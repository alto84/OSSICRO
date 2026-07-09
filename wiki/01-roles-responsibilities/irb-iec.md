---
title: "IRB / IEC — Institutional Review Board / Independent Ethics Committee"
section: "01-roles-responsibilities"
status: mixed
governing_authority:
  - "21 CFR Part 56"
  - "21 CFR Part 50"
  - "45 CFR Part 46 (revised Common Rule, 2018 Requirements)"
  - "21 CFR 312.66"
  - "ICH E6(R3) Section 1 (IRB/IEC)"
tags: [role/irb, cfr/56, cfr/50, cfr/312, ich/e6r3, lifecycle/irb, entity/irb]
aliases: ["IRB", "IEC", "Institutional Review Board", "Ethics Committee"]
updated: 2026-07-09
---

# IRB / IEC — Institutional Review Board / Independent Ethics Committee

> [!authority] Governing authority
> 21 CFR Part 56 (IRB standards for FDA-regulated research); 21 CFR Part 50 (informed consent); 45 CFR Part 46 (revised Common Rule, for federally supported research); 21 CFR 312.66 (investigator's IRB assurance); ICH E6(R3) Section 1. Status: **Mixed** — the regulatory requirements are confirmed black-letter law; OSSICRO's pre-check and gating design is an interpretive position, marked inline.

The IRB (US) / IEC (ICH international usage) is the independent body constituted to protect the rights, safety, and welfare of human research subjects. It is the ethics gatekeeper of the entire lifecycle: no investigator may involve a human subject in FDA-regulated research without prior IRB review and approval (21 CFR 56.103(a)), and enrollment in every OSSICRO-supported pathway — [[two-modes-site-vs-sponsor-investigator|Mode A, Mode B]], and [[expanded-access-workflow|expanded access]] — is gated on documented IRB action. The IRB's approval judgment is the paradigm non-delegable function: software may assemble, pre-check, route, and track the submission, but the review and the approval decision belong to the convened (or duly expedited) board and to no one else.

## 1. Which rule applies: 21 CFR 50/56 vs. 45 CFR 46

Two parallel regulatory regimes govern IRBs, and a study can be subject to one or both:

| Regime | Trigger | Key parts |
|---|---|---|
| FDA regulations | Any clinical investigation of an FDA-regulated product (any study under an IND) | [21 CFR Part 56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56) (IRBs), [21 CFR Part 50](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50) (consent) |
| Common Rule (2018 Requirements) | Research conducted or supported by a Common Rule federal department/agency, or at an institution whose Federalwide Assurance extends it | [45 CFR Part 46](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46), Subpart A + Subparts B (pregnant women/fetuses/neonates), C (prisoners), D (children) |

An NIH-funded IND trial is subject to both; a purely industry-funded IND trial at a private practice is subject to FDA rules only. The two regimes are closely parallel but not identical (e.g., continuing-review relief at 45 CFR 46.109(f)(1) has no FDA counterpart; FDA proposed harmonizing amendments to Parts 50 and 56 in 2022 that remain in motion — verify current status before relying on Common-Rule-only flexibilities in an FDA-regulated study). See [[regulatory-landscape]] for the full map. Children enrolled in FDA-regulated research get the additional safeguards of 21 CFR 50 Subpart D, mirroring 45 CFR 46 Subpart D.

IRBs reviewing FDA-regulated studies must be registered (21 CFR 56.106; 45 CFR 46.501–46.505 for OHRP registration).

## 2. Composition (21 CFR 56.107; 45 CFR 46.107)

Confirmed membership requirements:

- At least **five members** with varying backgrounds, sufficiently qualified through experience, expertise, and diversity (including race, gender, cultural background, and sensitivity to community attitudes) to promote respect for its advice (56.107(a)).
- At least one member whose primary concerns are in **scientific** areas and at least one whose primary concerns are in **nonscientific** areas (56.107(c)).
- At least one member **not otherwise affiliated** with the institution and not part of the immediate family of an affiliated person (56.107(d)).
- **No member may participate** in the initial or continuing review of any project in which the member has a conflicting interest, except to provide information requested by the IRB (56.107(e)).
- The IRB may invite non-voting consultants with competence in special areas (56.107(f)); where the IRB regularly reviews research involving a vulnerable category of subjects, it should consider including members knowledgeable about and experienced in working with those subjects (56.107(a)).

## 3. Functions and operations (21 CFR 56.108–56.110)

The IRB must follow written procedures for conducting initial and continuing review, determining which projects need review more often than annually, ensuring prompt reporting of changes, and ensuring that changes in approved research are not initiated without IRB approval except where necessary to eliminate apparent immediate hazards to subjects (56.108(a)–(b)). It must ensure prompt reporting to the IRB, institutional officials, and FDA of **unanticipated problems** involving risks to human subjects or others, serious or continuing noncompliance, and any suspension or termination of IRB approval (56.108(b); see [[safety-reporting-lifecycle]] for how the safety function feeds this channel).

Review at convened meetings requires a **majority quorum including at least one nonscientist** (56.108(c)). **Expedited review** (56.110; 45 CFR 46.110) by the chair or designee is available for research appearing on the published list of categories involving no more than minimal risk (63 FR 60364, Nov. 9, 1998) and for minor changes to approved research. The IRB must require that informed consent is sought and documented in accordance with Part 50 (56.109(b)–(c)) and must conduct **continuing review at intervals appropriate to the degree of risk, but not less than once per year** (56.109(f)) for FDA-regulated studies. The IRB has authority to suspend or terminate approval of research not conducted in accordance with its requirements or associated with unexpected serious harm (56.113).

## 4. Criteria for approval (21 CFR 56.111; 45 CFR 46.111)

The board may approve research only after determining that **all** of the following are satisfied — this list is the completeness spine OSSICRO's [[irb-submission-package]] validator pre-checks:

1. Risks to subjects are minimized by sound research design and, where appropriate, by using procedures already performed for diagnosis or treatment (56.111(a)(1)).
2. Risks are reasonable in relation to anticipated benefits and the importance of the knowledge expected (56.111(a)(2)).
3. Selection of subjects is equitable (56.111(a)(3)).
4. Informed consent will be sought from each prospective subject or legally authorized representative per Part 50 (56.111(a)(4)).
5. Informed consent will be appropriately documented per 50.27 (56.111(a)(5)).
6. Where appropriate, the research plan makes **adequate provision for monitoring the data collected to ensure the safety of subjects** (56.111(a)(6)) — the criterion that drives the data-safety-monitoring plan and, where warranted, a [[dsmb-dmc]].
7. Where appropriate, there are adequate provisions to protect subjects' privacy and maintain confidentiality of data (56.111(a)(7)).
8. Where subjects are vulnerable to coercion or undue influence, additional safeguards are included (56.111(b)).

The Common Rule adds the up-front "key information" requirement to consent (45 CFR 46.116(a)(5)(i)); see [[informed-consent-form]].

## 5. The investigator interface (21 CFR 312.66) and records (56.115)

Under 312.66 the [[investigator]] (or [[sponsor-investigator]]) must assure that an IRB compliant with Part 56 is responsible for initial and continuing review and approval; must promptly report to the IRB all changes in the research activity and all unanticipated problems involving risk to human subjects or others; and must not make any changes in the research without IRB approval, except where necessary to eliminate apparent immediate hazards. These commitments are also attested on [[form-fda-1572-statement-of-investigator|Form FDA 1572]] (Field 9). The IRB itself must prepare and maintain the records enumerated at 56.115 (research proposals reviewed, minutes with votes, continuing-review activities, correspondence, membership roster, written procedures) — the counterparty documents OSSICRO expects back into the TMF are the approval letter, approved consent form, and continuing-review/amendment approvals (see [[irb-submission-and-approval]] and [[document-catalog]]).

## 6. Single-IRB mandate and central IRBs

For cooperative research subject to the Common Rule, US institutions must rely on a **single IRB** (45 CFR 46.114(b), compliance date January 20, 2020); the NIH sIRB policy ([NOT-OD-16-094](https://grants.nih.gov/grants/guide/notice-files/NOT-OD-16-094.html)) applies to multi-site NIH awards from January 25, 2018. FDA regulations permit but do not compel central IRB use. For an OSSICRO sponsor-investigator without an institutional IRB, an independent/central IRB (e.g., WCG, Advarra) is the practical IRB of record, engaged through a reliance or services agreement. See [[single-irb-mandate-and-central-irbs]] for the reliance mechanics (SMART IRB / IREx).

> [!warning] Non-delegable
> The IRB's review and approval judgment — the ethics determination under 21 CFR 56.111 / 45 CFR 46.111 — is non-delegable to software, to the sponsor, to the investigator, and to OSSICRO. Likewise the IRB's continuing-review, amendment-approval, and suspension/termination authority (56.108–56.113). OSSICRO assembles and pre-checks the submission package and gates enrollment on the documented approval letter; it never renders, predicts as authoritative, or substitutes for the board's decision.

> [!interpretive] OSSICRO position
> OSSICRO's engine performs a **completeness and consistency pre-check of the submission package against the 56.111 criteria** (each element mapped to its supporting document) before routing to a human for submission — a drafting/QC aid modeled on published institutional checklist systems (see [[prior-art-vcap-irex-smartirb]]). This is an efficiency layer for the submitter; it has no bearing on, and asserts nothing about, how the IRB will or should decide. Enrollment gating on the approval letter in the TMF is a code-enforced control implementing 56.103(a), per [[non-delegable-functions-and-gates]].

## Related

- [[irb-submission-and-approval]] · [[irb-review-workflow]] · [[irb-submission-package]]
- [[single-irb-mandate-and-central-irbs]]
- [[informed-consent-form]] · [[informed-consent-document-vs-event]] · [[enrollment-and-consent]]
- [[investigator]] · [[sponsor-investigator]] · [[dsmb-dmc]]
- [[safety-reporting-lifecycle]] · [[pharmacovigilance-safety]]
- [[non-delegable-functions-and-gates]] · [[entity-map]] · [[regulatory-landscape]] · [[glossary]]

## Sources

- [21 CFR Part 56 — Institutional Review Boards (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56)
- [21 CFR Part 50 — Protection of Human Subjects (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50)
- [45 CFR Part 46 — Protection of Human Subjects (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46)
- [21 CFR 312.66 — Assurance of IRB review (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.66)
- [OHRP — Revised Common Rule (2018 Requirements)](https://www.hhs.gov/ohrp/regulations-and-policy/regulations/45-cfr-46/index.html)
- [OHRP — Categories of Research That May Be Reviewed Through an Expedited Review Procedure (1998)](https://www.hhs.gov/ohrp/regulations-and-policy/guidance/categories-of-research-expedited-review-procedure-1998/index.html)
- [NIH NOT-OD-16-094 — Single IRB Policy for Multi-Site Research](https://grants.nih.gov/grants/guide/notice-files/NOT-OD-16-094.html)
- [HHS OHRP — Single IRB Exception Determinations (45 CFR 46.114)](https://www.hhs.gov/ohrp/regulations-and-policy/single-irb-exception-determinations/index.html)
- [FDA — Institutional Review Boards Frequently Asked Questions (guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/institutional-review-boards-frequently-asked-questions)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06, PDF)](https://database.ich.org/sites/default/files/ICH_E6(R3)_Step4_FinalGuideline_2025_0106.pdf)
