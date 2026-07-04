# DATA-R03 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
layered training curriculum
knowledge consolidation policy
fractal context training
fractal zone training
single-timeframe entry training
human-inspectable model learning
training as capital
layer dependency model
```

## Core Hard Rules

```text
TRAINING_MUST_BE_LAYERED
TRAIN_CONTEXT_FIRST
TRAIN_ZONE_AFTER_CONTEXT
TRAIN_ENTRY_AFTER_CONTEXT_AND_ZONE
CONTEXT_IS_FRACTAL
ZONE_IS_FRACTAL
ENTRY_IS_SINGLE_TIMEFRAME
TRAINED_KNOWLEDGE_MUST_BE_PERSISTED
DO_NOT_RESTART_FROM_ZERO_EACH_TIME
LEARNED_KNOWLEDGE_MUST_BE_HUMAN_INSPECTABLE
EACH_COMPLETED_LAYER_SHOULD_BECOME_REUSABLE_INFRASTRUCTURE
```

## Core Learnable Policies

```text
context_family_quality
context_error_taxonomy
context_consolidation_threshold
zone_family_quality
zone_dependency_on_context
zone_consolidation_threshold
entry_family_quality
entry_dependency_on_context_zone
knowledge_freeze_threshold
knowledge_revision_policy
algorithm_optimization_policy
```

## Proposed Objects

```text
LayeredTrainingCurriculum
TrainingLayer
ContextTrainingStage
ZoneTrainingStage
EntryTrainingStage
TrainedKnowledgeArtifact
KnowledgeConsolidationRecord
KnowledgeFreezeState
HumanInspectionReport
LayerDependencyGraph
AlgorithmOptimizationReport
```

## Proposed Datasets

```text
layered_training_curriculum_v1.csv
context_training_stage_v1.csv
zone_training_stage_v1.csv
entry_training_stage_v1.csv
trained_knowledge_registry_v1.csv
knowledge_consolidation_policy_v1.csv
knowledge_freeze_state_v1.csv
human_inspection_training_report_v1.csv
layer_dependency_model_v1.csv
algorithm_optimization_report_v1.csv
context_error_taxonomy_v1.csv
zone_error_taxonomy_v1.csv
entry_error_taxonomy_v1.csv
```

## Proposed Fields

```text
training_layer_id
training_layer_name
layer_order
layer_role
is_fractal_layer
is_single_timeframe_layer
depends_on_layer_ids

training_status
training_started_at
training_completed_at
consolidation_status
freeze_state
version
supersedes_version
is_reusable_infrastructure

input_dataset_id
output_artifact_id
model_family
algorithm_id
feature_set_id
label_set_id

context_quality_score
zone_quality_score
entry_quality_score
layer_error_rate
layer_confidence_score
sample_size
oos_score
stability_score

human_readable_summary_path
known_strengths
known_weaknesses
common_errors
manual_corrections
algorithm_improvements
review_status
approved_by_user

downstream_layers_allowed
downstream_usage_notes
revision_required
deprecation_reason
```

## Proposed Labels

```text
LAYER_CONTEXT
LAYER_ZONE
LAYER_ENTRY
CONTEXT_FRACTAL_LAYER
ZONE_FRACTAL_LAYER
ENTRY_SINGLE_TIMEFRAME_LAYER
KNOWLEDGE_CONSOLIDATED
KNOWLEDGE_FROZEN
KNOWLEDGE_REVIEW_REQUIRED
REUSABLE_INFRASTRUCTURE
DOWNSTREAM_DEPENDENCY_APPROVED
MODEL_LEARNING_INSPECTABLE
```

## Proposed AI Modules

```text
Layered Training Orchestrator
Context Training Engine
Context Knowledge Consolidator
Zone Training Engine
Zone Knowledge Consolidator
Entry Training Engine
Entry Knowledge Consolidator
Human-Readable Learning Reporter
Layer Error Analyzer
Algorithm Optimization Loop
Knowledge Registry Manager
```

## Architecture Consequence

The training system should not begin with an end-to-end AI attempting to trade directly.

Recommended flow:

```text
Build Context Training Dataset
→ Train Context Layer
→ Produce Human Inspection Report
→ Correct / Optimize
→ Consolidate Context Knowledge
→ Freeze Context Baseline
→ Train Zone Layer using Context Baseline
→ Consolidate Zone Knowledge
→ Train Entry Layer using Context + Zone Baselines
→ Consolidate Entry Knowledge
```

This is consistent with the user's infrastructure-first philosophy.

## Open Questions

1. What exact targets should context training learn first?
2. What makes context knowledge "complete enough" to freeze?
3. Should frozen context knowledge be editable only through a formal revision branch?
4. What reports does the user need to understand what context learned?
5. What types of context errors should be tagged manually?
6. Which algorithms should be compared in the first context training stage?
7. How should zone training consume context knowledge?
8. What makes zone knowledge complete enough to freeze?
9. What exact timeframe should entry training use?
10. Can entry training ever use multiple timeframes, or is it strictly one?
11. How should knowledge artifacts be versioned?
12. How should a later layer reveal flaws in an earlier frozen layer?
13. Should knowledge be frozen globally or per market/timeframe?
14. Should consolidated knowledge be stored as models, rules, reports, or all three?
15. What is the first minimal context-training experiment?

## Attachment Index

No images were provided for this answer.
