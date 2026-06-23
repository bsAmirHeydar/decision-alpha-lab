# H0007 — F1 Adaptive Flag Counting / Native MQL5 Implementation

This is the MQL5-native implementation of the H0007 F1 grammar.

No Python module is required.

## Correct project location

The implementation belongs under the actual project MQL5 tree:

`mql5/Experts/DecisionAlphaLab/`

The main Expert Advisor is:

`mql5/Experts/DecisionAlphaLab/H0007_F1_Adaptive_Draw.mq5`

The include files are intentionally kept in the same folder:

- `mql5/Experts/DecisionAlphaLab/H0007_F1_Types.mqh`
- `mql5/Experts/DecisionAlphaLab/H0007_F1_NodeDetector.mqh`
- `mql5/Experts/DecisionAlphaLab/H0007_F1_Detector.mqh`
- `mql5/Experts/DecisionAlphaLab/H0007_F1_Renderer.mqh`

This matches the existing DecisionAlphaLab MQL5 layout and keeps H0007 beside the other MQL execution modules.

---

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

---

## Adaptive L

The detector does not use one fixed `L`.

It scans from `InpLMin` to `InpLMax`, detects valid F1 structures on every local scale, merges overlapping candidates, and records:

- `L_used`: the selected local scale
- `matched_L_values`: all L values that produced overlapping versions of the same event

---

## How to use

Open and compile:

`mql5/Experts/DecisionAlphaLab/H0007_F1_Adaptive_Draw.mq5`

Attach the Expert Advisor to a chart.

The EA draws:

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

---

## Expert behavior

The EA draws once on `OnInit()`.

Optional live redraw can be enabled with:

`InpRedrawOnNewBar = true`

No trades are sent.

No orders are created.

This is a visual audit EA only.

---

## Scope

This is still topology-only.

It does not define entry, stop, target, position sizing, expectancy, or live trading behavior.
