---
title: "Dependency Graph and Critical Path"
tags: [exp0019, faerie-protocol, implementation-program, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
implementation_program: FP-IMP-001
program_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Dependency Graph and Critical Path

## Program dependency graph

```mermaid
flowchart TD
  I00[FP-I00 Governance and Baseline] --> I01[FP-I01 Core Compatibility]
  I01 --> I02[FP-I02 Contracts and Identity]
  I02 --> I03[FP-I03 Time Session Week]
  I03 --> I04[FP-I04 M1 Data Sync]
  I04 --> I05[FP-I05 Windows and References]
  I05 --> I06[FP-I06 Relations Hunt Candidate]
  I06 --> I07[FP-I07 Confirmation and Lifecycle]
  I07 --> I08[FP-I08 WW Engine]
  I08 --> I09[FP-I09 Ledger Arbitration Restart]
  I09 --> I10[FP-I10 Indicator Shell]
  I10 --> I11[FP-I11 Indicator Visual Projection]
  I11 --> I12[FP-I12 Indicator Panel Alerts Export]
  I12 --> I13[FP-I13 Indicator Replay Performance Release]
  I13 --> I14[FP-I14 Diagnostic EA Differential Validation]
  I14 --> I15[FP-I15 Risk Quota Paper Execution]
  I15 --> I16[FP-I16 Live Gate Release Monitoring]
```

## Critical path

The critical path is `I00 → I01 → I02 → I03 → I04 → I05 → I06 → I07 → I08 → I09 → I10 → I11 → I12 → I13`. This path ends at the complete indicator release and is not blocked by the unresolved live quota-consumption decision.

Execution development branches after the indicator release:

```text
Complete Indicator
      ↓
Diagnostic EA
      ↓
Paper EA
      ↓
FP-DEC-012 freeze + broker safety evidence
      ↓
Live EA
```

## Parallelizable work

After I02 contracts are frozen, the following may proceed in parallel but cannot be merged before their dependency gate:

- fixture generation for later relation tests;
- visual style prototypes using synthetic signals;
- documentation and input catalog review;
- performance benchmark harnesses;
- migration analysis of legacy FP101 drawings.

## Forbidden parallelization

- Implementing WW gate before basic relation lifecycle is stable.
- Implementing indicator-specific detection instead of waiting for the shared context engine.
- Implementing live order logic before paper reconciliation and `FP-DEC-012` freeze.
- Optimizing away audit fields before golden parity exists.
