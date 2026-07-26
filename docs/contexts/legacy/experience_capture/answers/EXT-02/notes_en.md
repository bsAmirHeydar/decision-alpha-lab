# EXT-02 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
entry-layer separation principle
RTV exclusion rule
anchor-node source constraint
L2 default flexibility rule
lower-timeframe refinement rule
```

## Main Design Consequence

The future system must separate:

```text
Scenario Engine
Region Selector
Entry Family Selector
Extreme Anchor Node Selector
Execution Template
```

Extreme should not collapse these layers.

## Proposed Architecture Flow

```text
NDS Multi-Scenario Analysis
→ Direction Decision
→ Region Decision
→ Entry Family Selection
→ Lower-Timeframe Extreme Search
→ Anchor Node Selection
→ Entry/Stop/Destination Geometry
```

## Proposed Dataset Consequences

```text
entry_layer_decision_ledger_v1.csv
extreme_anchor_node_selection_v1.csv
entry_family_request_ledger_v1.csv
scenario_region_to_entry_refinement_v1.csv
```

## Proposed Fields

```text
scenario_id
direction
region_id
region_quality
entry_family_requested
entry_family_type
lower_timeframe_used
anchor_node_id
anchor_node_source_family
anchor_node_level
anchor_node_selection_reason
anchor_node_default_level
anchor_node_final_level
anchor_node_flexibility_state
rtv_used
rtv_rejected
```

## Proposed Hard Rules

```text
RTV_USED_FOR_EXTREME_ANCHOR = forbidden
EXTREME_AS_DIRECTION_ENGINE = forbidden
EXTREME_WITHOUT_SCENARIO_REGION = forbidden
```

## Proposed Flexible Rules

```text
L2_DEFAULT_ANCHOR = default
NODE_LEVEL_SELECTION = context-sensitive
LOWER_TIMEFRAME_REFINEMENT = allowed after region/direction decision
```

## Proposed AI Modules

```text
Entry Family Selector
Scenario Region Router
Extreme Anchor Node Selector
Node-Level Flexibility Policy
Lower-Timeframe Refinement Model
Extreme Standalone-Signal Rejection Gate
RTV Contamination Checker
```

## Open Questions

1. Which exact NDS node engine should produce anchor nodes first: Node-counting, X-axis structure, Hook/Rally-derived nodes, or F-context nodes?
2. Should the anchor node always be visible on the chart with a label?
3. Should the chart label become the official `extreme_anchor_node_id`?
4. Can L1 or L3 become the anchor if L2 is not available or not clean?
5. What makes a lower-level node valid enough for an Extreme entry?
6. When a large cycle exists, how small is too small for lower-timeframe Extreme refinement?
7. Should node-level selection be a hard rule, a feature, or a trained policy?
8. Should every Extreme record include the upstream scenario and region that requested it?
9. Can an Extreme be logged as a candidate if no higher-level scenario/region exists?
10. Should the system explicitly reject all Extreme-like patterns that are not requested by a scenario/region?
11. How should the system detect that anchor-node selection has become too mechanical or overfit?
12. Should L2 remain default in all symbols/scales, or be learned per context after baseline testing?

## Attachment Index

No images were provided for this answer.
