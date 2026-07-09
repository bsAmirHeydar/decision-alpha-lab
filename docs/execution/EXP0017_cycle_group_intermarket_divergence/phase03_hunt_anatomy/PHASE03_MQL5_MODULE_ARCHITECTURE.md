# Phase 03 MQL5 Module Architecture

## Expert

```text
EXP0017_CG_Hunt_Anatomy.mq5
```

The expert is a standalone validation layer. It can be attached to a chart to observe raw hunt behavior across all enabled Cycle Groups and both configured symbols.

## Include modules

```text
CGH_Types.mqh
CGH_HuntField.mqh
CGH_Display.mqh
CGH_Engine.mqh
```

## Dependency chain

```text
EXP0017_CG_Hunt_Anatomy.mq5
  -> CGH_Engine.mqh
    -> CGH_Display.mqh
      -> CGH_HuntField.mqh
        -> CGH_Types.mqh
        -> CGR_ReferenceField.mqh
        -> CGT_Time.mqh
```

Phase 03 depends on Phase 01 and Phase 02, but it does not replace them.

## Responsibilities

### CGH_Types

Defines the hunt-specific data contracts:

- current symbol range
- symbol hunt state
- reference hunt state
- group hunt state
- hunt configuration

### CGH_HuntField

Builds raw hunt states:

- aggregates current-cycle M1 high/low for both symbols
- calls the Phase 02 reference field
- compares current-cycle range against reference high/low
- records high hunt and low hunt flags
- counts one-symbol and both-symbol hunts

### CGH_Display

Builds the chart panel and print summary.

The display intentionally uses mechanical language:

```text
H = high hunted
L = low hunted
H+L = both sides hunted
- = not hunted
```

It does not display buy, sell, entry, target, or score.

### CGH_Engine

Coordinates the time snapshot, CG registry, hunt field, display panel, and timer refresh.

## Timer model

The expert refreshes on timer rather than every tick.

This keeps observation deterministic and avoids turning the phase into an execution layer.

Default timer:

```text
5 seconds
```
