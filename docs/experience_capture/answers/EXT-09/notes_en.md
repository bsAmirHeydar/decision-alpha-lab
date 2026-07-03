# EXT-09 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
context-priority rule
anchor-quality-secondary principle
reward-first expectancy principle
human-in-the-loop training requirement
layered branch-based research workflow
```

## Main Design Consequence

The future system should not make `extreme_anchor_node_quality` the top-level decision source.

Instead, the system should separate:

```text
context_quality
zone_potential_quality
reward_exposure_quality
anchor_node_quality
entry_execution_quality
```

Anchor quality is a secondary/refinement layer.

## Proposed Hard Rules

```text
ANCHOR_QUALITY_CANNOT_REPLACE_CONTEXT
ANCHOR_QUALITY_CANNOT_REPLACE_ZONE
WIN_RATE_CANNOT_BE_OPTIMIZED_BY_DESTROYING_REWARD
LEARNED_RULES_REQUIRE_HUMAN_REVIEW_AND_TESTING
```

## Proposed Flexible Rules

```text
anchor quality can be trained
path cleanliness can be tested
prior touches can be tested
parent-zone support can be tested
destination openness can be tested
anchor weakness can be learned
```

## Proposed Datasets

```text
extreme_anchor_node_quality_v1.csv
anchor_quality_feature_ledger_v1.csv
anchor_quality_hypothesis_test_v1.csv
human_reviewed_learned_rules_v1.csv
layered_training_branch_registry_v1.csv
algorithm_comparison_ledger_v1.csv
```

## Proposed Fields

```text
scenario_id
region_id
entry_family_type
anchor_node_id
anchor_node_level
context_quality_score
zone_potential_score
reward_exposure_score
anchor_quality_score
entry_execution_quality_score

prior_touch_count
path_cleanliness_to_node
parent_zone_support
destination_openness
stop_distance_raw
spread_to_stop_ratio
right_tail_potential
expected_r
win_rate
reward_preserved
winrate_improved_without_reward_loss

learned_rule_id
learned_rule_description
human_review_status
human_review_notes
test_status
accepted_policy_branch
rejected_policy_branch
algorithm_family
experiment_branch_id
```

## Proposed Labels

```text
ANCHOR_QUALITY_SECONDARY
CONTEXT_ZONE_REQUIRED
POTENTIAL_ZONE_FOUND
REWARD_EXPOSURE_PRIMARY
WIN_RATE_SECONDARY
ANCHOR_RULE_CANDIDATE_LEARNED
HUMAN_REVIEW_REQUIRED
TEST_REQUIRED
ACCEPTED_AFTER_TEST
REJECTED_AFTER_TEST
BRANCH_FOR_FURTHER_RESEARCH
```

## Proposed AI Modules

```text
Anchor Quality Feature Builder
Anchor Quality Discovery Model
Learned Rule Reporter
Human Review Gate
Layered Training Branch Manager
Algorithm Comparison Runner
Reward Preservation Gate
Win-Rate Improvement Without Reward Loss Gate
```

## Proposed Research Workflow

```text
1. Build NDS context and zone dataset.
2. Build Extreme anchor feature dataset.
3. Train anchor-quality discovery models.
4. Force each model to report learned rules or patterns.
5. Human reviews the learned patterns.
6. Convert approved patterns into testable hypotheses.
7. Run tests and ablations.
8. Keep accepted policies in separate branches.
9. Compare branches across algorithms and objectives.
10. Promote only NDS-compliant, reward-preserving, positive-expectancy policies.
```

## Open Questions

1. Should `extreme_anchor_node_quality` be a score, class, or both?
2. Which anchor-quality features are allowed in v1?
3. Should prior touch count be stored even if it is not trusted yet?
4. How should path cleanliness toward the node be measured in NDS terms?
5. Can parent-zone proximity improve anchor quality without becoming the main reason?
6. Can destination openness outweigh a weak anchor?
7. What defines a weak node if anchor quality is secondary?
8. Should anchor quality improve win rate only, or expected R?
9. How much reward sacrifice is unacceptable when improving win rate?
10. Should learned rules be written to Markdown automatically after every training run?
11. Should every model branch have a human decision file?
12. Which algorithms should be tested first?
13. Should anchor-quality models be trained separately for each entry family?
14. Should anchor-quality rules be symbol-specific or NDS-universal?
15. Should a model be allowed to reject a human-liked anchor if it preserves NDS and proves better through tests?

## Attachment Index

No images were provided for this answer.
