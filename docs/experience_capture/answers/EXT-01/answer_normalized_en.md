# EXT-01 — Normalized Interpretation

## Core Claim

Extreme is not the node itself.

Extreme is the near-death zone around an untouched node.

It is the area where price approaches the point at which a cycle would die, but before the cycle is fully killed.

The value of Extreme comes from:

```text
narrow structural risk
stop behind the node
convex reward potential
high asymmetry
```

## Extreme Is One Entry Family

Extreme must not become the whole entry layer.

It is one entry family among multiple possible NDS-native entry frameworks.

The system should eventually support an entry-family architecture such as:

```text
Extreme Entry
Hook-Hook-Rally Entry
Higher-TF F3 / Lower-TF 3F Reversal Entry
Post-F1 Continuation Entry
Other NDS-native entries
```

Extreme may be one of the most logical and convex entries, but it must remain one entry type.

## Cycle Death Concept

A cycle starts from a node.

The death of that cycle happens when price returns to that node and passes through it.

Extreme is the zone near that death point.

Formal interpretation:

```text
cycle_origin_node
cycle_death_node
near_death_zone
cycle_death_proximity
```

The Extreme trade attempts to enter near the death of the cycle, before or around the point where the cycle is structurally invalidated.

## Node Relationship

The node is the anchor.

The Extreme is the zone near the anchor.

The stop is placed behind the node.

Suggested geometry:

```text
anchor_node = untouched node
extreme_zone = near-death neighborhood around the node
entry = near the extreme zone
stop = behind the anchor node
reward = destination opened by reversal or continuation from near-death
```

## The 90% Number Is Not a Hard Rule

The 90% idea should not be treated as a fixed numeric rule.

It is a conceptual description of late-cycle / near-death proximity.

The real question is:

```text
how much Extreme permission should be allowed?
how narrow can the risk zone be?
how do we avoid overfitting?
how do we avoid fragility?
how do we preserve maximum convex reward?
```

Therefore, future models should not hardcode 90%.

They should test a range of near-death widths and learn which are robust.

## Limit Fill and Missed Entry

Sometimes price enters the near-death area but does not activate the limit order.

Then it reverses.

This must be tracked as a separate outcome:

```text
LIMIT_MISSED_THEN_REVERSAL
```

This is not simply failure.

It is an important execution-quality label.

It shows that the concept may be correct but the entry placement was too tight.

## Stop-Then-Reverse

Sometimes price hits the stop and then reverses.

This must also be tracked separately:

```text
STOP_HIT_THEN_REVERSAL
```

This means the concept may be near the right area, but the stop geometry, buffer, spread handling, or extreme width may be too fragile.

This should not automatically invalidate the Extreme concept.

It should become a design and optimization problem.

## Spread and Very Narrow Stops

Very narrow stops are not automatically bad.

They may be the source of the most explosive entries, especially on low timeframes such as M1.

The system should not filter them out blindly.

However, spread must be considered.

A possible practical rule from the answer:

```text
raw_stop_distance_without_spread should often be at least 2x to 3x the spread,
unless a future test proves a different threshold.
```

But this should be treated as a starting assumption, not a final hard rule.

## Convexity

Extreme is valuable because it can create convex payoff.

The loss can be small because the stop is behind the node.

The reward can be large because the entry is near the cycle-death zone.

This should create fields such as:

```text
raw_risk_distance
effective_risk_after_spread
destination_distance
convexity_score
right_tail_potential
left_tail_fragility
```

## Required Future Labels

```text
extreme_zone_entered
limit_order_filled
limit_missed_then_reversal
stop_hit_then_reversal
cycle_death_confirmed
cycle_death_avoided
reversal_from_near_death
continuation_through_node
destination_before_invalidation
invalidation_before_destination
```

## Short Formal Statement

Extreme is an NDS-native entry family defined as a near-death zone around an untouched node. It seeks convex entries near the point where a cycle would die, with stop behind the node and reward opened by reversal or continuation from that near-death region. The exact width is not a fixed 90% number and must be learned and tested without destroying the convex nature of the entry.
