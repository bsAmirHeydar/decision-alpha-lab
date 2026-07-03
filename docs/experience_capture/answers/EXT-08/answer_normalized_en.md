# EXT-08 — Normalized Interpretation

## Core Claim

Node freshness is not a primary standalone decision rule.

The system should not first ask:

```text
is this node fresh or old?
```

The system should first ask:

```text
is the correct context present?
is the correct trading zone present?
is an entry point needed inside that zone?
```

Only after context and zone are defined should the system evaluate Extreme entries and their anchor nodes.

## Correct Decision Sequence

The correct hierarchy is:

```text
1. Context
2. Zone / trading region
3. Entry point
4. Extreme anchor
```

This means freshness is secondary.

A fresh node is not automatically valid.

An old node is not automatically invalid.

A node becomes relevant when it belongs to the correct NDS context and the correct trading region.

## No Fresh-vs-Old Separation by Default

The answer explicitly says:

```text
we do not create a separation here
```

This means the system should not hardcode a rule such as:

```text
fresh nodes are always better
old nodes are always better
old nodes expire after N bars
```

Freshness can be stored as a feature, but it should not become a blind rule.

## Reward-First Logic

The system prioritizes reward and convexity over win rate.

The project accepts that Extreme-style entries may have many stop-outs.

This is acceptable because the risk is intended to be very small and the reward can be very large.

Possible acceptable win-rate range from the answer:

```text
10% to 20% can still be acceptable
```

But only if the reward distribution creates positive expectancy.

## Win Rate Is Secondary, Not Irrelevant

Win rate is not the primary criterion.

However, it is not useless.

The user says:

```text
if we can increase win rate without sacrificing reward, we should do it
```

This creates a clear optimization principle:

```text
reward first
win rate second
increase win rate only when reward is not sacrificed
```

## Node Expiry

The answer does not define expiry by age.

Therefore, the default interpretation should be:

```text
nodes do not expire only because they are old
```

A node should expire because of structural reasons, not because of time age alone.

Possible NDS-native expiry reasons:

```text
cycle-origin node penetrated
scenario invalidated
trading zone no longer valid
parent context changed
destination already resolved
entry opportunity no longer belongs to the active region
```

This connects to EXT-06:

```text
one-point penetration beyond the cycle-origin node invalidates the Extreme anchor
```

So the strongest expiry rule currently known is structural penetration, not freshness.

## Freshness as a Feature

Freshness should still be recorded as a feature because tests may show that it affects quality.

Suggested freshness fields:

```text
node_age_bars
node_age_time
node_age_in_structure_units
touch_count_since_creation
distance_from_current_price
context_still_valid
zone_still_valid
```

But freshness should be evaluated through expectancy, not assumed.

## What the System Should Test

The system should test whether freshness affects:

```text
entry frequency
fill rate
stop-out rate
stop-hit-then-reverse rate
destination-before-invalidation rate
average R
right-tail R
expected R
drawdown
path cleanliness
execution difficulty
```

A fresh node may win more often.

An old node may sometimes create larger reward or stronger attraction.

Neither should be assumed before testing.

## AI Relevance

AI should not use freshness as a standalone decision shortcut.

AI may use freshness as one feature inside a larger NDS context.

Allowed AI task:

```text
evaluate whether node freshness improves expectancy inside a valid context and zone
```

Forbidden AI task:

```text
choose a node only because it is fresh or old while ignoring context and zone
```

## Short Formal Statement

Node freshness is secondary to context and zone. The system should first establish the correct NDS context and trading region, then search for precise Extreme entries. Old or fresh nodes should not be separated by a blind rule. Freshness may be stored and tested as a feature, but reward, convexity, and positive expectancy dominate. Win rate may be improved only if reward is not sacrificed.
