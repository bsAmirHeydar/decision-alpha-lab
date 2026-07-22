# H0004 — Branch Regime Clustering

## Hypothesis

Completed M0001 node-territory events do not produce independent reversal/continuation branch labels. The branch labels form clustered regimes with measurable inertia.

## Primary claim

```text
P(same next branch) > iid count-preserving expectation
```

where iid expectation preserves the observed reversal/continuation frequencies.

## Data source

Exact M0001 completed events and M0002 branch labels.

## Measurement

Events are sorted by confirmed exit/outcome index. The sequence is encoded as:

```text
REVERSAL = 0
CONTINUATION = 1
```

## Metrics

- transition matrix: RR, RC, CR, CC
- same-branch transition lift
- branch-specific persistence lift
- lag-1 and lag-2 label correlation
- reversal and continuation run length distributions
- block-level continuation concentration
- session, trend, and pre-volatility segmented inertia

## Nulls

- label shuffle preserving counts
- run shuffle preserving counts
- block concentration shuffle preserving counts
- far-lag placebo/decay diagnostic

## Acceptance criteria

H0004 is provisionally accepted on a symbol/timeframe if:

1. sameLift is positive;
2. lag1Corr is positive;
3. at least one branch has positive persistence lift;
4. label-permutation stress rejects shuffled labels;
5. run or block concentration stress is positive.

A stronger version requires both branches to have positive persistence lift.


## Current implementation status

M0004 v1.01 now implements the requested H0004 scope: chronological branch-label transition matrix, run clustering, block concentration, lag decay, run-length conditioned continuation, session/pre-vol/revisit/spacing detail, and engineered strict nulls.

The core null preserves observed reversal/continuation counts. Additional nulls preserve session, pre-volatility, revisit bucket, and composite strata. A circular far-lag null and block-order shuffle null diagnose whether memory is local or longer-horizon.

Current interpretation: H0004 is complete as a branch-regime clustering test. It should be used as a state layer for later strategy extraction, not as a standalone directional entry rule.
