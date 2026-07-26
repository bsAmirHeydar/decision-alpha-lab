# RSK-R01 — Normalized Interpretation

## Core Claim

Risk budget in NDS must be learned and measured across three structural levels:

```text
context
zone
entry
```

Risk is not one flat value.

The system should measure how expensive or clean each layer is, and how much aggregate risk is being tolerated for a given profit potential and reward.

Recommended canonical model:

```text
Hierarchical Risk Cost Model
```

## Three Risk Levels

The user explicitly defines three levels:

```text
Context Risk
Zone Risk
Entry Risk
```

Each level can make the trade more or less expensive.

The final risk score should be an aggregate result of these layers.

Suggested hierarchy:

```text
Context → Zone → Entry
```

Context defines the background cost of the decision.

Zone defines the cost of exploiting the context.

Entry defines the precise execution cost and stop geometry.

## Context-Level Risk

At the context level, the system should learn:

```text
which contexts are expensive for decision-making
which contexts are cleaner and lower cost
```

A context can be expensive if it produces:

```text
wide invalidation
unclear constraint structure
low optionality
conflicting parent-child structure
low profit openness
high scenario churn
poor post-convexity performance
```

A context can be cleaner if it produces:

```text
clear structural constraints
lower cost zones
better reward openness
cleaner scenario weight
more stable destination opportunity
better convexity
```

## Zone-Level Risk

At the zone level, the system should learn which zones are:

```text
expensive
clean
low-cost
high-cost
worth exploiting
not worth exploiting
```

Zone risk may depend on:

```text
zone width
distance to invalidation
constraint density
parent context support
destination openness
number of competing zones
zone destruction risk
cost-to-potential ratio
```

A zone with good context may still be too expensive if its risk geometry is poor.

## Entry-Level Risk

At the entry level, the system should learn which entries are clean or expensive.

Entry risk may depend on:

```text
stop distance
node quality
Extreme Near Death quality
entry buffer
spread
broker constraints
fill probability
near-death precision
cost compression
```

A good context and zone can still be vetoed if the entry is too expensive or cannot compress cost enough.

## Aggregate Risk Tolerance

The user emphasizes:

```text
what level of risk we tolerate in aggregate in exchange for what profit and reward
```

This means the system should measure risk at multiple levels and then calculate an aggregate risk profile.

Suggested object:

```text
AggregateRiskTolerance
```

It should answer:

```text
how much structural cost are we paying?
what reward/potential are we receiving in exchange?
is the trade still convex after all costs?
```

## Risk in Exchange for Reward

Risk should not be measured alone.

Risk must be evaluated against:

```text
profit potential
reward
reward openness
destination openness
convexity
tail potential
```

The key question is:

```text
How much risk are we spending for how much open reward?
```

This links RSK-R01 to RSK-R02, which should formalize the cost-to-potential formula.

## Scoring

The final goal is scoring.

The user states:

```text
This way we can score them.
```

Suggested scores:

```text
context_cost_score
context_cleanliness_score
zone_cost_score
zone_cleanliness_score
entry_cost_score
entry_cleanliness_score
aggregate_risk_cost_score
reward_compensation_score
risk_to_reward_quality_score
risk_budget_score
```

The scoring should be trained, not guessed.

## Training Requirement

The user explicitly states:

```text
This must be trained completely.
```

Therefore, risk budget is a learnable policy layer.

The system should train on:

```text
historical outcomes
R distribution
drawdown per context
zone failure behavior
entry stop behavior
reward achieved versus reward available
post-convexity win rate
tail capture
profit openness preservation
```

## Risk Budget Allocation

Risk allocation should not be determined only by fixed rules.

It should depend on the learned cost and reward profile of each level.

Possible logic:

```text
clean context + clean zone + clean entry + open reward = higher risk permission
expensive context + expensive zone + weak entry = lower risk or veto
mixed levels = partial or reduced risk
```

## Veto Logic

A trade can be vetoed if any level becomes too expensive relative to reward.

Possible veto reasons:

```text
context too expensive
zone too expensive
entry too expensive
aggregate risk too high
reward does not compensate cost
profit path not open enough
cost-to-potential not convex
```

## Machine-Readable Summary

```text
risk_budget = trainable hierarchical model

risk levels:
  - context
  - zone
  - entry

measure:
  - which contexts are expensive or clean
  - which zones are expensive or clean
  - which entries are expensive or clean
  - aggregate risk tolerated
  - reward/profit received in exchange

goal:
  - score opportunities by risk spent versus reward/potential received
```

## Short Formal Statement

In NDS, risk budgeting must be measured and trained across context, zone, and entry levels. The system should learn which contexts make decisions expensive and which are cleaner and lower cost; the same must be done for zones and entries. Risk should be evaluated as an aggregate cost tolerated in exchange for profit, reward, reward openness, and convex potential. This produces a trainable scoring model that can decide how much risk to spend, when to reduce risk, and when to veto an opportunity because its cost is not justified by its potential.
