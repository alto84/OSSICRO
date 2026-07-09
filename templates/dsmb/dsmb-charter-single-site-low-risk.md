---
title: "DSMB/DMC Charter (single-site, lower-risk)"
doc_id: "dsmb-charter-single-site-low-risk"
category: "dsmb"
governing_citations: ["FDA Guidance: Clinical Trial Data Monitoring Committees (2006; 2024 draft rev.)"]
owner: "dsmb"
receiver: "sponsor"
gate: "none"
status: template
updated: 2026-07-09
---

# DSMB/DMC Charter (single-site, lower-risk) — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> FDA Guidance for Clinical Trial Sponsors: [Establishment and Operation of Clinical Trial Data Monitoring Committees (2006)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/establishment-and-operation-clinical-trial-data-monitoring-committees) and the [2024 draft revision, Use of Data Monitoring Committees in Clinical Trials](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-data-monitoring-committees-clinical-trials). See also ICH E6(R3) §3.10 ([ich.org](https://www.ich.org/page/efficacy-guidelines)) and, for interim-analysis methodology, ICH E9. This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** This charter establishes the composition, responsibilities, operating procedures, and decision framework of the Data and Safety Monitoring Board (DSMB) / Data Monitoring Committee (DMC) for a single-site, lower-risk investigational study. It is executed at study startup, before the first data review, and governs all DSMB activity for the study.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

[INSTRUCTION: Per the 2006 FDA guidance (§2) and the 2024 draft revision, a DMC is not required for most single-site, lower-risk trials; it is expected for trials with mortality/major-morbidity endpoints, vulnerable populations, or emergency research under 21 CFR 50.24(a)(7)(iv). If this study convenes a DSMB by sponsor choice or under NIH data-and-safety-monitoring policy, this simplified charter is appropriate. If the study instead uses a safety monitoring committee or independent medical monitor, say so in the Data and Safety Monitoring Plan and do not use this charter.]

## Template

### DATA AND SAFETY MONITORING BOARD CHARTER

**Study:** {{protocol_title}}
**Study ID / Protocol Number:** {{study_id}}
**Sponsor / Sponsor-Investigator:** {{sponsor_name}}
**Site:** {{site_name}}
**IND Number (if applicable):** {{ind_number}}
**Charter Version:** {{charter_version}} — **Date:** {{charter_date}}

---

#### 1. Purpose and Scope

This DSMB is convened to safeguard the interests of study participants and to assess, at pre-specified intervals, the safety of study interventions and the continuing validity and scientific merit of {{study_id}}. The DSMB is advisory to the Sponsor; the Sponsor retains final decision authority and regulatory responsibility.

Scope of review: {{scope_of_review}}
[INSTRUCTION: State whether the DSMB reviews safety only, or safety plus enrollment/conduct plus any interim efficacy or futility analyses. For a lower-risk single-site study, safety-and-conduct review without formal efficacy interim analyses is typical.]

#### 2. Membership

The DSMB consists of {{member_count}} voting members, all independent of the study team and free of significant financial or intellectual conflicts of interest with the Sponsor or the investigational product:

| Name | Role on DSMB | Expertise | Affiliation |
|---|---|---|---|
| {{chair_name}} | Chair | {{chair_expertise}} | {{chair_affiliation}} |
| {{member_2_name}} | Voting member | {{member_2_expertise}} | {{member_2_affiliation}} |
| {{member_3_name}} | Voting member (biostatistician) | Biostatistics | {{member_3_affiliation}} |

[INSTRUCTION: The 2006 FDA guidance (§4.2) recommends at minimum a clinician with expertise in the relevant specialty and a biostatistician experienced in clinical trials and interim data monitoring. Three members is a workable minimum for a single-site, lower-risk study. Populate additional rows from {{membership}} as needed. Each member completes a conflict-of-interest disclosure before appointment (see §9).]

Full membership roster with contact details: {{membership}}

Non-voting attendees (open session only, unless the DSMB requests otherwise): {{nonvoting_attendees}} [INSTRUCTION: e.g., sponsor representative, study coordinator, unblinded statistician presenting data.]

#### 3. Responsibilities

The DSMB will:
1. Review and approve this charter, the statistical monitoring guidelines in §7, and the format of data reports before the first data review.
2. Review accumulating safety data (adverse events, serious adverse events, laboratory safety signals, deaths, withdrawals for toxicity) at each scheduled meeting and at any ad hoc meeting.
3. Review study conduct: accrual against projections, protocol deviations, data quality and timeliness, and eligibility violations.
4. Make a formal recommendation to the Sponsor after each review (see §8).
5. Maintain confidentiality of all interim data and deliberations.

The DSMB will NOT: alter the protocol, communicate interim results to the study team or IRB, or make regulatory submissions. Those acts belong to the Sponsor and Investigator.

#### 4. Meeting Schedule and Format

- **Organizational meeting:** {{organizational_meeting_date}}, before or shortly after first participant enrolled.
- **Scheduled data reviews:** {{meeting_schedule}} [INSTRUCTION: State frequency (e.g., every 6 months, or after every N participants complete the DLT window) and the triggering rule. Anchor to enrollment milestones or calendar time, whichever the risk profile warrants.]
- **Ad hoc meetings:** may be called by the Chair, the Sponsor, or the medical monitor upon {{ad_hoc_triggers}} [INSTRUCTION: e.g., any death, any SUSAR, a pre-specified pause criterion being met.]
- **Format:** Meetings follow an open session (study conduct, blinded aggregate data; sponsor/study-team attendees permitted), a closed session (unblinded or by-arm data; voting members and the unblinded statistician only), and an executive session if requested by the Chair. Minutes are kept separately for open and closed sessions.
- **Quorum:** {{quorum_rule}} [INSTRUCTION: e.g., all three voting members, including the Chair and the biostatistician.]

#### 5. Data Flow and Reports

The {{report_preparer}} [INSTRUCTION: e.g., unblinded study statistician or independent statistical center] prepares the DSMB report at least {{report_lead_time}} before each meeting. Report contents: enrollment and disposition, demographics, protocol deviations, AE/SAE listings and summary tables, laboratory shift tables, and {{additional_report_content}}. For blinded studies, unblinded data are provided only in the closed-session report, and treatment codes are held by {{unblinding_custodian}}.

#### 6. Blinding and Access to Interim Data

Interim comparative data are accessible only to DSMB voting members and the unblinded statistician. The Sponsor and study team remain blinded to comparative interim results except as required to act on a DSMB recommendation. [INSTRUCTION: For an open-label single-arm study, replace this section with a statement that data are unblinded by design and confidentiality obligations attach to interim summaries.]

#### 7. Statistical Monitoring Guidelines and Stopping Rules

{{stopping_rules}}

[INSTRUCTION: State the pre-specified guidelines the DSMB uses to recommend pausing or stopping. For a lower-risk single-site study these are typically safety-based, e.g.: (a) pause enrollment if ≥ X of the first N participants experience a Grade ≥3 related AE; (b) stop for any treatment-related death; (c) Bayesian or exact-binomial toxicity boundary tables appended as Appendix A. If formal interim efficacy/futility analyses are planned, specify the alpha-spending approach (e.g., O'Brien-Fleming via Lan-DeMets) and cross-reference the Statistical Analysis Plan. Per the FDA 2006 guidance §6.2, these are guidelines, not binding rules — the DSMB may exercise judgment, and any departure is documented in the minutes.]

#### 8. Recommendations and Communication

After each review the DSMB issues one of the following recommendations to the Sponsor, in writing, within {{recommendation_turnaround}} of the meeting:
- Continue the study without modification;
- Continue with modification (specified);
- Pause enrollment or dosing pending specified actions;
- Terminate the study.

The recommendation and open-session minutes go to {{sponsor_contact_name}} ({{sponsor_contact_email}}). Closed-session minutes and interim data remain sequestered with {{minutes_custodian}} until study unblinding or termination. The Sponsor is responsible for onward communication to the IRB and FDA as required (21 CFR 312.66; 21 CFR 312.32); the DSMB communicates only with the Sponsor.

#### 9. Conflicts of Interest

Each member discloses financial and intellectual interests before appointment and updates the disclosure annually and upon change. {{coi_management}} [INSTRUCTION: State the disqualification threshold, e.g., any equity in the Sponsor or IP-holder, ongoing consulting for the Sponsor beyond DSMB service, or a competing product interest.]

#### 10. Compensation and Indemnification

{{compensation_terms}}

#### 11. Charter Amendments

This charter may be amended by written agreement of the Sponsor and the DSMB Chair; amendments are version-controlled and re-signed.

#### 12. Signatures

| Role | Name | Signature | Date |
|---|---|---|---|
| DSMB Chair | {{chair_name}} | ______________________ | ________ |
| DSMB Member | {{member_2_name}} | ______________________ | ________ |
| DSMB Member (Biostatistician) | {{member_3_name}} | ______________________ | ________ |
| Sponsor / Sponsor-Investigator | {{sponsor_name}} | ______________________ | ________ |

**Appendix A:** {{appendix_a_reference}} [INSTRUCTION: Attach stopping-boundary tables or safety-monitoring boundary tables if used.]

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_title}} | study.protocol.title | ICH M11 |
| {{study_id}} | study.identifiers.study_id | FDA DMC Guidance (2006) §4.4 |
| {{sponsor_name}} | study.sponsor.name | 21 CFR 312.3 |
| {{site_name}} | study.site.name | FDA DMC Guidance (2006) §2 |
| {{ind_number}} | study.identifiers.ind_number | 21 CFR 312.23(a)(1) |
| {{charter_version}} | dsmb.charter.version | FDA DMC Guidance (2006) §4.4 |
| {{charter_date}} | dsmb.charter.date | FDA DMC Guidance (2006) §4.4 |
| {{scope_of_review}} | dsmb.scope | FDA DMC Guidance (2006) §4.1 |
| {{member_count}} | dsmb.membership.count | FDA DMC Guidance (2006) §4.2 |
| {{chair_name}} | dsmb.membership.chair.name | FDA DMC Guidance (2006) §4.2.3 |
| {{chair_expertise}} | dsmb.membership.chair.expertise | FDA DMC Guidance (2006) §4.2.1 |
| {{chair_affiliation}} | dsmb.membership.chair.affiliation | FDA DMC Guidance (2006) §4.2 |
| {{member_2_name}} | dsmb.membership.members[1].name | FDA DMC Guidance (2006) §4.2 |
| {{member_2_expertise}} | dsmb.membership.members[1].expertise | FDA DMC Guidance (2006) §4.2.1 |
| {{member_2_affiliation}} | dsmb.membership.members[1].affiliation | FDA DMC Guidance (2006) §4.2 |
| {{member_3_name}} | dsmb.membership.members[2].name | FDA DMC Guidance (2006) §4.2.1 |
| {{member_3_affiliation}} | dsmb.membership.members[2].affiliation | FDA DMC Guidance (2006) §4.2 |
| {{membership}} | dsmb.membership | FDA DMC Guidance (2006) §4.2 |
| {{nonvoting_attendees}} | dsmb.nonvoting_attendees | FDA DMC Guidance (2006) §4.3.1 |
| {{organizational_meeting_date}} | dsmb.meetings.organizational_date | FDA DMC Guidance (2006) §4.3 |
| {{meeting_schedule}} | dsmb.meeting_schedule | FDA DMC Guidance (2006) §4.3 |
| {{ad_hoc_triggers}} | dsmb.meetings.ad_hoc_triggers | FDA DMC Guidance (2006) §4.3 |
| {{quorum_rule}} | dsmb.meetings.quorum | FDA DMC Guidance (2006) §4.3 |
| {{report_preparer}} | dsmb.data_flow.report_preparer | FDA DMC Guidance (2006) §4.4.2 |
| {{report_lead_time}} | dsmb.data_flow.report_lead_time | FDA DMC Guidance (2006) §4.4.2 |
| {{additional_report_content}} | dsmb.data_flow.report_content | FDA DMC Guidance (2006) §4.4.2 |
| {{unblinding_custodian}} | dsmb.blinding.custodian | FDA DMC Guidance (2006) §4.4.1 |
| {{stopping_rules}} | dsmb.stopping_rules | FDA DMC Guidance (2006) §6.2; ICH E9 |
| {{recommendation_turnaround}} | dsmb.communication.turnaround | FDA DMC Guidance (2006) §4.5 |
| {{sponsor_contact_name}} | study.sponsor.contact.name | FDA DMC Guidance (2006) §4.5 |
| {{sponsor_contact_email}} | study.sponsor.contact.email | FDA DMC Guidance (2006) §4.5 |
| {{minutes_custodian}} | dsmb.records.minutes_custodian | FDA DMC Guidance (2006) §4.4.3 |
| {{coi_management}} | dsmb.coi.management_plan | FDA DMC Guidance (2006) §4.2.2 |
| {{compensation_terms}} | dsmb.compensation | FDA DMC Guidance (2006) §4.2.2 |
| {{appendix_a_reference}} | dsmb.stopping_rules.appendix | FDA DMC Guidance (2006) §6.2 |

## Related

- [[03-documents/dsmb-charter-single-site-low-risk]]
- [[03-documents/dsmb-meeting-minutes-and-recommendation]]
- [[03-documents/data-safety-monitoring-plan]]
- [[03-documents/safety-management-pharmacovigilance-plan]]
- [[03-documents/statistical-analysis-plan-ich-e9]]
