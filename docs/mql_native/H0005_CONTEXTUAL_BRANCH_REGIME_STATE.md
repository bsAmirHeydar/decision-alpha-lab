# H0005 — Contextual Branch Regime State

H0005 is the next research layer after H0004.

H0004 proves that reversal/continuation labels are not iid and that branch labels form local event-time regimes. H0005 asks whether the market state is better described by a richer context than the immediately previous branch.

## Research question

```text
Is branch behavior driven only by the last completed node event, or by a wider local context made of recent branch composition, run state, spacing, pre-volatility, session, trend, and revisit state?
```

## Why this is closer to human perception

A human looking at a chart does not only remember the last touch or the last exit. A human sees that the market has been behaving in a continuation-heavy or reversal-heavy way for a local period. The human eye naturally compresses multiple recent events into a regime impression.

H0005 formalizes that intuition with a past-only context vector.

## Past-only context vector

For each event `i`, H0005/M0004-v1.03 can compute:

```text
lastBranch
currentRunLength
rollingContinuationPct(K)
ewmaContinuationPct(K)
eventSpacingBucket
session
preVolTercile
trendRegime
revisitBucket
```

The current event's label is never used to construct its own context.

## Two-mode design

The research must keep both views:

```text
Mode A — last-only branch state:
  tests the pure Markov/last-label hypothesis

Mode B — contextual branch state:
  tests whether a broader local regime explains branch behavior better
```

This keeps H0004 interpretable while allowing H0005 to become a state-machine research layer.

## Main decision metric

The most important H0005 test is the conflict test:

```text
When lastBranch and broaderContext disagree,
does the next/current event follow lastBranch or broaderContext?
```

If context wins in conflict cases, then the regime is not merely last-event memory.

## Context quality metrics

```text
dominantFollowPct
expectedFollowPct
dominantLiftPct
conflictLastFollowPct
conflictContextFollowPct
conflictContextMinusLastPct
consensusFollowPct
```

## Stress requirements

Context must survive:

```text
global label shuffle
session-stratified shuffle
prevol-stratified shuffle
revisit-stratified shuffle
composite session × prevol × trend × revisit shuffle
far-lag/circular shift checks
block-order shuffle checks
```

Only after surviving these nulls can the contextual regime be treated as a serious state variable.

## Strategy relevance

H0005 still does not prove directional profitability. It identifies state. The next tradeability layer should test whether context state changes:

```text
next event branch probability
next event RTV intensity
right-tail probability
post-event horizon volatility
MFE/MAE feasibility
stop/target stability
```


## Consensus state — lastBranch + human-eye context

The strongest practical H0005 state is not context replacing the last event. The strongest state is **agreement** between the last event and the human-eye EWMA context.

```text
lastBranch == EWMAContextDominantBranch
```

This is called `CONSENSUS_CONTEXT` in M0004-v1.03.

Interpretation:

```text
lastBranch = nearest local trigger
EWMAContext = broader local regime impression
consensus = trigger and context point to the same branch
conflict = trigger and context disagree
neutral = context is not dominant enough
```

M0004-v1.03 reports this state for both rolling context and EWMA human-eye context:

```text
DAL_M0004_FINAL_CONSENSUS_ROLLING_MAIN
DAL_M0004_FINAL_CONSENSUS_EWMA_MAIN
```

Key fields:

```text
consensusN / consensusPct
conflictN / conflictPct
neutralN / neutralPct
consensusFollowPct
expectedFollowPct
consensusLiftPct
consensusRevNextRevPct
consensusContNextContPct
consensusMeanDLog
consensusP90DLog / consensusP95DLog
consensusFollowMeanDLog
consensusSwitchMeanDLog
followMinusSwitchDLog
```

`consensusFollowPct` answers the core question:

```text
When lastBranch and context agree, how often does the next/current event follow that agreed branch?
```

`consensusLiftPct` compares that follow rate to the expected follow rate implied by base reversal/continuation frequencies.

The intensity fields connect H0005 back to H0002/H0003:

```text
Do consensus states only predict branch labels,
or do they also select stronger events / higher delta-log states?
```

M0004-v1.03 also adds engineered nulls for consensus:

```text
DAL_M0004_FINAL_CONSENSUS_SHUFFLE_STRESS_ROLLING
DAL_M0004_FINAL_CONSENSUS_STRATIFIED_STRESS_ROLLING
DAL_M0004_FINAL_CONSENSUS_SHUFFLE_STRESS_EWMA
DAL_M0004_FINAL_CONSENSUS_STRATIFIED_STRESS_EWMA
```

The hard null keeps the labels but destroys their chronological order, including a composite stratified version:

```text
session × prevol × trend × revisit
```

A valid consensus state should show positive `consensusLiftPct` and survive both global and stratified consensus shuffle stress.
