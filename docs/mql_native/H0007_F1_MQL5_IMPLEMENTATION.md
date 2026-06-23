# H0007 — F1 Adaptive Flag Counting / MQL5 Implementation

This is the MQL5-native implementation of the H0007 F1 grammar.

No Python module is required for this version.

## Core grammar

### Bullish F1

`H1 -> W -> H2 -> N1 -> R12 -> N2`

Rules:

- `H2 > H1`
- `N2 < N1`
- `N2 > W`
- `R12 < H2`
- breaking `R12` only arms the structure
- breaking `H2` confirms F1
- breaking `W` before confirmation invalidates F1

### Bearish F1

`L1 -> W -> L2 -> N1 -> R12 -> N2`

Rules:

- `L2 < L1`
- `N2 > N1`
- `N2 < W`
- `R12 > L2`
- breaking `R12` only arms the structure
- breaking `L2` confirms F1
- breaking `W` before confirmation invalidates F1

## Adaptive L

The detector does not use one fixed L.

It scans from `InpLMin` to `InpLMax`, detects valid F1 structures on every local scale, merges overlapping candidates, and records:

- `L_used`: the selected local scale
- `matched_L_values`: all L values that produced overlapping versions of the same event

## MQL5 files

- `H0007_F1_Adaptive_Draw.mq5`
- `Include/H0007_F1_Types.mqh`
- `Include/H0007_F1_NodeDetector.mqh`
- `Include/H0007_F1_Detector.mqh`
- `Include/H0007_F1_Renderer.mqh`

## How to use

Copy the folder:

`lab/09_execution/mql5/H0007_FlagCountingF1`

into the MT5 Scripts folder, or keep the same folder structure under `MQL5/Scripts`.

Compile:

`H0007_F1_Adaptive_Draw.mq5`

Run it on a chart.

The script draws:

- H1 / L1
- W
- H2 / L2
- N1
- R12
- N2
- protected waist line
- internal trigger line
- final confirmation line
- trigger bar
- confirmation bar
- invalidation bar if present

## Important implementation rule

Same-bar ambiguity is treated conservatively.

If a bar both violates the waist and reaches the trigger/confirmation side, the waist violation wins before confirmation.

## Scope

This is still topology-only.

It does not define entry, stop, target, position sizing, expectancy, or live trading behavior.
