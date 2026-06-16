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


## MQL input bridge

The MT5 Expert now exposes the Python brain parameters as inputs.  
Changing `InpBrainL`, `InpBrainZoneRatio`, `InpBrainExitGap`, `InpBrainBars`, mode, random baseline settings or symbol/timeframe in MT5 does **not** move the brain to MQL.

Instead, MQL writes those inputs into:

```text
MQL5/Files/DecisionAlphaLab/M0001/m0001_runtime_config.ini
```

The Python watcher reads that file and regenerates the visual CSV with the same Python engine used by tests and research.

Run the watcher:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_m0001_python_brain_to_mt5.ps1 -UseMqlInputs -WaitForMqlInputs
```

This preserves the core rule:

```text
The tested code and the chart-inspected code must be the same Python code.
```

## Event bridge sync mode

The latest mode synchronizes MT5 chart data with the Python brain.

MQL exports chart candles on a new bar or every tick, writes a runtime request, and Python recomputes the visual contract from that exact candle stream.

Run the bridge watcher:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_m0001_python_brain_to_mt5.ps1 -EventBridge -WaitForMqlInputs
```

Recommended non-repainting validation inputs:

```text
InpBridgeExportChartCandles = true
InpBridgeOnEveryTick = false
InpBridgeClosedBarsOnly = true
```

Live/tick visual inspection inputs:

```text
InpBridgeExportChartCandles = true
InpBridgeOnEveryTick = true
InpBridgeClosedBarsOnly = false
```

The MQL expert remains visual-only. The metric computation is still performed by the Python M0001 engine.


## M0001 Parquet Event Bridge

The event bridge now writes authoritative Python artifacts as Parquet:

```text
MQL5/Files/DecisionAlphaLab/M0001/parquet/<symbol>_<timeframe>/
  candles.parquet
  references.parquet
  events.parquet
  visual_rows.parquet
  manifest.parquet
```

MQL5 still reads one thin CSV render adapter because native MQL5 cannot read Parquet without external DLLs.  
The CSV is not the research artifact; it is only the drawing protocol for the visual terminal.

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_m0001_python_brain_to_mt5.ps1 -EventBridge -WaitForMqlInputs
```


## Common Files Sync

The bridge now defaults to MetaQuotes Common Files so MT5, Strategy Tester and Python watch the same directory.

MQL input:

```text
InpUseCommonFiles = true
```

Python watcher:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_m0001_python_brain_to_mt5.ps1 -EventBridge -WaitForMqlInputs
```

Default shared root:

```text
%APPDATA%\MetaQuotes\Terminal\Common\Files
```


## Parquet type safety

The bridge normalizes nullable numeric/boolean fields before writing Parquet.
This prevents pyarrow errors when visual rows contain blank values for fields
that are not applicable to that row type.


## Visual Toggle Sync

Manual layer inputs are only fully manual when `InpViewPreset=0`.  
If a preset is selected, it intentionally turns layers on.

Use these hard controls:

```text
InpRenderVisualObjects = false      # blank chart / cleanup mode
InpForceFlatCustomMode = true       # ignore presets and use only manual toggles
InpCleanAllM0001Objects = true      # delete old objects from previous versions
```


## Node arrow tip anchor

Node arrows are drawn at the exact Python node price.  
The MQL visual terminal sets the glyph anchor so the visible arrow tip, not the
glyph center, lands on the node price.

```text
HIGH node -> down arrow + ANCHOR_BOTTOM
LOW node  -> up arrow   + ANCHOR_TOP
```

Input:

```text
InpAnchorNodeArrowTip = true
```
