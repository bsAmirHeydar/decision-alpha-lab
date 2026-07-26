---
title: "Current-to-Target Architecture"
tags: [strategy-factory, phase-00, architecture, mermaid]
status: canonical
---

# Current-to-Target Architecture

## Current implemented flow

```mermaid
flowchart LR
    MT5[MetaTrader5 terminal] --> CON[MT5Connector]
    CON --> MDF[Normalized pandas bars]
    MDF --> MDE[MarketDataEngine]
    MDE --> PDS[ParquetStore]
    MDE --> LRN[LRuleNodeDetector]
    LRN --> NDS[(Node parquet cache)]
    LRN --> RTV[M0001RTV]
    RTV --> MCS[(Metric parquet cache)]
```

## Problems in the current flow

```mermaid
flowchart TD
    A[Naive terminal time] --> R1[Causality risk]
    B[Three persistence owners] --> R2[Identity and schema drift]
    C[DataFrame implicit contracts] --> R3[Unversioned interface]
    D[Live MT5 test scripts] --> R4[Non-deterministic test gate]
    E[Empty registries] --> R5[No governed run identity]
```

## Target migration shape

```mermaid
flowchart LR
    VENDOR[MT5 Data Adapter] --> BARS[Canonical Bar Contract]
    BARS --> DATA[Shared Market Data Port]
    DATA --> ART[Versioned Artifact Store]
    DATA --> ADAPTER[Structural Node Anatomy Adapter]
    ADAPTER --> EVT[Canonical AnatomyEvent]
    EVT --> FEAT[M0001 Feature/Label Plugin]
    FEAT --> REC[Versioned Feature or Outcome Record]
    EVT --> FACTORY[Shared Strategy Factory Modules]
    REC --> FACTORY
```

## Compatibility strategy

```mermaid
flowchart TD
    LEG[Legacy implementation] --> FIX[Frozen golden fixtures]
    LEG --> OLD[Legacy outputs]
    WRAP[Adapter-based implementation] --> NEW[Canonical outputs]
    FIX --> LEG
    FIX --> WRAP
    OLD --> DIFF[Differential comparison]
    NEW --> DIFF
    DIFF -->|Parity| PROMOTE[Promote wrapper]
    DIFF -->|Mismatch| BLOCK[Block migration and investigate]
```

## Non-negotiable boundary

The structural-node detector remains on the anatomy side of the adapter. The shared Factory receives an event contract; it does not call internal detector rules or infer what a node should be.
