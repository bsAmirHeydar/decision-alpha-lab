# EXT-06 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
hard structural invalidation rule
node penetration rule
Extreme death boundary
execution-sequence label requirement
```

## Proposed Hard Rule

```text
ONE_POINT_BEYOND_CYCLE_ORIGIN_NODE = INVALIDATION
```

## Proposed States

```text
NODE_VALID
NODE_PENETRATED
NODE_INVALIDATED
EXTREME_ALIVE
EXTREME_DEAD_BY_NODE_PENETRATION
```

## Proposed Datasets

```text
node_penetration_ledger_v1.csv
extreme_invalidation_ledger_v1.csv
penetration_then_reversal_ledger_v1.csv
stop_hit_then_reverse_ledger_v1.csv
```

## Proposed Fields

```text
episode_id
scenario_id
extreme_id
anchor_node_id
anchor_node_price
cycle_origin_node_id
cycle_origin_node_price

node_penetrated
node_penetration_points
node_penetration_time
penetration_before_fill
penetration_after_fill
entry_filled_before_penetration
entry_filled_after_penetration

extreme_invalidated_by_penetration
pending_cancel_required
structural_stop_triggered
price_returned_after_penetration
return_after_penetration_distance
destination_after_penetration_reached
```

## Proposed Labels

```text
PENETRATION_BEFORE_FILL
PENETRATION_AFTER_FILL
FILL_AND_IMMEDIATE_PENETRATION
PENETRATION_THEN_REVERSAL
PENETRATION_AND_CONTINUATION
OLD_EXTREME_INVALIDATED
NEW_STRUCTURE_REQUIRED
```

## Proposed AI Modules

```text
Node Penetration Detector
Extreme Invalidation Gate
Penetration-Then-Reversal Analyzer
Stop Geometry Fragility Analyzer
Extreme Width Policy Evaluator
Pending Cancel Router
```

## Architecture Consequence

This rule should live in a deterministic gate before AI policy.

Suggested gate:

```text
EXTREME_NODE_VALIDITY_GATE
```

Possible outputs:

```text
ANCHOR_VALID
ANCHOR_INVALIDATED_BY_PENETRATION
CANCEL_PENDING
STRUCTURAL_STOP_TRIGGERED
```

## Open Questions

1. Does "one point beyond the node" refer to bid/ask, mid, candle wick, or chart price?
2. For buy entries, should penetration be evaluated using bid or ask?
3. For sell entries, should penetration be evaluated using bid or ask?
4. Should the system store raw chart penetration separately from executable broker stop penetration?
5. Does spread affect structural penetration or only execution stop placement?
6. Can a new Extreme be created immediately after penetration if a new NDS structure forms?
7. Should penetration-then-reversal be used to widen future Extreme zones, or only to analyze stop fragility?
8. Should the old scenario die when the Extreme anchor dies, or only the entry candidate?
9. If parent scenario remains alive but lower Extreme dies, should the system look for a new lower-timeframe Extreme?
10. Should pending orders be cancelled immediately when penetration occurs before fill?
11. Should a filled trade close immediately on structural penetration even if broker stop is not hit?
12. Should stop-hit-then-reversal be considered a failure of the concept, the entry width, or the stop geometry?
13. Should the system track penetration by points and also by spread-normalized units?
14. Should the invalidation rule be tested as a hard rule, or is it already non-negotiable?
15. Should penetration events be visually marked on the chart for audit?

## Attachment Index

No images were provided for this answer.
