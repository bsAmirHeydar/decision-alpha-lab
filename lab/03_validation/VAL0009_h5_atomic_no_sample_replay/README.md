# VAL0009 — H5 Atomic No-Sample Replay

Purpose: validate H5 without building branch samples first.

This validator answers the user's core requirement:

```text
Do not first build a full sample universe.
Replay candle by candle.
At each candle, use only raw M0001 events that are knowable at that candle.
Then activate candidates and measure only after the entry trigger.
```

Use `D0009_H5AtomicNoSampleReplayAudit.mq5` in MetaEditor.

Recommended first run:

```text
InpReplayClosedBars = 1500
InpWarmupClosedBars = 300
InpFamiliesToAudit = DAL_D0009_BOTH
InpContinuationRiskMode = DAL_D0009_CONT_RISK_ATR
InpAtrPeriod = 14
InpAtrMultiplier = 4.0
InpRewardR = 1.0
InpSkipAmbiguousEnergyBatch = true
InpWriteCsv = true
```

The CSV output is `D0009_H5_Atomic_NoSample_Replay.csv`.
