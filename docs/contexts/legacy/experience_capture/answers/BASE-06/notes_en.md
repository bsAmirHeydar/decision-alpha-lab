# BASE-06 — Notes and Open Questions

## Classification

This experience should be treated as:

```text
hard-rule boundary
AI policy boundary
ontology governance rule
model acceptance rule
training scope definition
```

## Main Design Consequence

The system must have two separated layers:

```text
Layer 1 — Fixed NDS Anatomy
Layer 2 — Learnable Policy Over NDS Anatomy
```

Layer 1 is not trainable.

Layer 2 is trainable.

## Proposed Layer Separation

### Fixed Layer

```text
NDS Concept Registry
Hook Definition
Rally Definition
F-counting Definition
Node-counting Definition
X-axis/Y-axis Anatomy
Scenario Object Schema
Ontology Gate
```

### Learnable Layer

```text
Scenario Ranking
Context Power Scoring
Fractal Weighting
Ambiguity Classification
Entry Family Selection
Veto Policy
Execution Template Selection
Cancel/Replace Policy
Hedge Protection Routing
```

## Proposed Dataset Consequence

Every dataset should separate:

```text
source_state_fields
derived_policy_fields
model_prediction_fields
execution_decision_fields
```

This prevents AI outputs from being confused with NDS definitions.

## Proposed Model Manifest Requirement

Every model should declare:

```text
model_id
model_role
allowed_inputs
forbidden_inputs
nds_compliance_state
policy_layer_only
baseline_required
negative_controls_required
oos_required
ablation_required
```

## Proposed AI Modules

```text
NDS Ontology Gate
NDS Feature Validator
Policy-Layer Model Registry
Model Acceptance Gate
NDS Compliance Report Generator
```

## Proposed Acceptance States

```text
ACCEPTED_NDS_COMPLIANT
REJECTED_ONTOLOGY_VIOLATION
REJECTED_LEAKAGE_RISK
REJECTED_BASELINE_FAILURE
REJECTED_OOS_FAILURE
REJECTED_NEGATIVE_CONTROL_FAILURE
REJECTED_UNINTERPRETABLE_POLICY
WATCHLIST_NEEDS_MORE_TESTING
```

## Open Questions

1. Should the NDS concept registry be manually approved only?
2. Should AI ever suggest new NDS concepts, or only new policy uses of existing concepts?
3. How do we version Hook and Rally definitions if they ever evolve manually?
4. Should model training fail automatically if forbidden features are present?
5. Should all model outputs include a reason vector?
6. Should every accepted AI result be explainable in NDS language?
7. Should a model be allowed if it works only in one symbol but is NDS-compliant?
8. Should niche models be accepted if their scope is explicitly declared?
9. What is the minimum OOS evidence required before accepting a learnable policy?
10. What is the minimum improvement required over rule-based baseline?
11. Can AI downgrade a human-favored setup if it stays inside NDS?
12. Can AI propose hedge-protection if the original human hypothesis did not mention it for that case?
13. Should the first AI models be restricted to rank/veto only?
14. Should execution-routing models require stricter evidence than ranking models?
15. Should live execution require multiple independent model confirmations?

## Architecture Consequence

Before training AI, the project should define:

```text
NDS_CONCEPT_REGISTRY.md
MODEL_POLICY_BOUNDARY.md
MODEL_ACCEPTANCE_GATE.md
FEATURE_MANIFEST_SCHEMA.md
```

These documents will prevent the training pipeline from crossing red lines.
