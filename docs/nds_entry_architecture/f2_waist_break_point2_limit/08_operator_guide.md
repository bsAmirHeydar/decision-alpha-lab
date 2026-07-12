# 08 — Operator Guide

## Expert

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
```

## Recommended first run

```text
InpF2BTProfile = FAST
InpF2BTTradeEnabled = true
InpF2BTSendTesterOrders = true
InpF2BTRequireF2SizeGate = false
InpF2BTOneAttemptPerF2Body = true
InpF2BTCancelPendingIfTargetTouchedBeforeFill = true
InpF2BTMaxSetupAgeBars = 0
InpF2BTEntryBehindF2WaistTicks = 1
InpF2BTStopBehindF1WaistTicks = 1
InpF2BTUseMinimumRewardRiskFilter = true
InpF2BTMinimumRewardRisk = 1.0
InpF2BTAllowOppositeDirectionHedge = true
InpF2BTAllowSameDirectionMultipleContexts = true
InpF2BTMaxConcurrentManagedExposures = 0
InpF2BTFixedVolume = 0.01
```

## Interpretation of tester trades

Every submitted trade means:

```text
A complete unconfirmed F2 body existed.
Its waist was Point 1.
The limit beyond that waist represented Point 2.
The parent F1 waist defined failure.
The F2 Leg2 endpoint defined completion/target.
```

## No-log behavior

The expert intentionally emits no custom runtime prints. Use Strategy Tester Orders, Deals, Results and chart visualization for inspection.


## Account mode for hedge and parallel contexts

Use an MT5 hedging account in Strategy Tester when testing simultaneous same-symbol contexts. On netting accounts, the expert intentionally blocks the second exposure.

## RR interpretation

`InpF2BTMinimumRewardRisk = 1.0` means the distance from Entry to Target must be at least equal to the distance from Entry to Stop.
