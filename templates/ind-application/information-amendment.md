---
title: "Information Amendment"
doc_id: "information-amendment"
category: "ind-application"
governing_citations: ["21 CFR 312.31"]
owner: "sponsor-investigator"
receiver: "fda"
gate: "submission-to-fda"
status: template
updated: 2026-07-09
---

# Information Amendment  — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.31](https://www.law.cornell.edu/cfr/text/21/312.31) (information amendments to an IND). Related serial-submission mechanics: [21 CFR 312.23(d)](https://www.law.cornell.edu/cfr/text/21/312.23) (numbered serial submissions). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** An information amendment submits essential information to a live IND that is **not** within the scope of a protocol amendment (21 CFR 312.30), an IND safety report (21 CFR 312.32), or the annual report (21 CFR 312.33). Typical content: new chemistry/manufacturing/control (CMC) information, new pharmacology/toxicology data, new technical information, or a report of the discontinuance of a clinical investigation. It is transmitted to FDA under a signed [[form-fda-1571-ind-cover|Form FDA 1571]] as a numbered serial submission.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

[INSTRUCTION: Placed on sponsor letterhead and transmitted with a signed Form FDA 1571. For a sponsor-investigator IND, the sponsor and the signing physician are the same person.]

**{{sponsor_name}}**

{{submission_date}}

Food and Drug Administration
Center for Drug Evaluation and Research (CDER)   [INSTRUCTION: Route to CBER for a biological product.]
{{review_division}}

**RE: Information Amendment**
**IND Number: {{ind_number}}**
**Serial Number: {{serial_number}}**
**Drug/Biologic: {{drug_name}}**
**Content category: {{amendment_content_type}}**   [INSTRUCTION: Identify the category per 21 CFR 312.31(a): "New chemistry, manufacturing, and control information (CMC)"; "New pharmacology/toxicology information"; "New technical information"; or "Report of discontinuance of a clinical investigation." State the category in the subject line and again in section 1.]

Dear Sir or Madam:

Pursuant to 21 CFR 312.31, {{sponsor_name}} submits this information amendment to the above-referenced IND.

### 1. Category and purpose of this amendment
This information amendment is submitted under 21 CFR 312.31(a) as: **{{amendment_content_type}}**.

{{amendment_purpose}}
[INSTRUCTION: State in one or two sentences why the information is being submitted now and what prompted it.]

### 2. Summary of the information submitted
{{summary}}
[INSTRUCTION: Summarize the essential new information. Per 21 CFR 312.31(b), an information amendment should be labeled to identify its content and should not be used to submit protocol changes (use a protocol amendment), safety information reportable under 312.32 (use an IND safety report), or routine annual information (use the annual report). Keep the summary factual; cross-reference the attached detailed reports.]

### 3. Attached documentation
{{attached_documents}}
[INSTRUCTION: List each attachment (e.g., updated CMC section, new toxicology study report, revised specifications) with its location/eCTD node.]

| Attachment | Description | Location/Node |
|---|---|---|
| {{attachment_id}} | {{attachment_description}} | {{attachment_location}} |

### 4. Impact assessment
{{impact_assessment}}
[INSTRUCTION: State the sponsor's assessment of whether the new information affects subject safety, the risk-benefit balance, or the conduct of ongoing studies, and whether any protocol amendment or consent revision follows from it. Any conclusion about subject safety impact is a sponsor medical/scientific judgment drafted here for human sign-off.]

Please direct questions regarding this amendment to the contact below.

Sincerely,

_________________________________________
{{contact_name}}, {{contact_title}}
{{sponsor_name}}
Telephone: {{contact_phone}}

> [!warning] Non-delegable
> Submission to FDA is executed by the sponsor-investigator (21 CFR 312.20, 312.23, 312.31, 312.40; FD&C Act 505(i)). OSSICRO assembles and validates the amendment and drafts this transmittal; the engine cannot finalize it without a recorded human sign-off. Transmitting the amendment — and signing the accompanying Form FDA 1571 — is an explicit human-authorized act; software cannot be the sponsor (21 CFR 312.52).

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{sponsor_name}} | study.sponsor.name | 21 CFR 312.31 |
| {{submission_date}} | amendment.date | 21 CFR 312.31(b) |
| {{review_division}} | submission.review_division | 21 CFR 312.23(d) |
| {{ind_number}} | study.ind.number | 21 CFR 312.31 |
| {{serial_number}} | amendment.serial_number | 21 CFR 312.23(d) |
| {{drug_name}} | study.drug.name | 21 CFR 312.31 |
| {{amendment_content_type}} | amendment.content_type | 21 CFR 312.31(a) |
| {{amendment_purpose}} | amendment.purpose | 21 CFR 312.31(a) |
| {{summary}} | amendment.summary | 21 CFR 312.31(a)-(b) |
| {{attached_documents}} | amendment.attachments[] | 21 CFR 312.31(b) |
| {{attachment_id}} | amendment.attachments[].id | 21 CFR 312.31(b) |
| {{attachment_description}} | amendment.attachments[].description | 21 CFR 312.31(b) |
| {{attachment_location}} | amendment.attachments[].location | 21 CFR 312.31(b) |
| {{impact_assessment}} | amendment.impact_assessment | 21 CFR 312.31(a) |
| {{contact_name}} | study.sponsor.regulatory_contact.name | 21 CFR 312.23(a)(1) |
| {{contact_title}} | study.sponsor.regulatory_contact.title | 21 CFR 312.23(a)(1) |
| {{contact_phone}} | study.sponsor.regulatory_contact.phone | 21 CFR 312.23(a)(1) |

## Related
- [[ind-application-312-23]]
- [[form-fda-1571-ind-cover]]
- [[protocol-amendment-change-in-protocol]]
- [[ind-safety-report-7-15-day]]
- [[ind-annual-report-312-33]]
- [[annual-reporting-and-amendments]]
- [[non-delegable-functions-and-gates]]
