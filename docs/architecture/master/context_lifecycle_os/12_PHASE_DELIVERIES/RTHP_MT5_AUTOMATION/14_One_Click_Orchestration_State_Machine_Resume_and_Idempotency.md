---
title: RTHP MT5 Automation — One-Click Orchestration, State Machine, Resume, and Idempotency
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, orchestration, resume, idempotency]
---

# One-Click Orchestration, State Machine, Resume, and Idempotency

## Target state machine

```text
CREATED
→ TERMINAL_RESOLVED
→ SYMBOLS_RESOLVED
→ RANGE_RESOLVED
→ M1_ACQUIRED
→ SOURCE_VALIDATED
→ SOURCE_FROZEN
→ RTHP_MATERIALIZED
→ AI_INPUT_COMPILED
→ BATCH_FROZEN
→ TRAIN_COMPLETED
→ RUN_VERIFIED
```

Failure states are explicit and resumable where safe.

## One-click behavior

The `run` command performs all stages. Separate commands remain available for diagnostics:

```text
preflight
acquire
validate-source
materialize
train
verify-run
resume
```

## Idempotency

- Same configuration and same source revision produce the same run identity.
- Existing completed output is verified, not overwritten.
- Existing incomplete output is resumed only if its staging manifest is compatible.
- Different terminal metadata, symbol metadata, common range, or source hashes produce a different run identity.

## Atomic completion

A run is considered complete only after a final completion marker and verified hash ledger are written. Partially completed staging directories never masquerade as completed runs.
