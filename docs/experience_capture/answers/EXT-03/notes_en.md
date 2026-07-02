# EXT-03 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
node-level definition
default anchor-level policy
extreme convexity support principle
L-level testing requirement
adaptive anchor policy candidate
```

## Proposed Hard Rules

```text
L1 is not a valid default Extreme anchor.
L2 is the minimum meaningful NDS node level.
AI may not redefine L-level semantics.
```

## Proposed Flexible Rules

```text
L2 is the default Extreme anchor level.
Higher L levels may be selected when cycle size or context requires it.
Anchor-level selection should be tested and may become policy-learnable.
```

## Proposed Dataset Consequences

```text
node_level_candidate_ledger_v1.csv
extreme_anchor_level_test_v1.csv
adaptive_anchor_level_policy_v1.csv
```

## Proposed Fields

```text
node_id
node_price
node_level
left_candle_isolation_count
right_candle_isolation_count
is_minimum_valid_level
is_default_extreme_anchor_level
cycle_size_context
candidate_anchor_levels
selected_anchor_level
selected_anchor_level_reason
stop_distance_if_L2
stop_distance_if_L3
stop_distance_if_L4
convexity_if_L2
convexity_if_L3
convexity_if_L4
```

## Proposed Labels

```text
L2_destination_before_invalidation
L3_destination_before_invalidation
L4_destination_before_invalidation
L2_stop_hit_then_reverse
L3_stop_hit_then_reverse
L4_stop_hit_then_reverse
L2_limit_missed_then_reversal
L3_limit_missed_then_reversal
L4_limit_missed_then_reversal
best_anchor_level_for_episode
```

## Proposed AI Modules

```text
Anchor Level Candidate Builder
L-Level Baseline Tester
Adaptive Anchor Level Policy
Anchor Fragility Model
Anchor Convexity Model
Cycle-Size-to-Anchor-Level Mapper
```

## Open Questions

1. Should L2 always be generated, even if a higher L anchor is selected?
2. Should L1 be stored for diagnostics but never used?
3. What exact formula defines the left/right candle isolation count?
4. Does "not reaching that price" mean wick, body, close, or any price touch?
5. Does the L definition differ for highs and lows?
6. Should cycle size be measured in price distance, node count, F-count, or Hook/Rally state?
7. When cycle size is large, how much higher should L be allowed to go?
8. Should adaptive L selection be rule-based first or model-based from the beginning?
9. Is the main goal of L2 more opportunities, smaller stops, or better convexity?
10. How many bad L2 stop-outs are acceptable if the right tail is large?
11. Should L2 be treated differently on M1 versus higher scales?
12. Should symbol spread affect the allowed L level?
13. Can L3 ever be preferred because L2 is too fragile?
14. Can L2 and L3 both be used as layered entry templates?
15. Should the system compare L2 and higher-L performance in every backtest report?

## Attachment Index

No images were provided for this answer.
