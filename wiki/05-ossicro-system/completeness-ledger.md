---
title: "The Completeness Ledger — Green / Amber / Red Open-Items Contract"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "ICH E6(R3) Appendix C (Essential Records; risk-proportionate)"
  - "21 CFR 312.23 (IND content and format)"
  - "21 CFR 56.111 (criteria for IRB approval — pre-check only)"
  - "21 CFR Part 54 (financial disclosure — 3454/3455 selection logic)"
  - "21 CFR Part 11 (§11.10(e) audit trail for ledger events)"
tags: [ossicro/engine, ossicro/gating, cfr/312, cfr/11, ich/e6r3, status/interpretive]
aliases: ["Completeness Ledger", "Open-Items Contract", "Green Amber Red Ledger"]
updated: 2026-07-09
---

# The Completeness Ledger — Green / Amber / Red Open-Items Contract

> [!authority] Governing authority
> The requirements the ledger tracks are confirmed law and guidance: [21 CFR 312.23](https://www.law.cornell.edu/cfr/text/21/312.23) for IND content, [21 CFR 312.53(c)](https://www.law.cornell.edu/cfr/text/21/312.53) for the investigator package, [21 CFR Part 54](https://www.law.cornell.edu/cfr/text/21/part-54) for financial disclosure, [21 CFR 56.111](https://www.law.cornell.edu/cfr/text/21/56.111) for the IRB-approval pre-check, and ICH E6(R3) Appendix C for essential records, applied risk-proportionately. Status: **Mixed** — the requirements are confirmed; the ledger as an artifact, and its green/amber/red contract, are interpretive OSSICRO constructions. No regulation requires a ledger; the regulations require what the ledger makes checkable.

Every document package OSSICRO produces ships with a machine-checked **completeness ledger**: an enumeration of every requirement applicable to that package, each graded **green** (machine-validated, with the validating rule and citation attached), **amber** (requires human judgment — that is, a gate), or **red** (missing data, with the exact question whose answer resolves it). The ledger is the operating definition of the mission phrase *complete documentation*: in OSSICRO, "complete" never means an unaudited pile of files; it means **this ledger, with every red resolved or explicitly dispositioned and every amber discharged by its qualified human.** The ledger is emitted by the check pass of the [[generate-check-validate-engine]] and is the cover sheet the reviewer opens first in the [[single-pass-review-ux]].

## The requirements universe

"Every applicable requirement" is a computed set, not a fixed checklist, parameterized by pathway and risk:

- **Essential records** per ICH E6(R3) Appendix C (with E6(R2) §8 cross-numbering; see [[document-catalog]]), applied *risk-proportionately* as E6(R3) directs — the applicable rows depend on mode ([[two-modes-site-vs-sponsor-investigator]]), phase, design, and the trial's critical-to-quality factors, and the ledger records *why* each row is in or out of scope.
- **Content-item rules**: the [21 CFR 312.23(a)](https://www.law.cornell.edu/cfr/text/21/312.23) IND content list for Mode B; the [[form-fda-1571-ind-cover|1571]] item checklist; [[form-fda-3926-expanded-access|Form 3926]] items on the expanded-access branch ([21 CFR 312.310](https://www.law.cornell.edu/cfr/text/21/312.310)).
- **Form field rules**: 1572 fields 1–9 against FDA's official instructions; the 3454-versus-3455 selection logic under [Part 54](https://www.law.cornell.edu/cfr/text/21/part-54) (a disclosable interest under §54.2 forces disclosure — it cannot be certified away).
- **Package-composition rules**: the [[irb-submission-package]] pre-checked against [21 CFR 56.111](https://www.law.cornell.edu/cfr/text/21/56.111); the site-activation package against the sponsor's essential-document standard ([[site-activation]], [[startup-tmf-checklist]]).
- **Cross-document consistency**: facts asserted in multiple documents (PI name, IND number, protocol version/date, site identity, sub-investigator lists) verified identical everywhere they appear.

Every rule in this universe traces to a specific CFR/ICH subsection via [[compliance-mapping]]; a rule without a citation does not ship. The published precedent for computing a personalized requirements set from structured study inputs is Vanderbilt's V-CAP ([PMC3767144](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3767144/)); OSSICRO reimplements the pattern independently ([[prior-art-vcap-irex-smartirb]]).

## Grading semantics — precise, and deliberately narrow

**Green — machine-validated.** A checkable predicate exists, ran, and passed: the record is present, the field is populated and format-valid, the transcription matches its source datum ([[draft-provenance-model]]), the cross-document values agree. Green attaches the validating rule, its citation, and the evidence. Green is a *verification claim, never a compliance judgment*: by construction, **no requirement whose satisfaction requires judgment can ever be green by machine action alone.** An IRB-approval line item turns green only on the documented external event — the approval letter, filed and referenced — never on a prediction that approval will issue.

**Amber — requires human judgment.** The requirement is one whose discharge is a qualified human's act: a signature attestation, a seriousness/causality/expectedness call, a statistical sign-off, an eligibility determination, a PI-qualification attestation, an FMV justification on a [[clinical-trial-agreement-and-budget|CTA/budget]]. Each amber item *is* a gate in the sense of [[non-delegable-functions-and-gates]]: it names the act, the qualified human, the reserving authority, and the evidence that will discharge it. **The amber list of a package is exactly its gate list**, and it is what the foregrounded lane of [[single-pass-review-ux]] walks the reviewer through.

**Red — missing data.** The package cannot be completed from what the system has, and the ledger states **the exact question whose answer resolves it** and, where known, where the answer lives: "Date of the investigator's most recent GCP training — CV on file shows none after 2023"; "Sub-investigator DEA number — query the delegation log owner"; "Manufacturer letter of authorization — request via [[expanded-access-coordination|the manufacturer]], cannot be generated." Reds from [[matching-eligibility-adjudication]] close the loop with matching: a criterion graded *indeterminate — needs data* becomes a red carrying the specific chart datum required, routed through the [[privacy-state-machine]] if it requires a chart read.

## Ledger discipline

- **Recomputed, never patched.** The ledger is a deterministic function of the package state and is recomputed on every change. There is no interface for editing a grade directly.
- **Reds cannot be deleted — only resolved or dispositioned.** Resolution means the missing datum was supplied and the predicate now passes. Disposition means a qualified human recorded a not-applicable or justified-exception determination, with rationale — itself an audited, attributed act. A red can never be silenced anonymously.
- **Ambers discharge only through their gates.** A Part 11 signature ([§§11.50–11.300](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)) or a documented external event; nothing else, and never the machine.
- **Every grade transition is an Event** in the [[data-model]] audit trail per [21 CFR 11.10(e)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10) — the ledger's own history is inspectable, and the hash chain makes after-the-fact regrade invisible-editing impossible.
- **The ledger gates the state machine.** A document does not transition to `human-reviewed` with undispositioned ambers, and a package is not presented for filing with unresolved reds ([[data-model]]). Filing itself is always an explicit human-authorized act.
- **The ledger travels with the package.** In the [[verifiable-site-qualification-dossier]], the ledger is part of what a pharma counterparty can verify independently: requirement → artifact → citation → responsible-human signature.

> [!warning] Non-delegable
> The amber lane belongs to humans, categorically. The ledger computes that a judgment is *required* and by *whom*; it never renders the judgment. It can conclude "a 15-day IND safety report is due *if* this event is a serious, unexpected, suspected adverse reaction" and start the escalation timer ([[safety-clock-engine]]) — the causality call itself belongs to the [[medical-monitor]] under [21 CFR 312.32](https://www.law.cornell.edu/cfr/text/21/312.32). It can pre-check an IRB package against [56.111](https://www.law.cornell.edu/cfr/text/21/56.111) — approval belongs to the [[irb-iec|IRB]] alone. A ledger that turned its own ambers green would be the software-as-decision-maker failure the whole system is built to foreclose ([[legal-thesis-3123-vs-31252]], [[non-delegable-functions-and-gates]]).

> [!interpretive] OSSICRO position
> No regulation requires a completeness ledger. What the regulations require is that the records exist, are complete and accurate, and that identified responsibilities are discharged by qualified people — and what FDA inspects (BIMO) is whether they were. The ledger is OSSICRO's mechanism for making that state *checkable at all times rather than discoverable at inspection*: it converts "is this package complete?" from an opinion into a computed, cited, audit-trailed answer, and it converts every open item into either a machine task (red: fetch the datum) or a named human's task (amber: exercise the judgment). This is the contract that makes "OSSICRO drafts COMPLETE documentation for qualified human review" a testable claim rather than a slogan.

## Related

- [[generate-check-validate-engine]]
- [[single-pass-review-ux]]
- [[draft-provenance-model]]
- [[non-delegable-functions-and-gates]]
- [[data-model]]
- [[compliance-mapping]]
- [[document-catalog]]
- [[matching-eligibility-adjudication]]
- [[verifiable-site-qualification-dossier]]
- [[safety-clock-engine]]
- [[irb-submission-package]]
- [[startup-tmf-checklist]]
- [[two-modes-site-vs-sponsor-investigator]]
- [[prior-art-vcap-irex-smartirb]]

## Sources

- [ICH E6(R3) Step 4 Final Guideline (Jan 2025, PDF) — Appendix C, Essential Records](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [21 CFR 312.23 — IND content and format](https://www.law.cornell.edu/cfr/text/21/312.23)
- [21 CFR 312.32 — IND safety reporting](https://www.law.cornell.edu/cfr/text/21/312.32)
- [21 CFR 312.53 — Selecting investigators and monitors](https://www.law.cornell.edu/cfr/text/21/312.53)
- [21 CFR 312.310 — Individual patients (expanded access)](https://www.law.cornell.edu/cfr/text/21/312.310)
- [21 CFR Part 54 — Financial disclosure by clinical investigators](https://www.law.cornell.edu/cfr/text/21/part-54)
- [21 CFR 56.111 — Criteria for IRB approval of research](https://www.law.cornell.edu/cfr/text/21/56.111)
- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [FDA — Instructions for Filling Out Form FDA 1572](https://www.fda.gov/media/79326/download)
- Byrne DW et al., "Vanderbilt Customized Action Plan (V-CAP)" — rules-driven personalized regulatory checklist ([PMC3767144](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3767144/))
