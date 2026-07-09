---
title: "Form FDA 3674 — ClinicalTrials.gov Certification of Compliance"
section: "03-documents"
status: confirmed
governing_authority:
  - "42 U.S.C. 282(j)(5)(B) (PHS Act 402(j)(5)(B), FDAAA Title VIII)"
  - "42 CFR Part 11 (ClinicalTrials.gov registration/results)"
  - "Form FDA 3674, OMB No. 0910-0616"
tags: [fda-form/3674, usc/282j, cfr/11, role/sponsor, role/sponsor-investigator, lifecycle/ind, ossicro/gating, status/confirmed]
aliases: ["3674", "ClinicalTrials.gov certification", "FDAAA certification", "402(j) certification"]
updated: 2026-07-09
---

# Form FDA 3674 — ClinicalTrials.gov Certification of Compliance

> [!authority] Governing authority
> 42 U.S.C. § 282(j)(5)(B) (Public Health Service Act § 402(j)(5)(B), added by FDAAA 2007 Title VIII); 42 CFR Part 11 (ClinicalTrials.gov registration and results reporting); Form FDA 3674 (OMB No. 0910-0616). Status: **Confirmed** (the certification requirement is statutory; the accompanying FDA guidance is procedural).

Form FDA 3674 is the **certification of compliance** with the ClinicalTrials.gov data-bank requirements that must accompany specified FDA applications and submissions. Its statutory basis is § 402(j)(5)(B) of the PHS Act ([42 U.S.C. § 282(j)(5)(B)](https://www.law.cornell.edu/uscode/text/42/282)), added by Title VIII of the Food and Drug Administration Amendments Act of 2007 (FDAAA): at the time of submission, the application "shall be accompanied by a certification that all applicable requirements of this subsection have been met," and, **where available, shall include the appropriate National Clinical Trial (NCT) control numbers.** The requirement went into effect December 26, 2007. Registration and results-posting obligations themselves are governed by [42 CFR Part 11](clinicaltrials-gov-registration.md); the 3674 is the attestation that those obligations, to the extent applicable, have been met.

Within an IND, the 3674 is **Field 15, item 12** of the [Form FDA 1571](form-fda-1571-ind-cover.md) contents checklist. FDA recommends a 3674 accompany, among other submissions, an **IND** and a **new clinical protocol submitted to an existing IND** (the latter under 21 CFR 312.30(a)); it need not accompany other IND amendments.

## What the certification asserts
By signing, the submitter certifies that all **applicable** requirements of 42 U.S.C. § 282(j) — including registration of any applicable clinical trial in the trial's data bank — have been met, and supplies the NCT number(s) where available. The signature is a representation to FDA with legal consequences:

> [!warning] Non-delegable
> Failure to submit a required certification, **knowingly submitting a false certification**, failure to submit required clinical-trial information, and submission of false or misleading clinical-trial information are all **prohibited acts** under § 301(jj) of the FD&C Act ([21 U.S.C. § 331(jj)](https://www.law.cornell.edu/uscode/text/21/331)), with enforcement penalties also identified at 42 CFR 11.66. The certification is the responsible party's / sponsor's signed legal representation. OSSICRO drafts and pre-populates the 3674 (including inserting NCT numbers it has on record and asserting the applicable-trial determination as a *proposed* value), but the **certification itself is signed by the qualified human sponsor** — never machine-attested. A false certification is a criminal/civil exposure that only a human can knowingly assume, and only a human can lawfully avoid.

## Applicability logic — including the expanded-access carve-out

OSSICRO's determination of *whether* a trial is an "applicable clinical trial" (and thus whether registration is required and what the 3674 must assert) follows the statutory definition at § 402(j)(1)(A) and 42 CFR 11.10. One carve-out is load-bearing for OSSICRO's [expanded-access](../02-lifecycle/expanded-access-workflow.md) pathway:

> [!interpretive] OSSICRO position
> **Expanded access under FD&C Act § 561 (21 U.S.C. § 360bbb) is excluded from the definition of "applicable clinical trial"** (42 CFR 11.10; FDA 3674 guidance). Treatment use under an individual-patient expanded-access IND ([Form FDA 3926](form-fda-3926-expanded-access.md)) is therefore not itself subject to the individual registration/reporting requirements of Title VIII or 42 CFR Part 11, and FDA exercises enforcement discretion regarding certification for § 561-type INDs. OSSICRO encodes this branch: for an expanded-access IND the engine does **not** raise a ClinicalTrials.gov registration gate on the treatment use, while still surfacing the 3674 in the submission package per FDA's stated recommendation and enforcement-discretion posture. For an interventional [sponsor-investigator study](../01-roles-responsibilities/sponsor-investigator.md) that meets the applicable-clinical-trial definition, the engine raises a **hard registration gate**: the trial must be registered in ClinicalTrials.gov (yielding an NCT number) and the 3674 populated with that NCT number **before** the IND is flagged submission-ready. This applicable/not-applicable determination is proposed by the engine and confirmed by the human sponsor, and is recorded in [compliance-mapping](../05-ossicro-system/compliance-mapping.md).

## Interaction with informed consent
Since Form 3674's implementation, FDA promulgated 21 CFR 50.25(c), requiring a specific statement in certain [informed-consent documents](informed-consent-form.md) about the submission of trial information to ClinicalTrials.gov. OSSICRO's consent-form generator inserts the § 50.25(c) statement for applicable clinical trials, keeping the consent artifact and the 3674 applicability determination consistent.

## OSSICRO engine behavior
- **Generate:** renders the 3674 with the study's NCT number(s) where on record and a proposed applicable/not-applicable classification.
- **Check:** verifies the 3674 is present as item 12 of the [1571](form-fda-1571-ind-cover.md) contents checklist for an IND or a new-protocol submission; verifies an NCT number exists for any trial the engine classified as applicable.
- **Validate:** enforces the registration gate for applicable clinical trials (no NCT number → not submission-ready); applies the § 561 expanded-access carve-out; blocks any machine attempt to mark the certification "signed." The registration/results obligations continue past IND submission and are tracked in [clinicaltrials-gov-registration](clinicaltrials-gov-registration.md).

## Related
- [[form-fda-1571-ind-cover]]
- [[clinicaltrials-gov-registration]]
- [[form-fda-3926-expanded-access]]
- [[expanded-access-workflow]]
- [[informed-consent-form]]
- [[sponsor]]
- [[sponsor-investigator]]
- [[non-delegable-functions-and-gates]]
- [[compliance-mapping]]
- [[data-integrations-ctgov-pubmed]]

## Sources
- [42 U.S.C. § 282(j) — Clinical trial registry data bank](https://www.law.cornell.edu/uscode/text/42/282)
- [42 CFR Part 11 — Clinical Trials Registration and Results Information Submission](https://www.ecfr.gov/current/title-42/chapter-I/subchapter-A/part-11)
- [21 U.S.C. § 331(jj) — Prohibited acts (FDAAA Title VIII)](https://www.law.cornell.edu/uscode/text/21/331)
- [FDA Guidance — Form FDA 3674: Certifications to Accompany Drug, Biological Product, and Device Applications/Submissions (rev. June 2017)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/certifications-accompany-drug-biological-product-and-device-applicationssubmissions-compliance) — local original: `../sources/fda-form/FDA_Form-3674.pdf`
- [ClinicalTrials.gov PRS — registration and NCT numbers](https://prsinfo.clinicaltrials.gov/)
