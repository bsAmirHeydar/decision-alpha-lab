# ENT-R01 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
entry-level Extreme definition
Hook Extreme versus Entry Extreme taxonomy
Extreme Near Death entry model
zone-to-entry refinement policy
entry risk geometry model
convex entry compression model
```

## Core Hard Rules

```text
HOOK_EXTREME_AND_ENTRY_EXTREME_ARE_DIFFERENT
HOOK_EXTREME_IS_OPPOSITE_EXTREME_INSIDE_HOOK
ENTRY_EXTREME_IS_EXTREME_NEAR_DEATH
ENTRY_EXTREME_EXISTS_FOR_SMALLER_STOP
ENTRY_EXTREME_EXISTS_FOR_MORE_CONVEX_EXPLOITATION
ENTRY_EXTREME_COMPRESSES_COST_NOT_REWARD_SOURCE
```

## Core Learnable Policies

```text
how near to death is near enough
entry stop buffer
entry extreme validity threshold
entry cost threshold
when entry extreme outside zone should be ignored
best lower-timeframe scale for entry refinement
entry repricing after missed limit
```

## Proposed Objects

```text
HookExtreme
EntryLevelExtreme
ExtremeNearDeathEntry
EntryDeathBoundary
EntryRiskGeometry
EntryAuthorizationState
ZoneEntryRefinement
```

## Proposed Datasets

```text
entry_level_extreme_model_v1.csv
extreme_near_death_entry_model_v1.csv
hook_extreme_vs_entry_extreme_taxonomy_v1.csv
zone_to_entry_refinement_policy_v1.csv
limit_entry_authorization_v1.csv
entry_invalidation_policy_v1.csv
entry_risk_geometry_v1.csv
entry_cost_compression_model_v1.csv
```

## Proposed Fields

```text
entry_extreme_id
scenario_id
zone_id
parent_context_id
entry_scale_id
entry_timeframe
direction

entry_cyclehook_id
entry_cyclehook_origin_node_id
entry_death_boundary_price
entry_near_death_distance
entry_near_death_ratio
entry_extreme_price
entry_extreme_time

hook_extreme_id
hook_extreme_price
hook_extreme_role
is_hook_extreme
is_entry_extreme
is_extreme_near_death

inside_parent_zone
parent_zone_low
parent_zone_high
parent_zone_state

entry_price
stop_price
invalidation_price
stop_distance
spread_adjusted_stop_distance
broker_min_stop_ok
tick_size_ok
entry_cost_score
cost_compression_score

reward_destination_id
reward_distance
optionality_score
convexity_score
cost_to_potential_ratio

entry_authorization_state
limit_entry_allowed
entry_veto_reason
entry_invalidation_reason
```

## Proposed Labels

```text
HOOK_EXTREME
ENTRY_LEVEL_EXTREME
EXTREME_NEAR_DEATH
ENTRY_EXTREME_INSIDE_ZONE
ENTRY_EXTREME_OUTSIDE_ZONE
LIMIT_ENTRY_ALLOWED
ENTRY_COST_COMPRESSED
ENTRY_EXTREME_VETOED
ENTRY_EXTREME_INVALIDATED
ENTRY_SCALE_DEATH_BOUNDARY_CROSSED
```

## Proposed AI Modules

```text
Hook Extreme Classifier
Entry-Level Extreme Detector
Extreme Near Death Scorer
Zone-to-Entry Refinement Router
Entry Risk Geometry Builder
Entry Cost Compression Scorer
Limit Entry Authorization Model
Entry Invalidation Tracker
Entry Repricing Model
```

## Architecture Consequence

The system should not reuse one `extreme` field for both meanings.

Recommended separation:

```text
hook_extreme_* fields
entry_extreme_* fields
```

This prevents ontology contamination.

Hook Extreme belongs to structural anatomy.

Entry Extreme belongs to execution refinement.

## Open Questions

1. What exact numeric or adaptive threshold defines "excessively close to death"?
2. Should entry near-death be measured in points, percent of CycleHook range, R distance, or zone width?
3. Should entry stop always sit behind the entry-scale death boundary?
4. What buffer is required beyond the death boundary?
5. Should spread and broker minimum stop distance be handled inside entry model or only execution validator?
6. Can Entry-Level Extreme be valid outside a Potential Zone for research logging but not execution?
7. What lower timeframe should be used for entry refinement relative to the parent zone timeframe?
8. Should the lower-timeframe CycleHook need X closure, Y closure, or only near-death?
9. Can multiple Entry-Level Extremes inside one zone all remain live?
10. Should entry-level Extreme selection be deterministic first and trained later?
11. What exactly invalidates a missed limit order?
12. Can a missed Entry-Level Extreme be repriced into a new one?
13. How should entry-level Extreme performance be measured separately from zone quality?
14. Should entry-level Extreme optimize for smallest stop even if fill probability becomes low?
15. What is the minimum reward/optionality required for an otherwise excellent Entry-Level Extreme?

## Attachment Index

No images were provided for this answer.
