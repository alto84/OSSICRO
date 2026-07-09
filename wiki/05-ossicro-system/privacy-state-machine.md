---
title: "The Privacy State Machine — Code-Enforced 164.512(i) Preparatory → Enrollment Transition"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "45 CFR 164.512(i) (HIPAA — uses and disclosures for research)"
  - "45 CFR 164.508 (authorization)"
  - "45 CFR 164.514(b), 164.514(e) (de-identification; limited data set)"
  - "45 CFR 164.502(b) (minimum necessary)"
  - "45 CFR 164.528 (accounting of disclosures)"
  - "45 CFR 164.312 (Security Rule — technical safeguards)"
tags: [ossicro/gating, ossicro/matching, ossicro/part11, lifecycle/feasibility, status/interpretive]
aliases: ["Privacy State Machine", "HIPAA State Machine"]
updated: 2026-07-09
---

# The Privacy State Machine — Code-Enforced 164.512(i) Preparatory → Enrollment Transition

> [!authority] Governing authority
> [45 CFR 164.512(i)](https://www.law.cornell.edu/cfr/text/45/164.512) supplies the two research bases the state machine encodes — reviews preparatory to research (§164.512(i)(1)(ii)) and IRB/Privacy-Board waiver (§164.512(i)(1)(i) with criteria at §164.512(i)(2)) — and [45 CFR 164.508](https://www.law.cornell.edu/cfr/text/45/164.508) supplies the authorization path. [§164.502(b)](https://www.law.cornell.edu/cfr/text/45/164.502) (minimum necessary), [§164.514](https://www.law.cornell.edu/cfr/text/45/164.514) (de-identification; limited data set), [§164.528](https://www.law.cornell.edu/cfr/text/45/164.528) (accounting of disclosures), and [§164.312](https://www.law.cornell.edu/cfr/text/45/164.312) (technical safeguards) condition how each state operates. Status: **Mixed** — the HIPAA requirements are confirmed black-letter law; encoding them as a runtime state machine is the OSSICRO design position.

HIPAA's research provisions draw a bright line that most systems enforce only as policy: a covered entity may *use* PHI to look for a matching trial without the patient's authorization, but the moment the activity becomes research participation — enrollment, disclosure to a sponsor, entry of identified data into research records — a different legal basis is required. OSSICRO enforces this line in code. The privacy state machine is a runtime component (deployed inside the covered entity's boundary — [[offline-local-deployment]]) that assigns every unit of patient data a state, restricts what each state permits at the capability level, and makes the preparatory → enrollment transition a hard, logged, artifact-gated event rather than a habit of good behavior. It is the enforcement half of the legal analysis at [[hipaa-and-privacy-gating]]; this page specifies the states, guards, and transitions.

## The states

| State | Legal basis | What is permitted | What is blocked |
|---|---|---|---|
| `S0 NO_DATA` | — | Trial browsing against public registries with no patient data ([[data-integrations-ctgov-pubmed]]) | Any PHI read |
| `S1 PREPARATORY` | §164.512(i)(1)(ii) | Local chart ingestion ([[smart-on-fhir-integration]]), eligibility adjudication ([[matching-eligibility-adjudication]]), feasibility counts, panel screening | PHI egress of any kind; export; disclosure to sponsor/pharma/Micro-CRO; use in enrollment documents |
| `S2 AUTHORIZED` | §164.508 signed authorization (per patient) | Identified data flows into enrollment-stage documents; disclosures named in the authorization | Uses/disclosures beyond the authorization's scope |
| `S2W WAIVED` | §164.512(i)(1)(i) documented IRB/Privacy-Board waiver | Uses/disclosures within the waiver's documented scope | Anything outside the waiver documentation |
| `S3 LDS` | §164.514(e) limited data set + executed data use agreement | Disclosure of the LDS to the DUA counterparty for the DUA's stated purpose | Direct identifiers (the 16 excluded categories); use beyond the DUA |
| `S4 DEID` | §164.514(b) de-identification (safe harbor or expert determination) | Unrestricted under HIPAA (no longer PHI) — e.g., outbound registry queries, evaluation datasets | Re-identification; retention of the crosswalk outside `S1+` controls |

`S1` is where OSSICRO's matching lives and where most of the product's value is created; `S2`/`S2W` is where enrollment documentation lives. `S3` and `S4` are branch states for specific counterparty and query needs, not the main path.

## S1 PREPARATORY — what the regulation actually requires, and how each element is enforced

§164.512(i)(1)(ii) permits use of PHI without authorization where the covered entity obtains the researcher's representations that:

- **(A)** the use is *sought solely to review PHI as necessary to prepare a research protocol or for similar purposes preparatory to research* — enforced by capability restriction: in `S1`, the only operations the system exposes are matching, feasibility, and protocol-preparation views. Document generation that would embed identified data is disabled.
- **(B)** *no PHI is removed from the covered entity by the researcher in the course of review* — enforced at the network layer: in `S1` the deployment's egress policy blocks PHI-bearing payloads entirely; outbound registry queries carry only de-identified parameters ([[offline-local-deployment]]). Local exports (files, clipboard-scale extracts) of identified matching data are likewise disabled.
- **(C)** *the PHI is necessary for the research purposes* — enforced as minimum-necessary scoping (§164.502(b)): FHIR scopes and field-level filters expose only data classes the active criteria set requires; reads are **ephemeral and audited** — each access is logged (identity, resource, timestamp, purpose), and extracts are purged when the preparatory session or screening run ends rather than accumulating into a shadow registry.

The researcher's (A)–(C) representations are captured as a signed record at `S1` activation, so the covered entity's regulatory predicate for the state is itself a retained, auditable artifact.

An operational nuance the state machine deliberately does not disturb: a treating physician discussing a trial option with their own patient is a treatment communication, not a research disclosure — HHS's research guidance recognizes the treating relationship as the ordinary route from identification to conversation. The state machine governs *OSSICRO's* uses of data; it does not (and could not) gate the physician-patient conversation.

## The transition: preparatory → enrollment

The transition `S1 → S2` (or `S1 → S2W`) is the fulcrum of the whole design. It fires only when a gating artifact is present, validated, and recorded:

1. **Authorization path (`S2`).** A signed authorization satisfying §164.508(c) — required core elements (description of the information, who may use/disclose, recipients, purpose, expiration event or date, signature and date) and required statements (right to revoke, conditioning rules, redisclosure notice). The engine validates element completeness the way it validates any document ([[generate-check-validate-engine]]); the *research* authorization is typically presented with, or embedded in, the informed consent ([[informed-consent-form]], [[enrollment-and-consent]]).
2. **Waiver path (`S2W`).** IRB or Privacy Board documentation satisfying §164.512(i)(2)(ii): minimal privacy risk (adequate plan to protect identifiers, plan to destroy identifiers at the earliest opportunity consistent with the research, written assurances against reuse/redisclosure), impracticability of the research without the waiver, and impracticability without access to the PHI — plus the identification/date/vote and signature elements of §164.512(i)(2)(i), (iii)–(v).

The transition event is written to the Part 11 audit trail ([[data-model]]) with the artifact's identity and hash, the validating identity, and the timestamp — so every identified datum appearing in any enrollment-stage document is traceable *through the transition event* to its legal basis. Per-patient granularity is mandatory: the state machine tracks basis per patient, not per study; one patient's signed authorization unlocks nothing for the next chart.

Disclosures made under §164.512(i) (waiver path, preparatory representations, decedent research) are subject to the accounting-of-disclosures right at §164.528; the state machine's disclosure log is the system of record from which that accounting is produced.

> [!warning] Non-delegable
> The state machine gates on artifacts; humans and boards create them. The waiver determination belongs to a properly constituted IRB or Privacy Board ([[irb-iec]]) — OSSICRO can draft the waiver request and pre-check it against the §164.512(i)(2) criteria, but the approval judgment is the board's alone. The authorization belongs to the patient, obtained within the consent process that is itself a non-delegable human event ([[informed-consent-document-vs-event]]). And the covered entity's own HIPAA compliance obligations are not assumed by deploying OSSICRO. See [[non-delegable-functions-and-gates]].

## Failure posture and Security Rule alignment

The machine fails closed: an absent, expired, or revoked artifact means the data stays in (or reverts toward) `S1` restrictions, and a revocation of authorization (§164.508(b)(5)) halts further use except as already relied upon. Attempted operations that a state forbids are refused *and logged* — a denial is audit-trail evidence, not a silent no-op. Technically, the state machine is how the deployment discharges Security Rule expectations: access control (§164.312(a)), audit controls (§164.312(b)), integrity (§164.312(c)(1)), and transmission security (§164.312(e)) all have their research-context implementation here, sitting on the covered entity's §164.308(a)(1) risk analysis.

> [!interpretive] OSSICRO position
> HIPAA nowhere requires that the preparatory/enrollment boundary be enforced by software; it requires the legal bases and the covered entity's compliance. OSSICRO's thesis is that the boundary is exactly the kind of rule that policy enforcement handles badly and code enforces well — the same reasoning as the [[generate-check-validate-engine]]'s human gates. Encoding it also produces a side benefit: the state-transition log is affirmative evidence of compliance (which basis, which artifact, which date, which data), useful in an OCR inquiry or sponsor audit in a way that a written policy never is.

## Related

- [[hipaa-and-privacy-gating]]
- [[smart-on-fhir-integration]]
- [[offline-local-deployment]]
- [[matching-eligibility-adjudication]]
- [[matching-engine]]
- [[patient-trial-matching]]
- [[feasibility-and-patient-matching]]
- [[enrollment-and-consent]]
- [[informed-consent-document-vs-event]]
- [[informed-consent-form]]
- [[irb-iec]]
- [[data-model]]
- [[generate-check-validate-engine]]
- [[non-delegable-functions-and-gates]]
- [[architecture]]

## Sources

- [45 CFR 164.512 — Uses and disclosures for which an authorization or opportunity to agree or object is not required (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/164.512)
- [45 CFR 164.508 — Uses and disclosures for which an authorization is required (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/164.508)
- [45 CFR 164.514 — Other requirements relating to uses and disclosures of PHI (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/164.514)
- [45 CFR 164.502 — Uses and disclosures of PHI: general rules (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/164.502)
- [45 CFR 164.528 — Accounting of disclosures of PHI (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/164.528)
- [45 CFR 164.312 — Technical safeguards (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/164.312)
- [HHS OCR — Research (HIPAA Privacy Rule and research guidance)](https://www.hhs.gov/hipaa/for-professionals/special-topics/research/index.html)
- [NIH — Clinical Research and the HIPAA Privacy Rule (NIH publication)](https://privacyruleandresearch.nih.gov/clin_research.asp)
- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
