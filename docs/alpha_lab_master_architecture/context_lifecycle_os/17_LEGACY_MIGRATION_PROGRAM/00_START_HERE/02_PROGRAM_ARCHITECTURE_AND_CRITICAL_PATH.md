---
title: "Program Architecture and Critical Path"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Program Architecture and Critical Path

```mermaid
flowchart TD
    F[LCM-00 Baseline freeze] --> S[LCM-01 Forensic survey]
    S --> C[LCM-02 Classification and ownership]
    C --> I[LCM-03 Identity and alias registry]
    I --> B[LCM-04 Behavioral characterization]
    B --> T[LCM-05 Target topology and locator]
    T --> M[LCM-06 Migration framework]
    M --> E[LCM-07 Shared engine extraction]
    E --> X[LCM-08 Context migration]
    X --> U[LCM-09 Setup migration]
    U --> R[LCM-10 Treatment and execution separation]
    R --> V[LCM-11 Visualization standardization]
    V --> D[LCM-12 Documentation reconciliation]
    D --> W[LCM-13 Wave cutover and dual run]
    W --> Q[LCM-14 Deprecation and quarantine]
    Q --> Z[LCM-15 Controlled deletion and root hygiene]
    Z --> K[LCM-16 Full cutover and closure]
```

## Critical path

The critical path is not code movement. It is:

`owner resolution → behavioral capture → canonical specification → parity proof → cutover approval`.

Folder changes can proceed only after a file or domain family has crossed the required state boundary. The first irreversible action is deletion, therefore deletion is deliberately near the end of the program.

## Parallelizable work

The following can run in parallel after LCM-02:

- source characterization for independent domain families;
- documentation authority classification;
- root release-metadata cataloging;
- compatibility-adapter scaffolding;
- shared-engine candidate analysis.

The following must remain serialized:

- canonical identity assignment before package creation;
- behavior characterization before semantic refactor;
- parity before cutover;
- cutover before quarantine;
- quarantine before deletion.

## Program release model

Every phase is delivered as a root-relative patch. Move-only, characterization, refactor, cutover, quarantine and deletion changes are never combined in one commit.
