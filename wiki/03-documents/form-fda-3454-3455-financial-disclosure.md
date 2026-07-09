---
title: "Forms FDA 3454 / 3455 — Financial Disclosure by Clinical Investigators"
section: "03-documents"
status: mixed
governing_authority:
  - "21 CFR Part 54"
  - "21 CFR 312.53(c)(4)"
  - "Forms FDA 3454 / 3455, OMB No. 0910-0396"
tags: [fda-form/3454, fda-form/3455, cfr/54, role/sponsor, role/sponsor-investigator, role/investigator, lifecycle/activation, ossicro/gating, status/confirmed, status/interpretive]
aliases: ["3454", "3455", "financial disclosure", "Part 54"]
updated: 2026-07-09
---

# Forms FDA 3454 / 3455 — Financial Disclosure by Clinical Investigators

> [!authority] Governing authority
> 21 CFR Part 54 (financial disclosure by clinical investigators); 21 CFR 312.53(c)(4) (sponsor must collect financial-interest information); Forms FDA 3454 (certification) and 3455 (disclosure), OMB No. 0910-0396. Status: **Mixed** — the certification/disclosure requirement is confirmed; the self-disclosure analysis for the sponsor-investigator is an OSSICRO interpretive position.

Part 54 requires an applicant who submits a marketing application to certify the **absence** of, or **disclose** the presence of, specified financial interests and arrangements of each clinical investigator who participated in a covered study. **Form FDA 3454** is the certification (no disclosable interests); **Form FDA 3455** is the disclosure (interests present, with an attachment and a description of steps taken to minimize bias). For the purpose of both forms, "clinical investigator" **includes the investigator's spouse and each dependent child** ([21 CFR 54.2(d)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-54/section-54.2)).

Two timing facts must not be conflated, because OSSICRO's engine gates on both:
1. **Collection** happens at the front of the trial. Under [21 CFR 312.53(c)(4)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53), the sponsor must obtain, before an investigator begins, sufficient financial-interest information to later complete an accurate 3454/3455, **plus the investigator's commitment to update that information for one year following completion of the study.**
2. **Filing** happens at the back end. The completed 3454/3455 accompanies the eventual **marketing application** (NDA/BLA/etc.), not the IND. At the IND/[site-activation](../02-lifecycle/site-activation.md) stage OSSICRO collects and structures the data and drafts the provisional form; it does not file it with FDA until (and unless) a marketing application is assembled.

## What must be disclosed — the Part 54 interest categories

The four disclosable categories (the 3455 checkboxes track these):

| Category | Definition | Citation |
|----------|-----------|----------|
| Compensation affected by outcome | Any financial arrangement whereby the value of compensation to the investigator could be **affected by the study outcome** | 21 CFR 54.2(a) |
| Significant payments of other sorts | Payments from the sponsor with a cumulative monetary value **≥ $25,000** (e.g., grant to fund ongoing research, equipment, retainer for ongoing consultation, honoraria) made during the study and up to one year after completion, exclusive of the costs of conducting the study | 21 CFR 54.2(f) |
| Proprietary interest | A proprietary interest in the tested product (patent, trademark, copyright, licensing agreement) | 21 CFR 54.2(c) |
| Significant equity interest | An equity interest in a **publicly traded** sponsor exceeding **$50,000** in value, or **any** equity interest in a **non-publicly-traded** sponsor, held during the study and for one year after | 21 CFR 54.2(b) |

> The specific dollar thresholds ($25,000; $50,000) and the definitional scope are set by 21 CFR 54.2 and 54.4. OSSICRO cites the regulation, not a paraphrase, at the point of collection.

## The three Form 3454 certification statements

The 3454 requires the applicant to mark exactly one:
1. **As the sponsor of the submitted studies** — certifies no § 54.2(a) outcome-affected arrangement with the listed investigators, no disclosed § 54.2(b) proprietary/equity interest, and no § 54.2(f) significant payments. (Investigator names entered on the form or attached.)
2. **As an applicant submitting a study sponsored by another party** — certifies, based on information obtained from the sponsor or investigators, the same absence of interests.
3. **Due diligence exhausted** — certifies the applicant acted with due diligence to obtain the § 54.4 information from the investigators or sponsor and it was not possible; the reason is attached.

## The sponsor-investigator self-disclosure problem

> [!interpretive] OSSICRO position
> In the [sponsor-investigator](../01-roles-responsibilities/sponsor-investigator.md) model the applicant and the covered clinical investigator are the **same person**. A physician who holds a disclosable interest — an equity stake in the manufacturer, a proprietary interest in the compound, outcome-contingent compensation — **cannot certify it away on a 3454**; the interest must be reported on a **3455** with the required minimization-of-bias attachment. OSSICRO therefore treats the S-I financial-disclosure step as a mandatory self-attestation with a hard branch: the intake collects the § 54.2(a)–(f) data from the physician (and, per § 54.2(d), spouse and dependent children); if any category is positive, the engine routes to a 3455 draft and **blocks** the 3454 path. The physician cannot self-select "no disclosable interest" past a positive datum. This is an OSSICRO design position layered on the confirmed Part 54 requirement, recorded in [compliance-mapping](../05-ossicro-system/compliance-mapping.md).

## Non-delegable gate

> [!warning] Non-delegable
> The certification/disclosure on Form 3454/3455 is a signed representation to FDA about the truthfulness and completeness of financial-interest information. Determining whether an interest is disclosable, and signing the resulting attestation, is the applicant's (sponsor's / sponsor-investigator's) judgment and legal act — not the software's. OSSICRO collects, structures, and drafts; it flags which form is required and why; the human certifies. OSSICRO never asserts "no disclosable interest" as a machine conclusion — absence is a human certification, presence is a human disclosure.

## OSSICRO engine behavior
- **Generate:** builds one 3454 or 3455 **per covered investigator**, populated from the financial-interest intake and the covered-study list.
- **Check:** verifies a financial-interest record exists for every investigator and subinvestigator on the study, and that the one-year post-completion update commitment (§ 312.53(c)(4)) was captured.
- **Validate:** enforces the positive-datum → 3455 branch above; blocks a 3454 whose attached investigator list is incomplete relative to the delegation log; surfaces the marketing-application filing timing so the form is not mis-filed at IND stage.

See the master gate list in [non-delegable-functions-and-gates](../05-ossicro-system/non-delegable-functions-and-gates.md) and the collection step in [site-activation](../02-lifecycle/site-activation.md).

## Related
- [[form-fda-1571-ind-cover]]
- [[form-fda-1572-statement-of-investigator]]
- [[sponsor]]
- [[sponsor-investigator]]
- [[investigator]]
- [[subinvestigator-and-delegation]]
- [[site-activation]]
- [[non-delegable-functions-and-gates]]
- [[compliance-mapping]]

## Sources
- [21 CFR Part 54 — Financial Disclosure by Clinical Investigators](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-54)
- [21 CFR 54.2 — Definitions](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-54/section-54.2)
- [21 CFR 54.4 — Certification and disclosure requirements](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-54/section-54.4)
- [21 CFR 312.53(c)(4) — Sponsor collection of financial-interest information](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53)
- [FDA Form 3454 (Certification)](https://www.fda.gov/media/74190/download) — local original: `../sources/fda-form/FDA_Form-3454.pdf`
- [FDA Form 3455 (Disclosure)](https://www.fda.gov/media/74191/download) — local original: `../sources/fda-form/FDA_Form-3455.pdf`
- [FDA Guidance — Financial Disclosure by Clinical Investigators](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/financial-disclosure-clinical-investigators)
