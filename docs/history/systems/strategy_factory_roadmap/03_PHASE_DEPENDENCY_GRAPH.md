---
title: "Phase Dependency Graph"
tags:
  - strategy-factory
  - implementation-roadmap
  - alpha-lab
status: canonical
doc_version: 1.0.0
---

# Phase Dependency Graph

```mermaid
graph TD
    P00[00 Current-State Audit] --> P01[01 Contracts and Schema]
    P01 --> P02[02 Package Skeleton]
    P02 --> P03[03 Plugin Kernel]
    P03 --> P04[04 Manifest Compiler]
    P01 --> P05[05 Artifact Identity]
    P03 --> P06[06 Anatomy Adapter SDK]
    P04 --> P07[07 Context and Market Clock]
    P07 --> P08[08 Feature DAG and Cache]
    P04 --> P09[09 Candidate Policy Engine]
    P08 --> P10[10 Outcome Simulator]
    P09 --> P10
    P10 --> P11[11 Statistics and Nulls]
    P11 --> P12[12 Anti-Overfit Engine]
    P12 --> P13[13 Training Pipeline]
    P13 --> P14[14 Model Registry]
    P08 --> P15[15 Compiled Decision Runtime]
    P09 --> P15
    P14 --> P15
    P15 --> P16[16 Portfolio Risk and Action Plans]
    P16 --> P17[17 Paper Broker and Replay]
    P17 --> P18[18 MQL5 Runtime and Broker Boundary]
    P15 --> P19[19 Observability and Drift]
    P18 --> P19
    P06 --> P20[20 EXP0017 Pilot]
    P17 --> P20
    P20 --> P21[21 NDS Zone-AF Pilot]
    P21 --> P22[22 Multi-Strategy Portfolio]
    P22 --> P23[23 Production Hardening]
    P23 --> P24[24 V1 Release]
```

## Parallelization Rules

- Phases 03 and 05 may proceed in parallel after Phase 02.
- Phases 07 and 09 may proceed in parallel after the compiler is stable.
- Documentation, fixtures, and static schemas can be prepared one phase ahead.
- MQL5 runtime work must not begin before Python reference behavior and cross-language fixtures exist.
- Live execution work must not begin before paper replay parity is measurable.
