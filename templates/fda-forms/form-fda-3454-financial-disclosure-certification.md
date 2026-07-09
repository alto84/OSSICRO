---
title: "Form FDA 3454 - Certification: Financial Interests of Clinical Investigators"
doc_id: "form-fda-3454-financial-disclosure-certification"
category: "fda-forms"
governing_citations: ["21 CFR 54.4(a)(1)", "Form FDA 3454"]
owner: "sponsor-investigator"
receiver: "fda"
gate: "financial-disclosure-certification"
status: template
updated: 2026-07-09
---

# Form FDA 3454 - Certification: Financial Interests of Clinical Investigators — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 54.4(a)(1)](https://www.law.cornell.edu/cfr/text/21/54.4) (certification of absence of disclosable financial interests and arrangements), the defined interests at [21 CFR 54.2](https://www.law.cornell.edu/cfr/text/21/54.2), the sponsor collection duty at [21 CFR 312.53(c)(4)](https://www.law.cornell.edu/cfr/text/21/312.53), and Form FDA 3454 itself — obtain the current OMB-approved version from the [FDA Forms index](https://www.fda.gov/about-fda/reports-manuals-forms/forms); FDA's [Financial Disclosure by Clinical Investigators guidance (2013)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/financial-disclosure-clinical-investigators) governs interpretation. This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Form FDA 3454 is the applicant's certification to FDA that none of the listed clinical investigators (and, per Part 54, their spouses and dependent children) had disclosable financial interests or arrangements as defined in 21 CFR 54.2(a), (b), (c), and (f) for the covered clinical studies. It is submitted with a marketing application (NDA/BLA) that relies on covered studies; the underlying attestations are collected from each investigator before the study begins per 21 CFR 312.53(c)(4) and updated for one year after study completion. Any investigator for whom the certification cannot be made must instead be disclosed on Form FDA 3455.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Values are transcribed onto the current OMB-approved Form FDA 3454; this markdown template is the structured worksheet, not the form of record.

## Template

**CERTIFICATION: FINANCIAL INTERESTS AND ARRANGEMENTS OF CLINICAL INVESTIGATORS**

*(21 CFR Part 54)*

**Covered study:** {{protocol_title}} (protocol {{protocol_number}})

[INSTRUCTION: "Covered clinical study" is defined at 21 CFR 54.2(e) — generally any study submitted in a marketing application that the applicant or FDA relies on to establish effectiveness, or any study in which a single investigator makes a significant contribution to the demonstration of safety. Confirm with regulatory counsel which studies in the application are covered before certifying.]

**Certification** [INSTRUCTION: Check exactly ONE option on the form.]

- [ ] **(1)** As the sponsor of the submitted studies, I certify that I have not entered into any financial arrangement with the listed clinical investigators, whereby the value of compensation to the investigator could be affected by the outcome of the study as defined in 21 CFR 54.2(a). I also certify that each listed clinical investigator required to disclose to the sponsor whether the investigator had a proprietary interest in this product or a significant equity in the sponsor as defined in 21 CFR 54.2(b) did not disclose any such interests. I further certify that no listed investigator was the recipient of significant payments of other sorts as defined in 21 CFR 54.2(f).

- [ ] **(2)** As the applicant who is submitting a study or studies sponsored by a firm or party other than the applicant, I certify that based on information obtained from the sponsor or from participating clinical investigators, the applicant has not entered into any financial arrangement with the listed clinical investigators (attached list of investigators: {{investigator_name}}) whereby the value of compensation to the investigator could be affected by the outcome of the study as defined in 21 CFR 54.2(a); that no listed investigator disclosed a proprietary interest in the tested product or significant equity interest in the sponsor of the covered study as defined in 21 CFR 54.2(b); and that no listed investigator was the recipient of significant payments of other sorts as defined in 21 CFR 54.2(f).

- [ ] **(3)** As the applicant, I certify that I have acted with due diligence to obtain from the listed clinical investigators (attached list) or from the sponsor the information required under 54.4 and it was not possible to do so. The reason why this information could not be obtained is attached. [INSTRUCTION: If this option is checked, attach the due-diligence explanation required by 21 CFR 54.4(c) and, for the sponsor-investigator context, expect this option to be rare — the sponsor-investigator holds the information about themselves.]

**Attached list of clinical investigators to whom this certification applies:**

{{investigator_name}} [INSTRUCTION: Attach the complete list of all clinical investigators (including subinvestigators, per the 2013 guidance, where they are listed on the 1572 or make a direct and significant contribution to the data) for each covered study. Every listed investigator must have a signed financial-disclosure attestation on file; any investigator with a disclosable interest moves to Form FDA 3455 instead.]

**Name of person certifying:** {{certifier_name}}

**Title:** {{certifier_title}} [INSTRUCTION: The certifying official must be the applicant/sponsor or an authorized representative; in a sponsor-investigator study this is the sponsor-investigator personally.]

**Firm/organization:** {{certifier_organization}}

**Signature:** ______________________________

**Date:** {{certification_date}}

> A willfully false statement is a criminal offense (U.S.C. Title 18, Sec. 1001).

> [!warning] Non-delegable
> Financial disclosure certification / disclosure is executed by the investigator (21 CFR 54.4; Forms FDA 3454/3455). Certification of financial interests is a personal attestation under Part 54; OSSICRO pre-populates from structured data, but the certifying signature is human. The engine cannot finalize this document without a recorded human sign-off.

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_title}} | study.protocol.title | 21 CFR 54.2(e); Form FDA 3454 |
| {{protocol_number}} | study.protocol.number | Form FDA 3454 |
| {{investigator_name}} | study.investigators[].name (all with financial_disclosure.status = "no disclosable interests") | 21 CFR 54.4(a); 312.53(c)(4) |
| {{certifier_name}} | study.sponsor_investigator.authorized_signer.name | 21 CFR 54.4(a)(1) |
| {{certifier_title}} | study.sponsor_investigator.authorized_signer.title | Form FDA 3454 |
| {{certifier_organization}} | study.sponsor_investigator.organization | Form FDA 3454 |
| {{certification_date}} | gates.financial-disclosure-certification.discharge_date | Form FDA 3454 |

## Related

- [[form-fda-3454-3455-financial-disclosure]] (wiki document page)
- [[form-fda-3455-financial-disclosure]] (companion disclosure template)
- [[pre-ind-and-ind-preparation]]
- [[site-activation]]
- [[investigator]]
