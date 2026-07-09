---
title: "Form FDA 3926 — Individual Patient Expanded Access IND"
section: "03-documents"
status: confirmed
governing_authority:
  - "21 CFR 312.310 (individual patient expanded access)"
  - "21 CFR 312.305 (general expanded-access criteria and submission)"
  - "21 CFR 312.10 / 56.105 (waivers); Form FDA 3926, OMB No. 0910-0814"
tags: [fda-form/3926, cfr/312, role/sponsor-investigator, lifecycle/expanded-access, ossicro/gating, status/confirmed]
aliases: ["3926", "individual patient expanded access", "compassionate use", "single-patient IND"]
updated: 2026-07-09
---

# Form FDA 3926 — Individual Patient Expanded Access IND

> [!authority] Governing authority
> 21 CFR 312.310 (individual patient expanded access, including emergency use); 21 CFR 312.305 (general criteria and submission requirements); 21 CFR 312.10 and 56.105 (waivers invoked by Fields 10.a / 10.b); Form FDA 3926 (OMB No. 0910-0814); FDA guidance *Individual Patient Expanded Access Applications: Form FDA 3926* (June 2016, updated October 2017). Status: **Confirmed** (the enabling guidance is procedural/non-binding, but the Subpart I criteria and the Part 50/56 requirements it implements are black-letter).

Form FDA 3926 is the streamlined **individual-patient expanded-access IND** application a licensed physician uses to obtain an investigational drug — outside a clinical investigation — for a single patient with a **serious or immediately life-threatening** disease or condition for which there is **no comparable or satisfactory alternative therapy**. It is a tailored substitute for the [Form FDA 1571](form-fda-1571-ind-cover.md) cover otherwise required by § 312.23, sized to the single-patient use case. This is OSSICRO's [guiding-scenario](../00-overview/guiding-scenario.md) instrument: the clinician who has *this patient* and *this candidate therapy* right now. It is one of the three routes covered in [single-patient-site-enrollment](../02-lifecycle/single-patient-site-enrollment.md) and the [expanded-access workflow](../02-lifecycle/expanded-access-workflow.md).

The physician who submits a 3926 is a **[sponsor-investigator](../01-roles-responsibilities/sponsor-investigator.md)** (21 CFR 312.3) and is responsible for the sponsor and investigator duties in [Subpart D](../01-roles-responsibilities/sponsor.md) to the extent applicable to the treatment use — including [IND safety reporting](ind-safety-report.md), annual reporting, and drug-disposition recordkeeping.

## Authorization criteria (must all be met)

Under **§ 312.305(a)** (all expanded access) FDA must determine:
- The patient has a **serious or immediately life-threatening** disease or condition and there is **no comparable or satisfactory alternative** therapy;
- The potential patient benefit **justifies** the potential risks, which are not unreasonable in the context of the disease; and
- Providing the drug **will not interfere** with the initiation, conduct, or completion of clinical investigations that could support approval.

Under **§ 312.310(a)** (individual patient):
- The **patient's physician determines** that the probable risk to the patient from the drug is not greater than the probable risk from the disease or condition; and
- FDA determines the patient cannot obtain the drug under another IND or protocol.

## Field structure and the two waiver checkboxes

Form FDA 3926 collects: the physician's contact information; whether the submission is an **initial written request** or a follow-up (with the IND number); clinical information for the patient; treatment information (drug name, dose, route, planned duration, treatment/monitoring plan); the **Letter of Authorization (LOA)** reference; the physician's qualification statement; the IRB of record; the physician's certification statements; and the signature. Two checkboxes carry regulatory weight:

| Field | Effect | Authority |
|-------|--------|-----------|
| **10.a** | When checked and signed, FDA treats the form as a **request under § 312.10 for a waiver** of the additional Part 312 IND-submission requirements ordinarily met via Form 1571 and Form 1572 (their identity/qualification content is unnecessary for the Agency to evaluate a single-patient use, and noncompliance poses no significant/unreasonable risk to the patient) | 21 CFR 312.10 |
| **10.b** | When checked and signed, FDA treats the form as a **request under § 56.105 for a waiver** of the § 56.108(c) convened-IRB requirement, appropriate when the physician obtains **concurrence of the IRB chairperson (or a designated IRB member)** before treatment begins | 21 CFR 56.105, 56.108(c) |

The **Letter of Authorization** is the pivot: the physician ordinarily references the manufacturer's existing IND (§ 312.305(b)(1)), which requires the **IND holder's permission** in the form of an LOA that lets FDA cross-reference the manufacturer's data. Where no LOA is possible (the supplier has no IND on file), the physician contacts the FDA review division to determine what supporting information is needed.

## Consent, IRB, and the emergency pathway

- **Informed consent (21 CFR Part 50)** applies and **must be obtained before treatment begins**, including in emergencies, unless a Part 50 exception applies. This is the non-delegable [consent event](../04-coordination/informed-consent-document-vs-event.md).
- **IRB requirements (21 CFR Part 56)** apply; IRB approval must be obtained before treatment **unless** it is emergency use, in which case the IRB must be **notified within 5 working days** of treatment (§ 56.104(c)).
- **Emergency use (§ 312.310(d)):** the request may be made by telephone to the FDA review division; FDA may authorize by telephone if the physician explains how the use meets §§ 312.305 and 312.310 and **agrees to submit the written expanded-access application within 15 working days** of authorization.

**Timeline:** in a non-emergency, FDA assigns an IND number and either allows the use to proceed or imposes a [clinical hold](../02-lifecycle/ind-submission-and-30-day-clock.md) (§ 312.42). The IND goes into effect when FDA notifies the physician or, absent notification, **30 days** after FDA receives the completed 3926.

## Non-delegable gates

> [!warning] Non-delegable
> Three functions on the 3926 path stay with humans and counterparties, never OSSICRO:
> 1. **The treatment decision** — the § 312.310(a) determination that the probable risk from the drug is not greater than the probable risk from the disease is the treating physician's medical judgment.
> 2. **Informed consent** — a qualified person obtaining voluntary agreement from the patient (or legally authorized representative) before treatment (21 CFR Part 50). OSSICRO drafts the [consent form](informed-consent-form.md); it does not conduct the [consent event](../04-coordination/informed-consent-document-vs-event.md).
> 3. **The manufacturer's willingness to supply and to grant an LOA** — a counterparty decision by the IND holder. OSSICRO can assemble the request and the package; it cannot compel or substitute for the manufacturer's authorization.
> The physician's signature and certifications, and the IRB's concurrence/approval, are likewise non-delegable.

> [!interpretive] OSSICRO position
> OSSICRO assembles the complete 3926 package — form, clinical narrative, treatment plan, LOA request to the manufacturer, physician qualification statement, and the IRB-concurrence request — and presents it to the physician for review and signature. The engine's validate pass asserts the § 312.305(a)/§ 312.310(a) criteria are each addressed in the record, checks that an LOA reference (or a documented FDA-division contact where no LOA exists) is present, and confirms the consent-before-treatment and IRB (or 5-working-day emergency notification) obligations are surfaced as blocking gates. Because expanded access under FD&C Act § 561 is **excluded** from "applicable clinical trial" (42 CFR 11.10), the engine suppresses a ClinicalTrials.gov registration requirement for the treatment use while still handling the [Form 3674](form-fda-3674-clinicaltrialsgov-certification.md) certification per FDA's enforcement-discretion posture. See [expanded-access-coordination](../04-coordination/expanded-access-coordination.md) and [non-delegable-functions-and-gates](../05-ossicro-system/non-delegable-functions-and-gates.md).

## Related
- [[expanded-access-workflow]]
- [[single-patient-site-enrollment]]
- [[expanded-access-coordination]]
- [[sponsor-investigator]]
- [[form-fda-1571-ind-cover]]
- [[informed-consent-form]]
- [[informed-consent-document-vs-event]]
- [[irb-iec]]
- [[ind-safety-report]]
- [[non-delegable-functions-and-gates]]
- [[guiding-scenario]]

## Sources
- [21 CFR 312.310 — Individual patients, including for emergency use](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.310)
- [21 CFR 312.305 — Requirements for all expanded access uses](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.305)
- [21 CFR 56.104 / 56.105 — Exemptions and waivers of IRB requirements](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-56)
- [FDA Guidance — Individual Patient Expanded Access Applications: Form FDA 3926 (June 2016, updated Oct 2017)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/individual-patient-expanded-access-applications-form-fda-3926) — local original: `../sources/fda-guidance/FDA_Expanded-Access-Form-3926-Instructions.pdf`
- [FDA Guidance — Expanded Access to Investigational Drugs for Treatment Use: Q&A](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/expanded-access-investigational-drugs-treatment-use-questions-and-answers)
