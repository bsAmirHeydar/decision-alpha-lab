# EXT-01 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
entry family definition
extreme geometry principle
cycle-death concept
convex payoff principle
execution design requirement
```

## Proposed Datasets

```text
extreme_opportunity_dataset_v1.csv
extreme_geometry_ledger_v1.csv
untouched_node_death_proximity_ledger_v1.csv
extreme_fill_outcome_ledger_v1.csv
extreme_stop_then_reverse_ledger_v1.csv
```

## Proposed Fields

```text
anchor_node_id
anchor_node_level
anchor_node_price
anchor_node_unreached
cycle_origin_node_id
cycle_death_node_id
cycle_death_price
near_death_zone_upper
near_death_zone_lower
near_death_width
cycle_death_proximity_ratio
price_entered_extreme_zone
entry_price
stop_price
stop_distance_raw
spread_points
spread_to_raw_stop_ratio
effective_stop_distance
destination_price
reward_distance
convexity_score
right_tail_potential
```

## Proposed Outcome Labels

```text
EXTREME_NOT_REACHED
EXTREME_ZONE_ENTERED
LIMIT_FILLED
LIMIT_MISSED_THEN_REVERSAL
STOP_HIT_THEN_REVERSAL
STOP_HIT_AND_CONTINUED
REVERSAL_FROM_NEAR_DEATH
CYCLE_DEATH_CONFIRMED
DESTINATION_BEFORE_INVALIDATION
INVALIDATION_BEFORE_DESTINATION
```

## Proposed AI Modules

```text
Extreme Opportunity Builder
Extreme Geometry Builder
Extreme Quality Model
Extreme Width Policy Model
Limit-Fill vs Miss Model
Stop-Then-Reverse Analyzer
Spread Sanity Gate
Extreme Convexity Evaluator
```

## Open Questions

1. What exact geometric definition should determine the near-death zone width?
2. Should near-death width depend on scale, spread, node type, or scenario quality?
3. What is the difference between a valid stop-hit-then-reverse and a truly bad Extreme?
4. Should the system allow ultra-thin stops on M1 by default, or only after spread sanity passes?
5. Should missed-limit reversals lead to wider entries or multiple layered limit entries?
6. Should Extreme entries support multiple templates: edge entry, middle-zone entry, deep entry, and micro-extreme entry?
7. Is the node always L2 by default, or can the near-death concept apply to other node levels?
8. How should destination be selected for Extreme entries?
9. Should Extreme be primarily a reversal entry or a convex optionality entry that can include other outcomes?
10. How many stop-then-reverse events are acceptable before an Extreme template is considered too fragile?
11. Should raw spread thresholds be hard rules or learnable policy constraints?
12. Should Extreme Width Policy be rule-based first and AI-based later?

## Attachment Index

```text
images/EXT-01-image-01-near-death-reversal-example-a.png
images/EXT-01-image-02-near-death-reversal-example-b.png
images/EXT-01-image-03-near-death-reversal-example-c.png
```
