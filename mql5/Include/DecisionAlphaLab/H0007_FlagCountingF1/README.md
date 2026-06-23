# H0007 / M0007 — F1 Flag Counting Include Module

This folder contains the reusable MQL5 include layer for H0007 F1 adaptive flag counting.

## Correct project layout

Expert Advisor:

```text
mql5/Experts/DecisionAlphaLab/DAL_M0007_H0007_F1_Adaptive_Draw.mq5
```

Include files:

```text
mql5/Include/DecisionAlphaLab/H0007_FlagCountingF1/H0007_F1_Types.mqh
mql5/Include/DecisionAlphaLab/H0007_FlagCountingF1/H0007_F1_NodeDetector.mqh
mql5/Include/DecisionAlphaLab/H0007_FlagCountingF1/H0007_F1_Detector.mqh
mql5/Include/DecisionAlphaLab/H0007_FlagCountingF1/H0007_F1_Renderer.mqh
```

## Include contract

The EA includes the module using standard MQL5 include-root paths:

```mql5
#include <DecisionAlphaLab/H0007_FlagCountingF1/H0007_F1_Types.mqh>
#include <DecisionAlphaLab/H0007_FlagCountingF1/H0007_F1_Detector.mqh>
#include <DecisionAlphaLab/H0007_FlagCountingF1/H0007_F1_Renderer.mqh>
```

## Logic lock

Bullish F1:

```text
H1 -> W -> H2 -> N1 -> R12 -> N2
H2 > H1
N2 < N1
N2 > W
R12 < H2
break(R12) = internal trigger
break(H2) = final confirmation
break(W) before confirmation = invalidation
```

Bearish F1:

```text
L1 -> W -> L2 -> N1 -> R12 -> N2
L2 < L1
N2 > N1
N2 < W
R12 > L2
break(R12) = internal trigger
break(L2) = final confirmation
break(W) before confirmation = invalidation
```

## Scope

This module is visual/audit-only. It does not send orders and does not define execution logic.
