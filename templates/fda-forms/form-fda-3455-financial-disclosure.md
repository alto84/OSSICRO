---
title: "Form FDA 3455 - Disclosure: Financial Interests of Clinical Investigators"
doc_id: "form-fda-3455-financial-disclosure"
category: "fda-forms"
governing_citations: ["21 CFR 54.4(a)(3)", "Form FDA 3455"]
owner: "sponsor-investigator"
receiver: "fda"
gate: "financial-disclosure-certification"
status: template
updated: 2026-07-09
---

# Form FDA 3455 - Disclosure: Financial Interests of Clinical Investigators — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 54.4(a)(3)](https://www.law.cornell.edu/cfr/text/21/54.4) (disclosure of the specified financial interests and arrangements and the steps taken to minimize potential bias), the defined interests at [21 CFR 54.2](https://www.law.cornell.edu/cfr/text/21/54.2), FDA's evaluation criteria at [21 CFR 54.5](https://www.law.cornell.edu/cfr/text/21/54.5), and Form FDA 3455 itself — obtain the current OMB-approved version from the [FDA Forms index](https://www.fda.gov/about-fda/reports-manuals-forms/forms); FDA's [Financial Disclosure by Clinical Investigators guidance (2013)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/financial-disclosure-clinical-investigators) governs interpretation. This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Form FDA 3455 discloses to FDA, for each clinical investigator in a covered study who has a disclosable financial interest or arrangement (as defined at 21 CFR 54.2(a), (b), (c), and (f)), the nature of that interest and the steps taken to minimize the potential for bias. One form is completed per investigator with disclosable interests; it accompanies the marketing application alongside the Form FDA 3454 certification covering the remaining investigators. Note the sponsor-investigator conflict pattern: a physician who both sponsors the study and holds equity or IP in the product will almost always require a 3455 rather than a 3454 for themselves.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Values are transcribed onto the current OMB-approved Form FDA 3455; this markdown template is the structured worksheet, not the form of record.

## Template

**DISCLOSURE: FINANCIAL INTERESTS AND ARRANGEMENTS OF CLINICAL INVESTIGATORS**

*(21 CFR Part 54)*

**Covered study:** {{protocol_title}} (protocol {{protocol_number}})

**1. Name and address of the clinical investigator to whom this disclosure applies**

{{investigator_name}}
{{investigator_address}}

**2. Disclosable financial interests and arrangements** [INSTRUCTION: Check every category that applies and describe the interest with enough specificity for FDA to evaluate it under 21 CFR 54.5 — nature, magnitude/value, dates held, and relationship to the study outcome. Thresholds per 54.2: "significant equity interest" is any equity in a non-publicly-traded sponsor, or equity exceeding $50,000 in a publicly traded sponsor, during the study or for one year following completion; "significant payments of other sorts" are payments with a cumulative value exceeding $25,000 (grants, equipment, honoraria, consulting fees, excluding the costs of conducting the study) made to the investigator or institution to support the investigator's activities.]

- [ ] Compensation affected by the outcome of clinical studies (21 CFR 54.2(a)) — e.g., compensation tied to a favorable result, or in the form of an equity interest or royalty whose value depends on outcome.
- [ ] Significant equity interest in the sponsor of the covered study (21 CFR 54.2(b)).
- [ ] Proprietary interest in the tested product, including patent, trademark, copyright, or licensing agreement (21 CFR 54.2(c)).
- [ ] Significant payments of other sorts (21 CFR 54.2(f)).

**Details of each disclosed interest:**

{{disclosable_interests}}

[INSTRUCTION: One block per checked category. For a sponsor-investigator disclosing their own interest, state the dual role explicitly — FDA evaluates the disclosure in the context of the study design's protections (54.5(c)).]

**3. Steps taken to minimize the potential for bias resulting from any of the disclosed interests or arrangements** (21 CFR 54.4(a)(3)(v))

{{steps_to_minimize_bias}}

[INSTRUCTION: Describe design-level protections that are actually in place — e.g., blinding/masking of treatment assignment, independent or centrally adjudicated endpoints, an independent DSMB reviewing unblinded data, objective (laboratory/imaging) endpoints, multiple enrolling sites diluting any single investigator's data contribution, third-party statistical analysis, standard-of-care comparator administered per protocol. Do not assert protections the protocol does not contain; the cross-document consistency check validates each claim against the protocol and DSMB charter.]

**Name of person completing this form (applicant/sponsor or authorized representative):** {{certifier_name}}

**Title:** {{certifier_title}}

**Signature:** ______________________________

**Date:** {{disclosure_date}}

> A willfully false statement is a criminal offense (U.S.C. Title 18, Sec. 1001).

> [!warning] Non-delegable
> Financial disclosure certification / disclosure is executed by the investigator (21 CFR 54.4; Forms FDA 3454/3455). Disclosure of financial interests is a personal attestation under Part 54; OSSICRO pre-populates from structured data, but the underlying attestation and the certifying signature are human. The engine cannot finalize this document without a recorded human sign-off.

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_title}} | study.protocol.title | 21 CFR 54.2(e); Form FDA 3455 |
| {{protocol_number}} | study.protocol.number | Form FDA 3455 |
| {{investigator_name}} | investigator.name | 21 CFR 54.4(a)(3)(i); Form FDA 3455 item 1 |
| {{investigator_address}} | investigator.address | Form FDA 3455 item 1 |
| {{disclosable_interests}} | investigator.financial_disclosure.interests[] | 21 CFR 54.4(a)(3)(i)-(iv); 54.2(a),(b),(c),(f) |
| {{steps_to_minimize_bias}} | investigator.financial_disclosure.bias_minimization_steps | 21 CFR 54.4(a)(3)(v) |
| {{certifier_name}} | study.sponsor_investigator.authorized_signer.name | Form FDA 3455 |
| {{certifier_title}} | study.sponsor_investigator.authorized_signer.title | Form FDA 3455 |
| {{disclosure_date}} | gates.financial-disclosure-certification.discharge_date | Form FDA 3455 |

## Related

- [[form-fda-3454-3455-financial-disclosure]] (wiki document page)
- [[form-fda-3454-financial-disclosure-certification]] (companion certification template)
- [[pre-ind-and-ind-preparation]]
- [[dsmb-charter]]
- [[sponsor-investigator]]
