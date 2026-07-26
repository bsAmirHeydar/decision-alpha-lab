# 08 — Operator Guide

## Expert

```text
mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5
Version 2.00
```

## Recommended first run

```text
InpF2BTProfile = FAST
InpF2BTTradeEnabled = true
InpF2BTSendTesterOrders = true

InpF2BTRequireF2SizeGate = false
InpF2BTOneAttemptPerF2Body = true
InpF2BTConsumeAttemptOnlyOnFill = true
InpF2BTMaxSetupAgeBars = -1
InpF2BTCancelPendingIfTargetTouchedBeforeFill = true

InpF2BTEntryBehindF2WaistTicks = 1
InpF2BTStopBehindF1WaistTicks = 1

InpF2BTUseMinimumRewardRiskFilter = true
InpF2BTAdjustEntryToMinimumRewardRisk = true
InpF2BTMinimumRewardRisk = 1.0

InpF2BTUseStopSpaceOverlapDeduplication = true
InpF2BTStopSpaceOverlapThresholdPercent = 80.0

InpF2BTAllowOppositeDirectionHedge = true
InpF2BTAllowSameDirectionMultipleContexts = true
InpF2BTRequireHedgingAccountForParallelContexts = true
InpF2BTMaxConcurrentManagedExposures = 0

InpF2BTUseHigherTimeframeFPhaseFilter = true
InpF2BTHigherTimeframe = PERIOD_H1
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true
InpF2BTCancelPendingWhenHigherTimeframeDisallows = true

InpF2BTExitMode = FP_NDS_F2_EXIT_FIXED_F2_FLAG_END
InpF2BTRequireCanonicalF3SpawnForLocalExit = true
InpF2BTF3ExitHigherTimeframe = PERIOD_H1
InpF2BTF3ExitCorrectionTicks = 1.0
InpF2BTCloseAtMarketIfF3TargetAlreadyReached = true

InpF2BTEnableFunnelDiagnostics = false
InpF2BTFixedVolume = 0.01
```

Use `Every tick based on real ticks` for final execution validation.

## What each order proves

```text
complete unconfirmed F2 body existed
F2 Waist was Point 1
limit beyond Waist represented executable Point 2
confirmed direct-parent F1 Waist defined failure
original F2 Leg2 defined fixed TP and RR reference
HTF had one sole qualifying direction
when enabled, at least one same-direction HTF count was after F1 confirmation and before exact child F2 confirmation
```

## Frequency-corrected lifecycle

`InpF2BTMaxSetupAgeBars = -1` removes the old one-bar-only eligibility. The EA still refuses a missed trade: if Entry or Target has already been touched since the F2 became observable, it does not place a late order.

`InpF2BTConsumeAttemptOnlyOnFill = true` means a pending cancelled before fill does not permanently burn the F2 context.

## FAST and PARITY

```text
FAST   = 800 closed bars, L 2/3/5/8
PARITY = 2500 closed bars, L 2/3/5/8/13/21
```

Use FAST for iteration and PARITY for final structure-frequency comparison.

## HTF interpretation

The default H1 filter evaluates all canonical H1 counts. An unrelated Hook cannot veto another count. A newer count before F1 confirmation cannot hide a different open F1→F2 window.

```text
bullish qualifying counts only → Buy
bearish qualifying counts only → Sell
both directions qualify → block as ambiguous
no qualifying count → block
```

## Account mode

Parallel same-symbol and hedge tests require a hedging account. With the default fail-fast switch, a netting account does not initialize.

## Exit modes

- `FP_NDS_F2_EXIT_FIXED_F2_FLAG_END`: broker TP at original F2 Leg2.
- `FP_NDS_F2_EXIT_F3_FLAG_RETEST`: exact local direct-child F3, isolated per source F2 and position ticket. With `InpF2BTRequireCanonicalF3SpawnForLocalExit = true`, only source F2 bodies with canonical F3-spawn authority may enter under this mode.
- `FP_NDS_F2_EXIT_HIGHER_TIMEFRAME_F3_FLAG_RETEST`: exact per-position HTF F3 Leg1 retest after the same F3 forms its Waist.

Every mode preserves original F2 Leg2 as RR reference.

## Diagnostics

The EA emits no custom runtime prints. Optional funnel diagnostics are default-off:

```text
InpF2BTEnableFunnelDiagnostics = true
```

When enabled, one CSV row is written on deinitialization under MT5 Common Files. It is intended only for identifying the dominant rejection gate and adds no per-tick or per-bar print path.
