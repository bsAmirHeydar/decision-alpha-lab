# M0007 — Adaptive F1 Flag Counting MQL5 Implementation

## Correct project layout

The module is placed using the clean M-series folder convention:

```text
mql5/Experts/M0007/M0007_FlagCountingF1.mq5
mql5/Include/M0007/DAL_M0007F1Types.mqh
mql5/Include/M0007/DAL_M0007F1NodeDetector.mqh
mql5/Include/M0007/DAL_M0007F1Detector.mqh
mql5/Include/M0007/DAL_M0007F1Renderer.mqh
```

No folder repeats the project name. The project root already carries that identity.

## Naming lock

This is an MQL module, so its runtime/module name is `M0007`. Code, EA file names, include names, object prefixes, print tags, and module folders all use `M0007`.

## F1 rules implemented

Bullish sequence:

```text
H1 -> W -> H2 -> N1 -> R12 -> N2
```

Rules:

- `H2 > H1`
- `N2 < N1`
- `N2 > W`
- `R12 < H2`
- break of `R12` arms the structure
- break of `H2` confirms the structure
- break of `W` before confirmation invalidates the structure

Bearish sequence:

```text
L1 -> W -> L2 -> N1 -> R12 -> N2
```

Rules:

- `L2 < L1`
- `N2 > N1`
- `N2 < W`
- `R12 > L2`
- break of `R12` arms the structure
- break of `L2` confirms the structure
- break of `W` before confirmation invalidates the structure

## Adaptive L

The detector scans a range of L values and merges overlapping representations. Each event stores:

- `L_used`
- `matched_L_values`

This keeps counting adaptive while still deterministic.

## Scope

The Expert Advisor is for chart audit only. It does not send orders and does not define execution logic.
