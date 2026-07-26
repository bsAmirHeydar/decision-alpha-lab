---
title: "Program Architecture and Critical Path"
status: proposed-reference
version: 2.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration]
---
# Program Architecture and Critical Path

## Master-phase architecture

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

## Refined implementation train

```mermaid
flowchart LR
    L7[LCM-07] --> A8[08A Portfolio]
    A8 --> B8[08B Pilot]
    B8 --> C8[08C Context waves]
    C8 --> A9[09A Setup contracts]
    A9 --> B9[09B Setup migration]
    B9 --> A10[10A Capability inventory]
    A10 --> B10[10B Boundary construction]
    B10 --> C10[10C Dry parity and safety]
    C10 --> A11[11A Visual contracts]
    A11 --> B11[11B Visual parity/cutover]
    B11 --> A12[12A Doc authority]
    A12 --> B12[12B Obsidian reconciliation]
    B12 --> A13[13A Dual run]
    A13 --> B13[13B Consumer cutover]
    B13 --> C13[13C Rollback closure]
    C13 --> A14[14A Deprecation]
    A14 --> B14[14B Quarantine]
    B14 --> A15[15A Deletion proof]
    A15 --> B15[15B Reorganization]
    B15 --> C15[15C Deletion]
    C15 --> A16[16A Full audit]
    A16 --> B16[16B Closure]
```

## Critical path

The critical path is not file movement. It is:

`owner resolution → evidence capture → canonical contract → deterministic implementation → parity proof → reversible cutover → quarantine maturity → deletion proof → closure evidence`.

The balanced partition protects this path by separating concerns that have different failure and rollback semantics. Context portfolio selection is separated from pilot implementation; Treatment extraction is separated from execution safety proof; dual-run evidence is separated from consumer switching; deletion proof is separated from repository reorganization and destructive deletion.

## Serialization rules

The following transitions are strictly serialized:

- identity before package creation;
- characterization before semantic refactor;
- Context packages before Setup packages;
- Setup packages before Treatment extraction;
- disabled execution boundary before dry parity;
- visual contracts before visual cutover;
- documentation authority before relocation;
- dual-run evidence before consumer switch;
- cutover rollback proof before deprecation;
- deprecation before quarantine;
- quarantine maturity before deletion eligibility;
- deletion proof before reorganization and revalidation;
- full audit before closure decision.

## Parallel work allowed inside a subphase

Independent domain families may be analyzed in parallel only when they use separate packet identities, source digests, owners and acceptance records. A parallel task cannot publish directly to the next subphase; its outputs must be consolidated through the current subphase gate.

## Release model

Every subphase is a root-relative atomic patch. The master phase closes only after all of its subphase patches are accepted. See [[PHASE_PARTITION_AND_PATCH_GRANULARITY_STANDARD]] and [[SUBPHASE_HANDOFF_AND_CHECKPOINT_STANDARD]].
