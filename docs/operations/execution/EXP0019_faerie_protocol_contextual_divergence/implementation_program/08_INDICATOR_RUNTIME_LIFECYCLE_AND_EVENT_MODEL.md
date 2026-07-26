---
title: "Indicator Runtime Lifecycle and Event Model"
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
# Indicator Runtime Lifecycle and Event Model

## Event-loop design

The indicator runs a small orchestration shell around the shared engine.

### `OnInit`

1. Parse and validate inputs.
2. Resolve symbols and host confirmation timeframe.
3. Build configuration/context hash.
4. Verify shared-core compatibility.
5. Subscribe/select both symbols.
6. Load checkpoint if compatible.
7. Backfill required M1 history.
8. Build completed windows and replay semantic events.
9. Initialize projection, panel, and alert dedup stores.
10. Start timer only after the engine reaches a declared health state.

### `OnCalculate`

`OnCalculate` is not the primary multi-symbol scanner. It:

- notices host-chart bar/timeframe changes;
- updates host-chart projection coordinates;
- publishes optional machine-readable indicator buffers;
- schedules, but does not duplicate, engine processing.

### `OnTimer`

1. Synchronize new M1 bars for both symbols.
2. Repair gaps or enter `DATA_INCOMPLETE`.
3. Advance active windows.
4. evaluate hunts, candidates, confirmation deadlines, WW, suppression, and quota eligibility;
5. append ledger events;
6. update only dirty projections and panel cells;
7. route new alerts/exports;
8. persist checkpoint on policy-defined intervals.

### `OnChartEvent`

Handles only UI interactions such as filters, mode changes, panel paging, and forced refresh. UI actions may change projection state but not semantic signal state.

### `OnDeinit`

- stop timer;
- flush exporter and checkpoint;
- release resources;
- delete only objects owned by this instance when configured;
- leave no global mutable state.

## Dirty-set rendering

Every semantic event identifies affected projection IDs. The renderer updates those IDs only. Global redraw is allowed only on:

- initialization;
- timeframe/scale change requiring geometry rebuild;
- input reinitialization;
- explicit user refresh;
- data revision invalidation.

## Optional machine-readable buffers

The indicator may expose non-trading state buffers for `iCustom` consumers:

| Buffer | Meaning |
|---:|---|
| 0 | data health code |
| 1 | active WW direction (`-1/0/+1`) |
| 2 | last confirmed direction |
| 3 | last confirmed relation enum |
| 4 | current session quota available (`0/1`) |
| 5 | monotonic semantic event sequence |

Buffers are projections only and cannot replace ledger/event APIs.
