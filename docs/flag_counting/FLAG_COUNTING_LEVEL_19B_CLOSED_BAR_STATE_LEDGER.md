# Flag Counting Level 19B — Closed-Bar State Ledger

## Purpose

Level 19B adds a closed-bar state ledger on top of the clean isolated Level 19 State Gate.

This layer is still read-only.

It does not touch renderer files, drawing logic, chart curves, F/Hook/Node objects, RTV objects, zones, or execution logic.

## New output

Level 19B keeps the latest snapshot file:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_level19.csv
```

and adds an append-only closed-bar ledger:

```text
MQL5/Files/FlagCountingPhoenix/state_gate_level19_closed_bar_ledger.csv
```

## New input

```text
InpLevel19StateGateExportClosedBarLedgerCsv = true
```

## Behavior

The ledger writes one row per newly observed closed-bar time.

If the EA runs again on the same closed bar, the ledger skips the duplicate row in memory.

The latest snapshot still overwrites:

```text
latest_state_gate_level19.csv
```

The ledger appends:

```text
state_gate_level19_closed_bar_ledger.csv
```

## What each row records

The ledger row uses the same schema as the Level 19 snapshot:

```text
generated_at
version
symbol
period
bars
scale_count
timebase status
first/last bar time
node counts
hook counts
event counts
visible/hidden counts
F1/F2/F3 counts
ND count
export report state
render report state
validation report state
latest visible event summary
latest visible hook summary
state status
state key
no-touch contract
```

## Why this layer matters

The previous clean Level 19 snapshot only told us the current state.

Level 19B starts keeping a closed-bar history, so later layers can compare how state changes over time without touching chart rendering.

## Hard no-touch boundary

This phase does not modify:

```text
FP_Renderer.mqh
FP_RenderRules.mqh
FP_RenderTypes.mqh
F / Hook / Node drawing logic
curves
lines
RTV / zone objects
object cleanup behavior
license logic
execution logic
```

## Print behavior

Prints remain silent by default.

The Level 19 report print still only runs if:

```text
InpLevel19StateGatePrintSummary = true
```

## Panel behavior

The Level 19 panel remains disabled by default:

```text
InpLevel19StateGatePanelEnabled = false
```
