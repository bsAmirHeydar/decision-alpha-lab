---
title: "Quota Alerts"
tags: [exp0019, faerie-protocol, fp-i12, indicator, operator-ux, obsidian]
status: implemented
experiment: EXP0019
context_id: FP-CONTEXT-001
phase_id: FP-I12
phase_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Quota Alerts

## Purpose

This note defines the FP-I12 contract for **Quota Alerts**. The operator layer consumes accepted FP-I10 machine state and FP-I11 visual identities. It may change visibility, layout, notification delivery, local export, and operator preferences. It may not recompute relation truth, change signal identity, modify eligibility, consume quota, or mutate the semantic ledger.

## Normative rules

1. Every action is instance-scoped and reason-coded.
2. Filter changes affect projection only; the source snapshot hash remains unchanged.
3. Historical alerts are suppressed by default and require explicit operator opt-in.
4. Alert identity is deterministic by semantic ID, alert type, and alert contract version.
5. Audit export is append-only, local-file only, and complete for the configured scope.
6. `FP-DEC-012` remains visible as `UNSET`; FP-I12 does not invent a consumption point.
7. Missing or incompatible state fails closed and is shown as `DEGRADED` or `BLOCKED`.

## Implementation

- Python reference package: `phase_i12/python/fp_i12_operator`.
- MQL5 package: `mql5/Include/AlphaLab/EXP0019/FaerieProtocol/I12`.
- Production indicator: `EXP0019_FaerieProtocol_Context.mq5`.
- Self-test indicator: `EXP0019_FP_I12_OperatorUXSelfTest.mq5`.
- Contract version: `1.0.0`.

The implementation keeps panel, filters, alert router, exporter, preferences, checkpoint, action router, and diagnostics behind explicit interfaces. The product entry point only composes those interfaces.

## State and evidence

Required evidence includes instance ID, configuration hash, source snapshot hash, filter hash, panel hash, alert-state hash, export content hash, action ID, reason code, and source revision sequence. Persistence artifacts are caches; accepted semantic state remains upstream.

## Failure behavior

Invalid actions are rejected without changing preferences. Duplicate alerts are suppressed and recorded. Rate-limited alerts remain auditable. Export failures do not mutate the ledger. Corrupted or version-mismatched UX checkpoints are rejected and rebuilt from defaults plus accepted upstream state.

## Tests

- deterministic identity and hash tests;
- projection-only filter tests;
- alert duplicate, historical, rate-limit, acknowledgement, and restart tests;
- CSV/JSONL completeness and append-only tests;
- panel mode, paging, focus, and open-decision tests;
- multi-instance and authority-boundary tests.

## Operational notes

Popup, sound, push, and email are individually controlled and disabled where the input says so. CSV and JSONL export are optional and disabled by default. No external HTTP call is permitted. Panel removal on deinitialization is configurable and instance-scoped.

## Handoff

FP-I13 receives stable operator output, checkpoint, filter, alert, export, and panel contracts. FP-I13 may test historical replay, sustained performance, and multi-chart release behavior; it may not redefine FP-I12 identities.

## Navigation

- [[../fp_i11/55_HANDOFF_TO_FP_I12|FP-I11 handoff]]
- [[65_HANDOFF_TO_FP_I13|FP-I13 handoff]]
