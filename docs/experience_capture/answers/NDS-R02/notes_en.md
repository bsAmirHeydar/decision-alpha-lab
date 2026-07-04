# NDS-R02 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
CycleHook lifecycle definition
Hook/Cycle equivalence rule
positive-negative Hook model
sequence construction algorithm
X/Y sequence model
adaptive L policy
Hook closure model
Hook type A/B/C classifier
symmetry projection model
ND policy foundation
```

## Core Hard Rules

```text
HOOK_AND_CYCLE_ARE_ONE_ALGORITHMIC_OBJECT
EVERY_NODE_CAN_START_A_CYCLEHOOK
POSITIVE_CYCLEHOOK_COUNTS_VALLEYS
NEGATIVE_CYCLEHOOK_COUNTS_PEAKS
POSITIVE_SEQUENCE_REQUIRES_STRICTLY_LOWER_VALLEYS
NEGATIVE_SEQUENCE_REQUIRES_STRICTLY_HIGHER_PEAKS
EQUAL_NODES_ARE_NOT_ACCEPTED_IN_SEQUENCE
L_STARTS_AT_2
INCREASE_L_UNTIL_MAX_SEQUENCE_NODE_COUNT_LESS_OR_EQUAL_4
ORIGIN_PENETRATION_KILLS_CYCLEHOOK
```

## Core Flexible / Learnable Policies

```text
ND threshold
Extreme width
symmetry usefulness
Hook type reading in four-node cases
X/Y closure strength
L fixed-origin versus recalculated-origin usage
projection from multiple sequence symmetries
```

## Proposed Objects

```text
CycleHook
CycleHookOrigin
CycleHookExtreme
CycleHookNDZone
HookSequence
XSequence
YSequence
LCoefficientView
HookClosureState
HookTypeABC
SymmetryProjection
```

## Proposed Datasets

```text
cyclehook_lifecycle_state_model_v1.csv
hook_sequence_model_v1.csv
x_sequence_y_sequence_model_v1.csv
adaptive_l_coefficient_policy_v1.csv
l_fixed_origin_view_v1.csv
l_recalculated_origin_view_v1.csv
hook_closure_state_v1.csv
hook_type_abc_classifier_v1.csv
symmetry_projection_model_v1.csv
nd_threshold_policy_v1.csv
```

## Proposed Fields

```text
cyclehook_id
symbol
scale_id
timeframe
direction
origin_node_id
origin_price
origin_time
opposite_extreme_price
opposite_extreme_time
nd_zone_low
nd_zone_high
death_boundary_node_id
cyclehook_state

l_value
l_view_type
origin_fixed
origin_recalculated
max_nodes_per_sequence

sequence_id
sequence_starter_node_id
sequence_node_count
sequence_node_ids
sequence_prices
sequence_is_closed
sequence_closure_node_count
retracement_from_extreme_to_origin_ratio

x_sequence_strength
x_sequence_quality_score
y_sequence_present
y_sequence_valid
y_sequence_strength
xy_closure_state

hook_type
hook_type_confidence
hook_type_reading_mode
ignored_or_downweighted_node_id

symmetry_price_distance_score
symmetry_leg_size_score
symmetry_projection_price
symmetry_projection_confidence
```

## Proposed Labels

```text
CYCLEHOOK_BORN_FROM_NODE
CYCLEHOOK_ALIVE
CYCLEHOOK_NEAR_DEATH
CYCLEHOOK_DEAD_BY_ORIGIN_PENETRATION
POSITIVE_CYCLEHOOK
NEGATIVE_CYCLEHOOK

SEQUENCE_STRICT_LOWER_VALLEYS
SEQUENCE_STRICT_HIGHER_PEAKS
SEQUENCE_NODE_COUNT_3
SEQUENCE_NODE_COUNT_4
HOOK_X_CLOSED
HOOK_Y_CLOSED
HOOK_XY_CLOSED

L_FIXED_ORIGIN_VIEW
L_RECALCULATED_ORIGIN_VIEW

HOOK_TYPE_A
HOOK_TYPE_B
HOOK_TYPE_C
HOOK_TYPE_A_STRONGEST
HOOK_TYPE_B_MIDDLE
HOOK_TYPE_C_WEAKEST

SYMMETRY_NOT_REQUIRED_FOR_CLOSURE
SYMMETRY_USED_FOR_PROJECTION
PRICE_DISTANCE_SYMMETRY
LEG_SIZE_SYMMETRY
```

## Proposed AI Modules

```text
CycleHook Builder
PositiveNegative Hook Classifier
Hook Sequence Builder
XSequence Strength Scorer
YSequence Validator
Adaptive L Selector
FixedOrigin L View Builder
RecalculatedOrigin L View Builder
Hook Closure Detector
Hook Type ABC Classifier
Symmetry Projection Model
ND Threshold Policy Model
Extreme Width Policy Model
```

## Architecture Consequence

The first implementation should separate deterministic construction from learnable scoring.

Deterministic construction:

```text
nodes
CycleHook origin
positive/negative direction
sequences
L adjustment
basic closure
origin penetration death
```

Learnable scoring:

```text
symmetry projections
ND threshold
Extreme width
X/Y strength
Hook type in ambiguous four-node cases
reversal probability proxy
entry refinement usefulness
```

## Open Questions

1. What exact node detector feeds the CycleHook builder at L2 and higher L values?
2. Should a node that appears in multiple sequences have multiple sequence roles or one canonical role plus references?
3. How should a sequence starter be defined when multiple nodes occur at nearly the same price?
4. Should strict lower/higher comparison use raw price or normalized point/tick value?
5. Should spread ever affect equality or strictness, or is sequence logic purely chart-price based?
6. What exact retracement formula should be used for the 50% closure rule?
7. Should retracement be measured by wick, close, or any price touch?
8. What exact condition defines ND zone before origin penetration?
9. Should ND be built from fixed-origin L view, recalculated-origin L view, or both?
10. How should four-node Type A/B/C examples be labeled for AI training?
11. What makes an X-sequence strong versus weak?
12. What makes a Y-sequence strong versus weak?
13. How should price-distance symmetry be normalized across symbols?
14. How should leg-size symmetry be measured in Y-sequence mode?
15. Should the first backtest compare X-only closure versus XY closure separately?

## Attachment Index

```text
images/NDS-R02-image-01-hook-types-a-b-c.png
images/NDS-R02-image-02-multi-sequence-node-counting.png
images/NDS-R02-image-03-y-sequence-opposite-extremes.png
```
