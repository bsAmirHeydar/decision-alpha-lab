# VAL0006 — H5 live-valid touch-entry replay

Purpose: validate H0005 without future leakage using a live-like candle-by-candle replay.

Core rule:

```text
At each simulated candle, H5 may only use bars, nodes, events, and regime state available up to that candle.
The entry is not the signal close. The entry happens only if price later touches the activated structural zone.
Only after that touch/fill can MFE, MAE, R, and outcome be measured.
```

Run:

```text
Experts/DecisionAlphaLab/Debug/D0006_H5LiveTouchReplayAudit.mq5
```

Recommended first inputs:

```text
InpReplayClosedBars = 2000
InpWarmupClosedBars = 300
InpBuySlots = 3
InpSellSlots = 3
InpMaxBarsToWaitForTouch = 300
InpMaxBarsToMeasureAfterTouch = 300
InpRewardRForFirstHit = 1.0
InpWriteCsv = true
```

Accept/reject rule:

```text
futureNodeViolations must be 0.
Then compare expectancyR, avgMfeR, avgMaeR, rewardHitPct, stopHitPct, and fillRatePct against older full-history H5 reports.
```
