# OSSICRO — the physician's workflow (Route-3926, single-patient expanded access)

*One page, for teaching and presentation.* Blue = **OSSICRO drafts, computes, and assembles.**
Amber = a **hard gate** where a named human must commit. Red = a **non-delegable human
act OSSICRO refuses to perform, in code.** The software drafts everything and decides nothing.

```mermaid
---
title: "OSSICRO — Route-3926 Physician Workflow"
---
flowchart TD
    Start(["One patient · a serious illness<br/>no comparable therapy · no open trial"]):::start

    A1["<b>1 · Start a case</b><br/>draft workspace<br/>coded IDs · no PHI"]:::sw
    A2["<b>2 · Physician intake</b><br/>import chart / enter data<br/>confirm field-by-field"]:::sw

    G1{"<b>INV-3 commit gate</b><br/>a named human commits<br/>the input of record<br/>— nothing is drafted first"}:::commit

    A3["<b>3 · Generate</b><br/>the 8 FDA documents<br/>every field stamped to source"]:::sw
    A4["<b>Completeness ledger</b><br/>green / amber / red<br/>CFR-mapped · deadlines"]:::sw
    A5["<b>4 · Package review</b><br/>Form FDA 3926 (PDF)<br/>FDA + manufacturer views"]:::sw
    A6["<b>5 · Find candidates</b><br/>manufacturer<br/>registry search"]:::sw

    Auth["<b>Authorization</b><br/>four independent owners<br/>must each concur"]:::hub

    Start --> A1 --> A2 --> G1
    G1 -->|"committed"| A3 --> A4 --> A5 --> A6 --> Auth
    G1 -.->|"edit after commit → invalidated"| A2

    Auth --> P["<b>Treating physician</b><br/>obtains consent · signs 1572<br/>312.310(a) · Part 50"]:::gate
    Auth --> M["<b>Manufacturer</b><br/>agrees to supply · LOA<br/>FDCA §561A"]:::gate
    Auth --> F["<b>FDA review division</b><br/>proceed or clinical hold<br/>312.305 / .310"]:::gate
    Auth --> I["<b>IRB</b><br/>approval / §56.105<br/>Part 56"]:::gate

    P -.->|"if an SAE occurs"| SAE["<b>SAE causality</b><br/>physician judgment<br/>OSSICRO drafts the shell · 312.32"]:::gate

    A6 -.-> CRO{"<b>Micro-CRO</b><br/>transfer an<br/>obligation?"}:::commit
    CRO -->|"transferable"| CROok["<b>Draft the TORO</b><br/>312.52"]:::sw
    CRO -->|"non-delegable"| CROno["<b>REFUSED in code</b><br/>Part 50 / Part 56"]:::gate

    classDef start fill:#eef2ff,stroke:#4338ca,color:#1e1b4b;
    classDef sw fill:#e8f4ff,stroke:#2563eb,color:#0b2545;
    classDef commit fill:#fff4e0,stroke:#c77700,color:#5c3b00;
    classDef gate fill:#ffe9e9,stroke:#c81e1e,color:#5c0000;
    classDef hub fill:#f0fdf4,stroke:#15803d,color:#052e16;
```

**The teaching point.** The physician moves top-to-bottom through a workspace that turns a
patient's chart into a complete, cited FDA package in minutes instead of months. But at every
point where the law requires *human* judgment — committing the data of record, obtaining
consent, IRB approval, causality, signing, submitting — OSSICRO **stops and hands the pen to a
named person.** The four authorization owners are independent by design; no single party, and
never the software, can grant the whole thing. That boundary is not a policy document — it is
enforced in the engine, which is why the micro-CRO layer will *refuse* to draft a transfer of a
non-delegable obligation.

> A polished, self-contained HTML version of this diagram (theme-aware, for slides) can be
> regenerated from this source; see the submission materials.
