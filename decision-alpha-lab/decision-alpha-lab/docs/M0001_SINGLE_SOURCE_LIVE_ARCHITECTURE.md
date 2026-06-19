# M0001 Single-Source Live Architecture

## Core decision

M0001 has one brain only:

```text
Python Research Engine = source of truth
MQL5                   = visual terminal only
```

The MQL expert does not compute nodes, territories, events, RTV, hunts, random baselines, or validation logic. It reads the visual contract produced by Python and draws it on the MT5 chart.

## Why this matters

The lab is intentionally designed around one obsessive rule:

```text
The exact code used for tests, research, validation and backtest artifact generation
must be the same code whose output is inspected live on the chart.
```

There must not be a separate MQL implementation of the metric and a separate Python implementation of the metric. Two engines create a hidden risk: the visual chart can look correct while the research engine is different, or the backtest can pass while the live visual logic is not the same.

## Runtime flow

```text
MT5 / market cache / cached candles
        ↓
Python M0001 engine
        ↓
L-rule reference points
        ↓
Single candle-by-candle RTV state machine
        ↓
Events, territories, RTV, hunts, debug sample sets
        ↓
CSV visual contract
        ↓
MQL5 visual lab draws the contract
```

## Single-source invariant

The same Python modules are used by every mode:

```text
lab/core/CP0001_structural_nodes/metrics/M0001_rtv/
  schemas.py
  math_utils.py
  reference_points.py
  engine.py
  mql_visual_contract.py
```

These modules feed:

```text
unit tests
integration tests
random baseline tests
static export
live visual export
MT5 visual inspection
validation journal screenshots
```

## What MQL is allowed to do

MQL is allowed to:

```text
read CSV rows
draw nodes
draw active_from markers
draw territories
draw event windows
draw before/inside/outside candle samples
draw RTV labels
draw hunt markers
draw summary panels
filter and toggle visual packages
reload the file on a timer
```

MQL is not allowed to:

```text
detect L-rule nodes
compute territories
start or close events
compute mean_inside
compute mean_before
compute RTV
compute hunts
run random baselines
make research decisions
```

## Live-like behavior without two engines

The live behavior is produced by repeatedly running the Python engine on the latest available candle window and exporting the visual contract. MT5 reloads that contract on a timer.

This gives the live/testing feel while preserving single-source correctness:

```text
Python updates the truth
MQL updates the visualization
```

## Debug packages

The MQL expert supports visual packages controlled by `InpViewPreset`:

```text
0  Custom manual toggles
1  Structural Node Audit
2  Territory Construction Audit
3  Event Entry Exit Audit
4  Baseline vs Inside Sample Audit
5  RTV Formula Audit
6  Hunt Validation Audit
7  Live/Open Event Audit
8  Candle Classification Audit
9  State Machine Audit
10 Focused Event Inspector
11 Multi Event Overview
12 Full Research Lab
```

All manual visual toggles default to `false`. This keeps the chart clean and forces the researcher to turn on one package or one visual layer at a time.

## Validation philosophy

A result is not trusted because it looks good. It becomes trusted only when these layers agree:

```text
1. Python unit tests pass
2. Python integration tests pass
3. Random baseline comparison is generated from the same engine
4. Visual contract is generated from the same engine
5. MT5 visual inspection confirms node/event/RTV/hunt semantics
6. Screenshots are stored in a validation journal with expected vs observed behavior
```

## Professional framing

This is the correct way to describe the system:

```text
M0001 uses a single Python research engine for both validation and live visual inspection. MT5/MQL5 is used as a market-native visualization terminal that consumes deterministic Python-generated visual contracts. This prevents research/live divergence and makes every visual audit traceable to the same tested code path.
```

## Anti-pattern avoided

The lab intentionally avoids this structure:

```text
Python backtest engine
MQL live engine
manual visual interpretation
```

That structure is rejected because it creates logic drift.

The accepted structure is:

```text
Python engine once
multiple consumers
MQL visual-only consumer
```
