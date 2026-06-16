# M0001 Python Brain / MQL Visual Architecture

M0001 now follows one strict architecture rule:

```text
Python is the only brain.
MQL is only the visual terminal.
```

The same Python code path is used for:

```text
research
unit tests
integration tests
random baseline
backtest-style artifact generation
live-style visual export
MT5 visual inspection
validation screenshots
```

MQL does not compute the metric. It reads the Python-generated visual contract and draws it on the chart.

## Why this exists

The lab rejects a two-engine architecture:

```text
Python backtest logic
MQL live logic
```

That creates logic drift. The chart can look right while the tested code is different, or the backtest can pass while live visual behavior is computed by a different implementation.

The accepted architecture is:

```text
single Python engine
multiple consumers
MQL visual-only consumer
```

## Main files

```text
lab/core/CP0001_structural_nodes/metrics/M0001_rtv/
  schemas.py
  math_utils.py
  reference_points.py
  engine.py
  mql_visual_contract.py

tools/export_m0001_to_mql.py
tools/run_m0001_python_live_visual.py
tools/run_m0001_python_brain_to_mt5.ps1

mql5/Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5
```

## Run once

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_m0001_python_brain_to_mt5.ps1 -Symbol GOLD -Timeframe M15 -Bars 1200 -Once
```

## Run continuously

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_m0001_python_brain_to_mt5.ps1 -Symbol GOLD -Timeframe M15 -Bars 1200 -Interval 2
```

## MT5 expert

Compile and attach:

```text
Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5
```

The expert reloads the CSV contract on a timer:

```text
MQL5/Files/DecisionAlphaLab/M0001/GOLD_M15_visual.csv
```

All manual visual toggles default to `false`. Use `InpViewPreset` to activate one audit package at a time.

## Recommended visual validation order

```text
1  Structural Node Audit
2  Territory Construction Audit
3  Event Entry Exit Audit
4  Baseline vs Inside Sample Audit
5  RTV Formula Audit
6  Hunt Validation Audit
10 Focused Event Inspector
```

## Professional description

```text
M0001 uses a single Python research engine for both validation and live visual inspection. MT5/MQL5 is used as a market-native visualization terminal that consumes deterministic Python-generated visual contracts. This prevents research/live divergence and makes every visual audit traceable to the same tested code path.
```
