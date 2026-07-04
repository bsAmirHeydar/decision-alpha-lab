# RSK-R02 — Normalized Interpretation

## Core Claim

Risk in NDS is account-percentage based, but it is not fixed.

The base risk percentage should be adjusted by a setup-quality coefficient.

Then position sizing must be calculated so that the true monetary cost, after stop distance and commission, equals the intended risk budget.

Recommended canonical model:

```text
TargetRiskCost = AccountEquity × BaseRiskPercent × SetupQualityRiskCoefficient
```

And the executable size must satisfy:

```text
TrueTradeCost(stop distance, commission, spread, volume) = TargetRiskCost
```

This makes cost exact and auditable.

## Risk as Percent of Account

The user clarifies that risk means:

```text
percentage risk of the account
```

Therefore, the primary unit of risk budget should be:

```text
account_risk_percent
```

But this percentage should be modified by setup quality.

Suggested fields:

```text
base_account_risk_percent
setup_quality_risk_coefficient
effective_account_risk_percent
target_risk_cost_money
```

## Setup Quality Risk Coefficient

Setups have quality differences.

The risk coefficient should reflect this.

Possible interpretation:

```text
higher quality setup → larger allowed risk coefficient
lower quality setup → smaller allowed risk coefficient
poor setup → risk veto or near-zero coefficient
```

The coefficient should be trained from outcome data, not guessed permanently.

Suggested model:

```text
SetupQualityRiskCoefficient
```

This coefficient should be derived from the multi-level evaluation established in RSK-R01:

```text
context quality
zone quality
entry quality
aggregate risk/reward profile
optionality across levels
```

## True Cost

The user defines cost operationally:

```text
stop distance + commission
```

To be precise, true cost should include:

```text
stop distance loss
commission
spread cost
buffer cost
slippage estimate if used later
```

But the user explicitly named:

```text
stop distance
commission
```

So the first implementation should at minimum include these two.

Suggested field:

```text
true_trade_cost
```

The system should not assume that a position is using 1% risk simply because the input says 1%.

It must calculate the volume so that the actual cost equals the target risk amount.

## Position Sizing Consequence

Although this record is documentation-only and must not add execution code, the architecture implication is clear:

```text
target risk percent → target risk money → solve volume from stop distance and commission
```

The sizing model should be a validator/calculation object, not direct order sending.

The calculation should answer:

```text
What volume makes the true cost equal the intended risk budget?
```

This connects to later execution and broker validation modules.

## High Reward Target

The user states:

```text
We are looking for rewards above 10R.
```

Therefore, the opportunity model should treat:

```text
reward_above_10R
```

as an important target class.

This does not mean every trade must achieve 10R, but the strategy is structurally designed to seek reward opportunities above 10R.

Suggested labels:

```text
REWARD_TARGET_ABOVE_10R
HIGH_CONVEXITY_REWARD
TAIL_REWARD_CANDIDATE
```

## Cost-to-Potential

Cost must be compared to potential.

In this model:

```text
cost = true account-risk cost after stop distance and commission
potential = reward path, destination openness, tail potential, and reward above 10R possibility
```

Suggested relationship:

```text
CostToPotentialScore = Potential / TrueCost
```

But the exact formula should remain trainable.

The core principle is:

```text
spend less cost for wider, more open, and higher reward potential
```

## Optionality Is Multi-Level

The user clarifies that optionality should not be considered only at the final entry.

Optionality must be evaluated at:

```text
context level
zone level
entry level
```

This is important.

A small-stop entry does not automatically mean the whole trade has good optionality.

Optionality can be strong or weak at each layer.

Suggested objects:

```text
ContextOptionality
ZoneOptionality
EntryOptionality
AggregateOptionality
```

## Context Optionality

Context optionality measures whether the broader structural situation offers open paths, large destinations, and favorable scenario potential.

Possible inputs:

```text
parent Hook / CycleHook state
X/Y closure
multi-sequence closure
destination candidate openness
scenario conflict
higher timeframe support
open one-two structures
```

## Zone Optionality

Zone optionality measures whether a zone provides a low-cost access point to a large structural opportunity.

Possible inputs:

```text
zone width
zone invalidation clarity
parent context support
destination openness from the zone
competing zones
zone destruction risk
cost-to-potential ratio
```

## Entry Optionality

Entry optionality measures whether the final execution point compresses cost while preserving the larger opportunity.

Possible inputs:

```text
stop distance
Extreme Near Death quality
reference node quality
spread/commission impact
fill probability
entry precision
risk geometry
```

## Aggregate Optionality

The final optionality score should combine all levels:

```text
AggregateOptionality = f(ContextOptionality, ZoneOptionality, EntryOptionality)
```

This aggregate should be used before checking win rate.

Win rate should be measured after the setup passes convexity and optionality filters.

## Convexity Threshold

The answer does not define a numerical threshold, but it implies the model should prefer opportunities with:

```text
low true cost
high setup quality
reward potential above 10R
multi-level optionality
```

Therefore, a trade can be classified as meaningfully convex only if the total cost is justified by high and open potential.

Suggested class labels:

```text
NOT_CONVEX
WEAK_CONVEXITY
ACCEPTABLE_CONVEXITY
HIGH_CONVEXITY
EXTREME_CONVEXITY
```

## Machine-Readable Summary

```text
risk_unit = percent_of_account

effective_risk_percent =
    base_risk_percent × setup_quality_risk_coefficient

true_cost =
    stop_distance_cost + commission + optional spread/buffer/slippage costs

position_size should be solved so:
    true_cost == target_risk_cost

target_reward:
    prefer opportunities above 10R

optionality levels:
    - context optionality
    - zone optionality
    - entry optionality
    - aggregate optionality
```

## Short Formal Statement

In NDS, risk is expressed as a percentage of account equity, adjusted by a setup-quality coefficient. The executable size must be calculated so that, after stop distance and commission, the true monetary cost equals the intended risk budget. The strategy seeks rewards above 10R, so cost must be judged against large and open reward potential. Optionality is not only an entry-level concept; it must be measured separately at context, zone, and entry levels, then combined into an aggregate optionality score. Convexity is therefore a multi-level cost-to-potential relationship, not just a small stop at the final entry.
