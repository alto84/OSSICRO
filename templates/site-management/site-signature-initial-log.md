---
title: "Site Signature and Initials Log"
doc_id: "site-signature-initial-log"
category: "site-management"
governing_citations: ["ICH E6(R3) Appendix C"]
owner: "investigator"
receiver: "site-file"
gate: "none"
status: template
updated: 2026-07-09
---

# Site Signature and Initials Log — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [ICH E6(R3) Appendix C](https://www.ich.org/page/efficacy-guidelines) (essential records — signature sheet documenting signatures and initials of all persons authorized to make entries and/or corrections in trial records). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Provides a verified specimen of the signature and initials of every person authorized to make or correct entries in source documents and CRFs at this site, so that any initialed or signed entry in the trial record can be attributed to a specific individual (ALCOA: attributable).

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

### Site Identification

| Field | Value |
|---|---|
| Site name | {{site_name}} |
| Protocol number | {{protocol_number}} |
| Principal Investigator | {{investigator_name}} |

### Signature and Initials Entries

| Name (printed) | Role / title | Specimen signature | Specimen initials | Date added to log | Date removed / departed |
|---|---|---|---|---|---|
| {{staff_name}} | {{staff_role}} | | | {{entry_date}} | {{departure_date}} |
| | | | | | |
| | | | | | |
| | | | | | |

[INSTRUCTION: Every person who will sign or initial any source document, CRF, log, or correction at this site must appear on this log BEFORE their first entry in any trial record — including the Principal Investigator. Signatures and initials are handwritten specimens (or Part 11-compliant electronic equivalents), not typed. Complete the departure date when an individual leaves the study; never delete or obscure a row. This log complements, and does not replace, the Delegation of Authority Log: this log establishes WHO an initial belongs to, the delegation log establishes WHAT they were authorized to do.]

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{site_name}} | site.name | ICH E6(R3) Appendix C |
| {{protocol_number}} | study.protocol.number | ICH E6(R3) Appendix C |
| {{investigator_name}} | site.principal_investigator.name | ICH E6(R3) Appendix C |
| {{staff_name}} | site.staff[].name | ICH E6(R3) Appendix C |
| {{staff_role}} | site.staff[].role | ICH E6(R3) Appendix C |
| {{entry_date}} | site.staff[].signature_log_entry_date | ICH E6(R3) Appendix C |
| {{departure_date}} | site.staff[].departure_date | ICH E6(R3) Appendix C |

## Related
- [[03-documents/site-signature-initial-log]]
- [[03-documents/delegation-of-authority-log]]
- [[03-documents/source-document-worksheet-templates]]
