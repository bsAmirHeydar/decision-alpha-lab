# D0006 — H5 Live Touch Replay Audit

D0006 is the strict live-validity audit for H0005 reversal touch-entry logic.

It exists because full-history H5 reports can be useful for discovery, but they are not enough to prove live validity. A live-valid H5 test must separate three times:

1. the time the regime and zones are known,
2. the later time price actually touches the zone and fills the entry,
3. the future path used only for measurement after fill.

## Contract

D0006 enforces this contract:

```text
Decision = prefix-only bars up to the simulated cursor candle
Regime = latest M0002 branch available inside that prefix only
Nodes = confirmed and active M0001 nodes available inside that prefix only
Entry = future zone touch after activation, not candle close
Measurement = only after touch/fill
```

The audit is deliberately separate from E0001–E0005. It is a validator, not an executor.

## Reversal touch model

When the latest prefix-only M0002 regime is reversal, D0006 activates live candidates:

```text
LOW node below market  -> BUY touch candidate
HIGH node above market -> SELL touch candidate
```

The entry is not assumed at the signal candle. The candidate must be touched later:

```text
BUY fills when a later candle touches the LOW-node zone
SELL fills when a later candle touches the HIGH-node zone
```

Only after that fill does D0006 measure MFE, MAE, reward hit, stop hit, same-bar ambiguity, and realized R.

## Key summary fields

```text
passLiveDecisionContract
futureNodeViolations
candidateActivations
touchEntries
fillRatePct
rewardHitPct
stopHitPct
sameBarRewardStop
avgMfeR
avgMaeR
expectancyR
profitFactor
```

The critical field is:

```text
futureNodeViolations = 0
```

If this is not zero, H5 is still using something that should not be available at decision time.

## CSV

The default CSV is written to `MQL5/Files`:

```text
D0006_H5_Live_Touch_Replay.csv
```

Each row is one live candidate activation and its later touch/outcome measurement.

## Scientific meaning

The older full-history H5 reports should be treated as exploratory. D0006 is the stricter validation layer. H5 should only be trusted for live execution when D0006 shows that the edge survives prefix-only decision making and touch-entry measurement.
