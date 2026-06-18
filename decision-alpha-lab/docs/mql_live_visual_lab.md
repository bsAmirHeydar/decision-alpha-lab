# MQL5 Visual Lab: Python Brain, MT5 Eyes

MQL5 is now a visual-only layer.

The metric brain is Python:

```text
lab/core/CP0001_structural_nodes/metrics/M0001_rtv/engine.py
```

The MT5 expert reads the Python-generated CSV visual contract:

```text
MQL5/Files/DecisionAlphaLab/M0001/GOLD_M15_visual.csv
```

and draws it on the chart.

## Main expert

```text
mql5/Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5
```

Despite the name `LiveVisualLab`, the expert does not compute live logic. It reloads the Python visual contract on a timer and redraws it. This keeps research, tests, backtest artifacts and live visual inspection on one code path.

## Run Python brain once

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_m0001_python_brain_to_mt5.ps1 -Symbol GOLD -Timeframe M15 -Bars 1200 -Once
```

## Run Python brain continuously

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_m0001_python_brain_to_mt5.ps1 -Symbol GOLD -Timeframe M15 -Bars 1200 -Interval 2
```

## Compile and attach MQL

Compile:

```text
Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5
```

Attach it to the same symbol/timeframe chart and set:

```text
InpFileName = DecisionAlphaLab\M0001\GOLD_M15_visual.csv
InpAutoReloadSeconds = 2
InpViewPreset = 10
```

All manual visual toggles are false by default. Use presets or turn on layers one by one.

## Read more

```text
docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md
docs/mql_live_visual_lab_debug_packages.md
```
