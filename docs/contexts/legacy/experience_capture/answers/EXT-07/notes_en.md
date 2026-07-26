# EXT-07 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
multi-anchor opportunity-set principle
convexity-based anchor ranking
positive-expectancy anchor policy
non-predictive execution philosophy
```

## Main Design Consequence

The system should not store only one anchor too early.

It should first build:

```text
Extreme Anchor Opportunity Set
```

Then it may produce:

```text
selected_execution_anchor
ranked_anchor_candidates
secondary_anchor_watchlist
```

## Proposed Datasets

```text
extreme_anchor_opportunity_set_v1.csv
selected_extreme_anchor_ranking_v1.csv
multi_anchor_extreme_candidates_v1.csv
anchor_convexity_ranking_v1.csv
```

## Proposed Fields

```text
scenario_id
region_id
entry_family_type
candidate_anchor_id
candidate_anchor_node_level
candidate_anchor_price
candidate_anchor_distance_from_price
candidate_anchor_depth_rank
candidate_anchor_age
candidate_anchor_parent_support
candidate_anchor_stop_distance
candidate_anchor_spread_to_stop_ratio
candidate_anchor_destination_distance
candidate_anchor_destination_openness
candidate_anchor_reward_to_risk
candidate_anchor_convexity_score
candidate_anchor_expected_r
candidate_anchor_rank
selected_execution_anchor
secondary_anchor_candidate
layered_entry_candidate
```

## Proposed Labels

```text
ANCHOR_CANDIDATE_VALID
ANCHOR_CANDIDATE_REJECTED
SELECTED_EXECUTION_ANCHOR
SECONDARY_ANCHOR_WATCHLIST
LAYERED_ENTRY_CANDIDATE
BEST_ANCHOR_BY_CONVEXITY
BEST_ANCHOR_BY_EXPECTED_R
BEST_ANCHOR_BY_PARENT_SUPPORT
BEST_ANCHOR_BY_DESTINATION_OPENNESS
```

## Proposed AI Modules

```text
Extreme Anchor Opportunity Set Builder
Candidate Anchor Ranker
Convexity-Based Anchor Selector
Positive Expectancy Anchor Policy
Multi-Anchor Optionality Router
Layered Entry Evaluator
```

## Open Questions

1. Should every valid nearby L2 node be logged, even if only one order is placed?
2. How close is "nearby" for multiple L2 anchors?
3. Should nearby anchors be grouped into one cluster or kept as separate candidates?
4. Should the deepest anchor receive higher convexity score by default?
5. Should the nearest anchor receive higher fill probability score by default?
6. Should the freshest anchor be preferred when all else is equal?
7. Should old anchors be penalized or sometimes respected more?
8. Should parent confirmation be a score feature or a hard filter?
9. Should the best stop geometry outrank parent support?
10. Should destination openness outrank stop thinness?
11. Should multiple anchors allow layered entries, or only watchlist alternatives?
12. What minimum expected R is required for an anchor candidate to remain alive?
13. How should stop-hit-then-reversal statistics affect anchor ranking?
14. How should limit-missed-then-reversal statistics affect anchor ranking?
15. Should the first implementation be rule-based ranking before AI learns the ranking?

## Attachment Index

No images were provided for this answer.
