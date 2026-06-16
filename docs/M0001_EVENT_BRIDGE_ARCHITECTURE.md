# M0001 Event Bridge Architecture

## Goal

M0001 must be live-like without creating two brains.

The tested implementation, the research implementation, and the chart-inspected implementation must be the same Python code.

## Architecture

```text
MT5 chart / Strategy Tester tick or new bar
        ↓
MQL exports the currently visible/available candle stream
        ↓
MQL5/Files/DecisionAlphaLab/M0001/<symbol>_<timeframe>_candles.csv
        ↓
MQL writes runtime request/config
        ↓
MQL5/Files/DecisionAlphaLab/M0001/m0001_runtime_config.ini
        ↓
Python watcher reads the request and candle stream
        ↓
Python single-source M0001 engine computes nodes/events/RTV/hunts
        ↓
Python writes visual contract
        ↓
MQL5/Files/DecisionAlphaLab/M0001/<symbol>_<timeframe>_visual.csv
        ↓
MQL redraws chart objects and later can execute actions
```

MQL is not allowed to compute M0001. It only:

- exports market candles observed by MT5;
- writes input parameters;
- draws Python output;
- can later execute orders from Python decisions.

## Why this is different from the old bridge

The previous bridge only let MQL write parameters. Python still read cached candles. That was useful for research, but it did not feel synchronized with the visual chart.

The event bridge uses the chart as the market-data trigger. When a new candle arrives, or optionally every tick, MQL sends the current candle stream to Python.

## Important MQL inputs

```text
InpBridgeExportChartCandles = true
InpBridgeOnEveryTick = false
InpBridgeClosedBarsOnly = true
InpBridgeLookbackBars = 0
InpBridgeCandlesFile = ""
InpBridgeStatusFile = ""
InpShowBridgeStatusPanel = true
```

Recommended research mode:

```text
InpBridgeExportChartCandles = true
InpBridgeOnEveryTick = false
InpBridgeClosedBarsOnly = true
```

This is live-safe because the forming candle is excluded.

Tick-inspection mode:

```text
InpBridgeOnEveryTick = true
InpBridgeClosedBarsOnly = false
```

This updates faster, but the current candle can change. Use it for visual inspection, not final non-repainting validation.

## Python watcher

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_m0001_python_brain_to_mt5.ps1 -EventBridge -WaitForMqlInputs
```

The watcher reads the MQL config, then reads the candle CSV produced by MQL.

## Sync files

Default files:

```text
MQL5/Files/DecisionAlphaLab/M0001/m0001_runtime_config.ini
MQL5/Files/DecisionAlphaLab/M0001/GOLD_M1_candles.csv
MQL5/Files/DecisionAlphaLab/M0001/GOLD_M1_visual.csv
MQL5/Files/DecisionAlphaLab/M0001/GOLD_M1_status.ini
```

If MT5 says it cannot open the visual file, it means Python has not produced that exact file yet. Start the watcher and check the status panel.

## Validation rule

A visual screenshot is valid only if it includes the runtime config:

```text
symbol
timeframe
bars
L
zone_ratio
exit_gap
mode
closed_bars_only
trigger
request_id
```

This lets the visual journal reproduce the exact Python computation shown on the chart.
