---
title: "FP-I13 Delivery MOC"
tags: [exp0019, faerie-protocol, fp-i13, indicator-release, obsidian]
status: implemented
experiment: EXP0019
context_id: FP-CONTEXT-001
phase_id: FP-I13
phase_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# FP-I13 Delivery MOC

## Purpose

This MOC is the authoritative navigation surface for the complete indicator release-hardening phase. FP-I13 does not redefine relation, confirmation, WW, quota, visual, alert, or export semantics. It proves that the accepted FP-I03 through FP-I12 composition behaves identically across full replay, incremental updates, restart, chart timeframe changes, and multiple isolated instances.

## Acceptance domains

1. Historical replay and deterministic reducer.
2. Full versus incremental event and inventory parity.
3. Checkpoint/restart parity and rebuild behavior.
4. Chart-timeframe invariance with fixed resolved host timeframe.
5. Multi-chart and multi-instance isolation.
6. Latency, memory, object, object-operation, throughput, and checkpoint budgets.
7. Noncritical projection degradation without evidence loss.
8. Release profiles, source manifest, user guide, rollback, and local MetaEditor gate.

## Product state

The source release is accepted after all source-level gates pass. Production release readiness remains false until MetaEditor compilation and local chart acceptance are supplied. This distinction is intentional and reason-coded.

## Navigation

- [[01_PHASE_CHARTER|Phase charter]]
- [[10_REPLAY_ARCHITECTURE|Replay architecture]]
- [[20_FULL_INCREMENTAL_PARITY|Full/incremental parity]]
- [[30_RESTART_PARITY|Restart parity]]
- [[40_TIMEFRAME_INVARIANCE|Timeframe invariance]]
- [[50_MULTI_CHART_ISOLATION|Multi-chart isolation]]
- [[60_PERFORMANCE_ACCEPTANCE|Performance acceptance]]
- [[70_INDICATOR_USER_GUIDE|Indicator user guide]]
- [[80_PRODUCTION_ACCEPTANCE_MATRIX|Production acceptance matrix]]
- [[90_HANDOFF_TO_FP_I14|Handoff to FP-I14]]
## Implementation linkage

The **00 Fp I13 Delivery Moc** contract is implemented through the versioned `fp_i13_release` Python reference package, the MQL5 `I13` include boundary, the production indicator integration, and the FP-I13 release self-test. The implementation must consume accepted FP-I10–FP-I12 outputs rather than reconstructing context from chart objects.

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

