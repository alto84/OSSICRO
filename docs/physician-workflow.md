# OSSICRO — the physician's workflow (Route-3926, single-patient expanded access)

*One page, for teaching and presentation.* Blue = **OSSICRO drafts, computes, and assembles.**
Amber = a **hard gate** where a named human must commit. Red = a **non-delegable human
act OSSICRO refuses to perform, in code.** The software drafts everything and decides nothing.

```mermaid
---
title: "OSSICRO — Route-3926 Physician Workflow"
---
flowchart TD
    Start(["A neurologist has one patient — a serious illness,<br/>no comparable therapy, and no open trial"]):::start

    A1["<b>1 · Start a case</b><br/>Draft workspace · coded IDs only · no PHI"]:::sw
    A2["<b>2 · Physician intake</b><br/>Import the structured chart / enter data<br/>field-by-field confirmation"]:::sw

    G1{"<b>INV-3 commit gate</b><br/>A named human commits the input of record<br/>— nothing is drafted before this"}:::commit

    A3["<b>3 · Generate</b><br/>OSSICRO drafts the 8 expanded-access documents<br/>every field stamped back to its source"]:::sw
    A4["<b>Completeness ledger</b><br/>green / amber / red · each item mapped to its CFR<br/>+ computed statutory deadlines"]:::sw
    A5["<b>4 · Package review</b><br/>Assemble package · filled Form FDA 3926 as a PDF<br/>FDA-reviewer and manufacturer views"]:::sw
    A6["<b>5 · Find candidates</b><br/>Manufacturer registry search<br/>physician reviews the basis"]:::sw

    Auth["<b>Authorization</b><br/>four independent owners must each concur —<br/>OSSICRO drafts and assembles, but decides nothing"]:::hub

    Start --> A1 --> A2 --> G1
    G1 -->|"committed"| A3 --> A4 --> A5 --> A6 --> Auth
    G1 -.->|"any edit after commit → commit invalidated"| A2

    %% The four owners — each a human decision OSSICRO never makes
    Auth --> P["<b>Treating physician</b><br/>Risk determination · obtains consent · signs 1572 · submits<br/>21 CFR 312.310(a) · Part 50 · 312.53"]:::gate
    Auth --> M["<b>Manufacturer</b><br/>Whether to supply · LOA signature<br/>FDCA §561A"]:::gate
    Auth --> F["<b>FDA review division</b><br/>Allow-to-proceed or clinical hold<br/>21 CFR 312.305 / .310 / .42"]:::gate
    Auth --> I["<b>IRB</b><br/>Approval or §56.105 chair concurrence<br/>21 CFR Part 56"]:::gate

    %% Ongoing gate during treatment
    P -.->|"if a serious adverse event occurs"| SAE["<b>SAE causality</b> — physician / medical-monitor judgment<br/>OSSICRO computes the deadline and drafts the shell,<br/>never sets causality · 21 CFR 312.32"]:::gate

    %% Micro-CRO branch
    A6 -.-> CRO{"<b>Micro-CRO</b><br/>transfer an obligation?"}:::commit
    CRO -->|"transferable, e.g. monitoring or records"| CROok["Draft the TORO<br/>21 CFR 312.52"]:::sw
    CRO -->|"non-delegable: consent, IRB, causality, signatures"| CROno["<b>REFUSED in code</b><br/>the obligation cannot be transferred<br/>21 CFR Part 50 / Part 56"]:::gate

    classDef start fill:#eef2ff,stroke:#4338ca,color:#1e1b4b;
    classDef sw fill:#e8f4ff,stroke:#2563eb,color:#0b2545;
    classDef commit fill:#fff4e0,stroke:#c77700,color:#5c3b00;
    classDef gate fill:#ffe9e9,stroke:#c81e1e,color:#5c0000;
    classDef hub fill:#f0fdf4,stroke:#15803d,color:#052e16;
```

**The teaching point.** The physician moves left-to-right through a workspace that turns a
patient's chart into a complete, cited FDA package in minutes instead of months. But at every
point where the law requires *human* judgment — committing the data of record, obtaining
consent, IRB approval, causality, signing, submitting — OSSICRO **stops and hands the pen to a
named person.** The four authorization owners are independent by design; no single party, and
never the software, can grant the whole thing. That boundary is not a policy document — it is
enforced in the engine, which is why the micro-CRO layer will *refuse* to draft a transfer of a
non-delegable obligation.
