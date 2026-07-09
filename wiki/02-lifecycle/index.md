---
title: "Lifecycle — Master Phase List"
section: "02-lifecycle"
status: confirmed
governing_authority:
  - "21 CFR Part 312 (Investigational New Drug Application)"
  - "ICH E6(R3) Good Clinical Practice (FDA-adopted 2025-09-09)"
  - "21 CFR Parts 50, 54, 56"
tags: [lifecycle/feasibility, lifecycle/ind, lifecycle/irb, lifecycle/activation, lifecycle/conduct, lifecycle/safety, lifecycle/annual, lifecycle/closeout, lifecycle/retention, cfr/312, gcp/e6r3, status/confirmed]
aliases: ["Trial Lifecycle", "Phase Model", "Lifecycle Index"]
updated: 2026-07-09
---

# Lifecycle — Master Phase List

> [!authority] Governing authority
> 21 CFR Part 312 (IND), Parts 50/54/56 (consent, financial disclosure, IRB); ICH E6(R3) Good Clinical Practice, Appendix C (essential records), FDA-adopted 2025-09-09 (90 FR / [Federal Register 2025-17311](https://www.federalregister.gov/documents/2025/09/09/2025-17311)). Status: **Confirmed**.

This section is the canonical phase model for a US sponsor-investigator early-phase (e.g., Phase 1/2) IND trial, and for the physician-as-site (Mode A) and expanded-access branches that diverge from it. It is CTSA-convergent: the same ordered spine appears in the study-startup toolkits of Harvard Catalyst, Penn ITMAT/CHPS, Michigan MICHR, and NCATS' Trial Innovation Network, and it maps cleanly onto the three-part Startup / Conduct / Closeout framing of ICH E6(R3). Every phase below is a folder of workflow pages; each page carries its own governing-authority header and confirmed/interpretive badge.

The lifecycle is ordered by regulatory dependency, not convenience. Enrollment cannot begin before both an FDA safe-to-proceed determination (the 30-day clock under [21 CFR 312.40](https://www.ecfr.gov/current/title-21/section-312.40)) and documented IRB approval ([21 CFR 56.103](https://www.ecfr.gov/current/title-21/section-56.103)) exist; those two gates are independent and both are hard. OSSICRO drafts, assembles, checks, times, and version-controls every artifact across these phases — and stops at each non-delegable gate, where a qualified human reviews, judges, and signs.

## The canonical phases

| # | Phase | Lifecycle tag | Core authority | Page |
|---|-------|---------------|----------------|------|
| 0 | Phase-model overview (Startup / Conduct / Closeout) | — | ICH E6(R3) App. C; 21 CFR 312 | [[phase-model-overview]] |
| 1 | Feasibility & patient matching | `feasibility` | CT.gov v2 API; HIPAA [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512) | [[feasibility-and-patient-matching]] |
| 2 | Pre-IND & IND preparation | `ind` | 21 CFR 312.20–312.23; 312.47 | [[pre-ind-and-ind-preparation]] |
| 3 | IND submission & 30-day clock | `ind` | 21 CFR 312.40, 312.42 | [[ind-submission-and-30-day-clock]] |
| 4 | IRB submission & approval | `irb` | 21 CFR Part 56; 56.111; 45 CFR 46 | [[irb-submission-and-approval]] |
| 5 | Site activation | `activation` | 21 CFR 312.53; ICH E6(R3) §2 | [[site-activation]] |
| 6 | Enrollment & consent | `conduct` | 21 CFR Part 50; 50.20–50.27 | [[enrollment-and-consent]] |
| 7 | Conduct & monitoring | `conduct` | 21 CFR 312.56–312.62; ICH E6(R3) §5, §6 | [[conduct-and-monitoring]] |
| 8 | Safety reporting lifecycle | `safety` | 21 CFR 312.32; ICH E2A | [[safety-reporting-lifecycle]] |
| 9 | Annual reporting & amendments | `annual` | 21 CFR 312.30, 312.31, 312.33; ICH E2F | [[annual-reporting-and-amendments]] |
| 10 | Closeout | `closeout` | 21 CFR 312.38, 312.45; ICH E3 | [[closeout]] |
| 11 | Record retention & archival | `retention` | 21 CFR 312.57(c), 312.62(c); ICH E6(R3) §C.2 | [[record-retention-and-archival]] |
| — | Expanded-access workflow (parallel branch) | `expanded-access` | 21 CFR Part 312 Subpart I; Form FDA 3926 | [[expanded-access-workflow]] |
| — | Single-patient (n-of-1) site enrollment | `expanded-access` | 21 CFR 312.310; 312.315; 312.320 | [[single-patient-site-enrollment]] |
| — | IIS request workflow (Mode B funding) | `iis` | Sunshine Act (42 CFR Part 403); FMV | [[iis-request-workflow]] |

## Three ordering facts a first-time clinician must hold

1. **The IND clock and the IRB clock run in parallel, not in series.** You may submit the IND and the IRB package concurrently. You may not *enroll* until the later of the two clears. The 30-day FDA clock ([[ind-submission-and-30-day-clock]]) and the IRB approval ([[irb-submission-and-approval]]) are separate authorizations from separate bodies.
2. **In the sponsor-investigator model the phases do not disappear — they collapse onto one person.** Documents that normally flow *between* a sponsor and an investigator (the 1572 from investigator to sponsor; IND safety reports from sponsor to investigators) become self-directed obligations plus the outward flow to FDA and IRB. The obligation set is not reduced; it is concentrated ([[sponsor-investigator]], 21 CFR 312.3(b)).
3. **Which lifecycle you are in depends on the triage decision at Phase 1.** Mode A (site on a pharma protocol), Mode B (sponsor-investigator IND), and expanded access are three different document sets with three different accountable parties and three different legal-exposure profiles ([[the-three-pathways-triage]]).

## Related
- [[phase-model-overview]]
- [[sponsor-investigator]]
- [[the-three-pathways-triage]]
- [[document-catalog]]
- [[inter-entity-document-flow-map]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR Part 312 — Investigational New Drug Application (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312)
- [ICH E6(R3) Good Clinical Practice (ICH)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA adoption notice, E6(R3), 90 FR (Federal Register 2025-17311)](https://www.federalregister.gov/documents/2025/09/09/2025-17311)
- [21 CFR Part 56 — Institutional Review Boards (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56)
