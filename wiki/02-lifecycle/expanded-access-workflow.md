---
title: "Expanded Access Workflow (Subpart I — Individual, Intermediate, Treatment)"
section: "02-lifecycle"
status: mixed
governing_authority:
  - "21 CFR 312 Subpart I (312.300-312.320)"
  - "21 CFR 312.305 (general criteria)"
  - "21 CFR 312.310 (individual patients, incl. emergency)"
  - "21 CFR 312.315 (intermediate-size populations)"
  - "21 CFR 312.320 (treatment IND/protocol)"
  - "Form FDA 3926"
  - "FDCA §561 / §561A (21st Century Cures expanded-access policy)"
tags: [lifecycle/expanded-access, cfr/312, fda-form/3926, role/investigator, role/pharma, status/mixed]
aliases: ["compassionate use", "single-patient IND", "Subpart I", "treatment use"]
updated: 2026-07-09
---

# Expanded Access Workflow (Subpart I — Individual, Intermediate, Treatment)

> [!authority] Governing authority
> 21 CFR Part 312 **Subpart I** (§§312.300-312.320): §312.305 (general requirements/criteria), §312.310 (individual patients, including emergency use), §312.315 (intermediate-size patient populations), §312.320 (treatment IND/treatment protocol). Request instrument: **Form FDA 3926** for individual-patient access. Manufacturer supply obligation and expanded-access policy: **FDCA §561 / §561A** (21st Century Cures Act). Status: **Confirmed** for the regulatory pathway; **Interpretive** where OSSICRO asserts what its engine may draft vs. what remains a non-delegable human/counterparty act.

Expanded access ("compassionate use") is the pathway by which a patient with a serious or immediately life-threatening disease or condition gains **treatment** access to an investigational drug or biologic outside a clinical trial, when there is no comparable or satisfactory alternative therapy. It is **treatment, not research**: the primary purpose is to diagnose, monitor, or treat the individual patient, not to generate the kind of generalizable data derived from a clinical investigation (21 CFR 312.305(a)). OSSICRO surfaces expanded access as a **distinct workflow**, separated from trial site-enrollment ([[single-patient-site-enrollment]]) and from a [[sponsor-investigator]] IND, because the accountable parties, document sets, and legal exposure differ entirely ([[the-three-pathways-triage]]).

This page is the operating lifecycle for the expanded-access request. It maps the three access categories, the general criteria that gate all of them, the Form FDA 3926 individual-patient path (the OSSICRO primary target), the manufacturer authorization and IRB concurrence that no software can supply, and the safety/recordkeeping obligations that attach once treatment begins.

## The distinction OSSICRO must never blur

Expanded access is one of three ways a physician's patient can reach a pharma investigational product, and the wrong classification carries real regulatory and liability exposure:

- **(A) Site enrollment** — the physician joins a pharma company's existing trial as a site investigator. Research; sponsor is pharma. See [[single-patient-site-enrollment]] route (b).
- **(B) Sponsor-investigator IND** — the physician holds their own IND and studies the drug. Research; sponsor is the physician. See [[iis-request-workflow]] and [[pre-ind-and-ind-preparation]].
- **(C) Expanded access (this page)** — treatment use of an investigational product for a named patient or population. **Not research**; no efficacy endpoint, no randomization; the "investigator" label does not mean trial participation.

> [!warning] Non-delegable
> Whether a given patient's situation is properly an expanded-access **treatment** use or a research enrollment is a clinical and regulatory judgment owned by the treating physician (and, for research, the IRB and sponsor). OSSICRO drafts the triage record and the candidate document set; the pathway election is a qualified human's call. Misclassifying research as treatment (or vice versa) defeats subject protections and can invalidate the regulatory basis for administering the drug.

## The three access categories

Subpart I scales the mechanism to the size of the population and the stage of drug development.

### Individual patients — 21 CFR 312.310

For a single named patient, including the **emergency** case. The treating physician submits the request, ordinarily via **Form FDA 3926** (the streamlined individual-patient expanded-access application), or via the traditional Form FDA 1571/1572 route. Key features:

- **Emergency use (§312.310(d)):** where the situation requires the patient be treated before a written submission can be made, FDA may authorize shipment/use by **telephone or other rapid means**, and the physician must submit the written expanded-access request (Form 3926) **within 15 working days** of the authorization.
- **Treatment plan:** the physician provides a brief clinical history, the treatment plan (dose, route, duration, monitoring), and the rationale that the patient meets the §312.305 criteria.
- **Prescribing safeguards:** the physician agrees to obtain informed consent, to report adverse events, and to obtain IRB review (see IRB concurrence below).

### Intermediate-size patient populations — 21 CFR 312.315

For a group of patients (smaller than a treatment IND population) sharing a disease/condition, where enrollment in a trial is not possible. Requires more supporting information than an individual request (including, where available, evidence the drug is safe at the dose/duration proposed and some evidence of effectiveness) and typically a separate protocol.

### Treatment IND / treatment protocol — 21 CFR 312.320

The widest category: a drug that is under investigation (or has completed trials) for a serious/life-threatening disease, made available to a broad patient population during the review period, when there is preliminary evidence of effectiveness. Requires the most robust supporting data of the three.

## General criteria for all categories — 21 CFR 312.305(a)

Every expanded-access request, regardless of category, must satisfy the following gating criteria, and the FDA reviewer applies them:

1. **Serious or immediately life-threatening disease or condition**, and **no comparable or satisfactory alternative therapy** to diagnose, monitor, or treat it.
2. **Potential patient benefit justifies the potential risks**, and those risks are not unreasonable in the context of the disease.
3. **Providing the investigational drug will not interfere** with the initiation, conduct, or completion of clinical investigations that could support marketing approval, or otherwise compromise the drug's development.

FDA authorization of expanded access is generally reviewed within the standard IND clock, but individual-patient and emergency requests are typically acted on quickly; emergency requests can be authorized immediately by telephone (§312.310(d)).

## The Form FDA 3926 package (OSSICRO primary target)

Form FDA 3926 is the individual-patient expanded-access application; it consolidates the request, the treatment plan, and the physician's letter of authorization acknowledgment into a single streamlined form so the physician does not have to file a full Form 1571 IND. OSSICRO's [[generate-check-validate-engine]] assembles the complete package:

| Component | Source / owner | OSSICRO role |
|---|---|---|
| Form FDA 3926 fields (patient, physician, drug, IND reference) | Treating physician | Draft/auto-populate from structured intake ([[form-fda-3926-expanded-access]]) |
| Clinical history + treatment plan (dose, route, duration, monitoring) | Treating physician | Draft from structured clinical picture; physician reviews and owns |
| Manufacturer **Letter of Authorization (LOA)** to cross-reference the manufacturer's IND / to supply the drug | Manufacturer | Draft the request to the manufacturer; **cannot** supply the manufacturer's agreement |
| IRB review/concurrence evidence | IRB | Assemble the IRB submission; **cannot** grant approval |
| Informed consent form | Physician + IRB | Draft ICF per 21 CFR 50.25; the consent **event** is non-delegable ([[informed-consent-document-vs-event]]) |

> [!interpretive] OSSICRO position
> Form FDA 3926 is among the most tractable generate/check/validate targets in the entire system: the schema is fixed, the FDA field instructions are published, and the completeness rules map cleanly to the §312.305 criteria and the §312.310 emergency-timeline rule. OSSICRO's engine **checks** the drafted 3926 against the criteria, **validates** the 15-working-day follow-up deadline for emergency authorizations, and routes each accountable act to a human gate. This is a low-influence context of use under the FDA 2025 AI-credibility draft framework: the software drafts and times; the physician, the manufacturer, and the IRB decide (see [[part-11-and-ai-credibility]]).

## The two consents you cannot buy: manufacturer supply and IRB concurrence

Two approvals sit outside OSSICRO's reach and outside FDA's power to compel:

### Manufacturer must agree to supply — FDCA §561 / §561A

**FDA authorization of expanded access does not compel the manufacturer to provide the drug.** The company must independently agree to supply, and issue a **Letter of Authorization** permitting the physician's request to reference the manufacturer's IND. Under the 21st Century Cures Act (FDCA §561A), manufacturers of certain investigational products must publicly post an **expanded-access policy**, but a policy is not a promise to any individual patient. The manufacturer's decision balances limited drug supply, trial-enrollment priorities, and liability.

> [!warning] Non-delegable
> The manufacturer's decision to supply the investigational product is a **counterparty business/medical judgment** that OSSICRO cannot make or assume (FDCA §561A). OSSICRO drafts the request to the manufacturer and the LOA acceptance record; the manufacturer's agreement is theirs alone.

### IRB concurrence — 21 CFR Part 56

Expanded-access treatment use requires IRB review and concurrence. For **individual-patient** and **emergency** use, §312.310 and Part 56 permit review by the **IRB chairperson (or a designated member)** rather than a full-board convened meeting, and emergency use may proceed with subsequent reporting to the IRB — but IRB concurrence is still required and is not waived. See [[irb-iec]] and [[expanded-access-coordination]].

> [!warning] Non-delegable
> IRB approval/concurrence is the ethics gate (21 CFR 56.109-56.111; 45 CFR 46). OSSICRO assembles the IRB submission package; the approval judgment belongs to the IRB. Enrollment/treatment is gated on documented concurrence.

## After authorization: consent, safety, and recordkeeping

Once expanded access is authorized and the drug supplied, treatment-use obligations attach to the physician (who functions in the sponsor-investigator-analogous role for the access IND):

- **Informed consent** — 21 CFR 50.25 elements; the consent conversation is a non-delegable human event ([[informed-consent-form]], [[enrollment-and-consent]]).
- **Adverse event / safety reporting** — the physician reports adverse events consistent with 21 CFR 312.32 obligations for the access IND; serious, unexpected, suspected adverse reactions drive the 7-day/15-day IND safety-report clocks. See [[safety-reporting-lifecycle]] and [[ind-safety-report]]. Causality/expectedness is a medical judgment.
- **Drug accountability** — receipt, storage, dispensing, and disposition of the investigational product ([[drug-accountability-log]], 21 CFR 312.57/312.61/312.62), including the investigational-use label (21 CFR 312.6).
- **Recordkeeping / annual report** — for intermediate-size and treatment INDs the sponsor of the access IND files the annual report (312.33) and maintains records; individual-patient use has lighter recordkeeping but still requires AE reporting.

> [!warning] Non-delegable
> Seriousness, causality, and expectedness determinations that trigger a 15-day IND safety report are the treating physician's / medical monitor's judgment (21 CFR 312.32(c)). OSSICRO drafts the MedWatch 3500A / narrative and computes the clock; a qualified human owns and signs the determination ([[medical-monitor]], [[safety-clock-engine]]).

## Where OSSICRO adds value vs. where it stops

OSSICRO removes the paperwork barrier that keeps a busy clinician from ever attempting expanded access: it drafts the complete, cited Form 3926 package, the manufacturer LOA request, the IRB submission, and the consent form; it validates the §312.305 criteria and the emergency 15-working-day deadline; it tracks the AE-reporting clocks after authorization. It never makes the treatment decision, never supplies the manufacturer's agreement, never grants IRB concurrence, and never owns the consent conversation or the causality call. Expanded access is the fastest route to get a named patient a drug, but it yields no trial data and depends on manufacturer sign-off — a fact the engine surfaces at triage so the physician chooses the pathway with eyes open ([[the-three-pathways-triage]], [[two-modes-site-vs-sponsor-investigator]]).

## Related

- [[single-patient-site-enrollment]]
- [[iis-request-workflow]]
- [[the-three-pathways-triage]]
- [[form-fda-3926-expanded-access]]
- [[expanded-access-coordination]]
- [[single-patient-site-and-pharma-acceptance]]
- [[sponsor-investigator]]
- [[irb-iec]]
- [[informed-consent-document-vs-event]]
- [[safety-reporting-lifecycle]]
- [[ind-safety-report]]
- [[drug-accountability-log]]
- [[non-delegable-functions-and-gates]]
- [[pharma-partner-sponsor]]

## Sources

- [21 CFR Part 312 Subpart I — Expanded Access to Investigational Drugs for Treatment Use (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312)
- [21 CFR 312.315 — Intermediate-size patient populations (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.315)
- [FDA — Expanded Access: How to Submit a Request (Forms), incl. Form FDA 3926](https://www.fda.gov/news-events/expanded-access/expanded-access-how-submit-request-forms)
- [FDA — Expanded Access: Information for Physicians](https://www.fda.gov/news-events/expanded-access/expanded-access-information-physicians)
- [FDA Guidance — Individual Patient Expanded Access Applications: Form FDA 3926](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/individual-patient-expanded-access-applications-form-fda-3926)
- [FDA Guidance — Expanded Access to Investigational Drugs for Treatment Use: Qs & As](https://www.fda.gov/media/162793/download)
- [21 CFR 312.32 — IND safety reporting (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
