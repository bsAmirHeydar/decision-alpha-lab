---
title: "Full Replay Reducer"
tags: [exp0019, faerie-protocol, fp-i13, indicator-release, obsidian]
status: implemented
experiment: EXP0019
context_id: FP-CONTEXT-001
phase_id: FP-I13
phase_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Full Replay Reducer

Full replay starts from empty state and consumes the entire fixture once. `full_scan_count` must equal one. The resulting inventory records semantic payloads, visual semantic identities, instance-scoped object IDs, alert and export IDs, event-chain hash, and last sequence.

Full replay is the reference path for acceptance; it is not permitted on every timer or tick in production.
## Implementation linkage

The **12 Full Replay Reducer** contract is implemented through the versioned `fp_i13_release` Python reference package, the MQL5 `I13` include boundary, the production indicator integration, and the FP-I13 release self-test. The implementation must consume accepted FP-I10–FP-I12 outputs rather than reconstructing context from chart objects.

Behavior-bearing fields are represented in closed contracts and JSON schemas. Presentation-only fields remain outside semantic identity. Every accepted output carries a deterministic hash or derives from an upstream deterministic identity.

## Failure and health behavior

- Missing fixture, source revision, or configuration identity fails closed.
- Duplicate input with equal identity is idempotent and remains auditable.
- Identity collision with different payload blocks the affected run.
- Checkpoint mismatch causes deterministic rebuild instead of partial restoration.
- Soft resource overrun produces `DEGRADED` while preserving semantic processing.
- Hard resource, parity, or collision failure produces `BLOCKED` or rejects acceptance.
- Local MetaEditor evidence may remain `PENDING`; it may never be inferred from static validation.

## Required acceptance evidence

1. Configuration and context hash.
2. Fixture or runtime instance ID.
3. Source data revision ID.
4. Full, incremental, restart, or runtime inventory hash as applicable.
5. Closed reason codes for every non-ready result.
6. Performance counters when the operation changes state volume or projection work.
7. File, manifest, or checkpoint hash for persisted artifacts.
8. Reviewer-visible status separating source acceptance from local production acceptance.

## Operational verification

Operators reproduce this contract using the FP-I13 Python suite, MQL5 release self-test, local compile script, and the relevant acceptance template. Historical replay is quiet for alerts by default. Audit export remains append-only. Concurrent instances must use independent namespaces and persistence keys.

A result is not accepted merely because the chart appears correct. The semantic/event inventory, reason codes, and release-manifest identity must agree with the expected evidence.

## Change policy

Any change to this contract requires a new phase or contract version, updated schema and reason registry, regenerated golden vectors, full/incremental and restart replay, timeframe and multi-instance checks, performance remeasurement, file-hash regeneration, and a new release-manifest hash. Performance optimization may not remove confirmed, invalidated, suppressed, WW, quota, or health evidence.

