# Phase 06 Hotfix002 — Full Divergence Visual Language

## Purpose

This hotfix upgrades the visual layer from a minimal audit line into a complete origin-to-destination divergence drawing system.

The previous Phase 06 drawing answered only one question:

> Did the robot see a final confirmed or invalidated state?

The new visual language answers a deeper question:

> From exactly which origin did the divergence leg begin, where did it terminate, which symbol carried that leg, which reference was involved, which clean symbol failed to hunt, and what should be visually audited before any execution logic exists?

## Scope

This patch changes only visual language and display configuration.

It does **not** add:

- order placement
- risk sizing
- target logic
- stop management
- win/loss classification
- MFE/MAE calculation
- statistical scoring
- AI decision-making
- CG filtering
- strategy mutation

## New main drawing primitive

The main primitive is:

```text
origin point -> destination point
```

Default interpretation:

```text
origin symbol: hunter symbol
origin time: exact M1 timestamp of reference extreme
origin price: hunter reference price

destination symbol: hunter symbol
destination time: exact M1 timestamp of current-cycle extreme
destination price: hunter current-cycle extreme
```

For sell divergence:

```text
origin = hunter reference high
destination = hunter current-cycle high
```

For buy divergence:

```text
origin = hunter reference low
destination = hunter current-cycle low
```

## Independent input groups

Origin and destination are independently configurable.

### Origin symbol

- hunter symbol
- clean symbol
- chart symbol
- Symbol A
- Symbol B

### Origin time

- reference cycle start
- reference cycle middle
- reference cycle end
- exact reference extreme from M1
- current cycle start
- current cycle end
- exact current extreme from M1
- confirmation close

### Origin price

- hunter reference
- hunter current extreme
- clean reference
- clean current extreme
- clean stop reference

### Destination symbol, time and price

The destination has the same independent modes.

This gives the strategy architect full control over whether the visual line represents:

- hunter reference to hunter hunt point
- clean reference to clean current extreme
- reference-cycle boundary to confirmation close
- current-cycle start to current-cycle extreme
- exact wick-to-wick line where M1 data is available

## Full object set

The patch can draw:

1. Main divergence origin-to-destination line
2. Origin marker
3. Destination marker
4. Origin vertical line
5. Destination/confirmation vertical line
6. Hunter reference horizontal guide
7. Hunter current extreme guide
8. Clean reference guide
9. Clean stop-reference guide
10. Optional clean comparison line
11. Full label at destination
12. Tooltip with signal identity, CG, direction, side, hunter, clean, origin and destination values

## Chart scale caveat

The safest default visual line is hunter-symbol based.

If the chart symbol differs from the symbol whose price is being drawn, the object can still be created, but the scale may be visually misleading.

For clean-symbol comparison drawings, the default is conservative:

```text
clean comparison line is disabled by default
if enabled, it can be restricted to clean-symbol chart only
```

## Exact wick-time limitation and improvement

The previous Phase 06 used the reference-cycle anchor because exact wick timestamp was not stored by earlier phases.

Hotfix002 improves this without changing upstream data contracts by scanning M1 rates on demand in the drawing module.

For exact reference extreme:

```text
CopyRates(symbol, PERIOD_M1, reference_cycle_start_broker, reference_cycle_end_broker)
find max high for high-side signals
find min low for low-side signals
```

For exact current extreme:

```text
CopyRates(symbol, PERIOD_M1, current_cycle_start_broker, confirmation_time_broker)
find max high for high-side signals
find min low for low-side signals
```

If exact M1 lookup fails, the module falls back to the configured cycle-boundary or confirmation time.

## Base default

Recommended default:

```text
Main line: ON
Origin symbol: hunter
Origin time: exact reference extreme
Origin price: hunter reference
Destination symbol: hunter
Destination time: exact current extreme
Destination price: hunter current extreme
Origin marker: ON
Destination marker: ON
Destination vertical: ON
Hunter reference guide: ON
Clean stop guide: ON
Clean comparison: OFF
```

This default directly expresses the hunter-side visible divergence leg without contaminating it with clean-symbol chart-scale issues.
