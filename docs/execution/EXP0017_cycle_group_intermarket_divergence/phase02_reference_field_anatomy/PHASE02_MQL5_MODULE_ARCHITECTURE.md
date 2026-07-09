# Phase 02 MQL5 Module Architecture

## New expert

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Reference_Anatomy.mq5
```

This expert is a standalone validation tool for the reference field.

It should be attached to a chart to inspect whether the robot is building the same-day CG reference field correctly.

## New include modules

```text
mql5/Include/IntermarketDivergenceExecution/CG/CGR_Types.mqh
mql5/Include/IntermarketDivergenceExecution/CG/CGR_ReferenceField.mqh
mql5/Include/IntermarketDivergenceExecution/CG/CGR_Display.mqh
mql5/Include/IntermarketDivergenceExecution/CG/CGR_Engine.mqh
```

## Dependency rule

Phase 02 depends on the Phase 01 time anatomy module:

```text
CGT_Types.mqh
CGT_Time.mqh
```

It does not create an independent time source. All CG boundaries must come from the Phase 01 time contract.

## Main responsibilities

### `CGR_Types.mqh`

Defines data structures for:

- reference config
- per-symbol reference high/low
- paired references for both symbols
- per-CG reference state

### `CGR_ReferenceField.mqh`

Builds the reference field:

- converts NY cycle times to broker time
- calls `CopyRates()` on M1 data
- aggregates high/low values
- marks references as ready or missing

### `CGR_Display.mqh`

Builds chart-panel text and log summaries.

### `CGR_Engine.mqh`

Coordinates:

- time snapshot
- CG registry
- current cycle snapshot
- previous-cycle reference generation
- display output

## Non-goals

This module intentionally excludes:

- hunt detection
- divergence detection
- invalidation detection
- stop calculation
- entry calculation
- order placement
- statistical reporting
- model ranking
