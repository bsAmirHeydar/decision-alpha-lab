# MQL-Native Runtime Architecture

Version: 1.59

## Decision

The active runtime is MQL5-native.

Python, FastAPI, React, Parquet caches, CSV bridges, Excel/JSON report generation, and external watcher loops are not part of the active execution path.

## Active runtime flow

Fast final-only mode:

```text
MT5 OnTick
  -> candle gate
  -> append latest closed candle once
  -> no full recompute during runtime
  -> OnDeinit final compute
  -> final node/random reports
  -> final restored chart visuals
```

Visual replay mode:

```text
MT5 OnTick
  -> candle gate
  -> append latest closed candle once
  -> recompute nodes/events/audit state
  -> redraw chart objects
```

## Source of truth

MQL5 is the source of truth for:

- candle access,
- warmup historical seeding,
- L-rule structural node detection,
- M0001 territory/event construction,
- HUNT/TOUCH/revisit semantics,
- RTV/logRTV calculation,
- matched random baseline,
- final chart visualization.

## Active module layout

```text
mql5/
  Experts/
    DecisionAlphaLab/
      M0001/
        M0001_LiveVisualLab.mq5

  Include/
    DecisionAlphaLab/
      Common/
        DAL_Common.mqh
        DAL_Math.mqh
        DAL_ChartObjects.mqh
      Market/
        DAL_Bars.mqh
        DAL_LiveBarStream.mqh
      StructuralNodes/
        DAL_StructuralNodeEngine.mqh
        LRule/
          DAL_LRuleTypes.mqh
          DAL_LRuleDetector.mqh
      M0001/
        DAL_M0001Config.mqh
        DAL_M0001Types.mqh
        DAL_M0001Engine.mqh
        DAL_M0001AuditState.mqh
        DAL_M0001Visual.mqh
        DAL_M0001RtvNullComparison.mqh
```

## Removed from active runtime

```text
old validation journal script
old verbose distribution module
Excel/JSON report writers
Python bridge runtime
UI bridge runtime
```

## Logic lock

The canonical active semantics are documented in:

```text
docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md
```
