---
title: "FP-I04 — Multi-Symbol M1 Synchronization, Coverage, and Data Revision"
tags: [exp0019, faerie-protocol, implementation-program, fp-i04, obsidian]
status: implemented-python-static-validated
experiment: EXP0019
context_id: FP-CONTEXT-001
implementation_program: FP-IMP-001
program_version: 1.0.0
phase_version: 1.0.0
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# FP-I04 — Multi-Symbol M1 Synchronization, Coverage, and Data Revision

## Mission

Build the canonical two-symbol M1 data plane. Resolve broker aliases to stable symbols, validate closed bars, align both symbols by exact UTC M1 open, expose every absence and conflict, maintain parent-linked revisions, and support deterministic batch/incremental replay.

## Accepted architecture

```text
raw M1 deliveries
   │
   ├─ SymbolResolver
   ├─ closed-bar / tick-grid / OHLC validation
   ├─ duplicate normalization
   └─ transport-vs-semantic separation
   │
FP-I03 CalendarSnapshot ── expected UTC minute axis
   │
   ├─ MinuteCell(left)
   ├─ MinuteCell(right)
   ├─ coverage and gap runs
   └─ AlignedMinute rows
   │
   ├─ DataRevision / RevisionImpact
   ├─ IncrementalCursor
   ├─ BackfillRequest
   └─ PairDatasetSnapshot
   │
   ▼
FP-I05 window/reference engine
```

## Canonical policies

1. **Alignment key:** exact UTC M1 open only.
2. **Finality:** only closed M1 bars enter canonical results.
3. **Duplicate equality:** semantic bar hash, not arrival order.
4. **Conflict:** no winner; minute and result are blocked.
5. **Absence:** `MISSING` inside known coverage and `OUT_OF_COVERAGE` outside it.
6. **Calendar exclusions:** daily gap and weekend are not expected observations.
7. **Revision:** initial, append, late insert, correction, delete, conflict, or no change.
8. **Invalidation:** changed minutes and dependent windows only.
9. **Parity:** batch is the incremental/restart oracle.
10. **Synthetic data:** forbidden.

## Delivered code

| Surface | Path |
|---|---|
| Python package | `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04/python/fp_i04_data` |
| Tests | `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04/tests` |
| Schemas | `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04/schemas` |
| Config/examples | `lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04/config`, `examples` |
| MQL5 mirror | `mql5/Include/FaerieProtocol/EXP0019/Data` |
| Self-test | `mql5/Experts/FaerieProtocolTests/EXP0019_FP_I04_DataSyncSelfTest.mq5` |
| Diagnostic | `mql5/Experts/FaerieProtocol/EXP0019_FP_I04_DataSyncDiagnostic.mq5` |

## Public contracts

- `SymbolSpec`
- `SymbolPairSpec`
- `M1Bar`
- `DuplicateResolution`
- `CoverageInterval`
- `GapInterval`
- `MinuteCell`
- `AlignedMinute`
- `DataRevision`
- `IncrementalCursor`
- `BackfillRequest`
- `SynchronizationResult`
- `RevisionImpact`
- `SynchronizerConfig`
- `PairDatasetSnapshot`

## Acceptance evidence

- 67 phase tests.
- 279 cumulative FP-I00 through FP-I04 tests.
- 50 EXP0018 Daye regression tests.
- 15 closed JSON schemas.
- 10 executable conformance checks.
- MQL5 static contract parity and no forbidden authority.
- Clean-baseline patch verification required before release.

## Explicit non-goals

- No A/L/N/W aggregation.
- No reference creation or lifecycle.
- No hunt, relation, divergence, or confirmation.
- No indicator, drawing, alert, or panel.
- No paper/live execution.

## Handoff to FP-I05

FP-I05 consumes revision-bearing aligned rows and may aggregate them into symbol-local A/L/N/W windows. It may not compress missing calendar dates, substitute absent bars, alter the UTC join key, or erase revision lineage.

## Navigation

- [[../phase_deliveries/fp_i04/00_FP_I04_DELIVERY_MOC|FP-I04 Delivery MOC]]
- [[FP_I03_NEW_YORK_TIME_TRADING-DAY_SESSION_AND_WEEK_KERNEL|Previous: FP-I03]]
- [[FP_I05_SESSION_WEEK_WINDOW_STORE_CALENDAR-DAY_SELECTOR_AND_REFERENCE_ENGINE|Next: FP-I05]]
