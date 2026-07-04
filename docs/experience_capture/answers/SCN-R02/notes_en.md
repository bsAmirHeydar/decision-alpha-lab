# SCN-R02 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
potential zone model
context-to-zone promotion policy
zone source constraint model
zone-to-entry refinement policy
zone validity state machine
zone training granularity model
dynamic zone weight regime model
```

## Core Hard Rules

```text
ZONE_IS_PRICE_RANGE
CONTEXT_TELLS_SITUATION
ZONE_TELLS_WHERE_SITUATION_IS_EXPLOITABLE
ENTRY_IS_REFINED_ON_LOWER_TIMEFRAME
ZONE_REQUIRES_EXPLOITABLE_NDS_CONSTRAINT
ZONE_OUTPUT_MUST_INCLUDE_PRICE_RANGE
ENTRY_LEVEL_EXTREME_IS_DISTINCT_FROM_HOOK_EXTREME
```

## Core Learnable Policies

```text
zone_source_weighting
zone_boundary_selection
zone_start_from_symmetry_confluence
zone_end_from_hook_start_or_origin_boundary
zone_tradeability_score
zone_invalidation_policy
market_specific_zone_behavior
timeframe_specific_zone_behavior
dynamic_weight_regime
entry_refinement_threshold
```

## Proposed Objects

```text
PotentialZone
ZoneSourceConstraint
ZoneBoundary
ZonePromotionState
ZoneValidityState
ZoneEntryRefinement
EntryLevelExtreme
ZoneTrainingGranularity
ZoneWeightRegime
```

## Proposed Datasets

```text
potential_zone_model_v1.csv
context_to_zone_promotion_policy_v1.csv
zone_source_constraint_model_v1.csv
zone_validity_state_machine_v1.csv
zone_to_entry_refinement_policy_v1.csv
entry_level_extreme_model_v1.csv
zone_training_granularity_model_v1.csv
zone_weight_regime_model_v1.csv
market_specific_zone_policy_v1.csv
market_timeframe_zone_policy_v1.csv
```

## Proposed Fields

```text
zone_id
scenario_id
context_id
symbol
timeframe
scale_id
parent_scale_id
child_scale_id

zone_low
zone_high
zone_start_price
zone_end_price
zone_mid_price
zone_direction
zone_width
zone_boundary_source_start
zone_boundary_source_end

zone_source_constraints
zone_recipe_id
zone_family
zone_promotion_reason
zone_state
zone_validity_state

higher_timeframe_f_state
middle_timeframe_f_state
hook_completion_state
cyclehook_nd_present
cyclehook_origin_boundary
f2_ge_f1_constraint_present
f_move_completion_ratio
f2_waist_destination_present

symmetry_confluence_present
symmetry_confluence_price
symmetry_confluence_score
x_closure_present
y_closure_present
multi_sequence_closure_count

entry_refinement_required
entry_level_extreme_allowed
lower_tf_hook_closure_required
small_stop_available
limit_reversal_setup_allowed

destination_distance
destination_openness_score
optionality_score
cost_score
explosion_potential_score
zone_tradeability_score

training_scope
market_specific_weight_profile
timeframe_specific_weight_profile
dynamic_weight_regime_id
```

## Proposed Labels

```text
ZONE_CANDIDATE
POTENTIAL_ZONE
TRADABLE_ZONE
ENTRY_REFINEMENT_REQUIRED
EXTREME_ALLOWED_INSIDE_ZONE
ZONE_INVALIDATED
ZONE_EXPIRED
ZONE_DESTROYED

CONTEXT_TO_ZONE_PROMOTED
ZONE_FROM_CYCLEHOOK_ND
ZONE_FROM_HOOK_COMPLETION
ZONE_FROM_F2_GE_F1
ZONE_FROM_SYMMETRY_CONFLUENCE
ZONE_FROM_ORIGIN_BOUNDARY
ZONE_FROM_DESTINATION_STRUCTURE

ENTRY_LEVEL_EXTREME
HOOK_EXTREME
LOW_COST_HIGH_EXPLOSION_ZONE
DYNAMIC_ZONE_WEIGHT_REGIME
```

## Proposed AI Modules

```text
Potential Zone Builder
Zone Source Constraint Mapper
Context-to-Zone Promotion Model
Zone Boundary Selector
Symmetry Zone Start Detector
Hook-Origin Zone End Detector
Zone Validity Tracker
Entry-Level Extreme Router
Lower-Timeframe Entry Refinement Model
Zone Tradeability Scorer
Zone Training Granularity Router
Market-Specific Zone Learner
Market-Timeframe Zone Learner
Dynamic Zone Weight Regime Learner
```

## Architecture Consequence

Zone generation should be recipe-based and trainable.

The system should support many zone recipes, not one universal formula.

Recommended architecture:

```text
ContextState
→ PositionConstraintSet
→ ZoneRecipe candidates
→ PotentialZone objects
→ ZoneTradeabilityScorer
→ LowerTF EntryRefinement
```

Each zone must expose why it exists:

```text
zone_source_constraints
zone_recipe_id
zone_boundary_source_start
zone_boundary_source_end
```

This makes zone learning auditable.

## Open Questions

1. What exact formula defines F2 waist / midpoint?
2. Should the F2 >= F1 constraint use price distance only?
3. Should a zone created by F2 >= F1 require CycleHook ND, or can it stand alone?
4. What exact price range defines the ND-to-origin zone?
5. How should zone start from symmetry confluence be calculated?
6. Should zone end behind Hook start use a fixed point, spread, or structural buffer?
7. What exactly means the area itself is destroyed?
8. Can a zone remain valid after partial penetration?
9. Can multiple zones overlap and merge, or should they remain separate?
10. Should each zone family have its own invalidation rules?
11. Should zone training start globally or per-market first?
12. How much data is needed before market-timeframe-specific weights are trusted?
13. How should dynamic zone weight regimes be detected?
14. Should zone weight drift be learned by rolling windows?
15. Should the first implementation build zone candidates deterministically before training zone scoring?

## Attachment Index

No images were provided for this answer.
