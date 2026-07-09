---
title: "DSMB Meeting Minutes and Recommendation"
doc_id: "dsmb-meeting-minutes-and-recommendation"
category: "dsmb"
governing_citations: ["FDA Guidance: Clinical Trial Data Monitoring Committees (2006; 2024 draft rev.)"]
owner: "dsmb"
receiver: "sponsor"
gate: "none"
status: template
updated: 2026-07-09
---

# DSMB Meeting Minutes and Recommendation — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> FDA Guidance for Clinical Trial Sponsors: [Establishment and Operation of Clinical Trial Data Monitoring Committees (2006)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/establishment-and-operation-clinical-trial-data-monitoring-committees), §4.4.3 (records) and §4.5 (interactions with the sponsor), and the [2024 draft revision, Use of Data Monitoring Committees in Clinical Trials](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-data-monitoring-committees-clinical-trials). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Records the proceedings of a DSMB/DMC data-review meeting and transmits the Board's formal recommendation to the Sponsor. One instance is completed per meeting (scheduled or ad hoc), during the conduct phase of the study.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

[INSTRUCTION: Maintain open-session and closed-session minutes as SEPARATE records. The recommendation letter (Part C) plus the open-session minutes (Part A) go to the Sponsor promptly; the closed-session minutes (Part B) contain interim comparative data and remain sequestered with the designated custodian until study unblinding or termination, per the charter and FDA 2006 guidance §4.4.3. The recommendation itself is the DSMB's collective judgment; OSSICRO drafts the shell only.]

## Template

### PART A — OPEN SESSION MINUTES

**Study ID / Protocol Number:** {{study_id}}
**Protocol Title:** {{protocol_title}}
**Meeting Date:** {{meeting_date}} — **Meeting Type:** {{meeting_type}} [INSTRUCTION: scheduled / ad hoc; if ad hoc, state the trigger.]
**Meeting Number:** {{meeting_number}} — **Format:** {{meeting_format}} [INSTRUCTION: in person / video / teleconference.]
**Charter Version in Effect:** {{charter_version}}

**Attendance**

| Name | Role | Voting | Sessions attended |
|---|---|---|---|
| {{attendees}} | | | |

[INSTRUCTION: One row per attendee; include DSMB members, unblinded statistician, and any open-session sponsor/study-team attendees. Record explicitly whether quorum per the charter was met: {{quorum_met}}.]

**A.1 Review of prior minutes and action items.** {{prior_action_items_status}}

**A.2 Study conduct (blinded / aggregate).**
- Enrollment: {{enrollment_summary}} [INSTRUCTION: screened, enrolled, discontinued vs. projection; data cutoff date.]
- Data cutoff for this review: {{data_cutoff_date}}
- Protocol deviations since last review: {{deviation_summary}}
- Data quality/timeliness issues: {{data_quality_summary}}
- Protocol amendments or administrative changes since last review: {{amendments_summary}}

**A.3 Open-session discussion.** {{open_session_discussion}}

---

### PART B — CLOSED SESSION MINUTES (CONFIDENTIAL — sequestered)

[INSTRUCTION: Voting members and unblinded statistician only. Do not circulate outside the DSMB before unblinding.]

**B.1 Data reviewed.** {{data_reviewed}}

[INSTRUCTION: Itemize the report sections reviewed, e.g.: unblinded AE/SAE tables by arm, deaths, Grade ≥3 related events against the §7 charter boundaries, laboratory shift tables, discontinuations for toxicity, and any interim efficacy/futility analysis with the applicable alpha-spending boundary. Identify the report version/date: {{report_version}}.]

**B.2 Safety assessment.** {{safety_assessment}}
[INSTRUCTION: State whether any charter stopping/pausing guideline (§7 of the charter) was met or approached, and the Board's judgment on the overall benefit-risk of continuing.]

**B.3 Closed-session deliberations.** {{closed_session_discussion}}

**B.4 Vote (if taken).** {{vote_record}} [INSTRUCTION: motion, mover, count for/against/abstain; consensus-without-vote is acceptable if the charter allows — record it as such.]

---

### PART C — RECOMMENDATION TO THE SPONSOR

Following its review of the data through {{data_cutoff_date}}, the DSMB for study {{study_id}} recommends:

**☐ Continue the study without modification**
**☐ Continue the study with the following modification(s):** {{modification_details}}
**☐ Pause enrollment and/or dosing pending:** {{pause_conditions}}
**☐ Terminate the study**

**Recommendation (narrative):** {{recommendation}}

[INSTRUCTION: The narrative must stand alone without unblinded data — it is transmitted to the Sponsor and may reach the IRB and FDA. Do not include by-arm results unless the recommendation itself requires unblinding (e.g., termination for harm). Per FDA 2006 guidance §4.5, the Sponsor decides whether and how to act on the recommendation and handles onward reporting under 21 CFR 312.32 and 312.66.]

**Rationale (blinded-safe summary):** {{recommendation_rationale}}

**Action items and follow-up requests to the Sponsor:**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | {{action_item_1}} | {{action_item_1_owner}} | {{action_item_1_due}} |

**Next scheduled review:** {{next_meeting_date}} (or trigger: {{next_review_trigger}})

**Minutes prepared by:** {{minutes_author}} — **Date:** {{minutes_date}}
**Closed-session minutes custodian:** {{minutes_custodian}}

**Approval**

| Role | Name | Signature | Date |
|---|---|---|---|
| DSMB Chair | {{chair_name}} | ______________________ | ________ |

**Transmitted to Sponsor:** {{sponsor_contact_name}}, on {{transmittal_date}}, via {{transmittal_method}} (Part A + Part C only).

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{study_id}} | study.identifiers.study_id | FDA DMC Guidance (2006) §4.4 |
| {{protocol_title}} | study.protocol.title | ICH M11 |
| {{meeting_date}} | dsmb.meetings[n].date | FDA DMC Guidance (2006) §4.3 |
| {{meeting_type}} | dsmb.meetings[n].type | FDA DMC Guidance (2006) §4.3 |
| {{meeting_number}} | dsmb.meetings[n].number | FDA DMC Guidance (2006) §4.4.3 |
| {{meeting_format}} | dsmb.meetings[n].format | FDA DMC Guidance (2006) §4.3 |
| {{charter_version}} | dsmb.charter.version | FDA DMC Guidance (2006) §4.4 |
| {{attendees}} | dsmb.meetings[n].attendees | FDA DMC Guidance (2006) §4.4.3 |
| {{quorum_met}} | dsmb.meetings[n].quorum_met | FDA DMC Guidance (2006) §4.3 |
| {{prior_action_items_status}} | dsmb.meetings[n].prior_actions | FDA DMC Guidance (2006) §4.4.3 |
| {{enrollment_summary}} | study.conduct.enrollment_summary | FDA DMC Guidance (2006) §4.1 |
| {{data_cutoff_date}} | dsmb.meetings[n].data_cutoff | FDA DMC Guidance (2006) §4.4.2 |
| {{deviation_summary}} | study.conduct.deviations_summary | ICH E6(R3) Appendix C |
| {{data_quality_summary}} | study.conduct.data_quality | FDA DMC Guidance (2006) §4.1 |
| {{amendments_summary}} | study.protocol.amendments_summary | 21 CFR 312.30 |
| {{open_session_discussion}} | dsmb.meetings[n].open_session_notes | FDA DMC Guidance (2006) §4.4.3 |
| {{data_reviewed}} | dsmb.meetings[n].data_reviewed | FDA DMC Guidance (2006) §4.4.2 |
| {{report_version}} | dsmb.meetings[n].report_version | FDA DMC Guidance (2006) §4.4.2 |
| {{safety_assessment}} | dsmb.meetings[n].safety_assessment | FDA DMC Guidance (2006) §6.2 |
| {{closed_session_discussion}} | dsmb.meetings[n].closed_session_notes | FDA DMC Guidance (2006) §4.4.3 |
| {{vote_record}} | dsmb.meetings[n].vote_record | FDA DMC Guidance (2006) §4.3.2 |
| {{modification_details}} | dsmb.meetings[n].recommendation.modifications | FDA DMC Guidance (2006) §4.5 |
| {{pause_conditions}} | dsmb.meetings[n].recommendation.pause_conditions | FDA DMC Guidance (2006) §4.5 |
| {{recommendation}} | dsmb.meetings[n].recommendation.text | FDA DMC Guidance (2006) §4.5 |
| {{recommendation_rationale}} | dsmb.meetings[n].recommendation.rationale | FDA DMC Guidance (2006) §4.5 |
| {{action_item_1}} | dsmb.meetings[n].actions[0].description | FDA DMC Guidance (2006) §4.5 |
| {{action_item_1_owner}} | dsmb.meetings[n].actions[0].owner | FDA DMC Guidance (2006) §4.5 |
| {{action_item_1_due}} | dsmb.meetings[n].actions[0].due | FDA DMC Guidance (2006) §4.5 |
| {{next_meeting_date}} | dsmb.meetings[n+1].date | FDA DMC Guidance (2006) §4.3 |
| {{next_review_trigger}} | dsmb.meetings[n+1].trigger | FDA DMC Guidance (2006) §4.3 |
| {{minutes_author}} | dsmb.meetings[n].minutes_author | FDA DMC Guidance (2006) §4.4.3 |
| {{minutes_date}} | dsmb.meetings[n].minutes_date | FDA DMC Guidance (2006) §4.4.3 |
| {{minutes_custodian}} | dsmb.records.minutes_custodian | FDA DMC Guidance (2006) §4.4.3 |
| {{chair_name}} | dsmb.membership.chair.name | FDA DMC Guidance (2006) §4.2.3 |
| {{sponsor_contact_name}} | study.sponsor.contact.name | FDA DMC Guidance (2006) §4.5 |
| {{transmittal_date}} | dsmb.meetings[n].transmittal.date | FDA DMC Guidance (2006) §4.5 |
| {{transmittal_method}} | dsmb.meetings[n].transmittal.method | FDA DMC Guidance (2006) §4.5 |

## Related

- [[03-documents/dsmb-meeting-minutes-and-recommendation]]
- [[03-documents/dsmb-charter-single-site-low-risk]]
- [[03-documents/data-safety-monitoring-plan]]
- [[03-documents/sae-report-investigator-to-sponsor]]
- [[03-documents/ind-safety-report-7-15-day]]
