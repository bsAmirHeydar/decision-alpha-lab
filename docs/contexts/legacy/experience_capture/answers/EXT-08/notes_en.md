# EXT-08 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
context-first entry hierarchy
freshness-as-feature principle
reward-first expectancy principle
win-rate-improvement constraint
structural-expiry-over-age-expiry principle
```

## Main Design Consequence

The system should not let node freshness override the main decision hierarchy.

The hierarchy is:

```text
Context
→ Zone / Region
→ Entry
→ Extreme anchor
→ Freshness as supporting feature
```

## Proposed Hard Rules

```text
FRESHNESS_CANNOT_OVERRIDE_CONTEXT
FRESHNESS_CANNOT_OVERRIDE_ZONE
AGE_ONLY_EXPIRY_NOT_ASSUMED
REWARD_FIRST_WIN_RATE_SECOND
WIN_RATE_IMPROVEMENT_ALLOWED_ONLY_WITHOUT_REWARD_SACRIFICE
```

## Proposed Flexible Rules

```text
freshness can be a feature
oldness can be a feature
freshness impact must be tested by context
old nodes may remain valid if context and zone remain valid
```

## Proposed Datasets

```text
node_freshness_context_ledger_v1.csv
freshness_vs_expectancy_test_v1.csv
node_expiry_reason_ledger_v1.csv
context_zone_entry_sequence_v1.csv
reward_first_winrate_tradeoff_v1.csv
```

## Proposed Fields

```text
scenario_id
region_id
entry_family_type
anchor_node_id
anchor_node_level
node_created_time
node_age_bars
node_age_time
node_age_in_structure_units
node_is_fresh
node_is_old
context_valid
zone_valid
entry_requested
freshness_score
expiry_reason
reward_distance
risk_distance
reward_to_risk
win_rate_bucket
expected_r
right_tail_r
stop_out_count
stop_hit_then_reverse_count
destination_before_invalidation
```

## Proposed Labels

```text
FRESH_NODE_VALID
OLD_NODE_VALID
OLD_NODE_CONTEXT_INVALID
NODE_EXPIRED_BY_PENETRATION
NODE_EXPIRED_BY_CONTEXT_SHIFT
NODE_EXPIRED_BY_ZONE_INVALIDATION
REWARD_DOMINATES_WIN_RATE
WIN_RATE_IMPROVED_WITHOUT_REWARD_LOSS
WIN_RATE_IMPROVEMENT_REJECTED_DUE_TO_REWARD_LOSS
```

## Proposed AI Modules

```text
Context-Zone-Entry Router
Node Freshness Feature Builder
Freshness vs Expectancy Tester
Node Expiry Reason Classifier
Reward-First Anchor Policy
Win-Rate Improvement Gate
```

## Open Questions

1. Should node age be measured in bars, time, structural events, or all three?
2. Should age be measured on the entry timeframe or parent timeframe?
3. Does node freshness matter differently in Hook versus Rally contexts?
4. Does freshness matter differently for buy and sell?
5. Do old nodes create more attraction or more irrelevance?
6. Should old nodes be grouped by whether the parent context still remembers them?
7. What is the maximum acceptable stop-out count for a low-win-rate Extreme family?
8. Is 10% win rate acceptable only with very high R, or in all convex contexts?
9. What minimum expected R is needed for a low-win-rate node group?
10. How should the system detect reward sacrifice when improving win rate?
11. Should freshness be used in ranking nearby anchors?
12. Should old nodes be removed from charts if their context expires?
13. Can a node expire without penetration if the scenario region dies?
14. Can a node become valid again under a new context?
15. Should freshness analysis be part of every Extreme backtest report?

## Attachment Index

No images were provided for this answer.
