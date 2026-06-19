# M0001 Python Brain / MQL Input Bridge

## Purpose

M0001 must have one metric brain.

Python is the only source of truth for:

- L-rule reference extraction
- reference point normalization
- territory construction
- entry/exit state machine
- before/inside samples
- RTV calculation
- hunt detection
- random baseline generation
- visual contract generation

MQL5 is a visual terminal only.

The practical issue is that parameter changes must still feel native inside MT5.  
This bridge solves that without duplicating the brain.

## Architecture

```text
MT5 Expert Inputs
        ↓
MQL writes runtime config
        ↓
MQL5/Files/DecisionAlphaLab/M0001/m0001_runtime_config.ini
        ↓
Python watcher reads config
        ↓
Python single-source M0001 engine recomputes visual contract
        ↓
MQL5/Files/DecisionAlphaLab/M0001/<symbol>_<timeframe>_visual.csv
        ↓
MQL redraws chart objects
```

The code being tested is the code producing the chart output.  
MQL does not recompute the metric.

## Important MQL inputs

### Python brain parameters

```text
InpBrainSymbol
InpBrainTimeframe
InpBrainBars
InpBrainL
InpBrainZoneRatio
InpBrainExitGap
InpBrainConsumeOnTouch
InpBrainRandom
InpBrainRandomCount
InpBrainRandomSeed
InpBrainRefreshMs
```

### Bridge controls

```text
InpAutoBuildFileName
InpPythonConfigFile
InpWritePythonConfig
InpAutoReloadSeconds
```

Recommended defaults:

```text
InpAutoBuildFileName = true
InpWritePythonConfig = true
InpPythonConfigFile = DecisionAlphaLab\M0001\m0001_runtime_config.ini
InpAutoReloadSeconds = 2
```

## How to run

1. Attach `M0001_LiveVisualLab.mq5` to an MT5 chart.
2. Set the Python brain parameters inside the Expert inputs.
3. Start the Python watcher:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\run_m0001_python_brain_to_mt5.ps1 -UseMqlInputs -WaitForMqlInputs
```

4. Whenever you change inputs in MT5 and press OK:
   - MQL writes a new config file.
   - Python reads it on the next cycle.
   - Python recomputes the CSV with the same research engine.
   - MQL reloads and redraws.

## Why this is strict

This design intentionally avoids two independent implementations.

Bad architecture:

```text
Python backtest logic
MQL live logic
```

That creates silent drift.

Target architecture:

```text
One Python engine
Many consumers
```

MQL is one consumer.  
Reports, tests, random baselines, validation journals and MT5 visuals all consume the same Python output.

## Validation mindset

A screenshot is not proof by itself.

A valid M0001 visual test should include:

```text
symbol
timeframe
bars
L
zone_ratio
exit_gap
mode
random seed if used
view preset
focus node id
focus revisit id
expected behavior
observed behavior
pass/fail
```

This makes the visual journal reproducible.
