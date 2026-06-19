# H0001-H0004 Research Lock

This document audits the first four MQL-native Decision Alpha Lab hypotheses as one layered research stack. It answers two questions:

1. Are the four implemented hypotheses the same hypotheses that were discussed?
2. What still remains open before these facts can be converted into a trading strategy?

## Runtime target map

```text
H0001 / M0001: Structural node relative territory volatility
H0002 / M0002: Reversal vs continuation event-volatility branch model
H0003 / M0003: Continuation inertia, volatility memory, and cluster intensity
H0004 / M0004: Chronological branch-regime clustering
```

Current active build targets in this snapshot:

```text
M0002_ReversalContinuationExitVolatility: build 1.75
M0003_ContinuationInertiaMemory: build 1.04
M0004_BranchRegimeClustering: build 1.01
```

M0001 is the base event engine. M0002, M0003, and M0004 must not build independent event universes. They inherit completed M0001 events and M0002 branch labels.

## Non-negotiable stack guard

A report is part of the locked stack only if it respects these guards:

```text
lookaheadGuard = activeFrom_nodeIndexPlusL
exitGap = fully outside frozen zone on either side
exitGapGuard = exit-gap candles excluded from inside RTV
baselineGuard = equal-length window before event entry
sampleWindow = m0001EventRtv
measureMode = EVENT_RTV_LOCKED
consumeMode = input-driven HUNT/TOUCH lifecycle
eventUniverseGuard = exact M0001 events, then M0002 branch labels
```

Forbidden old semantics:

```text
neutral independent M0002 event stream
sampleStarts=afterOutcomeCandle
sampleBars as primary H0002 measure
useEventLength=0 primary production mode
exit that can only close on the reversal side
touch event cancelled before exit-gap just because node broke during the event
```

## H0001 — Structural node volatility fact

### Intended hypothesis

Structural highs/lows are not arbitrary points. Completed node-territory touch events should have higher relative territory volatility than matched random windows.

### Implemented algorithm

```text
1. Detect L-rule structural highs/lows.
2. Activate node only at node_index + L.
3. Build live territory around original node price from node-to-opposite-extreme distance.
4. Start event when a candle touches/intersects territory.
5. Freeze the event zone at touch.
6. Complete event only after exit_gap consecutive candles are fully outside the frozen zone, either above or below.
7. Exclude exit-gap candles from inside RTV.
8. Compare event RTV against equal-length pre-entry baseline.
9. Compare nodes against matched random windows and stress nulls.
```

### Status

H0001 matches the intended hypothesis. It is a market-structure volatility fact candidate, not a directional strategy.

## H0002 — Branch volatility model

### Intended hypothesis

After a completed M0001 event, reversal and continuation exits are different volatility branches. The branch model is not only direction-side classification; it should include frequency, intensity, tail behavior, and memory.

### Implemented algorithm

```text
1. Consume exact M0001 completed events.
2. Use the exit-completion outcome candle, default offset 0.
3. Label branch by outcome close relative to original node price.
4. Keep branchRTV = exact M0001 event RTV.
5. Split samples into REVERSAL_AFTER_EXIT and CONTINUATION_AFTER_EXIT.
6. Compare each branch to matched random.
7. Compare branches directly.
8. Report branch frequency, intensity, tail, and horizon-memory model.
```

### Branch definition

```text
LOW node:
  close > node_price -> reversal
  close < node_price -> continuation

HIGH node:
  close < node_price -> reversal
  close > node_price -> continuation
```

### Status

H0002 matches the requested model. Current empirical pattern across tested outputs:

```text
reversal = higher frequency, lower intensity
continuation = lower frequency, higher intensity, fatter tail, stronger post-event memory
```

This remains a volatility/intensity classifier, not a trade-entry rule.

## H0003 — Continuation volatility memory

### Intended hypothesis

Continuation exits may not only be stronger inside the event. They may carry higher volatility forward, creating a post-event volatility-memory state.

### Implemented algorithm

```text
1. Consume exact M0001 events and M0002 labels.
2. Compare branch event DLog.
3. Compare branch tail metrics P90/P95/CVaR90/CVaR95.
4. Compare post-event horizon DLog at h5/h10/h20/h50.
5. Compare carry/AUC persistence.
6. Compare branch lag/cluster memory.
7. Stress with label permutation, iid shuffle, contiguous block stress, and high-run stress.
```

### Status

H0003 matches the requested continuation-memory hypothesis. WTI M1 confirmed continuation higher at all tested horizons and stronger cluster memory. H0003 proves volatility memory, not directionality.

## H0004 — Branch regime clustering

### Intended hypothesis

Once market enters a reversal or continuation branch state, it may continue that branch over following events. We therefore test clusters of reversal and continuation labels themselves.

### Implemented algorithm

```text
1. Consume exact M0001 events and M0002 labels.
2. Sort branch samples chronologically by outcome/exit index.
3. Encode reversal=0 and continuation=1.
4. Compute transition matrix RR/RC/CR/CC.
5. Compare same-branch transitions to iid expectation using observed branch base rates.
6. Compute lag correlations, run lengths, and block concentration.
7. Stress with count-preserving label permutation.
8. Stress with run shuffle and block concentration shuffle.
9. Stress with stratified permutations by session, pre-vol, revisit, and composite strata.
10. Stress with circular far-lag null and block-order shuffle.
11. Segment by session, trend, pre-vol, revisit, spacing, block size, and run length.
```

### Status

H0004 matches the requested branch-regime clustering hypothesis. GOLD M1 v1.01 and WTI M1 showed strong local branch inertia, positive same-lift, run clustering, block concentration, and far-lag decay.

The most important H0004 discovery so far is event-spacing dependence:

```text
fast event spacing: strong branch memory
mid event spacing: weak branch memory
slow event spacing: near reset
```

Therefore branch regime is primarily a local event-time memory process.

## Completeness table

| Layer | Requested idea | Implemented? | Current status |
| --- | --- | --- | --- |
| H0001 | Nodes create higher RTV than random | Yes | Locked, stress-tested fact candidate |
| H0002 | Reversal/continuation differ in count and intensity | Yes | Expanded to frequency + intensity + tail + horizon memory |
| H0003 | Continuation creates volatility inertia/memory | Yes | Implemented with horizon, carry, lag, cluster, block/run stress |
| H0004 | Reversal/continuation labels cluster as regimes | Yes | Implemented with transition, run, block, lag-decay, stratified and engineered nulls |

## Known open items

These do not invalidate the four hypotheses, but they remain important for the next research stage:

```text
1. Trend-regime buckets need audit because some reports populate only seg0/seg1 while seg2/seg3 are zero.
2. H0002 direct branch difference should eventually receive its own branch-vs-branch bootstrap/permutation line in addition to branch-vs-random.
3. Random/null engine can be further hardened with seed ensembles, not only deterministic hash streams.
4. None of H0001-H0004 proves directional profitability. Strategy extraction needs MFE/MAE, stop/target, spread/slippage, and execution-risk tests.
```

## Final research statement

The locked H0001-H0004 stack currently supports this model:

```text
Structural nodes create volatility events.
Completed events split into reversal and continuation branches.
Continuation is usually lower-frequency but higher-intensity, fatter-tailed, and more persistent in post-event volatility.
Branch labels themselves are not iid; they form local event-time regimes with strong near-lag memory that decays at far lag.
```

This is a research-grade market-structure volatility map. It is not yet a production trading system.
