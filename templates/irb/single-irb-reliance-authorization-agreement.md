---
title: "Single IRB Reliance / Authorization Agreement"
doc_id: "single-irb-reliance-authorization-agreement"
category: "irb"
governing_citations: ["45 CFR 46.114", "NIH NOT-OD-16-094"]
owner: "irb"
receiver: "irb"
gate: "none"
status: template
updated: 2026-07-09
---

# Single IRB Reliance / Authorization Agreement — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [45 CFR 46.114](https://www.law.cornell.edu/cfr/text/45/46.114) (cooperative research; sIRB requirement for federally supported cooperative research conducted in the United States); [NIH NOT-OD-16-094](https://grants.nih.gov/grants/guide/notice-files/NOT-OD-16-094.html) (NIH Single IRB Policy for Multi-Site Research). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The written agreement by which a relying institution cedes IRB review of a specified study (or portfolio) to a reviewing ("single") IRB, and the two organizations allocate the responsibilities that reliance does not transfer. Required documentation of reliance arrangements under 45 CFR 46.114(b)(2); the standing vehicle in practice is often the SMART IRB master agreement, with this document serving as the study-specific implementation.

[INSTRUCTION: Scope check before use. The 46.114(b) sIRB mandate applies to federally supported cooperative research; the NIH policy applies to NIH-funded multi-site studies using the same protocol. FDA has not yet issued conforming sIRB regulations under 21 CFR Parts 50/56 — for FDA-regulated studies, reliance on a central IRB is permitted and common (FDA guidance, "Using a Centralized IRB Review Process in Multicenter Clinical Trials," 2006), but it is contractual, not mandated. State the applicable basis in §1.]

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

**IRB AUTHORIZATION (RELIANCE) AGREEMENT**

**Effective date:** {{effective_date}}

**Reviewing IRB:** {{reviewing_irb}} — IRB registration number {{reviewing_irb_registration}}; operated by {{reviewing_irb_institution}}, FWA {{reviewing_institution_fwa}} [INSTRUCTION: FWA applies where 45 CFR 46 applies; for a purely FDA-regulated study with no federal funding, an FWA may not exist — cite IRB registration only.]

**Relying institution:** {{relying_institution}} — FWA {{relying_institution_fwa}}; Institutional Official: {{relying_institutional_official}}

### 1. Scope

This Agreement applies to: {{scope}}

[INSTRUCTION: Either (a) study-specific — "the research protocol {{protocol_number}}, '{{protocol_title}}', Principal Investigator at the relying institution: {{site_investigator_name}}" — or (b) a defined portfolio/master arrangement. If executed under the SMART IRB Master Common Reciprocal Institutional Review Board Authorization Agreement, cite it here and note that this document functions as the study-specific reliance determination.]

Basis for reliance: {{reliance_basis}} [INSTRUCTION: e.g., "45 CFR 46.114(b) (federally supported cooperative research)"; "NIH Single IRB Policy, NOT-OD-16-094 (NIH-funded multi-site study)"; or "voluntary central-IRB reliance for an FDA-regulated investigation."]

### 2. Responsibilities of the Reviewing IRB

The Reviewing IRB will, for research within scope:

1. Serve as the IRB of record and conduct initial review, continuing review, and review of amendments in accordance with 45 CFR Part 46 and, where applicable, 21 CFR Parts 50 and 56.
2. Review and approve the site-specific consent form(s), incorporating relying-institution required institutional language provided under §3.
3. Review unanticipated problems, serious or continuing noncompliance, and subject complaints referred to it, and make the determinations reserved to the IRB of record.
4. Communicate its determinations in writing to the relying institution's designated point of contact and the site investigator within {{determination_notice_days}} business days.
5. Maintain review records per 21 CFR 56.115 / 45 CFR 46.115 and make them available to the relying institution on request.

### 3. Responsibilities of the Relying Institution

The Relying Institution retains responsibility for all obligations reliance does not transfer, and will:

1. Remain responsible for protecting human subjects at its site, including institutional oversight of its investigators' qualifications, training, conflicts of interest, and compliance.
2. Provide the Reviewing IRB with local context: state and local law requirements, institution-required consent language, and any local considerations bearing on the 56.111 / 46.111 criteria.
3. Report to the Reviewing IRB, within the timelines in the Reviewing IRB's SOPs, all unanticipated problems, protocol deviations, subject complaints, and any serious or continuing noncompliance occurring at its site.
4. Conduct its own ancillary reviews (radiation safety, biosafety, pharmacy, COI, HIPAA where the Reviewing IRB is not designated as Privacy Board) and not permit the research to begin locally until those clearances and the Reviewing IRB approval are both in place.
5. Not apply its own IRB review to research within scope, except to the extent of the ancillary reviews above.

**HIPAA Privacy Board designation:** {{privacy_board_designation}} [INSTRUCTION: State whether the Reviewing IRB will act as Privacy Board for waivers/alterations of HIPAA authorization under 45 CFR 164.512(i) for the relying site, or whether the relying institution retains that function.]

### 4. Communication and records

- Designated contacts: Reviewing IRB — {{reviewing_irb_contact}}; Relying institution — {{relying_institution_contact}}.
- Each party will maintain a copy of this Agreement and make it available to OHRP, FDA, and sponsors on request (45 CFR 46.114(b)(2) documentation requirement).

### 5. Term and termination

This Agreement is effective from {{effective_date}} and continues until the research within scope is closed, or until terminated by either party on {{termination_notice_days}} days' written notice. Termination does not relieve either party of obligations for research conducted while the Agreement was in effect; on termination, the parties will arrange orderly transfer of IRB oversight before any further subject-facing activity.

### 6. Signatures

For the Reviewing IRB / its institution:

______________________________  Date: ____________
{{reviewing_signatory_name}}, {{reviewing_signatory_title}}

For the Relying Institution:

______________________________  Date: ____________
{{relying_institutional_official}}, Institutional Official (or authorized designee)

[INSTRUCTION: Signatories must be officials authorized to bind their institutions — typically the Institutional Official or HRPP director, not the study investigator. OSSICRO drafts and tracks this agreement; execution is an institutional act.]

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{effective_date}} | irb.reliance.effective_date | 45 CFR 46.114(b)(2) |
| {{reviewing_irb}} | irb.reliance.reviewing_irb.name | 45 CFR 46.114(b) |
| {{reviewing_irb_registration}} | irb.reliance.reviewing_irb.registration_number | 21 CFR 56.106 / 45 CFR 46.501 |
| {{reviewing_irb_institution}} | irb.reliance.reviewing_irb.institution | 45 CFR 46.114 |
| {{reviewing_institution_fwa}} | irb.reliance.reviewing_irb.fwa_number | 45 CFR 46.103 |
| {{relying_institution}} | irb.reliance.relying_institution.name | 45 CFR 46.114(b) |
| {{relying_institution_fwa}} | irb.reliance.relying_institution.fwa_number | 45 CFR 46.103 |
| {{relying_institutional_official}} | irb.reliance.relying_institution.institutional_official | 45 CFR 46.114(b)(2) |
| {{scope}} | irb.reliance.scope | 45 CFR 46.114(b)(2) |
| {{protocol_number}} / {{protocol_title}} | study.protocol.number / .title | — |
| {{site_investigator_name}} | study.investigator.name | — |
| {{reliance_basis}} | irb.reliance.basis | 45 CFR 46.114(b); NOT-OD-16-094 |
| {{determination_notice_days}} | irb.reliance.determination_notice_days | — |
| {{privacy_board_designation}} | irb.reliance.privacy_board_designation | 45 CFR 164.512(i) |
| {{reviewing_irb_contact}} / {{relying_institution_contact}} | irb.reliance.contacts.* | — |
| {{termination_notice_days}} | irb.reliance.termination_notice_days | — |
| {{reviewing_signatory_name}} / {{reviewing_signatory_title}} | irb.reliance.signatories.reviewing.* | — |

## Related

- [[single-irb-mandate-and-central-irbs]] — coordination page on the sIRB mandate and central-IRB practice
- [[irb-submission-package]] — wiki document page covering the IRB document set
- [[irb-review-workflow]] — coordination page for the review cycle under reliance
- [[irb-submission-and-approval]] — lifecycle page (startup)
