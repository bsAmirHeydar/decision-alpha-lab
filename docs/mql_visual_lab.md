# MQL5 Visual Lab Architecture

The React/FastAPI UI has been removed. The project now uses a cleaner split:

```text
Python = deterministic research and metric engine
MQL5   = market-native visual terminal on the MT5 chart
```

## Core idea

M0001 is computed in Python from the same live-style candle-by-candle engine for:

- actual L-rule structural nodes
- random baseline reference points

Python exports a simple CSV visual contract. MQL5 reads the CSV and draws objects directly on the MT5 chart.

## Main files

```text
lab/core/CP0001_structural_nodes/metrics/M0001_rtv/
  schemas.py             # config, reference points, event schema
  math_utils.py          # log_move, territory, hunt logic
  reference_points.py    # L-rule refs and random refs
  engine.py              # single M0001 RTV state machine
  mql_visual_contract.py # CSV rows for MT5 drawing

tools/export_m0001_to_mql.py
  Exports visual CSV files for MQL5.

mql5/Experts/DecisionAlphaLab/M0001_VisualLab.mq5
  MT5 expert that reads the CSV and draws nodes, territories, events, RTV labels and hunt markers.
```

## Export example

From the project root:

```powershell
py tools/export_m0001_to_mql.py --symbol GOLD --timeframe M15 --bars 5000 --L 5 --zone-ratio 0.9 --exit-gap 6 --mode hunt
```

With random baseline:

```powershell
py tools/export_m0001_to_mql.py --symbol GOLD --timeframe M15 --bars 5000 --L 5 --zone-ratio 0.9 --exit-gap 6 --mode hunt --random --seed 42
```

Default output:

```text
mql5/Files/DecisionAlphaLab/M0001/GOLD_M15_visual.csv
```

Copy that CSV to your real terminal data folder:

```text
<MQL5 Terminal>/MQL5/Files/DecisionAlphaLab/M0001/GOLD_M15_visual.csv
```

Copy the expert:

```text
mql5/Experts/DecisionAlphaLab/M0001_VisualLab.mq5
```

to:

```text
<MQL5 Terminal>/MQL5/Experts/DecisionAlphaLab/M0001_VisualLab.mq5
```

Then compile it in MetaEditor and attach it to the same symbol/timeframe chart.

## Visual layers

The MQL expert has inputs for toggling:

```text
Actual
Random
Nodes
Territories
Events
RTV labels
Hunts
```

## Why this is cleaner

The research truth stays in Python, where it is testable and reproducible.
The visual inspection happens in MT5/MQL5, where the chart, market context and execution feeling are native.


## Live visual testing mode

A second expert exists for live / Strategy Tester style inspection:

```text
mql5/Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5
```

This expert does not read the Python CSV. It computes L-rule nodes and M0001 RTV directly from the currently available MT5 bars, updating on new closed bars.

Read:

```text
docs/mql_live_visual_lab.md
```
