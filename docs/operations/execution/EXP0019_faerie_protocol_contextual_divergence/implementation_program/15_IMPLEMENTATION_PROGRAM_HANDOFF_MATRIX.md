---
title: "Implementation Program Handoff Matrix"
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
# Implementation Program Handoff Matrix

## Product milestones

| Milestone | Last required phase | Deliverable |
|---|---|---|
| context engine diagnostic | FP-I09 | deterministic semantic ledger |
| complete indicator beta | FP-I12 | full visual/UI/alert/export functionality |
| complete indicator release | FP-I13 | replay/performance/restart evidence |
| diagnostic EA | FP-I14 | differential runtime harness |
| paper execution | FP-I15 | simulated order/reconciliation evidence |
| live release candidate | FP-I16 | blocked until all live gates pass |

## Handoff evidence

Every phase hands the next phase:

- accepted public contracts;
- exact module and version list;
- golden fixtures and expected hashes;
- open risks and known limitations;
- performance baseline;
- compiled test entry points;
- rollback instructions.

## Indicator-to-EA handoff

The indicator release exports no private detector API. Instead, both Indicator and EA instantiate `FP_Engine` with the same semantic configuration. The handoff contract is:

```text
FP_Engine snapshot/events/ledger
        ├── FP_IndicatorProjection
        └── FP_ExecutionPolicy adapters
```

Any signal-ID mismatch between products blocks execution development.
