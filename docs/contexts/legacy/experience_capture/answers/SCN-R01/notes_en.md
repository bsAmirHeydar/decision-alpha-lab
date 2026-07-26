# SCN-R01 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
context power model
position-first model
constraint exploitability model
context-to-zone promotion policy
parent-child dominance rule
destination optionality model
multi-state policy learning target
```

## Core Hard Rules

```text
CONTEXT_BEFORE_ZONE_BEFORE_ENTRY
POWER_ALONE_IS_NOT_ENOUGH
POSITION_MUST_BE_IDENTIFIED
BET_ON_NDS_CONSTRAINTS_NOT_PREDICTION
HIGHER_TIMEFRAME_IS_DOMINANT
LOWER_TIMEFRAME_REFINES_HIGHER_TIMEFRAME_MAP
ENTRY_WITHOUT_CONTEXT_ZONE_IS_WEAK
```

## Core Learnable Policies

```text
constraint_exploitability
context_power_score
reversal_probability_proxy
zone_promotion_threshold
symmetry_confluence_value
x_closure_weight
y_closure_zone_precision_weight
multi_sequence_confluence_weight
destination_optionality_score
risk_allocation_across_multiple_entries
stepwise_exit_policy
```

## Proposed Objects

```text
ContextState
PositionState
ConstraintSet
ConstraintPower
ConstraintExploitability
ZonePromotionState
DestinationOptionality
ParentChildContextRelation
OpenOneTwoDestination
```

## Proposed Datasets

```text
context_power_model_v1.csv
position_constraint_model_v1.csv
scenario_ranking_v1.csv
parent_child_context_dominance_v1.csv
context_to_zone_promotion_policy_v1.csv
constraint_exploitability_training_v1.csv
symmetry_confluence_zone_v1.csv
open_one_two_destination_v1.csv
destination_optionality_model_v1.csv
```

## Proposed Fields

```text
scenario_id
context_id
position_id
symbol
active_scale_id
parent_scale_id
child_scale_id

bullish_hook_state
bullish_rally_state
bearish_hook_state
bearish_rally_state
parent_context_direction
child_execution_state

x_closure_present
x_closure_strength
y_closure_present
y_closure_strength
xy_closure_present
closed_sequence_count
hook_type
symmetry_confluence_score

constraint_type
constraint_strength
constraint_exploitability_score
cost_to_trade_constraint
reward_potential
expected_reward_path_length

zone_candidate
zone_promoted
zone_promotion_reason
entry_refinement_required
entry_permission_state

destination_open_one_two_present
destination_distance
destination_openness_score
optionality_score
stepwise_exit_available
multiple_entry_points_available

context_power_score
position_quality_class
tradeability_class
veto_reason
```

## Proposed Labels

```text
POSITION_IDENTIFIED
CONSTRAINT_IDENTIFIED
CONSTRAINT_EXPLOITABLE
CONTEXT_ONLY
ZONE_CANDIDATE
ZONE_PROMOTED
ZONE_TRADABLE
ENTRY_REFINEMENT_REQUIRED
ENTRY_ALLOWED
WATCHLIST
VETO

X_CLOSED_REVERSAL_POWER
Y_CLOSED_ZONE_PRECISION
XY_CLOSED_HIGHER_REVERSAL_PROBABILITY
MULTI_SEQUENCE_CONFLUENCE
SYMMETRY_CONFLUENCE_ZONE
SYMMETRY_CONFLUENCE_EXTREME
OPEN_ONE_TWO_DESTINATION
LOW_OPTIONALITY_DESTINATION_TOO_CLOSE
PARENT_CONTEXT_DOMINANT
CHILD_CONTEXT_REFINES_PARENT
```

## Proposed AI Modules

```text
Position State Builder
Constraint Set Builder
Constraint Exploitability Model
Context Power Scorer
X/Y Closure Weight Learner
Multi-Sequence Confluence Scorer
Symmetry Confluence Zone Promoter
Open One-Two Destination Detector
Destination Optionality Scorer
Parent-Child Context Mapper
Context-to-Zone Promotion Model
Entry Permission Router
```

## Architecture Consequence

The future system should not feed AI only a context score.

The model should produce a structured packet:

```text
Position
Constraint Set
Constraint Exploitability
Context Power
Zone Promotion
Destination Optionality
Entry Permission
```

This packet should sit between canonical NDS state and execution candidate generation.

## Open Questions

1. What exact structure defines an open one-and-two?
2. Is open one-and-two always a destination magnet, or only in some contexts?
3. How should timing uncertainty of open one-and-twos be represented?
4. What exact minimum X closure is required for reversal power?
5. Can Y closure alone ever create a tradable zone?
6. How should X-only, Y-only, and XY closure be weighted?
7. How should multiple closed sequences be normalized?
8. What exact rule promotes symmetry confluence into a zone?
9. What exact threshold makes destination too close and optionality too low?
10. Should multiple entries with different risk be simulated as one scenario or separate scenarios?
11. Should stepwise exits be part of scenario definition or execution policy?
12. Can child timeframe ever veto parent context, or only delay/refine execution?
13. What exact conditions create weak context?
14. Should context power be a numeric score, class, or both?
15. Should the first implementation be rule-based before training the constraint exploitability model?

## Attachment Index

No images were provided for this answer.
