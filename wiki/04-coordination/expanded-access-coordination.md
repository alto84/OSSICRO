---
title: "Expanded-Access Coordination: Physician ↔ Manufacturer ↔ FDA ↔ IRB"
section: "04-coordination"
status: confirmed
governing_authority:
  - "21 CFR Part 312 Subpart I (312.300–312.320)"
  - "21 CFR 312.305 (general criteria); 312.310 (individual patient)"
  - "21 CFR 312.315 (intermediate-size population); 312.320 (treatment IND/protocol)"
  - "21 CFR Part 50 (informed consent); 21 CFR Part 56 (IRB); 56.104(c)/56.105"
  - "FDCA §561 / §561A (manufacturer expanded-access policy, 21st Century Cures)"
tags: [role/sponsor-investigator, role/pharma, role/fda, role/irb, cfr/312, fda-form/3926, lifecycle/expanded-access, ossicro/gating, status/confirmed]
aliases: ["expanded access coordination", "compassionate use coordination", "single patient IND concurrence", "LOA to supply"]
updated: 2026-07-09
---

# Expanded-Access Coordination: Physician ↔ Manufacturer ↔ FDA ↔ IRB

> [!authority] Governing authority
> 21 CFR Part 312 Subpart I — § 312.305 (requirements for all expanded-access uses), § 312.310 (individual patients, including emergency use), § 312.315 (intermediate-size patient populations), § 312.320 (treatment IND/protocol); 21 CFR Part 50 (informed consent) and Part 56 (IRB), including § 56.104(c) emergency-use notification and § 56.105 waiver; FDCA § 561 / § 561A (21st Century Cures manufacturer expanded-access policy). Status: **Confirmed** — the criteria, the four-party concurrence, and the consent/IRB requirements are black-letter; the enabling [Form 3926](../03-documents/form-fda-3926-expanded-access.md) guidance is procedural.

Expanded access is **treatment, not research** — "use of an investigational drug when the primary purpose is to diagnose, monitor, or treat a patient rather than to obtain the kind of information generally derived from clinical trials." It is legally and operationally distinct from a [trial enrollment](../02-lifecycle/site-activation.md) and from a [sponsor-investigator IIS](pharma-partner-interface-iis.md): no efficacy endpoint, no randomization, and the "investigator" label does not mean trial participation. What makes expanded access a **coordination** problem rather than a solo act is that authorization requires **four parties to concur** — the treating physician, the drug's manufacturer, FDA, and an IRB — and no single party can compel the others. This page maps that four-way concurrence, its sequencing, and the non-delegable gates OSSICRO must surface at each node.

## The four parties and what each must independently decide

| Party | Decision it owns | Can it be compelled? |
|-------|------------------|----------------------|
| **Treating physician** (becomes [sponsor-investigator](../01-roles-responsibilities/sponsor-investigator.md)) | That the probable risk from the drug is not greater than the probable risk from the disease (§ 312.310(a)); submits the request; obtains consent | No — it is the physician's medical judgment |
| **Manufacturer** (IND holder) | Whether to **supply** the drug and grant a Letter of Authorization | **No — FDA authorization does not compel supply** (FDCA § 561A) |
| **FDA** (review division) | Whether the § 312.305/§ 312.310 criteria are met; allow-to-proceed or [clinical hold](fda-interactions-meetings-holds.md) | — |
| **IRB** | Approval (or, in emergency, post-hoc notification within 5 working days) | No — independent board judgment (Part 56) |

> [!warning] Non-delegable
> **Four independent judgments sit at the four nodes, and OSSICRO owns none of them.** (1) The physician's § 312.310(a) treatment determination is medical judgment. (2) The manufacturer's decision to supply and to grant a Letter of Authorization is a counterparty decision by the IND holder — FDA authorization does **not** compel it (FDCA § 561A). (3) FDA's authorization is the Agency's. (4) The IRB's approval/concurrence is an independent board's. OSSICRO assembles and routes the request package; a qualified human or entity owns and signs at each node. See [non-delegable-functions-and-gates](../05-ossicro-system/non-delegable-functions-and-gates.md).

## The three tiers of Subpart I

| Tier | Section | Scope | Typical instrument |
|------|---------|-------|--------------------|
| **Individual patient** (incl. emergency) | **§ 312.310** | One named patient | [Form FDA 3926](../03-documents/form-fda-3926-expanded-access.md) (or 1571/1572 route) |
| **Intermediate-size population** | **§ 312.315** | A defined group, smaller than a treatment IND | Protocol under new or existing IND |
| **Widespread treatment use** | **§ 312.320** | Broad population, usually late-stage development | Treatment IND / treatment protocol |

All three must satisfy the **§ 312.305(a)** general criteria (see below). The individual-patient tier is OSSICRO's [guiding scenario](../00-overview/guiding-scenario.md) instrument and the focus of [single-patient-site-enrollment](../02-lifecycle/single-patient-site-enrollment.md).

## The § 312.305(a) criteria (all tiers)

FDA must be able to determine that:
1. The patient(s) have a **serious or immediately life-threatening** disease or condition and there is **no comparable or satisfactory alternative** therapy;
2. The potential benefit **justifies** the potential risks, and those risks are not unreasonable in the context of the disease; and
3. Providing the drug **will not interfere** with the initiation, conduct, or completion of clinical investigations that could support marketing approval.

For the individual-patient tier, **§ 312.310(a)** adds: the patient's physician determines the probable risk from the drug is not greater than the probable risk from the disease, and FDA determines the patient cannot obtain the drug under another IND or protocol.

## The Letter of Authorization — the manufacturer node

The **Letter of Authorization (LOA)** is the pivot of the whole coordination. The physician ordinarily references the manufacturer's existing IND (§ 312.305(b)(1)), which requires the **IND holder's permission** in the form of an LOA that lets FDA cross-reference the manufacturer's CMC and safety data. The LOA is the concrete form the manufacturer's "agreement to supply" takes.

- **No LOA possible** (the supplier has no IND on file): the physician contacts the FDA review division to determine what supporting information the Agency needs to evaluate the request directly.
- **The manufacturer cannot be forced.** Under FDCA § 561A (21st Century Cures), certain manufacturers must **publish an expanded-access policy**, but publishing a policy does not obligate the company to grant any individual request. The supply decision is the manufacturer's, full stop.

## Sequencing and timelines

```
Physician determines treatment appropriate (§312.310(a))
      │
      ├──► Contact manufacturer → request LOA / supply agreement   ◄── manufacturer may decline
      │
      ├──► Submit request to FDA (Form 3926 or 1571/1572)
      │        • Non-emergency: FDA assigns IND number; allow-to-proceed or clinical hold (§312.42)
      │        • IND effective on FDA notice, or 30 days after receipt if no notice
      │        • Emergency (§312.310(d)): telephone request to FDA review division;
      │          FDA may authorize by phone; WRITTEN application within 15 WORKING DAYS
      │
      ├──► Informed consent (Part 50) — BEFORE treatment, including in emergencies
      │
      └──► IRB (Part 56):
               • Standard: IRB approval BEFORE treatment
               • Emergency use: IRB NOTIFIED within 5 WORKING DAYS of treatment (§56.104(c))
               • §56.105 waiver: IRB-chair (or designated member) concurrence in lieu of full board
```

Two clocks matter and are easy to miss: the **15-working-day** written-application deadline after an emergency telephone authorization, and the **5-working-day** IRB-notification deadline after emergency treatment without prior approval. OSSICRO's [safety-clock-engine](../05-ossicro-system/safety-clock-engine.md)-style deadline tracking should compute and escalate both, while never itself filing.

## Consent and IRB in expanded access

- **Informed consent (Part 50)** applies fully and **must be obtained before treatment begins**, including in emergencies, unless a Part 50 exception applies. This is the non-delegable [consent event](informed-consent-document-vs-event.md); OSSICRO drafts the [consent form](../03-documents/informed-consent-form.md), it does not conduct consent.
- **IRB (Part 56)** applies. Standard use requires approval before treatment. **Emergency use** (§ 56.104(c)) permits treatment before review provided the IRB is notified within 5 working days. The **§ 56.105 waiver** allows FDA to accept concurrence of the IRB chairperson (or a designated member) in lieu of a convened board for a single-patient use — the mechanism the [Form 3926](../03-documents/form-fda-3926-expanded-access.md) Field 10.b checkbox invokes.

## Post-authorization obligations

Expanded access does not end at the grant. The physician-as-sponsor-investigator carries, to the extent applicable to the treatment use: [IND safety reporting](../03-documents/ind-safety-report.md) (§ 312.32), annual reporting (§ 312.33), drug-accountability and disposition recordkeeping (§ 312.57, § 312.59, § 312.62), and the duty to permit FDA inspection. Adverse events observed during treatment feed the [safety-reporting-workflow](safety-reporting-workflow.md) exactly as in a trial, with causality remaining the physician/medical-monitor's non-delegable call.

## ClinicalTrials.gov and expanded access

Expanded access under FDCA § 561 is **excluded** from the definition of "applicable clinical trial" (42 CFR 11.10), so a ClinicalTrials.gov **results-reporting** obligation does not attach to the treatment use. FDA's expanded-access Q&A and [Form 3674](../03-documents/form-fda-3674-clinicaltrialsgov-certification.md) handling still apply per the Agency's enforcement posture; OSSICRO suppresses the trial-registration requirement for the treatment use while surfacing any residual certification handling.

> [!interpretive] OSSICRO position
> OSSICRO's role in expanded access is **package assembly and four-node routing**, not adjudication. The engine drafts the complete request — [Form 3926](../03-documents/form-fda-3926-expanded-access.md) (or the 1571/1572 route), clinical narrative, treatment/monitoring plan, the LOA request to the manufacturer, physician qualification statement, [consent form](../03-documents/informed-consent-form.md), and the IRB submission or § 56.105 concurrence request — and its validate pass asserts each § 312.305(a) and § 312.310(a) criterion is addressed, that an LOA reference (or documented FDA-division contact) is present, and that the consent-before-treatment and IRB (or 5-working-day emergency-notification) obligations are surfaced as **blocking gates**. The two working-day clocks are computed and escalated. Every one of the four node-decisions is presented for a human/entity to make; OSSICRO never authorizes, never supplies, never consents, and never approves. Status: interpretive as to the automation boundary; the underlying obligations are confirmed.

## Related
- [[form-fda-3926-expanded-access]]
- [[expanded-access-workflow]]
- [[single-patient-site-enrollment]]
- [[single-patient-site-and-pharma-acceptance]]
- [[sponsor-investigator]]
- [[pharma-partner-interface-iis]]
- [[informed-consent-form]]
- [[informed-consent-document-vs-event]]
- [[irb-iec]]
- [[ind-safety-report]]
- [[fda-interactions-meetings-holds]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR Part 312 Subpart I — Expanded Access to Investigational Drugs for Treatment Use (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I)
- [21 CFR 312.305 — Requirements for all expanded access uses](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.305)
- [21 CFR 312.310 — Individual patients, including for emergency use](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.310)
- [21 CFR 312.315 — Intermediate-size patient populations](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.315)
- [21 CFR 56.104 / 56.105 — Exemptions and waivers of IRB requirements](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56)
- [FDA Guidance — Expanded Access to Investigational Drugs for Treatment Use: Q&A](https://www.fda.gov/media/162793/download)
- [FDA — Expanded Access: Information for Physicians](https://www.fda.gov/news-events/expanded-access/expanded-access-information-physicians)
- [FDA Guidance — Individual Patient Expanded Access Applications: Form FDA 3926](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/individual-patient-expanded-access-applications-form-fda-3926)
