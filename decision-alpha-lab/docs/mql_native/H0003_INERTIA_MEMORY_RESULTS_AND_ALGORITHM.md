# H0003 — Continuation Inertia, Volatility Memory, and Clustered Event Intensity

## Research question

H0003 asks whether the continuation branch discovered in H0002 is only a stronger event-volatility bucket, or whether it also creates a persistent post-event volatility regime.

The question is deliberately not directional alpha yet. It is a volatility-state question:

```text
After a completed M0001 node-territory event, does the continuation branch preserve elevated volatility for more future horizons than the reversal branch?
```

## Dependency chain

H0003 is downstream of the locked H0001/H0002 stack:

1. H0001 builds completed M0001 node-territory events.
2. H0001 event RTV is computed from the exact event window, with the final exit-gap candles excluded from RTV.
3. H0002 labels each completed event as reversal or continuation using the exit candle close relative to the original node price.
4. H0003 never rebuilds a separate event universe. It consumes exact M0001/M0002 branch samples.

This guard is critical:

```text
M0003 event universe = exact M0001 events -> exact M0002 branch samples
M0003 measurement = M0001 event RTV locked
```

## Branch definitions inherited from H0002

For a LOW node:

```text
exit close > node price => REVERSAL
exit close < node price => CONTINUATION
```

For a HIGH node:

```text
exit close < node price => REVERSAL
exit close > node price => CONTINUATION
```

The branch label is a classification over a completed M0001 event. It must not alter the measured RTV window.

## H0003 model

H0003 expands H0002 into four sub-models:

```text
Event intensity:
Continuation event DLog > reversal event DLog

Tail inertia:
Continuation P90/P95/CVaR90/CVaR95 > reversal P90/P95/CVaR90/CVaR95

Horizon memory:
Continuation post-event horizon DLog > reversal post-event horizon DLog

Cluster memory:
Continuation event deltas have stronger lag and contiguous-block persistence
```

## Stress tests

M0003 includes the following validation tests:

- exact M0001 event universe audit
- event RTV locked audit
- branch frequency audit
- event DLog comparison
- P90/P95/CVaR tail comparison
- horizon memory at h5/h10/h20/h50
- carry-AUC memory summary
- branch lag correlation at lag 1 and lag 2
- day/week cluster robust means
- label-permutation stress for branch cluster difference
- iid shuffle stress for within-branch lag memory
- contiguous block stress
- high-run clustering and run-shuffle stress

## Current WTI M1 result snapshot

A WTI M1 run produced:

```text
paired = 16776
reversal = 9871  (58.84%)
continuation = 6905 (41.16%)
```

Event intensity:

```text
revEventDLog = 0.2584
contEventDLog = 0.3508
contMinusRevEventDLog = 0.0924
contOverRevEventRatio = 1.0968
```

Tail inertia:

```text
contOverRevP90 = 1.2072
contOverRevP95 = 1.3000
contOverRevCVaR90 = 1.3320
contOverRevCVaR95 = 1.3609
```

Memory summary:

```text
continuationHigherHorizons = 4 / 4
continuationHigherCarryHorizons = 4 / 4
contOverRevHorizonAuc = 1.5714
memoryModel = continuation_higher_inertia_and_memory_all_tested_horizons
```

Horizon-by-horizon memory:

```text
h5:  rev = 0.2201, cont = 0.3110, cont/rev = 1.4128
h10: rev = 0.1553, cont = 0.2288, cont/rev = 1.4737
h20: rev = 0.1051, cont = 0.1889, cont/rev = 1.7973
h50: rev = 0.0790, cont = 0.1504, cont/rev = 1.9049
```

Cluster memory:

```text
revLag1 = 0.1249
contLag1 = 0.1940
contMinusRevLag1 = 0.0690

revLag2 = 0.0722
contLag2 = 0.1441
contMinusRevLag2 = 0.0719
```

Permutation stress confirmed the continuation cluster-memory difference:

```text
diffLag1Z = 4.2851, empP = 0.0050
diffLag2Z = 4.5892, empP = 0.0050
```

Run clustering was mixed:

```text
reversal maxRun = 15
continuation maxRun = 9
reversal avgRun = 1.4673
continuation avgRun = 1.6011
runSide = mixed_run_clustering
```

Interpretation:

```text
Continuation has stronger average run persistence, but reversal produced the longest single high-volatility run in this WTI sample.
```

## Current scientific statement

The current H0003 statement is:

```text
In completed node-territory events, the continuation branch is generally lower-frequency than reversal, but it carries higher event volatility, fatter right tails, and stronger post-event volatility memory. On WTI M1 this continuation memory is confirmed across all tested horizons and by label-permutation/lag-shuffle stress tests.
```

## Important boundary

H0003 still does not prove directionality. It proves branch-conditioned volatility persistence, not entry profitability. Directional alpha requires separate MFE/MAE, stop/target, spread/slippage, and execution-path tests.


## Completeness audit

H0003 matches the requested research question when all of the following are true:

```text
uses exact M0001 completed events
uses exact M0002 branch labels
keeps EVENT_RTV_LOCKED for event intensity
compares reversal vs continuation event DLog
compares P90/P95/CVaR tails
compares post-event horizons h5/h10/h20/h50
compares carry persistence across horizons
checks lag/cluster memory by branch
checks label-permutation stress for branch memory difference
checks iid shuffle stress for within-branch serial memory
checks contiguous block stress and high-run stress
```

This module is complete as a volatility-memory and inertia test. It is intentionally not a directional trading model. Directional alpha remains a later layer.
