# M0002 — Hunt vs Reject Post-Exit Volatility

M0002 is the second hypothesis module in the MQL-native Decision Alpha Lab.
It reuses the M0001 structural-node/event engine, but it has its own Expert Advisor and its own report module.

## Purpose

M0001 established that confirmed structural node territories produce higher future volatility expansion than matched random windows.
M0002 asks a second question:

> After a confirmed territory exit, is the later volatility concentrated more in the branch that eventually hunts the node, or in the branch that rejects away from the node?

The hypothesis is not directional PnL yet. It is a branch-level volatility concentration test.

## Folder layout

```text
mql5/Experts/DecisionAlphaLab/M0002/M0002_HuntRejectExitVolatility.mq5
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Types.mqh
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Engine.mqh
mql5/Include/DecisionAlphaLab/M0002/DAL_M0002Reports.mqh
```

M0002 deliberately imports and reuses the M0001 modules:

```text
M0001Config
M0001Engine
M0001Types
M0001RtvNullComparison
StructuralNodes
Market bars / live stream
```

This keeps the node definition, territory formula, touch/exit/hunt semantics, warmup behavior, and random/null metric machinery consistent with M0001.

## Base event source

M0002 first builds the same M0001 event set:

```text
structural nodes
active_from = node_index + L
territory from node_price and tracking extreme
touch event
strict exit_gap confirmation
M0001 HUNT / TOUCH semantics
```

Then M0002 only consumes confirmed post-exit events:

```text
event.closed == true
event.touch_confirmed == true
event.entry_time >= analysis_start
```

Warmup bars are still used only to seed old structural node memory. Warmup events are excluded from M0002 statistics by analysis_start.

## Branch definition

For each confirmed M0001 exit event:

```text
exit_index = event.exit_index
scan bars after exit_index for up to InpOutcomeLookaheadBars
```

If the node price is hunted inside the lookahead window:

```text
LOW node:  bar.low  < node_price
HIGH node: bar.high > node_price
```

then the sample is classified as:

```text
HUNT_AFTER_EXIT
```

Otherwise it is classified as:

```text
REJECT_AFTER_EXIT
```

This classification separates post-exit states without changing M0001 event logic.

## Sample definition

M0002 measures volatility after the outcome state:

```text
REJECT_AFTER_EXIT sample starts at exit_index + 1
HUNT_AFTER_EXIT sample starts at hunt_index + 1 when InpHuntSampleStartsAfterHunt=true
```

If `InpHuntSampleStartsAfterHunt=false`, the hunt branch is measured from `exit_index + 1`, while still being classified by the later hunt.

Sample length:

```text
InpPostExitSampleBars
```

If `InpUseEventLengthForSample=true`, the sample length is inherited from the original M0001 RTV sample length.

Baseline:

```text
same number of bars immediately before the original event entry
```

This preserves a before-entry baseline and avoids using future information.

Metric:

```text
branchRTV = mean(post_outcome_log_range) / mean(pre_entry_log_range)
branchLog = log(branchRTV)
```

The per-candle volatility is the same as M0001:

```text
abs(log(high / low))
```

## Random baseline

Each branch sample is compared to a matched random baseline with the same sample length:

```text
InpRandomSamplesPerEvent
```

M0002 uses the existing M0001 random/null functions for consistency.

## Final reports

M0002 prints compact final reports once on `OnDeinit`:

```text
DAL_M0002_BASE_STATE
DAL_M0002_FINAL_AUDIT
DAL_M0002_FINAL_HUNT_AFTER_EXIT
DAL_M0002_FINAL_HUNT_AFTER_EXIT_RANDOM
DAL_M0002_FINAL_HUNT_AFTER_EXIT_COMPARE
DAL_M0002_FINAL_HUNT_AFTER_EXIT_ROBUST
DAL_M0002_FINAL_HUNT_AFTER_EXIT_SESSION_REGIME
DAL_M0002_FINAL_REJECT_AFTER_EXIT
DAL_M0002_FINAL_REJECT_AFTER_EXIT_RANDOM
DAL_M0002_FINAL_REJECT_AFTER_EXIT_COMPARE
DAL_M0002_FINAL_REJECT_AFTER_EXIT_ROBUST
DAL_M0002_FINAL_REJECT_AFTER_EXIT_SESSION_REGIME
DAL_M0002_FINAL_HUNT_VS_REJECT
```

The first comparison answers whether each branch beats random.
The direct HUNT-vs-REJECT line answers where volatility is more concentrated between the two post-exit states.

## Inputs

Key M0002-specific inputs:

```text
InpOutcomeLookaheadBars
InpPostExitSampleBars
InpUseEventLengthForSample
InpHuntSampleStartsAfterHunt
InpRandomSamplesPerEvent
InpBrokerUtcOffsetHours
InpRegimeLookbackBars
```

`InpBrokerUtcOffsetHours` controls UTC session attribution:

```text
broker server time = UTC + InpBrokerUtcOffsetHours
```

## Runtime model

M0002 is candle-gated and final-only by default:

```text
OnTick intra-candle -> return
new candle opens -> append previous closed candle once
OnDeinit -> compute M0001 events once
OnDeinit -> compute M0002 branch samples once
OnDeinit -> print branch reports once
```

No tick-based research logic is used.

## Interpretation rules

If `HUNT_AFTER_EXIT` has materially higher dLogMean / winPct / tail metrics than `REJECT_AFTER_EXIT`, then post-exit volatility is concentrated more after hunt.

If `REJECT_AFTER_EXIT` is stronger, then rejection away from the zone is the more volatile branch.

If both are strong versus random and direct HUNT-vs-REJECT is small, then volatility is mixed and the node territory itself is the dominant driver rather than the post-exit branch.

If one branch beats random but the other does not, then M0002 gives a candidate filter for the next directional/decision hypothesis.
