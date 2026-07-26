# H0007 / M0007 — F1 Adaptive Flag Counting MQL5 Implementation

## Correct folder structure

The implementation follows the DecisionAlphaLab MQL5 layout:

```text
mql5/Experts/DecisionAlphaLab/DAL_M0007_H0007_F1_Adaptive_Draw.mq5
mql5/Include/DecisionAlphaLab/H0007_FlagCountingF1/H0007_F1_Types.mqh
mql5/Include/DecisionAlphaLab/H0007_FlagCountingF1/H0007_F1_NodeDetector.mqh
mql5/Include/DecisionAlphaLab/H0007_FlagCountingF1/H0007_F1_Detector.mqh
mql5/Include/DecisionAlphaLab/H0007_FlagCountingF1/H0007_F1_Renderer.mqh
```

The EA file stays inside `mql5/Experts/DecisionAlphaLab`.

The reusable `.mqh` files stay inside `mql5/Include/DecisionAlphaLab/H0007_FlagCountingF1`.

## Design

The module is a native MQL5 visual audit implementation of H0007 F1.

It performs:

- adaptive L scanning,
- L-rule node extraction,
- bullish and bearish F1 topology detection,
- protected waist invalidation,
- R12 internal trigger detection,
- H2/L2 final confirmation detection,
- overlap merge between candidate structures,
- chart drawing of the complete F1 count.

## No trading execution

This is not a trading robot.

It does not call `OrderSend`, does not place pending orders, does not open positions, and does not define risk logic.

Its only purpose is to make F1 mechanically countable and visually auditable before F2 is defined.
