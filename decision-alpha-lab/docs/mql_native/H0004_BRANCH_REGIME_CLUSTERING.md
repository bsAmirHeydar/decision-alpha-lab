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

## Version 1.01 — expanded regime diagnostics and engineered nulls

H0004 v1.01 expands the regime layer from a simple transition/run test into a more diagnostic branch-regime audit. The goal is not just to say that labels cluster, but to locate where and how they cluster, and to make the null model strict enough to expose accidental regime leakage or counting bugs.

### Added regime detail metrics

M0004 now prints richer segment detail lines for session, pre-volatility, revisit bucket, and event-spacing buckets.

```text
DAL_M0004_FINAL_SESSION_DETAIL_0..3
DAL_M0004_FINAL_PREVOL_DETAIL_0..2
DAL_M0004_FINAL_REVISIT_DETAIL_0/1/2/3PLUS
DAL_M0004_FINAL_SPACING_DETAIL_FAST/MID/SLOW
```

Each detail line includes:

```text
n
revPct / contPct
samePct / iidSamePct / sameLift
switchPct
P(reversal | reversal)
P(continuation | continuation)
reversalPersistenceLift
continuationPersistenceLift
lag1 / lag2
markovChi2
mutualInfoNats
allAvgRun / allMaxRun
revRunOverIid / contRunOverIid
```

This gives a much more complete view of branch regimes by context. For example, it can reveal whether continuation clustering is stronger in low pre-volatility regimes, after later revisits, or when completed events are close together in event-time.

### Added block-regime profiles

M0004 now prints block profiles at three granularities:

```text
DAL_M0004_FINAL_BLOCK_PROFILE_FAST
DAL_M0004_FINAL_BLOCK_PROFILE_MAIN
DAL_M0004_FINAL_BLOCK_PROFILE_SLOW
```

The block profile measures how branch composition and inertia vary across contiguous event blocks:

```text
globalContPct
meanContPct / sdContPct / minContPct / maxContPct
meanSameLift / sdSameLift / minSameLift / maxSameLift
meanLag1 / sdLag1
positiveLiftBlockPct
positiveLagBlockPct
hotContinuationBlockPct
coldContinuationBlockPct
```

This separates a real branch-regime process from one or two isolated extreme runs. A strong H0004 should show positive lift across many blocks, not only a high maximum run.

### Added run-length conditioned transitions

M0004 now prints:

```text
DAL_M0004_FINAL_RUN_LENGTH_TRANSITION
```

This asks whether a branch becomes more likely to continue after it has already persisted for 1, 2, 3, or 4+ consecutive events.

```text
run1SamePct
run2SamePct
run3SamePct
run4plusSamePct
runXRevSamePct
runXContSamePct
```

This is the start of a state-duration model. If `run4plusSamePct` is higher than `run1SamePct`, the branch regime has positive duration dependence. If it drops, the branch may mean-revert after long runs.

### Added lag-decay curve

M0004 now prints:

```text
DAL_M0004_FINAL_LAG_DECAY
```

It reports branch-label correlation across several lags:

```text
lag1, lag2, lag3, lag5, lag10, lag20, lag50, lag100, configured placebo lag
```

This shows whether branch memory is local, persistent, or decaying. A clean local regime should usually show high near-lag correlation and near-zero far-lag correlation.

### Engineered strict null suite

The old global label-permutation null remains, but v1.01 adds stricter nulls.

#### 1. Stratified permutation nulls

```text
DAL_M0004_FINAL_STRATIFIED_PERM_SESSION
DAL_M0004_FINAL_STRATIFIED_PERM_PREVOL
DAL_M0004_FINAL_STRATIFIED_PERM_REVISIT
DAL_M0004_FINAL_STRATIFIED_PERM_COMPOSITE
```

These shuffle labels only within matched strata, preserving branch counts inside each regime bucket. This prevents a false H0004 caused only by session mix, pre-volatility mix, revisit mix, or their combination.

The composite null uses:

```text
session × pre-vol tercile × trend regime × revisit bucket
```

If branch inertia survives the composite stratified null, it is much harder to dismiss as regime-composition leakage.

#### 2. Circular shift far-lag null

```text
DAL_M0004_FINAL_CIRCULAR_SHIFT_STRESS
```

This compares observed lag-1 branch correlation against correlations produced by circular far shifts of the same label sequence. It preserves the full label distribution and much of the sequence identity but breaks exact local adjacency.

This is stricter than simple iid permutation for detecting whether near-neighbor label memory is real.

#### 3. Block-order shuffle null

```text
DAL_M0004_FINAL_BLOCK_ORDER_SHUFFLE_STRESS
```

This shuffles contiguous blocks while preserving labels inside each block. It is diagnostic: if the observed score is not much above the block-order null, most of the regime evidence is local within-block clustering. If it remains above, the branch regime also has broader block-order structure.

### Interpretation upgrade

After v1.01, H0004 should be read in layers:

```text
Layer 1: global branch inertia
Layer 2: run clustering
Layer 3: block concentration
Layer 4: session / pre-vol / revisit / spacing dependence
Layer 5: survival against stratified and circular engineered nulls
```

A high-confidence H0004 result should survive at least the global permutation null, show positive block or run structure, and remain positive under at least the session and pre-vol stratified nulls. The composite null is the strongest diagnostic.


## Current GOLD M1 v1.01 validation snapshot

A GOLD M1 run with build 1.01 produced a clean H0004 confirmation. The important configuration was:

```text
symbol = GOLD
timeframe = M1
measureMode = EVENT_RTV_LOCKED
branchSequence = chronological_M0002_exit_labels
consumeMode = HUNT_NODE_BREAK
stressSuite = H4_FULL
```

Main sample:

```text
paired = 9247
reversal = 5588  (60.43%)
continuation = 3659 (39.57%)
countRatioRevToCont = 1.5272
```

Main transition result:

```text
samePct = 72.03
iidSamePct = 52.18
sameLiftPct = 19.86
lag1Corr = 0.4152
lag2Corr = 0.1803
P(reversal | reversal) = 76.86
P(continuation | continuation) = 64.66
reversalPersistenceLift = 16.43
continuationPersistenceLift = 25.09
```

Interpretation:

```text
Both branches cluster in time. Reversal has longer raw runs because it is the higher-frequency branch. Continuation has stronger persistence lift relative to its base frequency.
```

Run result:

```text
revAvgRun = 4.3184
contAvgRun = 2.8299
revAvgRunOverIid = 1.7088
contAvgRunOverIid = 1.7101
```

The normalized run clustering is almost identical for both branches, which supports the model that both branches are regimes rather than one branch being merely the default state.

Engineered nulls:

```text
TRANSITION_PERM_STRESS: sameLiftEmpP = 0.0020, lag1EmpP = 0.0020
RUN_SHUFFLE_STRESS: allAvgRunEmpP = 0.0020, allMaxRunEmpP = 0.0060
BLOCK_CONCENTRATION_STRESS: pctSdEmpP = 0.0020
STRATIFIED_PERM_COMPOSITE: sameLiftEmpP = 0.0020, lag1EmpP = 0.0020
CIRCULAR_SHIFT_STRESS: lag1EmpP = 0.0020
```

The composite stratified null preserves session, pre-volatility tercile, trend bucket, and revisit bucket. H0004 surviving this null means the branch inertia is not explained only by regime-composition leakage.

Lag decay:

```text
lag1 = 0.4152
lag2 = 0.1803
lag3 = 0.0696
lag5 = 0.0065
lag10 = 0.0046
lag20 = -0.0196
lag50 = -0.0089
lag100 = 0.0151
```

This is the desired shape for a local event-time regime: strong near memory, rapid decay, and near-zero far-lag placebo.

Spacing dependence was the sharpest diagnostic:

```text
fast spacing: sameLift = 17.83, lag1 = 0.3589
mid spacing:  sameLift = 4.24,  lag1 = 0.0894
slow spacing: sameLift = 1.27,  lag1 = 0.0287
```

This means branch-regime memory is strongest when completed events occur close together. When event spacing is slow, branch state mostly resets. This makes event-spacing a required state variable for later models.

## Completeness audit

H0004 matches the requested branch-regime hypothesis when the module:

```text
uses exact M0001 events and exact M0002 branch labels
sorts labels chronologically by outcome/exit index
preserves reversal/continuation base counts in the main null
reports transition matrix and same-branch lift
reports branch-specific persistence lifts
reports lag1/lag2 and lag-decay curve
reports run length, max run, and run-over-iid by branch
reports block concentration and block profiles
reports run-length conditioned transition probabilities
reports session, trend, pre-volatility, revisit, and event-spacing detail
checks global label permutation
checks run shuffle
checks block concentration shuffle
checks stratified permutation by session, pre-vol, revisit, and composite strata
checks circular far-lag adjacency placebo
checks local block-order shuffle
```

The current v1.01 module covers all of these points. The only known open audit item is the trend-regime bucket design: in several reports only two trend segments are populated while seg2/seg3 remain zero. This does not invalidate H0004, but it means future versions should either simplify the trend bucket to the populated states or expand the trend classifier so all intended states can occur.

## v1.02 contextual branch-regime extension

The first H0004 implementation measured the last-event state:

```text
P(next branch | previous branch)
```

This is necessary, but it is not the full human interpretation of a market regime. A human does not only see the last event; a human sees a local context: recent branch composition, run pressure, spacing between events, volatility regime, session, and node freshness.

M0004 v1.02 keeps the original last-event/Markov reports unchanged and adds a contextual layer:

```text
P(current branch | rolling or EWMA context before the event)
```

The contextual layer is still past-only. For event `i`, the context is computed from events `< i`; the current event label is never used to build its own context.

### Context modes

M0004 now reports both modes:

```text
last-only mode:
  previous branch label only

rolling-context mode:
  continuation percentage over the previous K events

EWMA human-eye context:
  recency-weighted continuation pressure over the previous K events
```

The EWMA context is intended to be closer to how a discretionary observer sees a chart: the most recent events matter most, but the eye still carries a memory of the local sequence.

### Context state definition

For each event, M0004 computes a past-only continuation pressure score:

```text
contextContPct in [0,1]
```

If `contextContPct >= contextStrongThreshold`, the context is continuation-dominant. If `contextContPct <= 1 - contextStrongThreshold`, the context is reversal-dominant. Otherwise it is neutral/mixed.

Default inputs:

```text
InpContextLookbackFast = 5
InpContextLookbackMain = 10
InpContextLookbackSlow = 20
InpContextEwmaAlpha = 0.35
InpContextStrongThreshold = 0.60
```

### Context reports

M0004 v1.02 adds:

```text
DAL_M0004_FINAL_CONTEXT_LAST_ONLY_REFERENCE
DAL_M0004_FINAL_CONTEXT_ROLLING_FAST
DAL_M0004_FINAL_CONTEXT_ROLLING_MAIN
DAL_M0004_FINAL_CONTEXT_ROLLING_SLOW
DAL_M0004_FINAL_CONTEXT_EWMA_MAIN
DAL_M0004_FINAL_CONTEXT_BUCKETS_ROLLING_MAIN
DAL_M0004_FINAL_CONTEXT_BUCKETS_EWMA_MAIN
DAL_M0004_FINAL_CONTEXT_SHUFFLE_STRESS_ROLLING
DAL_M0004_FINAL_CONTEXT_STRATIFIED_STRESS_ROLLING
DAL_M0004_FINAL_CONTEXT_SHUFFLE_STRESS_EWMA
DAL_M0004_FINAL_CONTEXT_STRATIFIED_STRESS_EWMA
```

Important fields:

```text
dominantFollowPct:
  how often the current label follows the dominant prior context

expectedFollowPct:
  expected follow rate from global branch base rates

dominantLiftPct:
  context-follow excess over the base-rate expectation

conflictLastFollowPct:
  in cases where last branch and contextual majority disagree, how often the current label follows the last branch

conflictContextFollowPct:
  in those same conflict cases, how often the current label follows the wider context

conflictContextMinusLastPct:
  direct evidence for whether context beats last-only in disagreement cases
```

### Why this matters

The old H0004 question was:

```text
Does the market tend to repeat the last branch?
```

The contextual question is stronger:

```text
Does the local branch environment create a regime state that can beat a last-event-only view?
```

A positive contextual result means branch-regime is not just Markov persistence; it is a local state machine.

### Contextual nulls

M0004 v1.02 tests contextual effects against:

```text
global label shuffle
composite stratified shuffle
```

The composite stratified null preserves structure across:

```text
session × pre-volatility tercile × trend regime × revisit bucket
```

If contextual lift survives this null, it is unlikely to be explained only by session mix, volatility mix, trend bucket, or revisit distribution.

