# BASE-04 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
ontology boundary rule
AI input restriction
dataset feature gate
label-design constraint
anti-contamination principle
```

## Main Design Consequence

Every future dataset, model, feature, label, and execution reason must pass an ontology filter.

The system must not allow external concepts to enter silently.

## Proposed Ontology Gate

```text
NDS_ONTOLOGY_GATE
```

Gate states:

```text
NDS_ALLOWED
NDS_TRANSLATION_REQUIRED
NDS_REJECTED
```

## Proposed Feature Manifest Requirement

Every future dataset should include a feature manifest.

Each feature should declare:

```text
feature_name
feature_family
nds_concept_source
allowed_state
translation_required
rejected_reason
```

## Proposed Forbidden Feature Families

```text
indicator_features
ict_features
generic_ta_features
candle_pattern_features
time_of_day_features
day_of_week_features
artificial_horizon_features
raw_prediction_features
```

## Proposed Allowed Feature Families

```text
hook_features
rally_features
f_counting_features
node_counting_features
x_axis_features
y_axis_features
fractal_context_features
scenario_features
execution_geometry_features
nds_reason_vector_features
```

## Proposed Dataset Consequence

Future datasets should include an NDS ontology manifest:

```text
dataset_feature_manifest_v1.csv
```

Possible columns:

```text
dataset_name
feature_name
feature_family
nds_source_concept
allowed_state
notes
```

## Proposed AI Modules

```text
NDS Ontology Gate
Feature Manifest Validator
Reason Vector Validator
Dataset Contamination Checker
Label Ontology Checker
```

## Open Questions

1. Are spread, commission, and slippage allowed as execution-cost fields even though they are not market-anatomy concepts?
2. Is raw price allowed only as geometry, or can it become a feature directly?
3. Are volume/tick-volume fields forbidden by default?
4. Can session information ever be allowed if it is used only for execution permission rather than signal logic?
5. Can statistical diagnostics be used for evaluation even if they are not part of the trading ontology?
6. If an external concept resembles an NDS concept, should it be rejected or translated manually?
7. Who has authority to approve a new NDS concept?
8. Should each new AI model include an ontology-compliance report?
9. Should each backtest report explicitly list forbidden concepts that were not used?
10. Should NDS have a formal glossary and version number?

## Architecture Consequence

Before building AI, the project needs a formal NDS concept registry:

```text
NDS_CONCEPT_REGISTRY.md
```

Future implementation path:

```text
NDS concept registry
feature manifest
ontology gate
dataset contamination checker
AI input validator
```
