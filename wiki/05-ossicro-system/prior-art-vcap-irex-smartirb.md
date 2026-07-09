---
title: "Prior Art — V-CAP, IREx, SMART IRB, and the Consult-Service Precedents"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "45 CFR 46.114 (cooperative research / single-IRB mandate)"
  - "21 CFR Part 56 (IRB review)"
  - "NIH Single IRB Policy (NOT-OD-16-094)"
tags: [ossicro/engine, ossicro/gating, role/irb, entity/ncats, entity/vanderbilt, lifecycle/irb, status/confirmed, status/interpretive]
aliases: ["Prior Art", "V-CAP", "IREx", "SMART IRB"]
updated: 2026-07-09
---

# Prior Art — V-CAP, IREx, SMART IRB, and the Consult-Service Precedents

> [!authority] Governing authority
> The reliance mechanics described here implement [45 CFR 46.114](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.114) (single-IRB mandate for cooperative research, compliance date 2020-01-20) and the [NIH Single IRB Policy](https://grants.nih.gov/grants/guide/notice-files/NOT-OD-16-094.html) (effective 2018-01-25), operating alongside [21 CFR Part 56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56). Status: **Mixed** — the precedent systems and their published designs are confirmed facts; the claim that they validate OSSICRO's design pattern is the OSSICRO interpretive position.

OSSICRO's core mechanisms are not speculative. Two of its three central design patterns — the rules-driven personalized compliance checklist and programmatic IRB-reliance coordination — have been built, deployed, and published by academic institutions; the third — the shared human regulatory-consult layer — has a decade of peer-reviewed operating history. This page documents the precedents, what each proves, and precisely what OSSICRO takes from each (published methodology, reimplemented independently) versus what it does not (the tools themselves, which are institution-bound or access-gated).

## Vanderbilt V-CAP — the personalized required-approvals checklist

The **Vanderbilt Customized Action Plan (V-CAP)**, built by the Vanderbilt Institute for Clinical and Translational Research (VICTR) and described in a published methodology ([PMC3767144](https://pmc.ncbi.nlm.nih.gov/articles/PMC3767144/)), is an informatics tool that asks an investigator structured questions about a proposed study and returns a printable, individualized list of the institutional approvals and applications that study requires, with links to each application. Vanderbilt's underlying regulatory-landscape assessment identified up to **twenty distinct approval types** a single study can trigger — a number that quantifies exactly the coordination burden OSSICRO exists to absorb. Vanderbilt also operates a Program for Investigator-Initiated Trials that wraps human support around the tool ([VICTR/VCC program page](https://vcc.vumc.org/who-we-are/teams/program-for-investigator-initiated-trials/)).

**What V-CAP proves:** structured study-characteristic inputs can deterministically drive a personalized, complete compliance checklist — the *check* pass of the [[generate-check-validate-engine]] in embryonic form. **What OSSICRO takes:** the published question-set→checklist methodology, reimplemented independently and extended from *which approvals do you need* to *which essential records must exist, in what state, validated against which CFR/ICH subsection* ([[document-catalog]], [[completeness-ledger]]). **What OSSICRO does not take:** the tool itself, which is not publicly deployed outside Vanderbilt; the methodology paper is the citable artifact.

## SMART IRB — the master reliance agreement

**SMART IRB** ([smartirb.org](https://smartirb.org/)) is the NCATS-funded national platform that solved the contract problem behind single-IRB review. Its instrument is a **master Authorization Agreement**: an institution signs a **joinder** once, and thereafter any two participating institutions can establish an IRB-of-record reliance for a given study without negotiating a bespoke bilateral agreement. The platform includes SOPs, determination-letter templates, and a harmonized framework for the responsibilities that remain local (investigator training, COI review, local-context requirements, HIPAA determinations) versus those that follow the reviewing IRB. SMART IRB is the operational backbone for compliance with the revised Common Rule's [§46.114](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.114) cooperative-research mandate and the NIH sIRB policy.

**What SMART IRB proves:** a standing legal instrument plus a defined role split can collapse an N×N negotiation problem into a sign-once joinder — the same structural move OSSICRO's [[transfer-of-regulatory-obligations-toro|TORO]] tooling and [[micro-cro-operating-model|micro-CRO]] service agreements make for sponsor-obligation transfer. **What OSSICRO takes:** the agreement architecture (master instrument + per-study implementation) as the model for reliance coordination in [[single-irb-mandate-and-central-irbs]]; where an OSSICRO study is multi-site, the system generates the SMART IRB reliance-request package rather than inventing a parallel mechanism.

## IREx — programmatic single-IRB coordination

The **IRB Reliance Exchange (IREx)** ([irbexchange.org](https://www.irbexchange.org/)), operated by Vanderbilt in support of the NCATS Trial Innovation Network, is the web platform that *operationalizes* single-IRB review on top of the SMART IRB agreement: it captures each site's reliance decision, tracks local-context and HIPAA documentation, records the reviewing IRB's approvals, and surfaces study-wide sIRB status to all participating sites. The Trial Innovation Network pairs it with central IRBs and a Standard Agreement System built on the Federal Demonstration Partnership Clinical Trials Subaward Agreement (FDP-CTSA) as a harmonized multi-site contract template ([NCATS TIN](https://ncats.nih.gov/ctsa/projects/network)).

**What IREx proves:** inter-institutional regulatory coordination — documented determinations, local requirements, approval states, per-site status — can run as a shared workflow system with per-role views, and IRBs and institutions will actually use it at national scale. This is the direct precedent for OSSICRO's coordination layer: the [[inter-entity-document-flow-map]], the per-persona portal views ([[four-entry-points]]), and the [[communication-hub]]. **What OSSICRO takes:** the workflow-state-machine pattern for multi-party regulatory status; IREx itself remains the venue for CTSA-network sIRB coordination, and OSSICRO interoperates with (not replaces) it where a study runs through the TIN.

## The human consult-service precedents

The shared *human* layer also has published precedent, which matters because it is the design ancestor of the [[micro-cro-accountable-layer|micro-CRO]]:

- **Harvard Catalyst IND/IDE Consult Service** — a decentralized consult network across Massachusetts academic centers supporting sponsor-investigators; the founding paper states the problem OSSICRO answers: investigator-sponsors "often do not fully appreciate their regulatory obligations nor have resources to ensure compliance" (Kim MJ, Winkler SJ, Bierer BE, Wolf D. *Clin Transl Sci.* 2014;7(2):150-5. PMID [24455986](https://pubmed.ncbi.nlm.nih.gov/24455986/); DOI [10.1111/cts.12146](https://doi.org/10.1111/cts.12146)). Harvard Catalyst subsequently published the contributory-network model for sharing S-I IND/IDE resources across institutions.
- **MICHR (Michigan)** — tiered service delivery: free automated/triage support escalating to paid human consultation, the direct precedent for OSSICRO's service tiers ([[micro-cro-operating-model]]).
- **UCSF CTSI Design Studio and the Emory/Georgia CTSA "Navigator Team"** — structured human consultation gates before trial launch and a single accountable shepherd from concept to approval: both are organizational precedents for OSSICRO's pre-flight review step, where non-delegable decision points are surfaced to a human before the software proceeds.

**What these prove:** the demand is real, the shared-services model works, and the correct division of labor places judgment with credentialed humans and coordination with the shared layer. OSSICRO's thesis is that the coordination half of that division is now automatable to a much greater depth — while the judgment half is not automatable at all ([[non-delegable-functions-and-gates]]).

> [!interpretive] OSSICRO position
> The interpretive claim of this page is the synthesis, not the facts: V-CAP validates rules-driven personalized compliance checking; SMART IRB validates the master-instrument legal architecture; IREx validates programmatic multi-party regulatory workflow; Harvard Catalyst/MICHR validate the thin accountable human layer. No single precedent combines all four with a generate/check/validate document engine and code-enforced gates — that combination is OSSICRO's contribution, and it is presented as a design position, not an established regulatory category. Each precedent's methodology is reimplemented from published sources; no institution-gated tool or proprietary template is copied ([[external-templates-and-licenses]]).

> [!warning] Non-delegable
> None of the precedents automated the judgment they coordinated: V-CAP tells an investigator which approvals to seek — it grants none; IREx records IRB determinations — it makes none. OSSICRO preserves exactly this line. The IRB reliance *decision* and the reviewing IRB's *approval* remain board judgments (21 CFR 56.109-56.111; 45 CFR 46.109-46.114); OSSICRO assembles, routes, and records.

## Related

- [[generate-check-validate-engine]]
- [[single-irb-mandate-and-central-irbs]]
- [[irb-review-workflow]]
- [[micro-cro-accountable-layer]]
- [[micro-cro-operating-model]]
- [[transfer-of-regulatory-obligations-toro]]
- [[communication-hub]]
- [[inter-entity-document-flow-map]]
- [[completeness-ledger]]
- [[document-catalog]]
- [[failed-disintermediation-case-studies]]
- [[external-templates-and-licenses]]
- [[institutional-resources]]

## Sources

- [V-CAP methodology paper (VICTR), PMC3767144](https://pmc.ncbi.nlm.nih.gov/articles/PMC3767144/)
- [Vanderbilt Program for Investigator-Initiated Trials (VICTR/VCC)](https://vcc.vumc.org/who-we-are/teams/program-for-investigator-initiated-trials/)
- [SMART IRB — national IRB reliance platform](https://smartirb.org/)
- [IRB Reliance Exchange (IREx)](https://www.irbexchange.org/)
- [NCATS CTSA Trial Innovation Network](https://ncats.nih.gov/ctsa/projects/network)
- [45 CFR 46.114 — Cooperative research (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.114)
- [NIH Single IRB Policy for Multi-Site Research (NOT-OD-16-094)](https://grants.nih.gov/grants/guide/notice-files/NOT-OD-16-094.html)
- [Kim MJ, Winkler SJ, Bierer BE, Wolf D. Harvard Catalyst IND/IDE Consult Service. Clin Transl Sci. 2014;7(2):150-5. PMID 24455986](https://doi.org/10.1111/cts.12146)
- [Harvard Catalyst — Sharing Sponsor-Investigator IND/IDE Resources: A Contributory Network Model](https://catalyst.harvard.edu/publications-documents/sharing-sponsor-investigator-ind-ide-resources-a-contributory-network-model-of-scalable-adaptable-support-services-across-massachusetts-academic-institutions/)
