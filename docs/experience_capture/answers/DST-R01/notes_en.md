# DST-R01 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
destination taxonomy
destination candidate set
open one-two destination model
higher Hook counting destination model
trainable destination policy
profit openness destination model
destination uncertainty model
```

## Core Hard Rules

```text
DESTINATION_LOGIC_IS_NOT_FULLY_SOLVED
DESTINATION_SHOULD_SUPPORT_CANDIDATE_SETS
DESTINATION_CAN_EMERGE_FROM_LATER_F_COUNTING
OPEN_ONE_TWO_CAN_BE_A_DESTINATION_CANDIDATE
HIGHER_HOOK_COUNTING_CAN_CREATE_DESTINATION_CANDIDATES
PROFIT_OPENNESS_IS_A_DESTINATION_OBJECTIVE
DESTINATION_POLICY_NEEDS_TRAINING
```

## Core Learnable Policies

```text
destination_candidate_weight
destination_candidate_priority
destination_confidence
destination_repricing
destination_family_performance
open_one_two_reach_probability
higher_hook_destination_quality
profit_openness_preservation
when_destination_should_trigger_partial_exit
when_destination_should_not_close_full_position
```

## Proposed Objects

```text
DestinationCandidate
DestinationCandidateSet
FCountingDestination
OpenOneTwoDestination
HigherHookCountingDestination
DestinationWeight
DestinationConfidence
DestinationOpenness
DestinationTrainingTarget
```

## Proposed Datasets

```text
destination_taxonomy_v1.csv
open_one_two_destination_model_v1.csv
higher_hook_counting_destination_model_v1.csv
destination_candidate_set_v1.csv
destination_trainable_policy_v1.csv
profit_openness_destination_model_v1.csv
destination_uncertainty_model_v1.csv
destination_family_performance_v1.csv
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
source_timeframe
source_scale_id

destination_family
destination_source
is_f_counting_destination
is_open_one_two_destination
is_higher_hook_counting_destination

f_count_id
open_one_two_id
higher_hook_count_id
path_structure_id

destination_price
destination_zone_low
destination_zone_high
destination_time_created
destination_weight
destination_confidence
destination_openness_score
profit_openness_preserved
trainable_destination_policy_id

is_dynamic
created_after_entry
repriced
consumed
completed
invalidated

reached
reach_time
exit_used
partial_exit_triggered
full_exit_triggered
runner_kept_open
```

## Proposed Labels

```text
DESTINATION_CANDIDATE
F_COUNTING_DESTINATION
OPEN_ONE_TWO_DESTINATION_CANDIDATE
HIGHER_HOOK_COUNTING_DESTINATION
DESTINATION_CREATED_AFTER_ENTRY
DESTINATION_TRAINABLE
DESTINATION_UNCERTAIN
PROFIT_OPENNESS_DESTINATION
DESTINATION_WEIGHT_UPDATED
DESTINATION_REACHED
DESTINATION_CONSUMED
```

## Proposed AI Modules

```text
Destination Candidate Builder
F-Counting Destination Detector
Open One-Two Destination Detector
Higher Hook Counting Destination Model
Destination Weighting Model
Destination Openness Scorer
Destination Repricing Engine
Destination Family Performance Evaluator
Profit Openness Destination Policy Learner
```

## Architecture Consequence

The destination layer should not output one fixed final target only.

Recommended flow:

```text
Scenario / Position
→ observe path structure
→ detect later F-counting
→ detect open one-and-two candidates
→ detect higher Hook internal counting candidates
→ build DestinationCandidateSet
→ score profit openness
→ train destination family behavior
```

Destination candidates should feed DST-R02 exit policy, but should not force full exit by default.

## Open Questions

1. What exact structure qualifies as an open one-and-two destination?
2. Is open one-and-two always a magnet candidate or only under higher Hook conditions?
3. How should timing uncertainty be represented?
4. How should later F-counting update existing destination candidates?
5. Can a destination candidate appear after entry and change exit policy?
6. How should destination confidence be calculated?
7. Should destination candidates be ordered, tree-based, or graph-based?
8. How should parent Hook counting and child path counting be linked?
9. What makes a destination too close and harmful to optionality?
10. When should a destination trigger partial exit rather than full exit?
11. How should destination-family performance be trained per market/timeframe?
12. Can a destination candidate in the opposite direction reduce profit openness?
13. How should consumed destinations remain in the ledger?
14. What minimum sample is needed to trust a destination family?
15. Should the first implementation log all destination candidates without using them for execution?

## Attachment Index

No images were provided for this answer.
