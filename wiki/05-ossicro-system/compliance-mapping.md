---
title: "Compliance Mapping — Artifact → Authority → Validation Rule → Human Sign-off"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "21 CFR Part 312 (IND)"
  - "21 CFR Part 11 (Electronic Records; Electronic Signatures)"
  - "21 CFR Part 50 (Informed Consent); Part 54 (Financial Disclosure); Part 56 (IRB)"
  - "ICH E6(R3) Good Clinical Practice"
tags: [ossicro/engine, ossicro/gating, ossicro/part11, cfr/312, cfr/11, cfr/50, cfr/54, cfr/56, gcp/e6r3, status/interpretive]
aliases: ["Compliance Mapping", "Citation-Carrying Manifest", "Artifact-Authority Map"]
updated: 2026-07-09
---

# Compliance Mapping — Artifact → Authority → Validation Rule → Human Sign-off

> [!authority] Governing authority
> [21 CFR Part 312](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312), [Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11), [Part 50](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50), [Part 54](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54), [Part 56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56); ICH E6(R3). Status: **Mixed** — every row's *authority* column is black-letter; the *validation rule* and *sign-off routing* are the OSSICRO design encoding of that authority, labelled interpretive.

Compliance mapping is the **citation-carrying manifest** at the center of the OSSICRO system: for every artifact the engine produces, it names the governing authority, the machine-checkable validation rule that traces to that authority, and the qualified human who must sign off. It is the operating form of the HARD PRINCIPLE — OSSICRO drafts complete documentation for qualified human review and never owns a non-delegable act — because it makes the human sign-off a *structural field of every artifact*, not a policy statement. If a row has an authority and a rule but no accountable human, the artifact cannot leave the [[generate-check-validate-engine|engine]] as anything but a gated draft.

## The four-column contract

Each generated artifact is described by a row with exactly four load-bearing columns:

1. **Artifact** — the document, form, or record the engine produces (a draft, always).
2. **Governing authority** — the specific CFR subsection / ICH section / FDA guidance the artifact must satisfy. Not a Part-level reference; the exact subsection, so the rule is auditable.
3. **Validation rule** — the machine-checkable predicate the [[generate-check-validate-engine|validate pass]] applies, traced to that authority. A rule that touches an accountable act **fails to a human gate** rather than passing autonomously.
4. **Responsible human sign-off** — the named, qualified human who owns the judgment and the signature. This is a [[non-delegable-functions-and-gates|Gate object]] in the [[data-model]], not a checkbox.

This is the same discipline the FDA 2025 AI-credibility draft guidance asks for — every AI-supported output tied to the regulatory question it bears on and to the human who owns the decision (see [[part-11-and-ai-credibility]]). The prior-art precedent is Vanderbilt's V-CAP, which outputs a personalized required-approvals checklist from structured inputs (PMC3767144); OSSICRO reimplements that pattern independently and extends it from *checklist* to *citation-traced validation with an explicit sign-off owner* (see [[prior-art-vcap-irex-smartirb]]).

> [!interpretive] OSSICRO position
> The claim is not that the manifest *proves* compliance — only a qualified human and, ultimately, FDA can determine that. The claim is that a compliance artifact whose every element carries its citation and its accountable signer is (a) far cheaper for a reviewer to audit than free-text, and (b) structurally incapable of hiding an ungated act, because the missing-signer case is a visible red row in the [[completeness-ledger]]. The mapping is a transparency and auditability instrument, not a substitute for judgment.

## The core mapping

The table below is representative, not exhaustive; the full per-record mapping lives in [[document-catalog]] and the master gate list in [[non-delegable-functions-and-gates]]. Every "responsible human" entry is the party who owns the act by law — OSSICRO's role in every row is *draft and check*.

| Artifact | Governing authority | Validation rule (traced) | Responsible human sign-off |
|---|---|---|---|
| [[form-fda-1571-ind-cover|Form FDA 1571]] (IND cover) | [21 CFR 312.23(a)(1)](https://www.law.cornell.edu/cfr/text/21/312.23) | All required cover fields present; commitment statements intact; sponsor identity consistent across package. | **Sponsor / [[sponsor-investigator]]** — the IND-holder attestation. Non-delegable. |
| [[form-fda-1572-statement-of-investigator|Form FDA 1572]] | [21 CFR 312.53(c)](https://www.law.cornell.edu/cfr/text/21/312.53) | Fields 1-8 complete; §9 commitments present; sub-investigators listed; IRB named; retained by sponsor, **not** filed direct to FDA. | **Investigator** — the personal conduct/consent/IRB commitment. Non-delegable. |
| [[form-fda-3454-3455-financial-disclosure|Form FDA 3454/3455]] | [21 CFR Part 54](https://www.law.cornell.edu/cfr/text/21/part-54); [312.53(c)(4)](https://www.law.cornell.edu/cfr/text/21/312.53) | 3454-vs-3455 selection logic on the $25k/$50k thresholds; one-year post-completion update commitment captured. | **Sponsor** certifies/discloses to FDA; **investigator** self-discloses in the S-I model. Non-delegable. |
| [[informed-consent-form|Informed consent form]] | [21 CFR 50.25](https://www.law.cornell.edu/cfr/text/21/50.25); Common Rule key-information | All §50.25 required elements present; key-information section present; eConsent conforms to Part 11 if electronic. | **IRB** approves the document; **investigator** obtains the consent *event*. Non-delegable — document ≠ event. |
| [[irb-submission-package|IRB submission package]] | [21 CFR 56.111](https://www.law.cornell.edu/cfr/text/21/56.111) | Completeness pre-check against the §56.111 approval criteria; all referenced attachments present. | **IRB** — the approval judgment. Non-delegable; software pre-checks completeness only. |
| [[ind-safety-report|IND safety report]] (7/15-day) | [21 CFR 312.32(c)](https://www.law.cornell.edu/cfr/text/21/312.32) | Report-type × trigger × deadline table (serious + unexpected + suspected → 15-day; fatal/life-threatening → 7-day); clock computed from initial receipt. | **[[medical-monitor|Medical monitor]] / sponsor** — the **causality and expectedness** determination. Non-delegable; the [[safety-clock-engine]] computes the clock but never makes the call and never files. |
| [[ind-annual-report-dsur|IND annual report / DSUR]] | [21 CFR 312.33](https://www.law.cornell.edu/cfr/text/21/312.33); ICH E2F | Due within 60 days of the IND anniversary; required content sections present; DSUR substitution rules applied. | **Sponsor / [[sponsor-investigator]]** signs and submits. |
| [[clinical-protocol-and-synopsis|Clinical protocol]] | [21 CFR 312.23(a)(6)](https://www.law.cornell.edu/cfr/text/21/312.23); ICH M11 | M11 CeSHarP structured-content completeness; internal consistency (objectives ↔ endpoints ↔ analysis). | **[[sponsor-investigator]]** (with [[biostatistician]] for design/analysis). |
| [[statistical-analysis-plan|Statistical analysis plan]] | [ICH E9 / E9(R1)](https://database.ich.org/sites/default/files/E9_Guideline.pdf) | Estimand framework present; analysis populations and methods specified before unblinding. | **[[biostatistician]]** — statistical sign-off is accountable. Non-delegable. |
| [[drug-accountability-log|Drug accountability log]] | [21 CFR 312.57](https://www.law.cornell.edu/cfr/text/21/312.57), [312.59](https://www.law.cornell.edu/cfr/text/21/312.59), [312.61](https://www.law.cornell.edu/cfr/text/21/312.61), [312.62](https://www.law.cornell.edu/cfr/text/21/312.62) | Receipt/storage/dispensing/return/destruction chain complete; quantities reconcile. | **Investigator** (drug control); **sponsor** (disposition records). |
| [[transfer-of-regulatory-obligations-toro|TORO instrument]] | [21 CFR 312.52(a)](https://www.law.cornell.edu/cfr/text/21/312.52) | Each assumed obligation enumerated in writing; any unlisted obligation flagged as **retained by sponsor** by default. | **[[micro-cro-operating-model|Micro-CRO]]** and **sponsor** — both sign; the CRO becomes directly liable to FDA for enumerated items ([§312.52(b)](https://www.law.cornell.edu/cfr/text/21/312.52)). |
| All electronic records/signatures | [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) | Validated system; time-stamped independent audit trail (§11.10(e)); e-signature binding (§11.50, §11.70); access control. | System-enforced; the signing human authenticates per §11.100-11.300. See [[part-11-and-ai-credibility]]. |

## How a rule is encoded

Each validation rule is a small, testable predicate whose identity is its authority citation. The encodable model is Mayo's report-type × trigger × deadline table for safety reporting and MD Anderson's annual-per-IIT-IND recurring-audit cadence (see [[safety-report-timelines-7-15-day]] and [[annual-reporting-and-amendments]]). A rule carries:

- **`authority`** — the exact CFR/ICH subsection (e.g., `21 CFR 312.32(c)(1)`), keyed to [[cfr-citation-map]] and [[ich-guideline-map]].
- **`predicate`** — the machine check (field present, threshold selected, deadline computed, cross-document value identical).
- **`disposition`** — `pass`, `fail-to-fix` (a data/completeness gap the engine can resolve or the human can supply), or `fail-to-gate` (an accountable act that **must** route to a named human and can never auto-pass).
- **`owner`** — the Gate's responsible-human reference.

The cross-document consistency rules (PI name, address, IND number, protocol version identical across the [[form-fda-1572-statement-of-investigator|1572]], [[delegation-of-authority-log|delegation log]], and [[clinical-protocol-and-synopsis|protocol]]) are run by the adversarial pre-review agent described in [[generate-check-validate-engine]] and surfaced to the human alongside the draft.

> [!warning] Non-delegable
> No validation rule in this manifest may carry a `disposition` of `pass` for a row whose act is an accountable human judgment — informed consent, IRB approval, causality/expectedness, statistical sign-off, or the 1571/1572/3454-3455 signatures. Those rows are hard-coded `fail-to-gate`. A `pass` on such a row would be the software asserting an authority it does not have; the [[data-model|Gate object]] makes this state unrepresentable.

## What the mapping produces downstream

- The **[[completeness-ledger]]** renders the manifest as a per-package status: green (validated), amber (needs human judgment = an open gate), red (missing data + the exact resolving question). This is the operating definition of COMPLETE documentation.
- The **[[verifiable-site-qualification-dossier]]** hash-chains the requirement→artifact→citation→signer rows into a manifest a [[pharma-partner-sponsor|pharma partner]] can verify without trusting OSSICRO — the pharma trust wedge.
- The **[[draft-provenance-model]]** links each span of a generated artifact to its source datum and citation, so the manifest's authority column is traceable down to the sentence.
- The **[[references/regulatory-change-log|regulatory-change log]]** uses the manifest as a citation-dependency graph: when eCFR/ICH/FDA text moves, every affected artifact, rule, and page is flagged for a human curator to confirm — the anti-rot mechanism.

## Related

- [[generate-check-validate-engine]]
- [[non-delegable-functions-and-gates]]
- [[completeness-ledger]]
- [[draft-provenance-model]]
- [[verifiable-site-qualification-dossier]]
- [[data-model]]
- [[part-11-and-ai-credibility]]
- [[document-catalog]]
- [[cfr-citation-map]]
- [[ich-guideline-map]]
- [[prior-art-vcap-irex-smartirb]]
- [[references/regulatory-change-log|Regulatory change log]]

## Sources

- [21 CFR Part 312 — Investigational New Drug Application (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312)
- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [21 CFR 312.23 — IND content and format (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.23)
- [21 CFR 312.32 — IND safety reporting (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.32)
- [21 CFR 312.52 — Transfer of obligations to a CRO (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.52)
- [21 CFR 312.53 — Selecting investigators and monitors (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.53)
- [21 CFR 50.25 — Elements of informed consent (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/50.25)
- [21 CFR 56.111 — Criteria for IRB approval of research (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/56.111)
- [21 CFR Part 54 — Financial Disclosure by Clinical Investigators (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/part-54)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025, PDF)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA Draft Guidance — Considerations for the Use of Artificial Intelligence to Support Regulatory Decision-Making (Jan 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological)
- Pulley JM et al., V-CAP required-approvals checklist. PMC[3767144](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3767144/)
