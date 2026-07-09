# QA Review — REGULATORY reviewer — regulatory-affairs / GCP expert

**Model:** Fable 5 | claude-fable-5  
**Verdict:** Strong regulatory register and mostly accurate CFR paraphrase, but a fabricated 312.40 subsection, a phantom E6(R3) numbering scheme in the essential-records catalog, and a dropped 15-day follow-up deadline are exactly the errors an FDA reviewer or GCP auditor would catch — fix before showing this to anyone in the field.

## Strengths
- CFR paraphrase accuracy in sponsor.md and investigator.md is unusually high for generated content: the 312.56(d) 5-working-day discontinuation clock, the 312.57(c)/312.62(c) two-year retention rules, the 312.64(d) one-year post-study financial-disclosure update window, and the 312.53(c)(1)-(c)(4) investigator-package breakdown (protocol outline Phase 1 vs detailed Phase 2/3) are all correct.
- The 7/15-day safety architecture is correctly structured, including nuances most drafts get wrong: the 7-day report goes to FDA only with the complete report following in the 15-day frame; clock start is 'sponsor determines it qualifies' for (c)(1) vs 'initial receipt' for (c)(2); and the 2012 guidance's single-occurrence vs aggregate-analysis distinction for 'reasonable possibility' is faithfully rendered.
- document-catalog.md gets the Form 3454/3455 routing right ('→ FDA with marketing app', not with the IND) — a common error — and its Confirmed/Conditional/Interpretive tagging plus the risk-proportionate 'applicable subset is a documented decision' framing correctly reflects E6(R3) Appendix C's philosophy.
- cfr-citation-map.md is genuinely accurate across an unusually wide span: 54.4(a)(1) vs (a)(3) for 3454/3455, 42 U.S.C. 282(j) and 21 U.S.C. 331(jj) for ClinicalTrials.gov enforcement, 360bbb-0 as FDCA 561A, 56.109(e) for the IRB written decision, and the 164.512(i)(1)(ii) preparatory-to-research boundary; the maintenance rules (change-watch, dated snapshots) are the right anti-rot design.
- The 30-day-clock page correctly states clock start from FDA receipt (not send date), silence-as-authorization on day 31, the 312.42(c) 30-day written-explanation and (e) 30-day complete-response cycles, and the independence of the FDA clock from IRB approval (56.103).
- Anchor dates check out: E6(R3) Step 4 2025-01-06, the IND safety final rule at 75 FR 59935 (Sept. 29, 2010), the December 2012 IND safety guidance, the 2015 sponsor-investigator draft guidance, and the October 2009 Investigator Responsibilities guidance are all real and correctly dated.
- The non-delegable gating discipline (consent administration, IRB judgment, causality/expectedness, 1571/1572 attestations, 312.52 transferee-must-be-entity) is consistently and correctly threaded through every assigned file, including the engine registry's gate fields.

## Findings
### [HIGH] wiki/02-lifecycle/ind-submission-and-30-day-clock.md
**Issue:** Fabricated CFR subsections on a page marked status: confirmed. The bullet list attributes 'FDA may impose a clinical hold during the 30 days' to 312.40(c) and 'sponsor may not begin if a hold is in force' to 312.40(d). In the actual regulation, 312.40(c) governs SHIPMENT of investigational drug to investigators (30 days after receipt or on earlier authorization), and 312.40(d) does not exist. The hold mechanics live in 312.40(b)(1) ('unless FDA notifies the sponsor that the investigations... are subject to a clinical hold') and 312.42. The 312.40(a) bullet also inserts 'a signed agreement' — 312.40(a)(2) requires IRB review/approval compliance; the signed 1572 requirement is 312.53(c), not 312.40(a).

**Recommendation:** {f.get('recommendation','')}

### [HIGH] wiki/03-documents/document-catalog.md
**Issue:** The 'E6 ref' column uses a phantom E6(R3) numbering scheme that does not exist in the Step 4 guideline. E6(R3) is structured as Principles + Annex 1 (§1 IRB/IEC, §2 Investigator, §3 Sponsor, §4 Data Governance) + Appendices A (IB), B (Protocol), C (Essential Records). The catalog cites 'R3 §7' for the protocol (should be Appendix B), 'R3 §8' for the IB (should be Appendix A), 'R3 §4' for consent (consent duties are Annex 1 §2; §4 is data governance), 'R3 §5' for DSMB/CTA (no §5 exists in Annex 1), '§6.9' for monitoring (monitoring is Annex 1 §3.11), and '§6 (ALCOA++)' for data integrity (data governance is Annex 1 §4). Worse, engine/registry/documents.json uses the CORRECT scheme (ICH E6(R3) Appendix A for the IB, Appendix B for the protocol, Annex-1-style 2.x/3.x) — so the wiki 'source of truth' and the validation engine contradict each other on the project's flagship standard.

**Recommendation:** {f.get('recommendation','')}

### [HIGH] wiki/02-lifecycle/safety-reporting-lifecycle.md
**Issue:** The follow-up reporting deadline is wrong. Stage 3 says follow-up information 'must be submitted as soon as the information is available' and the clocks table row reads 'As soon as available (312.32(d))'. 21 CFR 312.32(d)(2) actually requires relevant follow-up to an IND safety report 'as soon as possible, but in no case later than 15 calendar days after the sponsor receives the information.' The hard 15-day backstop is the enforceable part of the clock, and this page is the one the safety-clock-engine is built from. sponsor.md states the 15-day follow-up deadline correctly, so the wiki is also internally inconsistent on a safety timeline.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] engine/registry/documents.json
**Issue:** site-initiation-visit-report cites '21 CFR 312.53(b)' as governing authority. 312.53(b) is 'Control of drug' — the sponsor ships only to participating investigators. It has nothing to do with site initiation visits; the regulatory hooks for SIVs are 312.53(d) (selecting monitors), 312.56(a) (monitoring), and E6(R3) Annex 1 §3.11.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] engine/registry/documents.json
**Issue:** The registry (58 entries) is missing several rows the document-catalog marks Confirmed, so the engine's completeness check cannot flag their absence: A10 IRB roster/assurance (56.107), A11 FDA IND acknowledgment / safe-to-proceed correspondence, A27 IRB-approved recruitment/advertising materials, B7 IB updates/revisions (312.55(b)), B14 correspondence log, C7 audit certificate (conditional), and C10 final screening/enrollment logs + safety reconciliation. For a system whose selling point is 'COMPLETE documentation,' the check pass is only as complete as this registry.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] wiki/03-documents/document-catalog.md
**Issue:** The catalog claims to be the master E6(R3) Appendix C superset but omits the record classes R3 actually added: computerized-systems records (system validation documentation, access/user-account records, audit-trail review records), service-provider oversight records (R3's expanded sponsor duty over technology vendors — directly relevant since OSSICRO itself is such a system), and serious-breach/noncompliance documentation. A sponsor QA reviewer comparing this against Appendix C will notice the gap immediately.

**Recommendation:** {f.get('recommendation','')}

### [LOW] wiki/03-documents/document-catalog.md
**Issue:** Row B6 lists the IRB as a receiver of 312.32 IND safety reports. 312.32(c) requires notification of FDA and all participating investigators; IRB receipt runs through the separate 312.66/56.108(b)(1) unanticipated-problem route (a distinction safety-reporting-lifecycle.md itself draws correctly — 'Not every IND safety report is an unanticipated problem').

**Recommendation:** {f.get('recommendation','')}

### [LOW] wiki/02-lifecycle/ind-submission-and-30-day-clock.md
**Issue:** The clinical-hold grounds bullet 'for certain expanded-access/treatment protocols, additional 312.42(b)(2)–(b)(4) grounds' mischaracterizes the subsections: (b)(2) is the Phase 2/3 design-deficiency ground (already listed separately above it), (b)(3) is expanded-access holds, and (b)(4) covers studies not designed to be adequate and well-controlled.

**Recommendation:** {f.get('recommendation','')}

### [LOW] wiki/01-roles-responsibilities/investigator.md
**Issue:** The authority callout asserts '§§312.63, 312.65, and 312.67 are reserved.' The eCFR does not designate these as [Reserved] sections — they are simply unassigned numbers in Subpart D. Asserting a 'reserved' designation the CFR doesn't make is a small fabrication on an authority-bearing line.

**Recommendation:** {f.get('recommendation','')}

### [LOW] wiki/02-lifecycle/safety-reporting-lifecycle.md
**Issue:** SUSAR is attributed to 'ICH E2A terminology.' E2A defines the concept (serious, unexpected, suspected adverse reaction) but the acronym itself is EU Clinical Trials Directive/Regulation usage; FDA regulations never use it. Minor, but this wiki's register invites exactness.

**Recommendation:** {f.get('recommendation','')}

### [LOW] wiki/03-documents/document-catalog.md
**Issue:** Currency drift in Sources: the FDA E6(R3) link is still labeled '(draft)' while the wiki elsewhere asserts FDA final adoption September 2025; and the RBM authority cited for A13 is the 2013 guidance without the April 2023 final Q&A ('A Risk-Based Approach to Monitoring of Clinical Investigations: Questions and Answers') that supplements it.

**Recommendation:** {f.get('recommendation','')}

### [LOW] engine/registry/documents.json
**Issue:** The TORO entry has owner 'cro' and receiver 'fda'. The 312.52(a) written transfer is executed by the sponsor (with the CRO as transferee), and for INDs it is not a routine FDA submission — it is a sponsor record describing what was transferred (contrast 314.50(a)(5) for marketing applications).

**Recommendation:** {f.get('recommendation','')}

## Must-fix
- Correct the 312.40 subsection attributions in ind-submission-and-30-day-clock.md — 312.40(c) is drug shipment, 312.40(d) does not exist, and the hold exception belongs to 312.40(b)(1)/312.42 — the page is marked 'confirmed' and currently cites law that isn't there.
- Replace the phantom E6(R3) numbering in document-catalog.md's E6-ref column (§4/§5/§6/§6.9/§7/§8) with the actual Step 4 structure (Annex 1 §§1–4 + Appendices A/B/C) and reconcile it with engine/registry/documents.json so wiki and engine cite one consistent scheme.
- Fix the 312.32(d) follow-up deadline in safety-reporting-lifecycle.md (Stage 3 text and clocks table) to the regulation's hard 15-calendar-day limit, and verify the safety-clock-engine rules did not inherit the 'as soon as available' formulation.
