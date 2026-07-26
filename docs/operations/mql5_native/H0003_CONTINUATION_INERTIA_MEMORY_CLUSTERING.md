# H0003 — Continuation Inertia, Volatility Memory, and Clustered Persistence

## Research question

H0003 asks whether the higher volatility created inside a completed node-territory event behaves differently after the exit branch is known. The specific hypothesis is:

> Continuation exits are lower-frequency than reversal exits, but the volatility produced around the zone has higher inertia, stronger post-event memory, fatter right-tail behavior, and more clustered high-volatility persistence.

This is not a directional trading rule. It is a volatility-state hypothesis layered above H0001 and H0002.

## Reuse policy and semantic lock

H0003 must not define a new event universe. It reuses the existing stack:

1. **H0001 / M0001** builds the completed node-territory events, including node activation, dynamic territory, touch confirmation, frozen zone, two-sided exit-gap completion, and input-driven node consumption.
2. **H0002 / M0002** labels each completed event as `REVERSAL_AFTER_EXIT` or `CONTINUATION_AFTER_EXIT` using the exit candle close relative to the original node price.
3. **H0003 / M0003** measures inertia, memory, clustering, and high-volatility runs over those same branch samples.

The measurement window remains locked to the completed M0001 event RTV:

```text
measureMode=EVENT_RTV_LOCKED
sampleWindow=m0001EventRtv
oldPostOutcomeFieldsForbidden=sampleBars_sampleStarts_afterOutcomeCandle
```

## Core model

H0003 tests the full branch-volatility model:

```text
continuation = lower frequency + higher zone volatility + higher post-event memory + fatter tail + stronger cluster/runs
reversal     = higher frequency + lower intensity + weaker persistence
```

The model is accepted only when the branch-level evidence agrees across several dimensions, not just the mean.

## Primary metrics

### 1. Event inertia

`EVENT_INERTIA` compares the event-level log-RTV deltas:

```text
contMinusRevEventDLog = contEventDLog - revEventDLog
contOverRevEventRatio = exp(contMinusRevEventDLog)
```

Positive values mean continuation has stronger volatility inside the completed event.

### 2. Tail inertia

`TAIL_INERTIA` compares right-tail levels and conditional tail averages:

```text
contOverRevP90
contOverRevP95
contOverRevCVaR90
contOverRevCVaR95
```

CVaR fields are important because continuation may be a tail-heavy volatility state even when the median difference is modest.

### 3. Horizon memory

`MEMORY_HORIZON` prints one short line for each configured horizon. This avoids MetaTrader Journal truncation and makes h5/h10/h20/h50 auditable separately.

Each horizon reports:

```text
revDLog
contDLog
contMinusRev
contOverRev
revCarry
contCarry
contMinusRevCarry
```

`Carry` means how much of the event volatility survives into the future horizon:

```text
branchCarry = horizonDLog / eventDLog
```

### 4. Memory summary

`MEMORY_SUMMARY` aggregates the horizon tests:

```text
continuationHigherHorizons
continuationHigherCarryHorizons
contMinusRevHorizonAuc
contOverRevHorizonAuc
contMinusRevCarryAuc
memoryModel
```

This turns post-event memory into a compact, repeatable decision layer.

### 5. Cluster memory

`CLUSTER_MEMORY` is printed separately for reversal and continuation. It contains:

```text
lag1DeltaCorr
lag2DeltaCorr
dayMean / dayT
weekMean / weekT
clusterModel
```

Positive lag correlations imply serial memory in event deltas. Positive day/week cluster means imply the effect survives time-cluster aggregation.

### 6. Cluster comparison

`CLUSTER_COMPARE` compares continuation and reversal directly:

```text
contMinusRevLag1
contMinusRevLag2
contMinusRevDayMean
contMinusRevWeekMean
clusterSide
```

`clusterSide=continuation_stronger_cluster_memory` means continuation is stronger across lag and calendar-cluster dimensions.

## Cluster stress tests

H0003 adds stress tests specifically for clustering, not just mean edge.

### Lag shuffle stress

`LAG_SHUFFLE_STRESS` compares the observed lag-1 and lag-2 serial correlations with deterministic Fisher-Yates shuffles of the same branch distribution. The shuffle is without replacement, so it tests ordering/temporal memory rather than changing the branch distribution.

Fields:

```text
obsLag1
shuffleMeanLag1
shuffleSdLag1
lag1Z
lag1EmpP
obsLag2
shuffleMeanLag2
shuffleSdLag2
lag2Z
lag2EmpP
stressVerdict
```

This answers: are observed lag correlations just a distribution artifact, or do they exceed an iid temporal shuffle?

### Branch cluster permutation stress

`BRANCH_CLUSTER_PERM_STRESS` tests whether continuation has stronger serial cluster memory than reversal after randomly permuting branch labels while preserving branch sample sizes. This is a direct branch-difference stress test, not just a within-branch shuffle.

Fields:

```text
obsDiffLag1
permMeanDiffLag1
permSdDiffLag1
diffLag1Z
diffLag1EmpP
obsDiffLag2
permMeanDiffLag2
permSdDiffLag2
diffLag2Z
diffLag2EmpP
stressVerdict
```

This answers: is continuation's extra lag memory branch-specific, or would the difference also appear after relabeling the same deltas?

### Contiguous block stress

`BLOCK_CLUSTER_STRESS` groups branch samples into contiguous event blocks and checks whether block means remain positive:

```text
blockSize
blocks
blockMean
blockSd
blockT
blockMin
positiveBlockPct
stressVerdict
```

This guards against one or two dense local bursts dominating the sample.

### High-run structure

`HIGH_RUNS` measures high-volatility streaks above a configurable branch percentile, default p75:

```text
thresholdPct
thresholdDelta
gtThresholdPct
runCount
maxRun
avgRun
iidExpectedAvgRun
avgRunOverIid
```

The p75 rate is mechanically near 25%, so the useful fields are `maxRun`, `avgRun`, and `avgRunOverIid`.

### Run shuffle stress

`RUN_SHUFFLE_STRESS` compares observed high-volatility run length to deterministic Fisher-Yates shuffles of the same high/low event sequence:

```text
obsMaxRun
shuffleMaxRunMean
shuffleMaxRunSd
maxRunZ
maxRunEmpP
obsAvgRun
shuffleAvgRunMean
shuffleAvgRunSd
avgRunZ
avgRunEmpP
stressVerdict
```

This answers whether high-volatility runs are genuinely clustered rather than a random ordering of high events.

### Run comparison

`RUN_COMPARE` directly compares reversal and continuation high-run behavior:

```text
contMinusRevMaxRun
contMinusRevAvgRun
contOverRevAvgRun
runSide
```

## Output map

M0003 prints the following final reports:

```text
DAL_M0003_FINAL_AUDIT
DAL_M0003_FINAL_SUMMARY
DAL_M0003_FINAL_EVENT_INERTIA
DAL_M0003_FINAL_TAIL_INERTIA
DAL_M0003_FINAL_MEMORY_SUMMARY
DAL_M0003_FINAL_MEMORY_H5
DAL_M0003_FINAL_MEMORY_H10
DAL_M0003_FINAL_MEMORY_H20
DAL_M0003_FINAL_MEMORY_H50
DAL_M0003_FINAL_REVERSAL_CLUSTER
DAL_M0003_FINAL_CONTINUATION_CLUSTER
DAL_M0003_FINAL_CLUSTER_COMPARE
DAL_M0003_FINAL_BRANCH_CLUSTER_PERM_STRESS
DAL_M0003_FINAL_REVERSAL_LAG_STRESS
DAL_M0003_FINAL_CONTINUATION_LAG_STRESS
DAL_M0003_FINAL_REVERSAL_BLOCK_STRESS
DAL_M0003_FINAL_CONTINUATION_BLOCK_STRESS
DAL_M0003_FINAL_REVERSAL_HIGH_RUNS
DAL_M0003_FINAL_CONTINUATION_HIGH_RUNS
DAL_M0003_FINAL_RUN_COMPARE
DAL_M0003_FINAL_REVERSAL_RUN_STRESS
DAL_M0003_FINAL_CONTINUATION_RUN_STRESS
```

## Interpretation standard

The strongest confirmation pattern is:

```text
continuationLowerFrequency = true
contMinusRevEventDLog > 0
contOverRevCVaR95Ratio > 1
continuationHigherHorizons = all tested horizons
continuationHigherCarryHorizons >= majority
contMinusRevLag1 > 0 and contMinusRevLag2 > 0
continuation blockMean > reversal blockMean
continuation maxRun/avgRun > reversal maxRun/avgRun
lag/run shuffle stressVerdict supports clustering, and branch-cluster permutation supports continuation-specific memory
```

When these conditions align, H0003 supports the claim that continuation is not merely a stronger event branch; it is a volatility-memory state.

## Known engineering guardrails

- H0003 must run with the same M0001 inputs as H0001/H0002 for direct comparability.
- If `m0001Events` differs meaningfully from a previous M0002 run on the same symbol/timeframe/date range, first verify inputs, compiled EX5 version, warmup, and date window.
- Long report lines are avoided by design; M0003 uses split reports to prevent Journal truncation.
- Half-life fields in shared horizon reports now include `halfLifeStatus`. If `halfLifeH=0` with `halfLifeStatus=not_reached_within_tested_horizons`, the correct interpretation is `> lastTestedH`, not zero persistence.
