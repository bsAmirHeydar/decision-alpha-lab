# Flag Counting Level 19C — Closed-Bar State Delta Ledger

## Purpose

Level 19C adds a state-delta ledger on top of the Level 19B closed-bar state ledger.

This layer is still read-only.

It records how the Level 19 State Gate snapshot changes from one closed bar to the next.

## New output

Level 19C keeps:

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_level19.csv
MQL5/Files/FlagCountingPhoenix/state_gate_level19_closed_bar_ledger.csv
```

and adds:

```text
MQL5/Files/FlagCountingPhoenix/state_gate_level19_state_delta.csv
```

## New input

```text
InpLevel19StateGateExportStateDeltaCsv = true
```

## What it measures

For each newly observed closed bar, the delta ledger compares the current Level 19 snapshot against the previous closed-bar snapshot.

It records:

```text
events delta
hooks delta
visible events delta
F1 delta
F2 delta
F3 delta
ND delta
latest visible event id change
latest visible hook id change
render ok change
validation ok change
state key change
state status change
```

## Delta statuses

The state delta row can classify a bar as:

```text
STATE_DELTA_BASELINE_FIRST_ROW
STATE_DELTA_NO_CHANGE
STATE_DELTA_MINOR_CHANGE
STATE_DELTA_STRUCTURAL_CHANGE
STATE_DELTA_MAJOR_CHANGE
```

## Duplicate behavior

The delta ledger writes at most one row per closed-bar time while the EA instance is running.

Repeated ticks on the same closed bar are skipped in memory.

## Hard no-touch boundary

Level 19C does not modify:

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

## Panel behavior

The Level 19 panel remains disabled by default:

```text
InpLevel19StateGatePanelEnabled = false
```

## Print behavior

Prints remain disabled by default.

The Level 19 report print still only runs if:

```text
InpLevel19StateGatePrintSummary = true
```

## Why this layer matters

Level 19B tells us what the state was at each closed bar.

Level 19C tells us what changed between closed bars.

This is the first safe diagnostic layer for studying state transitions without touching chart visuals or execution.
