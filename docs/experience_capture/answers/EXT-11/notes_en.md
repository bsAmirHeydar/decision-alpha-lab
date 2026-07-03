# EXT-11 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
entry-direction relation rule
Extreme entry-family definition
local reversal entry rule
order-type constraint
stop-behind-node confirmation
```

## Proposed Hard Rules

```text
EXTREME_ENTRY_ORDER_TYPE = LIMIT
EXTREME_LOCAL_RELATION = CONTRARIAN_AT_ENTRY_LEVEL
EXTREME_STOP_PLACEMENT = BEHIND_NODE
EXTREME_IS_NOT_BREAKOUT_ENTRY
EXTREME_IS_NOT_MOMENTUM_ENTRY
```

## Proposed Flexible Rules

```text
higher-timeframe scenario can align with the Extreme entry
local contrarian entry can serve a higher-timeframe directional thesis
continuation entries should be separate entry families
```

## Proposed Datasets

```text
extreme_entry_direction_relation_v1.csv
entry_family_direction_relation_v1.csv
local_move_into_anchor_ledger_v1.csv
limit_reversal_entry_geometry_v1.csv
```

## Proposed Fields

```text
scenario_id
region_id
entry_family_type
entry_order_type
entry_direction
current_move_direction
current_move_scale
current_move_start_node_id
current_move_target_anchor_node_id
entry_direction_relation_to_current_move
higher_context_direction
higher_context_alignment
stop_behind_node
node_invalidation_rule
```

## Proposed Labels

```text
CONTRARIAN_AT_ENTRY_LEVEL
ALIGNED_WITH_HIGHER_CONTEXT
AGAINST_HIGHER_CONTEXT
LOCAL_REVERSAL_ENTRY
LIMIT_BASED_EXTREME
STOP_BEHIND_NODE
NOT_CONTINUATION_EXTREME
SEPARATE_CONTINUATION_ENTRY_FAMILY_REQUIRED
```

## Proposed AI Modules

```text
Entry Direction Relation Classifier
Local Move Into Anchor Detector
Extreme Limit Reversal Validator
Entry Family Separation Gate
Higher-Context Alignment Annotator
```

## Open Questions

1. Should every Extreme record force `entry_order_type = LIMIT`?
2. Should any market-entry version of Extreme be forbidden or treated as a separate family?
3. How exactly should the local current move be detected?
4. Should current move be defined on the entry timeframe only?
5. Can the same Extreme be contrarian locally but aligned with parent context?
6. Should higher-context alignment increase Extreme quality?
7. Should Extreme entries against parent context be allowed if reward potential is large?
8. Should continuation entries be placed in a separate `POST_F1_CONTINUATION` family?
9. Should the system reject any Extreme labeled as breakout/momentum?
10. Should the stop always be behind the anchor node or behind the cycle-origin node specifically?
11. How should spread alter stop placement while preserving structural stop-behind-node logic?
12. Should local contrarian entry be a hard rule or just the current definition?
13. Should AI ever be allowed to discover an Extreme-like continuation variant?
14. If it discovers one, should it be renamed rather than called Extreme?
15. Should `entry_direction_relation_to_current_move` be used by all entry families, not only Extreme?

## Attachment Index

No images were provided for this answer.
