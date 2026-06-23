# H0007_FlagCountingF1 — MQL5 Native

This folder contains the MQL5-native implementation of H0007 F1 adaptive flag counting.

## Entry file

Compile and run:

`H0007_F1_Adaptive_Draw.mq5`

## Includes

- `Include/H0007_F1_Types.mqh`
- `Include/H0007_F1_NodeDetector.mqh`
- `Include/H0007_F1_Detector.mqh`
- `Include/H0007_F1_Renderer.mqh`

## Inputs

- `InpBarsToScan`
- `InpLMin`
- `InpLMax`
- `InpBreakMode`
- `InpEpsilonPoints`
- `InpOverlapThreshold`
- `InpMaxEventsToDraw`
- `InpDrawOnlyConfirmed`
- `InpObjectPrefix`

## Logic

Bullish F1:

`H1 -> W -> H2 -> N1 -> R12 -> N2`

Bearish F1:

`L1 -> W -> L2 -> N1 -> R12 -> N2`

The detector is adaptive across L, not fixed to one L.
