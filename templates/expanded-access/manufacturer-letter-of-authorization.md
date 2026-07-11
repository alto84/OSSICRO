---
title: "Manufacturer Letter of Authorization (LOA)"
doc_id: "manufacturer-letter-of-authorization"
category: "expanded-access"
governing_citations: ["21 CFR 312.23(b)", "FDCA 561A"]
owner: "sponsor"
receiver: "fda"
gate: "none"
status: template
updated: 2026-07-09
---

# Manufacturer Letter of Authorization (LOA) — TEMPLATE (DRAFT for qualified human review)

> [!warning] Legacy paths (Overhaul P4, m5)
> The `## Fields` table below uses this template's ORIGINAL study-record vocabulary, which predates the canonical intake schema. The canonical dotted field ids live in `engine/registry/routes.json`, and the shipped generator is `ea_generators.gen_loa`. Key renames: `physician.*` → `investigator.*`; `drug.manufacturer` / `drug.manufacturer_address` → `manufacturer.name` / `manufacturer.address`; `loa.referenced_file_numbers` → `manufacturer.ind_dmf_reference`; `fda.review_division` → `submission.fda_division`; `loa.signatory.*` → `manufacturer.loa_signatory` (a RECEIVED-LOA fact — recorded, never drafted); `loa.date` → the physician-entered as-of anchor (`submission.date` et al.). Terms only the manufacturer can supply (sections excluded, effective/expiration) have NO intake field by design and render as explicit MISSING markers in the draft.

> [!authority] Governing authority
> [21 CFR 312.23(b)](https://www.law.cornell.edu/cfr/text/21/312.23) (reference to information submitted by another person requires a written statement authorizing the reference); FD&C Act § 561A, [21 U.S.C. § 360bbb-0](https://www.law.cornell.edu/uscode/text/21/360bbb-0) (manufacturer expanded access policy context); see also [FDA expanded access resources](https://www.fda.gov/news-events/public-health-focus/expanded-access). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The LOA is the manufacturer's (or IND/NDA holder's) written permission for FDA to cross-reference its existing application — IND, NDA/BLA, or Drug Master File — on behalf of a named physician's expanded access request, supplying the chemistry/manufacturing/controls and pharmacology/toxicology information the physician could not otherwise provide. The physician attaches it to Form FDA 3926 (field 6) or an expanded access IND; without it, the physician must submit the 21 CFR 312.305(b) technical package directly.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. The letter is issued on the manufacturer's letterhead and signed by an official authorized to bind the company; OSSICRO drafts it for the manufacturer's review — the physician cannot sign this document on the manufacturer's behalf.

## Template

[INSTRUCTION: Place on {{manufacturer_name}} letterhead.]

{{letter_date}}

Food and Drug Administration
{{fda_review_division}}
[INSTRUCTION: Address to the review division holding the referenced application (e.g., "Division of Oncology 1, Office of Oncologic Diseases, CDER"). For biologics referenced to a BLA/IND held at CBER, address CBER accordingly.]

**Re: Letter of Authorization — Right of Reference to {{referenced_application_type}} {{drug_master_file_reference}} for {{drug_name}}**

Dear Sir or Madam:

Pursuant to 21 CFR 312.23(b), {{manufacturer_name}}, located at {{manufacturer_address}}, hereby authorizes the Food and Drug Administration to reference the following application(s) held by {{manufacturer_name}} on behalf of the party identified below, solely in support of the expanded access use described:

- **Referenced application(s):** {{referenced_application_type}} No. {{drug_master_file_reference}}
  [INSTRUCTION: Identify each referenced file precisely — IND number, NDA/BLA number, and/or DMF number, with the drug/product name as it appears in that file. List multiple lines if more than one file is referenced.]
- **Drug product:** {{drug_name}} ({{dosage_form_strength}})
- **Sections authorized for reference:** {{sections_authorized}}
  [INSTRUCTION: Typically the chemistry, manufacturing, and controls (CMC) information and the pharmacology/toxicology information. State any sections expressly excluded.]

**Authorized party (holder of the right of reference):**

- Name: {{authorized_party}}
- Address: {{authorized_party_address}}
- Purpose: {{scope_of_use}}
  [INSTRUCTION: State the scope narrowly and accurately, e.g., "an individual patient expanded access IND under 21 CFR 312.310 for the treatment of one patient with {{diagnosis}}" or an intermediate-size population per 312.315. The authorization extends only to this use; it is not a general right of reference.]

This authorization is effective as of {{effective_date}} and remains in effect until {{expiration_or_revocation_terms}}, unless earlier revoked by written notice to FDA and the authorized party.

{{manufacturer_name}} will supply {{drug_name}} for the use described above under its applicable expanded access policy (FD&C Act § 561A). [INSTRUCTION: Retain or adapt this sentence per the manufacturer's supply commitment; the LOA itself authorizes reference — the supply arrangement may be documented separately.]

Questions regarding this authorization may be directed to the undersigned.

Sincerely,

______________________________
{{authorized_signatory_name}}
{{authorized_signatory_title}}, {{manufacturer_name}}
Telephone: {{signatory_phone}}  Email: {{signatory_email}}

[INSTRUCTION: Signature must be an official of the manufacturer/application holder with authority to grant rights of reference. Provide a copy to the requesting physician for attachment to Form FDA 3926, and submit the original to the referenced application file per the division's procedures.]

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{letter_date}} | loa.date | 21 CFR 312.23(b) |
| {{fda_review_division}} | fda.review_division | 21 CFR 312.23(b) |
| {{manufacturer_name}} | drug.manufacturer | 21 CFR 312.23(b) |
| {{manufacturer_address}} | drug.manufacturer_address | 21 CFR 312.23(b) |
| {{referenced_application_type}} | loa.referenced_application_type | 21 CFR 312.23(b) |
| {{drug_master_file_reference}} | loa.referenced_file_numbers | 21 CFR 312.23(b) |
| {{drug_name}} | drug.name | 21 CFR 312.23(b) |
| {{dosage_form_strength}} | drug.dosage_form_strength | 21 CFR 312.305(b)(2)(v) |
| {{sections_authorized}} | loa.sections_authorized | 21 CFR 312.23(b) |
| {{authorized_party}} | physician.name | 21 CFR 312.23(b) |
| {{authorized_party_address}} | physician.address | 21 CFR 312.23(b) |
| {{scope_of_use}} | loa.scope_of_use | 21 CFR 312.310; 312.315 |
| {{diagnosis}} | patient.diagnosis | 21 CFR 312.305(a)(1) |
| {{effective_date}} | loa.effective_date | 21 CFR 312.23(b) |
| {{expiration_or_revocation_terms}} | loa.expiration_terms | 21 CFR 312.23(b) |
| {{authorized_signatory_name}} | loa.signatory.name | 21 CFR 312.23(b) |
| {{authorized_signatory_title}} | loa.signatory.title | 21 CFR 312.23(b) |
| {{signatory_phone}} | loa.signatory.phone | — |
| {{signatory_email}} | loa.signatory.email | — |

## Related
- [[03-documents/manufacturer-letter-of-authorization]] — wiki document page
- [[form-fda-3926-individual-patient-expanded-access]] — the application this LOA supports (field 6)
- [[expanded-access-treatment-plan]] — the clinical plan the LOA's technical cross-reference completes
