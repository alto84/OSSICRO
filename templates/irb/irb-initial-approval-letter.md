---
title: "IRB Initial Approval Letter"
doc_id: "irb-initial-approval-letter"
category: "irb"
governing_citations: ["21 CFR 56.109(e)", "21 CFR 312.66"]
owner: "irb"
receiver: "investigator"
gate: "irb-approval"
status: template
updated: 2026-07-09
---

# IRB Initial Approval Letter — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 56.109(e)](https://www.law.cornell.edu/cfr/text/21/56.109) (the IRB shall notify investigators and the institution in writing of its decision to approve or disapprove, or of modifications required to secure approval); [21 CFR 312.66](https://www.law.cornell.edu/cfr/text/21/312.66) (the investigator may not begin the investigation at the site without this approval on file). Approval criteria: [21 CFR 56.111](https://www.law.cornell.edu/cfr/text/21/56.111). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The IRB's written notification of its determination to approve a protocol, issued after convened (or, where permitted, expedited) review. This letter — not any internal minute — is the document the investigator files in the regulatory binder and the sponsor verifies before shipping investigational product (21 CFR 312.53(b)). OSSICRO provides this shell so an issuing IRB (or a site reconstructing its expected contents) knows what a complete approval letter contains; the determination itself belongs to the IRB alone.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

**[{{irb_name}} letterhead]**
IRB registration number (per 21 CFR Part 56, Subpart E): {{irb_registration_number}}
{{irb_address}}

{{letter_date}}

{{investigator_name}}, {{investigator_degrees}}
{{site_name}}
{{site_address}}

**Re: NOTICE OF INITIAL APPROVAL — Protocol {{protocol_number}}**

**Protocol title:** {{protocol_title}}
**Protocol version/date approved:** {{protocol_version}}, dated {{protocol_date}}
**Principal Investigator:** {{investigator_name}}
**Review type:** {{review_type}} [INSTRUCTION: "Convened review at the meeting of {{meeting_date}}" or "Expedited review under 21 CFR 56.110, category {{expedited_category}}, on {{expedited_review_date}}". Most greater-than-minimal-risk drug studies require convened review.]
**Approval date:** {{approval_date}}
**Approval expiration date:** {{expiration_date}} [INSTRUCTION: Continuing review must occur at intervals appropriate to the degree of risk and not less than once per year (21 CFR 56.109(f)). The expiration date must not exceed one year from the approval date.]

Dear Dr. {{investigator_name}}:

At its review identified above, {{irb_name}} determined that the above-referenced research satisfies the criteria for approval at 21 CFR 56.111, including: risks to subjects are minimized and reasonable in relation to anticipated benefits; selection of subjects is equitable; informed consent will be sought from each prospective subject or the subject's legally authorized representative in accordance with 21 CFR Part 50 and will be documented in accordance with 21 CFR 50.27; and, where appropriate, adequate provisions exist for monitoring data, protecting privacy, and maintaining confidentiality.

**Documents reviewed and approved:**

| Document | Version | Date |
|----------|---------|------|
| Clinical protocol | {{protocol_version}} | {{protocol_date}} |
| Informed consent form | {{icf_version}} | {{icf_date}} |
| {{other_approved_document}} | {{other_approved_document_version}} | {{other_approved_document_date}} |

[INSTRUCTION: One row per approved document, including recruitment materials and HIPAA authorization if reviewed. Only the IRB-approved (and, where the IRB's SOPs so provide, validation-stamped) version of the consent form may be used to consent subjects.]

**Conditions of approval.** As Principal Investigator you must:

1. Use only the IRB-approved version of the consent form to obtain consent, and give each person signing a copy (21 CFR 50.27(a)).
2. Not initiate any change in the research without prior IRB approval, except where necessary to eliminate apparent immediate hazards to human subjects (21 CFR 56.108(a)(4), 312.66); report any such emergency change promptly.
3. Promptly report to the IRB all unanticipated problems involving risks to human subjects or others, and all serious or continuing noncompliance (21 CFR 56.108(b)).
4. Submit a continuing review progress report before the expiration date above. **If approval lapses, all research activity except that necessary to protect the safety of enrolled subjects must stop.**
5. Notify the IRB when the study is completed or terminated at this site.

This IRB is duly constituted, operates in compliance with 21 CFR Parts 50 and 56, and is registered with FDA/OHRP as listed above.

Sincerely,

______________________________  Date: ____________
{{irb_chair_name}}, {{irb_chair_degrees}}
Chair (or designated voting member), {{irb_name}}

[INSTRUCTION: The signatory must be the IRB Chair or an IRB member/official authorized under the IRB's written procedures — never study staff, never the investigator, never software.]

> [!warning] Non-delegable
> IRB review and approval determination is executed by the IRB (21 CFR 56.108–56.111; 21 CFR 312.66). OSSICRO drafts this template; the engine cannot finalize it without a recorded human sign-off. OSSICRO never renders, records, or simulates an approval on the IRB's behalf; a filled copy of this shell has no regulatory effect until issued and signed by the IRB itself.

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{irb_name}} | study.irb.name | 21 CFR 56.109(e) |
| {{irb_registration_number}} | study.irb.registration_number | 21 CFR 56.106 |
| {{irb_address}} | study.irb.address | — |
| {{letter_date}} | irb.initial_approval.letter_date | 21 CFR 56.109(e) |
| {{investigator_name}} / {{investigator_degrees}} | study.investigator.name / .degrees | 21 CFR 312.66 |
| {{site_name}} / {{site_address}} | study.site.name / .address | — |
| {{protocol_number}} | study.protocol.number | 21 CFR 56.109 |
| {{protocol_title}} | study.protocol.title | 21 CFR 56.109 |
| {{protocol_version}} / {{protocol_date}} | study.protocol.version / .date | 21 CFR 56.109 |
| {{review_type}} | irb.initial_approval.review_type | 21 CFR 56.108(c), 56.110 |
| {{meeting_date}} | irb.initial_approval.meeting_date | 21 CFR 56.108(c) |
| {{expedited_category}} / {{expedited_review_date}} | irb.initial_approval.expedited_category / .expedited_date | 21 CFR 56.110 |
| {{approval_date}} | irb.initial_approval.approval_date | 21 CFR 56.109(e) |
| {{expiration_date}} | irb.initial_approval.expiration_date | 21 CFR 56.109(f) |
| {{icf_version}} / {{icf_date}} | documents.icf.version / .date | 21 CFR 50.27 |
| {{other_approved_document}} (+version/date) | irb.initial_approval.documents[] | 21 CFR 56.109 |
| {{irb_chair_name}} / {{irb_chair_degrees}} | study.irb.chair_name / .chair_degrees | 21 CFR 56.107 |

## Related

- [[irb-submission-package]] — wiki document page covering the IRB document set
- [[irb-review-workflow]] — coordination page for the review cycle this letter concludes
- [[irb-submission-and-approval]] — lifecycle page (startup)
- [[site-activation]] — approval on file is a precondition to shipping IP (21 CFR 312.53(b))
