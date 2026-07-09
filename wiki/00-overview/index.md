---
title: "Overview — Orientation, Legal Frame, and Reading Order"
section: "00-overview"
status: mixed
governing_authority:
  - "21 CFR Part 312 (Investigational New Drug Application)"
  - "21 CFR 312.3(b); 312.52"
  - "ICH E6(R3) Good Clinical Practice"
tags: [ossicro/engine, lifecycle/ind, status/mixed]
aliases: ["Overview", "Start Here"]
updated: 2026-07-09
---

# Overview — Orientation, Legal Frame, and Reading Order

> [!authority] Governing authority
> This section orients the reader to the binding legal frame that governs everything downstream: 21 CFR Part 312 (the IND regulations), the sponsor-investigator construct at [21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3), the transfer-of-obligations rule at [21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52), and ICH E6(R3) Good Clinical Practice (FDA-adopted 2025-09-09). Status: **Mixed** — black-letter regulatory scaffolding plus the OSSICRO architectural thesis, each labelled where it appears.

This is the entry point to the OSSICRO wiki. OSSICRO exists to remove the paperwork barrier that keeps qualified physicians — especially in under-resourced settings — out of clinical research, so that a clinician with a patient and a candidate early-phase therapy can lawfully reach enrollment. The wiki is reference-grade regulatory documentation: every requirement is cited to its governing authority, and every OSSICRO design position is labelled **interpretive** and defended, never smuggled in as law.

## The one idea to carry into every page

Sponsor obligations transfer, in writing, only to a **legally accountable entity** — a CRO that thereby becomes "subject to the same regulatory action as a sponsor" under [21 CFR 312.52(b)](https://www.law.cornell.edu/cfr/text/21/312.52). Software cannot be subject to FDA enforcement, so **software can never be the transferee**. This single fact forecloses "let the software be the CRO," and it forces OSSICRO's viable architecture onto the **sponsor-investigator IND** ([21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3)): one physician lawfully holds both the sponsor and investigator obligation sets, and AI absorbs the coordination labor without disintermediating the accountable human. See [[legal-thesis-3123-vs-31252]] for the load-bearing argument and [[what-is-ossicro]] for the mission and scope.

## The HARD LINE

OSSICRO drafts, checks, routes, times, and version-controls **complete, compliant documentation for qualified human review**. It never *owns* a non-delegable act: informed consent ([21 CFR 50](https://www.law.cornell.edu/cfr/text/21/part-50)), IRB approval ([21 CFR 56](https://www.law.cornell.edu/cfr/text/21/part-56)), SAE causality/expectedness determination ([21 CFR 312.32](https://www.law.cornell.edu/cfr/text/21/312.32)), statistical sign-off, or the 1571/1572 legal attestations. Every generated artifact carries a citation to governing authority and a gate that routes accountable judgment to a named human. The master gating matrix lives at [[non-delegable-functions-and-gates]].

> [!warning] Non-delegable
> The functions above are not "hard to automate"; they are **legally reserved** to a qualified human or accountable entity. Where this wiki describes OSSICRO generating a document, read "generating a DRAFT for human review." No page in this corpus authorizes automating a reserved act.

## Reading order

**For a first-time clinician** (you have a patient and a candidate therapy):

1. [[what-is-ossicro]] — what the system is and what it refuses to do.
2. [[guiding-scenario]] — the end-to-end narrative from "I have a patient" to enrollment.
3. [[the-three-pathways-triage]] — the decision tree that routes you to (A) site, (B) sponsor-investigator, or (C) expanded access.
4. [[four-entry-points]] — where you sit among Patient, HCP, Micro-CRO, and Pharma, and how the journeys interlock.
5. Then the role page that fits you: [[sponsor-investigator]], [[investigator]], or [[06-personas/hcp-physician|the enrolling HCP persona]].

**For a regulatory reviewer** (you are checking whether the architecture is lawful):

1. [[legal-thesis-3123-vs-31252]] — why 312.3(b) is lawful and 312.52 forecloses software disintermediation.
2. [[failed-disintermediation-case-studies]] — Science 37 and TrialSpark→Formation Bio as market corroboration.
3. [[regulatory-landscape]] — binding law vs. non-binding guidance, and which authorities are in active motion.
4. [[confirmed-vs-interpretive]] — the calibration standard for the entire wiki.
5. [[entity-map]] — who signs, who judges, who is enforceable.

## What lives in this section

| Page | Purpose |
|---|---|
| [[what-is-ossicro]] | Mission, scope, the open-source + thin-micro-CRO thesis, the HARD LINE. |
| [[guiding-scenario]] | "A clinician has a patient and a candidate early-phase treatment" — end-to-end walkthrough. |
| [[the-three-pathways-triage]] | Decision tree: site (A) / sponsor-investigator (B) / expanded access (C). |
| [[four-entry-points]] | Patient / HCP / Micro-CRO / Pharma entry points and how they interlock. |
| [[legal-thesis-3123-vs-31252]] | The load-bearing argument: 312.3(b) lawful, 312.52 forecloses software-as-CRO. |
| [[failed-disintermediation-case-studies]] | Value follows accountability, not coordination software. |
| [[glossary]] | Controlled-vocabulary definitions, each tagged to its citation. |
| [[regulatory-landscape]] | Map of binding law vs. guidance; authorities in motion. |
| [[entity-map]] | The coordinating entities and their legal relationships. |
| [[confirmed-vs-interpretive]] | The calibration standard for the whole corpus. |

> [!interpretive] OSSICRO position
> The "thin micro-CRO" — a real, named, legally-accountable entity that holds only the functions [312.52(b)](https://www.law.cornell.edu/cfr/text/21/312.52) requires an entity for, when the sponsor-investigator cannot personally hold them — is an OSSICRO design position, not a regulatory category. It is lawful precisely because it is an entity, not software. See [[micro-cro-accountable-layer]].

## Related

- [[what-is-ossicro]]
- [[guiding-scenario]]
- [[the-three-pathways-triage]]
- [[four-entry-points]]
- [[legal-thesis-3123-vs-31252]]
- [[confirmed-vs-interpretive]]
- [[non-delegable-functions-and-gates]]
- [[INDEX]]

## Sources

- [21 CFR 312.3 — Definitions (sponsor / investigator / sponsor-investigator)](https://www.law.cornell.edu/cfr/text/21/312.3)
- [21 CFR 312.52 — Transfer of obligations to a CRO](https://www.law.cornell.edu/cfr/text/21/312.52)
- [21 CFR Part 312 Subpart D — Sponsor & investigator obligations](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)
- [FDA — E6(R3) Good Clinical Practice (Sept 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
- [Federal Register — E6(R3) GCP; FDA adoption (Sept 9 2025)](https://www.federalregister.gov/documents/2025/09/09/2025-17311/e6r3-good-clinical-practice-international-council-for-harmonisation-guidance-for-industry)
