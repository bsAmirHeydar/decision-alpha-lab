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

For each event `i`, H0005/M0004-v1.02 can compute:

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

