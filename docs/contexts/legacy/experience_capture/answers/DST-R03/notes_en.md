# DST-R03 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
NDS-only destination lifecycle
destination repricing policy
destination completion policy
destination consumption model
destination weight update model
destination audit ledger
destination ontology boundary
```

## Core Hard Rules

```text
DESTINATION_USES_NDS_ANATOMY_ONLY
DESTINATION_USES_SAME_WEIGHTS_AS_NDS
DESTINATION_USES_SAME_LOGICS_AS_NDS
NO_EXTERNAL_DESTINATION_LOGIC
NO_GENERIC_TARGET_MODEL_AS_NATIVE_DESTINATION
DESTINATION_REPRICING_MUST_BE_EXPLAINED_BY_NDS_STRUCTURE
DESTINATION_COMPLETION_MUST_BE_EXPLAINED_BY_NDS_STRUCTURE
```

## Core Learnable Policies

```text
destination_weight_update
destination_touch_vs_pass_through_completion
destination_consumption_threshold
destination_openness_decay
destination_candidate_priority
opposite_destination_effect
destination_archival_rules
destination_family_performance
```

## Proposed Objects

```text
DestinationCandidate
DestinationCandidateSet
DestinationLifecycleState
DestinationWeightUpdate
DestinationRepricingEvent
DestinationCompletionEvent
DestinationConsumptionEvent
DestinationAuditRecord
NDSOnlyDestinationRule
```

## Proposed Datasets

```text
destination_state_machine_v1.csv
destination_repricing_policy_v1.csv
destination_completion_policy_v1.csv
destination_consumption_model_v1.csv
nds_only_destination_lifecycle_v1.csv
destination_weight_update_model_v1.csv
destination_audit_ledger_v1.csv
opposite_destination_effect_model_v1.csv
```

## Proposed Fields

```text
destination_candidate_id
destination_set_id
scenario_id
zone_id
position_id
parent_hook_id
parent_cyclehook_id
source_scale_id
source_timeframe

destination_state
previous_destination_state
state_transition_reason
destination_family
destination_source

nds_anatomy_source
nds_weight_source
nds_logic_source
external_logic_used
external_logic_vetoed

destination_weight
previous_destination_weight
weight_delta
weight_update_reason

destination_openness_score
previous_openness_score
openness_delta
profit_path_open
profit_path_closed

repriced
repricing_reason
old_destination_price
new_destination_price
old_destination_zone_low
old_destination_zone_high
new_destination_zone_low
new_destination_zone_high

consumed
consumption_reason
completed
completion_reason
invalidated
invalidation_reason
historical
archive_reason

opposite_destination
opposite_destination_effect
partial_exit_triggered
full_exit_triggered
runner_kept_open
```

## Proposed Labels

```text
NDS_ONLY_DESTINATION
DESTINATION_USES_INTERNAL_ANATOMY
DESTINATION_WEIGHT_UPDATED
DESTINATION_REPRICED_BY_NDS_STRUCTURE
DESTINATION_COMPLETED_BY_NDS_LOGIC
DESTINATION_CONSUMED_BY_NDS_LOGIC
DESTINATION_INVALIDATED_BY_NDS_LOGIC
EXTERNAL_DESTINATION_LOGIC_VETOED
DESTINATION_ARCHIVED
OPPOSITE_DESTINATION_REGISTERED
```

## Proposed AI Modules

```text
NDS-Only Destination Validator
Destination Weight Update Engine
Destination Repricing Engine
Destination Completion Detector
Destination Consumption Detector
Destination Openness Decay Model
Opposite Destination Effect Model
Destination Lifecycle Auditor
Destination Family Performance Evaluator
```

## Architecture Consequence

The destination layer must not become a generic target engine.

Recommended flow:

```text
NDS State Update
→ detect destination candidate changes
→ update destination weights using NDS logic
→ reprice or complete destination if NDS anatomy requires
→ update profit openness
→ feed exit policy
→ audit every transition
```

Any destination output should be explainable by NDS-native objects and weights.

## Open Questions

1. Which NDS weights should be reused directly for destination scoring?
2. Should destination weight equal scenario weight, or have a separate derived score?
3. What exact NDS event causes destination repricing?
4. Does a destination complete on touch, penetration, or structural fulfillment?
5. Can a destination be consumed without price touching it?
6. How should destination openness decay be measured?
7. How should opposite destinations affect active positions?
8. Should destination lifecycle update on every tick, bar close, or structural event?
9. Should a repriced destination keep the same ID or create a new candidate?
10. Should completed destinations remain in candidate sets as historical nodes?
11. How should destination-family performance be trained?
12. Can AI propose a destination only if it maps to existing NDS anatomy?
13. What is the minimum explanation required for a destination transition?
14. Should destination transitions trigger partial exit candidates?
15. Should the first implementation be audit-only with no execution use?

## Attachment Index

No images were provided for this answer.
