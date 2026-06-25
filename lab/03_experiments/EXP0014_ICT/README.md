# EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab

This experiment is a deterministic, bar-based ICT module scaffold for Decision Alpha Lab.

It does **not** run on every tick. The default expert runs once on init, scans historical bars, writes CSV journals, and removes itself.

## Core modules

### 1. L-node sweep

Source: `mql5/Include/ICT/DAL_ICTSweepDetector.mqh`

Uses the existing DAL structural node engine:

- `DAL_DetectConfirmedStructuralNodes`
- L-rule confirmed highs/lows
- active-from index/time is respected to avoid future leakage

A high node sweep creates a bearish setup context. A low node sweep creates a bullish setup context.

Modes:

- `ICT_SWEEP_TOUCH`: price reaches the configured node zone touch depth.
- `ICT_SWEEP_HUNT`: price pierces the node zone and closes back through the node level.

Zone model:

- node zone = `[node_price - zone_half_width, node_price + zone_half_width]`
- touch percent decides how deep into the zone price must travel.

### 2. FVG / IFVG

Source: `mql5/Include/ICT/DAL_ICTFVGDetector.mqh`

FVG rules:

- Bullish FVG: `bar[i-2].high < bar[i].low`
- Bearish FVG: `bar[i-2].low > bar[i].high`

IFVG rules:

- After a high sweep, the model looks for a bullish FVG in the pre-sweep displacement path, then waits for price to re-enter the gap and close below the lower edge.
- After a low sweep, the model looks for a bearish FVG in the pre-sweep displacement path, then waits for price to re-enter the gap and close above the upper edge.

### 3. CISD

Source: `mql5/Include/ICT/DAL_ICTCISDDetector.mqh`

CISD is represented as a close through the open of the last displacement leg:

- High sweep -> bearish setup: close below the open of the last bullish/up leg.
- Low sweep -> bullish setup: close above the open of the last bearish/down leg.

### 4. Execution model

Source: `mql5/Include/ICT/DAL_ICTExecutionModel.mqh`

Sequence:

1. Detect L-node sweep on the signal timeframe.
2. Find the FVG in the path that produced the sweep.
3. Wait for IFVG confirmation.
4. Wait for CISD confirmation.
5. Enter at CISD close as market-entry proxy.
6. Stop goes beyond the sweep extreme plus buffer.
7. Target goes to the next opposite structural node using touch/hunt mode.
8. Only keep signals with `RR >= InpMinRR`.
9. Resolve exit by TP, SL, optional next sweep, or CSV end.

## Default expert

`mql5/Experts/ICT/ICT001_SweepIFVGCISDExecutor.mq5`

Default timeframe is `PERIOD_M10`.

Important inputs:

- `InpSignalTimeframe = PERIOD_M10`
- `InpL = 3`
- `InpSweepMode = ICT_SWEEP_HUNT`
- `InpTargetMode = ICT_TARGET_TOUCH`
- `InpNodeZoneHalfWidthPoints = 20.0`
- `InpSweepZoneTouchPct = 50.0`
- `InpTargetZoneTouchPct = 50.0`
- `InpFvgMinGapPoints = 1.0`
- `InpFvgTouchPctForIFVG = 50.0`
- `InpMinRR = 2.0`
- `InpRunOnceOnInit = true`

## Output

Default output folder:

`MetaQuotes/Terminal/Common/Files/ict/EXP0014/`

Files:

- `ict001_entry_signals.csv`
- `ict001_summary.csv`

The entry CSV is Excel-ready and includes:

- sweep validity window
- next sweep window boundary
- entry time
- SL / TP / RR
- FVG / IFVG / CISD timestamps
- target node
- exit time and exit reason
- realized R

## Research warning

This is a first deterministic version of the ICT hypotheses. It is designed to audit the sequence and produce reproducible event journals, not to claim profitability.
