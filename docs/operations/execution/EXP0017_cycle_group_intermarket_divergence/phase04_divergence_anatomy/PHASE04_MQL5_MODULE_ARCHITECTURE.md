# Phase 04 MQL5 Module Architecture

## Expert

```text
EXP0017_CG_Divergence_Anatomy.mq5
```

This expert is a standalone observation tool. It attaches to a chart and displays raw divergence candidates across enabled CGs.

## Include modules

```text
CGD_Types.mqh
CGD_DivergenceField.mqh
CGD_Display.mqh
CGD_Engine.mqh
```

## Dependency chain

```text
EXP0017_CG_Divergence_Anatomy.mq5
  -> CGD_Engine.mqh
    -> CGD_Display.mqh
      -> CGD_DivergenceField.mqh
        -> CGD_Types.mqh
        -> CGH_HuntField.mqh
          -> CGR_ReferenceField.mqh
          -> CGT_Time.mqh
```

## Design principle

Phase 04 does not duplicate Phase 03 hunt logic. It asks Phase 03 for raw hunt states and converts only one-sided high/low hunt states into divergence candidates.

## Module responsibilities

### CGD_Types

Defines divergence candidate and group state contracts.

### CGD_DivergenceField

Consumes hunt states and produces candidate divergence objects.

### CGD_Display

Builds the chart panel and print summaries.

### CGD_Engine

Coordinates time snapshots, cycle snapshots, group iteration, candidate aggregation, display, and timer refresh.
