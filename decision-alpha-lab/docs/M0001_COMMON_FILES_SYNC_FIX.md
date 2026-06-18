# M0001 Common Files Sync Fix

## Problem

When the Expert is attached in MT5, MQL can write files into a different sandbox than the Python watcher is reading from, especially in Strategy Tester / Visual Mode.

Typical symptom:

```text
Python waits for:
MQL5\Files\DecisionAlphaLab\M0001\m0001_runtime_config.ini

MQL chart says:
Waiting for Python visual contract
```

The EA may actually be writing into tester/local file storage, not the same folder watched by Python.

## Fix

Use MetaQuotes Common Files as the bridge root.

MQL input:

```text
InpUseCommonFiles = true
```

Python watcher default:

```powershell
-UseCommonFiles $true
```

Shared root:

```text
%APPDATA%\MetaQuotes\Terminal\Common\Files
```

Bridge files:

```text
%APPDATA%\MetaQuotes\Terminal\Common\Files\DecisionAlphaLab\M0001\
  m0001_runtime_config.ini
  GOLD_M1_candles.csv
  GOLD_M1_visual.csv
  GOLD_M1_status.ini
  parquet\GOLD_M1\
    candles.parquet
    references.parquet
    events.parquet
    visual_rows.parquet
    manifest.parquet
```

## Run

Attach and compile:

```text
Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5
```

Set:

```text
InpUseCommonFiles = true
InpBridgeExportChartCandles = true
InpAutoBuildFileName = true
InpWritePythonConfig = true
```

Run Python:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_m0001_python_brain_to_mt5.ps1 -EventBridge -WaitForMqlInputs
```

The PowerShell output should now watch:

```text
...\MetaQuotes\Terminal\Common\Files\DecisionAlphaLab\M0001\m0001_runtime_config.ini
```
