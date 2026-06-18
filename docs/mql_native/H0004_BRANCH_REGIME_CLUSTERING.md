# H0004 — Reversal/Continuation Branch Regime Clustering

## Research question

H0004 asks whether reversal and continuation are only independent labels on completed node-territory events, or whether they form branch regimes with inertia.

Core question:

```text
If the market exits one completed node event as reversal or continuation, is the next completed node event more likely to keep the same branch label than expected under an iid label sequence with the same reversal/continuation frequencies?
```

This is different from H0003.

- H0003 tests volatility-memory inside each branch.
- H0004 tests memory of the branch labels themselves.

H0004 is a regime-state hypothesis.

## Dependency chain

H0004 uses the same locked event stack:

1. H0001 detects structural nodes and completed node-territory events.
2. H0001 computes exact event RTV.
3. H0002 labels each completed event as reversal or continuation.
4. H0004 sorts valid M0002 branch samples chronologically by outcome/exit index.
5. H0004 studies the branch-label sequence.

No separate event builder is allowed.

```text
M0004 universe = exact M0001 events -> exact M0002 branch labels -> chronological label sequence
```

## Null hypothesis

The null is not equal 50/50 labels. The null preserves the observed reversal/continuation counts and shuffles label order.

```text
H0:
Branch labels are exchangeable in time after conditioning on their total counts.

H1:
Same-branch transitions, branch runs, or block concentrations exceed the shuffled-label null.
```

This matters because reversal is usually more frequent than continuation. A correct null must preserve that imbalance.

## Primary metrics

### Frequency model

```text
reversalN
continuationN
reversalPct
continuationPct
countRatioRevToCont
```

This tells whether reversal remains the higher-frequency branch.

### Transition matrix

```text
RR = reversal after reversal
RC = continuation after reversal
CR = reversal after continuation
CC = continuation after continuation
```

Derived probabilities:

```text
P(reversal | previous reversal)
P(continuation | previous reversal)
P(reversal | previous continuation)
P(continuation | previous continuation)
```

Main inertia metrics:

```text
samePct = (RR + CC) / all transitions
iidSamePct = p(reversal)^2 + p(continuation)^2
sameLift = samePct - iidSamePct
```

Branch-specific persistence:

```text
reversalPersistenceLift = P(reversal | reversal) - P(reversal)
continuationPersistenceLift = P(continuation | continuation) - P(continuation)
```

### Lag correlation

Branch labels are encoded as:

```text
reversal = 0
continuation = 1
```

Then H0004 measures:

```text
lag1Corr
lag2Corr
farLagCorr
```

### Run clustering

H0004 measures reversal and continuation runs separately:

```text
revRuns, revMaxRun, revAvgRun, revAvgRunOverIid
contRuns, contMaxRun, contAvgRun, contAvgRunOverIid
```

Under iid labels:

```text
expectedAvgRun(branch) = 1 / (1 - p(branch))
```

### Block concentration

The branch label sequence is divided into contiguous event blocks. For each block, continuation percentage is calculated.

If block-to-block continuation percentage dispersion is much larger than shuffled-label dispersion, the market is moving through branch regimes rather than independent labels.

## Stress suite

M0004 prints:

```text
DAL_M0004_FINAL_TRANSITION
DAL_M0004_FINAL_RUNS
DAL_M0004_FINAL_TRANSITION_PERM_STRESS
DAL_M0004_FINAL_RUN_SHUFFLE_STRESS
DAL_M0004_FINAL_BLOCK_CONCENTRATION_STRESS
DAL_M0004_FINAL_FAR_LAG_PLACEBO
DAL_M0004_FINAL_SESSION_REGIME
DAL_M0004_FINAL_TREND_REGIME
DAL_M0004_FINAL_PREVOL_REGIME
```

Stress tests:

- label permutation preserving reversal/continuation counts
- same-lift z-score and empirical p-value
- lag-1 correlation z-score and empirical p-value
- run max/avg shuffle stress
- continuation-run shuffle stress
- contiguous block concentration shuffle stress
- far-lag placebo/decay check
- session-segment branch inertia
- trend-regime branch inertia
- pre-volatility tercile branch inertia

## Interpretation rules

Strong H0004 support requires:

```text
sameLift > 0
lag1Corr > 0
pRevAfterRev > baseRevPct
pContAfterCont > baseContPct
transition permutation stress positive
run or block concentration stress positive
```

If only continuation has persistence:

```text
Continuation is a branch regime; reversal is mostly the base/default branch.
```

If both have persistence:

```text
Both reversal and continuation are Markov-like branch regimes.
```

If same-lift is positive but run/block tests fail:

```text
There is local transition inertia, but not enough evidence for full regime clustering.
```

## Relationship to H0003

H0003 and H0004 together form a stronger model:

```text
H0003:
Continuation carries stronger volatility memory.

H0004:
Continuation/reversal labels themselves may cluster into regimes.
```

If both are confirmed, the market state becomes:

```text
branch type has memory
branch volatility has memory
```

That is a true regime model, not a single-event anomaly.
