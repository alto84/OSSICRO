---
title: "IRB Review Workflow — Initial, Continuing, and Expedited Review"
section: "04-coordination"
status: mixed
governing_authority:
  - "21 CFR Part 56 (esp. 56.103, 56.107-56.115)"
  - "21 CFR 312.66"
  - "45 CFR 46.109-46.110 (Common Rule, where applicable)"
tags: [role/irb, lifecycle/irb, cfr/56, cfr/50, cfr/312, ossicro/gating, ossicro/engine]
aliases: [irb-review]
updated: 2026-07-09
---

# IRB Review Workflow — Initial, Continuing, and Expedited Review

> [!authority] Governing authority
> 21 CFR Part 56 (IRB standards for FDA-regulated clinical investigations), 21 CFR 312.66 (investigator's IRB assurances), 45 CFR 46.109-46.110 where the study is also federally supported. Status: **Mixed** — the review requirements are black-letter; OSSICRO's pre-submission completeness validation and gating design are interpretive positions.

The IRB is the ethics gate. No clinical investigation subject to FDA's IND regulations may involve human subjects unless an IRB meeting the requirements of 21 CFR Part 56 has reviewed and approved it (21 CFR 56.103(a)), and the investigator personally assures that an IRB will conduct initial and continuing review, that changes and unanticipated problems will be reported, and that no change will be made without IRB approval except to eliminate apparent immediate hazards (21 CFR 312.66). For the [[sponsor-investigator]] without an institutional research office, IRB interaction is one of the two most intimidating workflows (the other is [[safety-reporting-workflow|safety reporting]]); this page specifies it end to end. The composition and authority of the board itself is covered at [[irb-iec]].

## Prerequisites

- **IRB registration.** An IRB reviewing FDA-regulated studies must be registered with HHS (21 CFR 56.106; registration through the OHRP/FDA joint system). A sponsor-investigator using a commercial IRB should verify registration status — see [[single-irb-mandate-and-central-irbs]].
- **Membership and conflicts.** The board must have at least five members with varying backgrounds, including at least one scientist, one nonscientist, and one member not otherwise affiliated with the institution; no member may participate in review of a project in which the member has a conflicting interest, except to provide information requested by the IRB (21 CFR 56.107).

## Initial review

### 1. Submission

The [[irb-submission-package]] typically comprises: the [[clinical-protocol-and-synopsis|protocol]] and any amendments; the [[investigators-brochure|IB]]; the draft [[informed-consent-form|informed consent form(s)]] and all recruitment/advertising materials; investigator CV and licensure; [[form-fda-1572-statement-of-investigator|Form FDA 1572]]; financial-interest information (21 CFR Part 54); the IND number; the data-safety-monitoring plan; and HIPAA authorization language where applicable ([[hipaa-and-privacy-gating]]). The IRB must review, and retain records of, the materials it acted on (21 CFR 56.115(a)).

> [!interpretive] OSSICRO position
> OSSICRO runs a completeness validator over the package against the receiving IRB's checklist and against the 21 CFR 56.111 criteria *before* submission — a pre-review that reduces modification cycles. The validator predicts; only the IRB decides. Prior art for criteria-driven checklist generation: Vanderbilt's V-CAP ([[prior-art-vcap-irex-smartirb]]).

### 2. Convened review

Except where expedited review applies, proposed research is reviewed at a convened meeting at which a majority of members is present, including at least one member whose primary concerns are in nonscientific areas; approval requires a majority of members present (21 CFR 56.108(c)).

### 3. The approval criteria — 21 CFR 56.111

To approve, the IRB must determine **all** of the following are satisfied:

1. Risks to subjects are minimized by sound design and, where appropriate, use of procedures already performed for diagnosis/treatment (56.111(a)(1));
2. Risks are reasonable in relation to anticipated benefits and the importance of the knowledge expected (56.111(a)(2));
3. Selection of subjects is equitable, with attention to vulnerable populations (56.111(a)(3));
4. Informed consent will be sought from each prospective subject or the subject's legally authorized representative, per 21 CFR Part 50 (56.111(a)(4));
5. Informed consent will be appropriately documented per 21 CFR 50.27 (56.111(a)(5));
6. Where appropriate, the research plan makes adequate provision for monitoring the data to ensure subject safety (56.111(a)(6)) — the hook that makes the [[dsmb-charter|DSMP/DMC]] an IRB concern;
7. Adequate provisions protect subject privacy and data confidentiality (56.111(a)(7));
8. Additional safeguards where subjects are vulnerable to coercion or undue influence (56.111(b)).

### 4. Outcomes and notification

The IRB may approve, require modifications to secure approval, or disapprove (21 CFR 56.109(a)), and must notify the investigator and institution in writing, including the reasons for any disapproval and an opportunity to respond (56.109(e)). Only a convened board may disapprove. The dated approval letter and the IRB-approved consent version are essential records filed to the TMF/ISF ([[document-catalog]]).

> [!warning] Non-delegable
> The approval judgment — weighing risk against benefit, equity of selection, adequacy of consent — is the constituted committee's and cannot be authored, predicted-and-acted-on, or bypassed by software. OSSICRO hard-gates enrollment: no subject-facing activity is unlocked until a documented IRB approval letter and the approved ICF version exist in the TMF ([[non-delegable-functions-and-gates]]).

## Expedited review — 21 CFR 56.110

Expedited review is available for (a) research appearing on the FDA/HHS list of categories involving no more than minimal risk (published at 63 FR 60353 (FDA) and 63 FR 60364 (HHS), November 9, 1998), and (b) **minor changes in previously approved research** during the approval period — the common early-phase use case. Review is carried out by the IRB chairperson or experienced designated reviewers; they may exercise all IRB authorities **except disapproval** (disapproval requires the convened board), and the IRB must keep all members advised of expedited approvals (56.110(b)-(c)). An interventional early-phase drug trial itself will essentially never qualify as minimal-risk; expedited review matters operationally for administrative amendments, personnel changes, and minor consent-form edits.

## Continuing review

For FDA-regulated studies the IRB conducts continuing review at intervals appropriate to the degree of risk, **not less than once per year** (21 CFR 56.109(f)). The continuing-review package typically includes enrollment status, withdrawals, unanticipated problems and deviations since last review, current safety summary (including [[ind-safety-report|IND safety reports]] received), the current consent form, and any interim findings. Lapse in approval means the study must stop enrollment and, absent IRB determination that continuation is in subjects' best interests, study activity.

**Divergence to note:** the revised Common Rule eliminated mandatory continuing review for studies that qualified for expedited review and for studies remaining open only for data analysis or standard-of-care follow-up data collection, unless the IRB justifies otherwise (45 CFR 46.109(f)(1)). FDA regulations contain no such elimination; a dual-regulated study follows the stricter FDA rule. FDA proposed harmonizing changes in September 2022 (87 FR 58733); verify current status before relying on any relaxation.

> [!interpretive] OSSICRO position
> OSSICRO tracks the continuing-review clock from the approval-letter date, assembles the progress-report package from accumulated study data, and escalates at configurable lead times (e.g., 90/60/30 days). A lapsed approval trips the same hard enrollment gate as a missing initial approval.

## Amendments and unanticipated problems

- **Amendments.** Changes in approved research may not be initiated without IRB review and approval except where necessary to eliminate apparent immediate hazards to subjects (21 CFR 56.108(a)(4); 312.66). Protocol changes also flow to FDA as protocol amendments under 21 CFR 312.30 — the dual-arrow pattern drawn in [[inter-entity-document-flow-map]].
- **Unanticipated problems.** The investigator promptly reports unanticipated problems involving risk to human subjects or others to the IRB (312.66); the IRB in turn has written procedures for ensuring prompt reporting to the IRB, institution, and FDA of unanticipated problems and of serious or continuing noncompliance (56.108(b)), and must report any suspension or termination of approval with reasons (56.113).

## Sequence summary (initial review)

1. Assemble package → completeness pre-check ([[generate-check-validate-engine]]) →
2. Submit to the reviewing IRB (institutional or central; see [[single-irb-mandate-and-central-irbs]]) →
3. Convened review against 56.111 →
4. Outcome letter; respond to modifications-required with tracked-change revisions →
5. File approval letter + approved ICF version to TMF →
6. Enrollment gate opens; consent events may begin ([[informed-consent-document-vs-event]]) →
7. Clock the continuing-review interval; route amendments and unanticipated problems as they arise.

## Related

- [[irb-iec]] — the board itself: composition, authority, records
- [[irb-submission-package]] — package composition and the 56.111 validator
- [[irb-submission-and-approval]] — the lifecycle-phase view of the same gate
- [[single-irb-mandate-and-central-irbs]] — which IRB reviews, and reliance mechanics
- [[informed-consent-document-vs-event]] — what the IRB approves vs what the investigator performs
- [[inter-entity-document-flow-map]] — this workflow's arrows in the consolidated map
- [[non-delegable-functions-and-gates]] — the enrollment gate specification

## Sources

- [21 CFR Part 56 (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56)
- [21 CFR 56.111 — Criteria for IRB approval (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/56.111)
- [21 CFR 56.110 — Expedited review (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/56.110)
- [21 CFR 56.109 — IRB review of research (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/56.109)
- [21 CFR 312.66 — Assurance of IRB review (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.66)
- [Expedited review categories, 63 FR 60364 / 60353 (Nov. 9, 1998) — Federal Register](https://www.federalregister.gov/documents/1998/11/09/98-29749/protection-of-human-subjects-categories-of-research-that-may-be-reviewed-by-the-institutional-review)
- [FDA — Expedited review categories guidance page](https://www.fda.gov/science-research/clinical-trials-and-human-subject-protection/categories-research-may-be-reviewed-institutional-review-board-irb-through-expedited-review)
- [45 CFR 46.109 (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.109)
- [FDA Proposed Rule — Protection of Human Subjects and Institutional Review Boards, 87 FR 58733 (Sept. 28, 2022)](https://www.federalregister.gov/documents/2022/09/28/2022-21088/protection-of-human-subjects-and-institutional-review-boards)
