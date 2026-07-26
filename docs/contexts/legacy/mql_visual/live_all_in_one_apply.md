# MQL Live Visual Lab — All-in-One Apply

This snapshot is the combined architecture change:

- removes the old React/FastAPI UI stack from the working tree
- keeps the Python research engine
- adds the modular M0001 RTV engine
- keeps the Python-to-MQL CSV exporter for audit/static visualization
- adds the MQL5 static CSV visualizer
- adds the MQL5 live visual tester that computes RTV directly in MT5

## One-shot apply

From the project root:

```powershell
Expand-Archive -Path .\quant_lab_mql_live_all_in_one_snapshot.zip -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File .\tools\apply_mql_live_lab_all_in_one.ps1
```

Then compile in MetaEditor:

```text
Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5
```

## What stays in Python

Python remains the reproducible research engine:

```text
lab/core/CP0001_structural_nodes/metrics/M0001_rtv/
```

It can compute actual L-rule nodes and random baselines with the same metric logic.

## What runs live in MQL

```text
mql5/Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5
```

This expert computes from currently available MT5 bars:

- L-rule nodes
- node confirmation delay
- territories
- events
- RTV
- hunt markers
- currently open event labels

Use `InpUseClosedBarsOnly=true` and `InpUpdateOnEveryTick=false` for live-safe bar-by-bar testing.
