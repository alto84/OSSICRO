---
title: "IRB Continuing Review Progress Report"
doc_id: "irb-continuing-review-progress-report"
category: "irb"
governing_citations: ["21 CFR 56.109(f)"]
owner: "investigator"
receiver: "irb"
gate: "irb-approval"
status: template
updated: 2026-07-09
---

# IRB Continuing Review Progress Report — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 56.109(f)](https://www.law.cornell.edu/cfr/text/21/56.109) (an IRB shall conduct continuing review of research at intervals appropriate to the degree of risk, but not less than once per year). Investigator duty to maintain continuing IRB review: [21 CFR 312.66](https://www.law.cornell.edu/cfr/text/21/312.66). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The investigator's progress report submitted to the reviewing IRB before the current approval expires, giving the board the information it needs to re-apply the 21 CFR 56.111 criteria and re-approve the study for a further period. If the IRB has not re-approved by the expiration date, approval lapses and research activity must stop except as needed to protect enrolled subjects.

[INSTRUCTION: FDA regulations require continuing review at least annually for all FDA-regulated research. The 2018 revised Common Rule's elimination of continuing review for certain minimal-risk categories (45 CFR 46.109(f)) does NOT apply to FDA-regulated studies. Submit early enough for the IRB to complete review before {{current_expiration_date}} — most IRBs recommend 4–8 weeks lead time.]

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

{{submission_date}}

To: {{irb_name}}
From: {{investigator_name}}, Principal Investigator, {{site_name}}

**Re: Continuing review progress report — Protocol {{protocol_number}}**

**Protocol title:** {{protocol_title}}
**Current protocol version/date:** {{protocol_version}}, dated {{protocol_date}}
**Current approval period:** {{current_approval_date}} through {{current_expiration_date}}
**Review period covered by this report:** {{review_period}}
**Requested action:** Re-approval for a further period not to exceed one year (21 CFR 56.109(f)).

### 1. Study status

Current status: {{study_status}} [INSTRUCTION: One of — enrolling; enrollment closed, subjects in active treatment; enrollment closed, follow-up only; data analysis only. The board calibrates its review to remaining subject risk.]

Progress narrative: {{progress_summary}} [INSTRUCTION: 1 paragraph — where the study stands relative to plan, and anything that changes the risk-benefit balance since last review.]

### 2. Enrollment summary ({{enrollment_summary}})

| Metric | This site, cumulative | This review period |
|---|---|---|
| Screened | {{screened_total}} | {{screened_period}} |
| Screen failures | {{screen_fail_total}} | {{screen_fail_period}} |
| Enrolled | {{enrolled_total}} | {{enrolled_period}} |
| Active (on treatment / in follow-up) | {{active_n}} | — |
| Completed | {{completed_n}} | — |
| Withdrawn / discontinued | {{withdrawn_n}} | {{withdrawn_period}} |

Reasons for withdrawal: {{withdrawal_reasons}} [INSTRUCTION: Summarize; withdrawals for safety or tolerability must be called out explicitly, not buried in totals.]

### 3. Safety summary ({{safety_summary}})

- Serious adverse events at this site during the period: {{sae_count}}. Narrative: {{sae_narrative}} [INSTRUCTION: For each SAE — event term, relatedness as assessed, outcome, and whether previously reported to the IRB. Do not re-adjudicate causality here; that determination belongs to the qualified physician/medical monitor.]
- Unanticipated problems involving risks to subjects or others reported since last review: {{unanticipated_problems_summary}}
- IND safety reports received from the sponsor since last review: {{ind_safety_reports_received}} [INSTRUCTION: Count and one-line disposition — e.g., "3 received; none required consent form revision" or identify the resulting ICF amendment.]
- Protocol deviations during the period: {{deviations_summary}} [INSTRUCTION: Counts by category; deviations affecting subject safety or data integrity individually described.]

### 4. Amendments and consent documents

- Amendments approved since last continuing review: {{amendments_summary}}
- Consent form version currently in use: {{icf_version_in_use}}, dated {{icf_date_in_use}} [INSTRUCTION: Confirm this matches the IRB-approved version; attach the current ICF — many IRBs re-stamp at each re-approval.]
- Any new information (literature, DSMB findings, sponsor communications) bearing on the risk-benefit assessment or requiring consent revision: {{new_information_summary}}

### 5. Investigator's assessment

{{risk_benefit_reassessment}} [INSTRUCTION: 2–4 sentences: in the investigator's judgment, the risk-benefit relationship remains acceptable and the study should continue, or state what changed. This is the substantive heart of the report — write it, don't boilerplate it.]

I certify that the information above is accurate and complete, that the study is being conducted in accordance with the IRB-approved protocol, and that I will continue to comply with 21 CFR 312.66.

______________________________  Date: ____________
{{investigator_name}}, {{investigator_degrees}}
Principal Investigator

> [!warning] Non-delegable
> IRB review and approval determination is executed by the IRB (21 CFR 56.108–56.111; 21 CFR 312.66). OSSICRO drafts this template; the engine cannot finalize it without a recorded human sign-off. This report requests re-approval; only the convened or expedited IRB renders the re-approval determination and sets the new expiration date, and the investigator's signature above is likewise a personal attestation.

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{submission_date}} | submissions.irb_continuing.date | 21 CFR 56.109(f) |
| {{irb_name}} | study.irb.name | 21 CFR 312.66 |
| {{investigator_name}} / {{investigator_degrees}} | study.investigator.name / .degrees | 21 CFR 312.66 |
| {{site_name}} | study.site.name | — |
| {{protocol_number}} / {{protocol_title}} | study.protocol.number / .title | 21 CFR 56.109 |
| {{protocol_version}} / {{protocol_date}} | study.protocol.version / .date | 21 CFR 56.109 |
| {{current_approval_date}} / {{current_expiration_date}} | irb.current_approval.approval_date / .expiration_date | 21 CFR 56.109(f) |
| {{review_period}} | submissions.irb_continuing.review_period | 21 CFR 56.109(f) |
| {{study_status}} | study.status | 21 CFR 56.111 |
| {{progress_summary}} | submissions.irb_continuing.progress_summary | 21 CFR 56.111 |
| {{enrollment_summary}} (table: {{screened_total}}, {{screened_period}}, {{screen_fail_total}}, {{screen_fail_period}}, {{enrolled_total}}, {{enrolled_period}}, {{active_n}}, {{completed_n}}, {{withdrawn_n}}, {{withdrawn_period}}) | site.enrollment.* | 21 CFR 56.111(a)(3) |
| {{withdrawal_reasons}} | site.enrollment.withdrawal_reasons | 21 CFR 56.111 |
| {{safety_summary}} / {{sae_count}} / {{sae_narrative}} | site.safety.sae_count / .sae_narratives | 21 CFR 56.111(a)(6) |
| {{unanticipated_problems_summary}} | site.safety.unanticipated_problems | 21 CFR 56.108(b)(1) |
| {{ind_safety_reports_received}} | site.safety.ind_safety_reports_received | 21 CFR 312.32(c) |
| {{deviations_summary}} | site.deviations.summary | 21 CFR 312.66 |
| {{amendments_summary}} | irb.amendments_since_last_review | 21 CFR 56.108(a)(3) |
| {{icf_version_in_use}} / {{icf_date_in_use}} | documents.icf.version / .date | 21 CFR 50.27 |
| {{new_information_summary}} | site.safety.new_information | 21 CFR 50.25(b)(5) |
| {{risk_benefit_reassessment}} | submissions.irb_continuing.risk_benefit_assessment | 21 CFR 56.111(a)(2) |

## Related

- [[irb-submission-package]] — wiki document page covering the IRB document set
- [[irb-review-workflow]] — coordination page (continuing review cycle)
- [[annual-reporting-and-amendments]] — lifecycle page; pairs with the IND annual report to FDA
- [[irb-initial-approval-letter]] — template for the approval this report renews
