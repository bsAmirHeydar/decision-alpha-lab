---
title: CH13 Future Idea Register and Non-Actionable Hypotheses
project: EXP0017 Cycle Group Intermarket Divergence
chapter: 13
layer: strategy-architect answers
status: doctrine
---

# CH13 — Future Idea Register and Non-Actionable Hypotheses

## 1. Purpose

The architect says that some ideas are not used now but may become useful after statistical testing.

This creates a separate category:

> non-actionable hypothesis.

A non-actionable hypothesis is an idea worth saving but not allowed to affect current base decisions.

## 2. Definition

A future idea is:

- not a current rule;
- not a filter;
- not a priority condition;
- not a risk adjustment;
- not an execution modifier;
- not a validity condition.

It is only a research candidate.

## 3. Idea lifecycle

```text
Idea
  -> preserved as hypothesis
  -> measured against raw data
  -> compared against neutral baseline
  -> accepted, rejected, or transformed
  -> possibly promoted to rule/model feature later
```

## 4. Examples of future ideas

Possible ideas that must stay non-actionable until tested:

- avoid certain CGs;
- favor certain CGs;
- favor cash-session signals;
- penalize outside-cash signals;
- prefer SPXUSD clean signals;
- prefer NDXUSD clean signals;
- prefer buy over sell;
- prefer sell over buy;
- use deeper hunts differently;
- use exact touches differently;
- use invalidation speed;
- use distance from reference;
- use overlapping CG signals;
- use stop-pressure zones;
- combine time target with price target;
- use separate risk weights;
- add no-trade filters;
- build AI confidence scoring.

## 5. Why preserve ideas?

Rejecting an idea too early is also a bias.

The correct stance is:

- do not apply it now;
- do not delete it;
- test it later.

## 6. Idea promotion requirements

An idea should not be promoted unless it shows measurable improvement in at least some of:

- expectancy;
- win rate;
- average dollar outcome;
- median dollar outcome;
- drawdown behavior;
- invalidation rate;
- profit capture;
- movement quality;
- robustness across periods;
- robustness across market regimes;
- robustness across symbols and directions.

## 7. Idea rejection requirements

An idea should be rejected or downgraded if it:

- reduces sample size too much;
- improves win rate but damages expectancy;
- improves average return only through rare outliers;
- fails out-of-sample;
- only works in one narrow period;
- contradicts the core divergence logic;
- increases complexity without measurable benefit.

## 8. Doctrine

> Future ideas must be stored, not obeyed.

This keeps the project open-minded without becoming chaotic.
