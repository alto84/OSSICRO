---
title: "The Three Pathways — Triage Decision Tree"
section: "00-overview"
status: confirmed
governing_authority:
  - "21 CFR 312.3(b) (sponsor-investigator)"
  - "21 CFR 312.52 (transfer of obligations)"
  - "21 CFR Part 312 Subpart I (312.300–312.320, expanded access)"
  - "21 CFR 312.53(c) (Form FDA 1572)"
tags: [lifecycle/ind, lifecycle/expanded-access, role/investigator, role/sponsor-investigator, status/confirmed]
aliases: ["Three Pathways", "Triage", "Pathway Decision Tree"]
updated: 2026-07-09
---

# The Three Pathways — Triage Decision Tree

> [!authority] Governing authority
> The three pathways are defined by distinct regulatory bases: **(A)** site enrollment under a sponsor's IND ([21 CFR 312.53](https://www.law.cornell.edu/cfr/text/21/312.53), investigator obligations [312.60–312.69](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)); **(B)** sponsor-investigator IND ([21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3), full [312.20–312.59](https://www.law.cornell.edu/cfr/text/21/part-312) obligation set); **(C)** expanded access ([21 CFR Part 312 Subpart I](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-I)). Status: **Confirmed** — the pathway definitions are black-letter; OSSICRO's triage logic is the operational overlay.

When a clinician has a patient and a candidate early-phase therapy, the first decision is *which pathway*. The three are not interchangeable: their document sets, accountable parties, timelines, and legal exposure differ **entirely**. Choosing wrong is expensive and can be unlawful. This page is the decision tree; each branch links to its full workflow.

## The decision tree

```
START: clinician has a patient + a candidate early-phase pharma therapy
│
├─ Q1. Is there an OPEN trial the patient may be eligible for,
│       and will the sponsor accept a new site?
│   │
│   ├─ YES ──────────────────────────────► PATHWAY A — Enroll as a SITE
│   │        (physician = investigator on the sponsor's existing IND)
│   │
│   └─ NO / unsure ──► Q2
│
├─ Q2. Does the clinician want to RUN AN INVESTIGATION
│       (generate generalizable data), and hold their own IND?
│   │
│   ├─ YES ──────────────────────────────► PATHWAY B — SPONSOR-INVESTIGATOR IND
│   │        (physician = sponsor AND investigator; IIS/IIT)
│   │
│   └─ NO ──► Q3
│
└─ Q3. Is the need single-patient TREATMENT (not research),
        no suitable trial available, and a manufacturer willing to supply?
    │
    ├─ YES ──────────────────────────────► PATHWAY C — EXPANDED ACCESS
    │        (treatment use; Subpart I; Form FDA 3926)
    │
    └─ NO ──► No pathway fits; document the indeterminate result and stop.
              Re-run matching as new trials open ([[matching-engine]]).
```

The single-patient (n-of-1) case can resolve to **B** or **C**, and sometimes to a one-patient add under **A**; that branch is detailed in [[single-patient-site-enrollment]].

## Pathway A — Enroll as a site

**What it is:** The pharma company is the [[pharma-partner-sponsor|sponsor]] and holds the IND. The physician joins the existing protocol as a site [[investigator]], taking on the investigator obligation set ([21 CFR 312.60–312.69](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)) but **not** the sponsor obligations.

- **Accountable party:** The pharma sponsor for sponsor duties; the physician for investigator duties (memorialized in the signed [[form-fda-1572-statement-of-investigator|Form FDA 1572]]).
- **Document set:** Site-activation essential documents — 1572, CV/license, [[form-fda-3454-3455-financial-disclosure|financial disclosure]], GCP training, [[clinical-trial-agreement-and-budget|CTA/budget]], IRB approval, lab certs, [[delegation-of-authority-log|delegation log]], drug-accountability SOPs. See [[site-activation]].
- **Legal exposure:** Bounded — the physician answers for site conduct, not for the IND. Lowest barrier; fastest to enrollment.
- **OSSICRO's job:** Produce the site-activation package to sponsor standard so a new/small site becomes acceptable ([[single-patient-site-and-pharma-acceptance]], [[verifiable-site-qualification-dossier]]).

> [!warning] Non-delegable
> The physician's **PI qualification attestation**, the **1572 signature**, **IRB approval**, **informed consent**, and **SAE reporting to the sponsor** remain the physician's/IRB's acts ([312.64](https://www.law.cornell.edu/cfr/text/21/312.64), [312.66](https://www.law.cornell.edu/cfr/text/21/312.66)).

## Pathway B — Sponsor-investigator IND

**What it is:** The physician **both initiates and conducts** the investigation and holds the IND — the [[sponsor-investigator]] construct of [21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3). Every investigator-initiated trial (IIT/IIS) uses this structure. The two role-holders of a conventional trial collapse into one person, who carries **both** obligation sets.

- **Accountable party:** The physician, for everything — the full sponsor set ([312.50–312.59](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)), IND submission/maintenance ([312.20–312.23](https://www.law.cornell.edu/cfr/text/21/312.23)), safety reporting ([312.32](https://www.law.cornell.edu/cfr/text/21/312.32)), annual reports ([312.33](https://www.law.cornell.edu/cfr/text/21/312.33)) **and** the full investigator set ([312.60–312.69](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)).
- **Document set:** The full [[ind-application-312-23|312.23 IND package]] — [[form-fda-1571-ind-cover|Form 1571]], general investigational plan, [[investigators-brochure|IB]], [[clinical-protocol-and-synopsis|protocol]], CMC, pharmacology/toxicology, prior human experience — plus the entire Mode A site package (the physician is also the site). See [[pre-ind-and-ind-preparation]] and [[ind-submission-and-30-day-clock]].
- **Legal exposure:** Highest — direct FDA regulatory relationship, the [30-day clock](https://www.law.cornell.edu/cfr/text/21/312.40), clinical-hold risk ([312.42](https://www.law.cornell.edu/cfr/text/21/312.42)), and personal accountability for data integrity and subject safety.
- **Pharma's role (if any):** Only an IIS supplier/funder via [[iis-request-workflow|Medical Affairs]] — FMV-set, [Sunshine Act](https://www.healthaffairs.org/content/briefs/physician-payments-sunshine-act)-reportable. Pharma is **never** OSSICRO's transferee.
- **OSSICRO's job:** Absorb the coordination labor that makes the dual role practical for a solo clinician; hold the irreducible accountable functions in the [[micro-cro-accountable-layer|micro-CRO]] via a [[transfer-of-regulatory-obligations-toro|TORO]] only where [312.52](https://www.law.cornell.edu/cfr/text/21/312.52) requires an entity.

> [!warning] Non-delegable
> The **1571/1572 legal attestations**, **IND-holder accountability**, the [decision to discontinue an investigation posing an unreasonable and significant risk within 5 working days](https://www.law.cornell.edu/cfr/text/21/312.56), plus all of Mode A's gates. A sponsor-investigator cannot self-delegate these to software.

## Pathway C — Expanded access

**What it is:** Treatment use of an investigational drug for a patient with a serious condition and no comparable alternative, when the patient cannot enroll in a trial — [21 CFR Part 312 Subpart I](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-I). Three sizes: **individual-patient** ([312.310](https://www.law.cornell.edu/cfr/text/21/312.310), incl. emergency), **intermediate-size** ([312.315](https://www.law.cornell.edu/cfr/text/21/312.315)), **treatment IND/protocol** ([312.320](https://www.law.cornell.edu/cfr/text/21/312.320)).

- **This is treatment, not research** — no generalizable-data expectation. It is legally and operationally distinct from a trial.
- **Accountable party:** The treating physician (as expanded-access sponsor or the manufacturer's protocol investigator), the IRB, and the manufacturer.
- **Document set:** [[form-fda-3926-expanded-access|Form FDA 3926]] (individual-patient), the manufacturer's **letter of authorization** (right of reference to the IND/CMC), and **IRB concurrence**. See [[expanded-access-workflow]] and [[expanded-access-coordination]].
- **Timeline:** Non-emergency requests ordinarily may proceed 30 days after FDA receipt; **emergency** use may proceed on FDA authorization (often by phone) with the written submission to follow within 15 working days ([312.310(d)](https://www.law.cornell.edu/cfr/text/21/312.310)).
- **OSSICRO's job:** Generate the 3926 and supporting letters; drive the manufacturer-acceptance backend.

> [!warning] Non-delegable
> The **manufacturer's decision to supply** the drug is a counterparty judgment that no one can compel and OSSICRO cannot make ([FDCA §561A](https://uscode.house.gov/) does not obligate a manufacturer to provide). **IRB concurrence** and the **treating physician's clinical judgment** are likewise reserved.

## Why the triage matters

| | A — Site | B — Sponsor-Investigator | C — Expanded Access |
|---|---|---|---|
| Legal basis | 312.53, 312.60–312.69 | 312.3(b), full Part 312 | Subpart I (312.300–312.320) |
| Holds the IND? | No (sponsor does) | **Yes** | Expanded-access IND / manufacturer protocol |
| Purpose | Research | Research | **Treatment** |
| Physician's burden | Investigator set | **Both** sets | Treating-physician + submission |
| Key form | [[form-fda-1572-statement-of-investigator\|1572]] | [[form-fda-1571-ind-cover\|1571]] + 1572 | [[form-fda-3926-expanded-access\|3926]] |
| Barrier height | Lowest | Highest | Low–moderate |

Picking the pathway is the first gate the clinician passes through. OSSICRO surfaces the tree, but the choice — like every accountable act downstream — is the clinician's. The end-to-end story of a Pathway-A run is in [[guiding-scenario]]; the mode mechanics are in [[two-modes-site-vs-sponsor-investigator]].

## Related

- [[guiding-scenario]]
- [[two-modes-site-vs-sponsor-investigator]]
- [[sponsor-investigator]]
- [[investigator]]
- [[expanded-access-workflow]]
- [[single-patient-site-enrollment]]
- [[legal-thesis-3123-vs-31252]]
- [[non-delegable-functions-and-gates]]

## Sources

- [21 CFR 312.3 — Definitions](https://www.law.cornell.edu/cfr/text/21/312.3)
- [21 CFR Part 312 Subpart D — Sponsor & investigator obligations](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)
- [21 CFR Part 312 Subpart I — Expanded access](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-I)
- [21 CFR 312.310 — Individual patients, including for emergency use](https://www.law.cornell.edu/cfr/text/21/312.310)
- [FDA — Individual Patient Expanded Access: Form FDA 3926 guidance](https://www.fda.gov/media/162793/download)
- [FDA — Overview of Sponsor-Investigator Roles and Responsibilities](https://www.fda.gov/media/174660/download)
- [FDA — Expanded Access: Information for Physicians](https://www.fda.gov/news-events/expanded-access/expanded-access-information-physicians)
