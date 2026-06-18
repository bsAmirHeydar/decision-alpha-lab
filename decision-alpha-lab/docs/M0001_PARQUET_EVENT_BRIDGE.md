# M0001 Parquet Event Bridge

## Why

The M0001 research brain must stay in Python, and all durable research artifacts should be stored as Parquet.

MQL5 cannot read or write Parquet natively without external DLLs.  
Therefore the architecture is:

```text
MQL5 chart candles
  -> MQL exports a small native candle adapter file
  -> Python reads it
  -> Python writes authoritative Parquet artifacts
  -> Python writes one thin CSV render adapter for MQL
  -> MQL draws the chart
```

The CSV render adapter is not the research artifact.  
It exists only because MQL can read simple text files natively.

## Authoritative Parquet artifacts

Python writes these on every bridge cycle:

```text
MQL5/Files/DecisionAlphaLab/M0001/parquet/<symbol>_<timeframe>/
  candles.parquet
  references.parquet
  events.parquet
  visual_rows.parquet
  manifest.parquet
```

These are the files to use for:

- research replay
- validation journal
- Python/MQL visual audit
- reproducibility
- future reports
- strategy decision logs

## MQL render adapter

MQL still consumes:

```text
MQL5/Files/DecisionAlphaLab/M0001/<symbol>_<timeframe>_visual.csv
```

This file is only a drawing contract.  
It should not be used as the source of truth.

## Run

Attach the Expert:

```text
Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5
```

Recommended MQL inputs:

```text
InpBridgeExportChartCandles = true
InpBridgeClosedBarsOnly = true
InpBridgeOnEveryTick = false
InpAutoBuildFileName = true
InpShowBridgeStatusPanel = true
InpBrainBars = 800
InpBrainL = 5
InpBrainZoneRatio = 0.90
InpBrainExitGap = 6
InpBrainConsumeOnTouch = false
```

Then run the Python watcher:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_m0001_python_brain_to_mt5.ps1 -EventBridge -WaitForMqlInputs
```

## Status

The status panel shows:

```text
status=ok
artifact_format=parquet
mql_visual_adapter=csv
candles_parquet=...
events_parquet=...
visual_rows_parquet=...
mql_adapter=...
```

If the chart says it is waiting for the Python visual contract, the watcher is not running or has not produced the adapter file yet. Check the PowerShell output and the status file.
