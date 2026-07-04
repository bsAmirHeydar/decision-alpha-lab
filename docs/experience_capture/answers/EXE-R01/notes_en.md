# EXE-R01 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
execution intent boundary
fractal four-state decision pipeline
context-zone-entry conversion model
quality-based trade decision
unknown execution contract fields
```

## Core Hard Rules

```text
FOUR_STATE_VIEW_IS_FRACTAL
FRACTAL_VIEW_BECOMES_CONTEXT_ZONE_ENTRY
TRADE_DECISION_IS_BASED_ON_LAYER_QUALITIES
EXECUTION_INTENT_IS_NOT_DIRECT_ORDER_SENDING
UNKNOWN_FIELDS_MUST_NOT_BE_PREMATURELY_FROZEN
```

## Core Learnable Policies

```text
context_quality_score
zone_quality_score
entry_quality_score
aggregate_quality_score
intent_creation_threshold
quality_to_intent_permission
quality_to_risk_permission
```

## Proposed Objects

```text
FractalFourStateView
ContextLayer
ZoneLayer
EntryLayer
LayerQualityScore
AggregateQualityScore
ExecutionIntentCandidate
ExecutionIntentContractDraft
UnknownExecutionField
```

## Proposed Datasets

```text
execution_intent_contract_v1.csv
fractal_four_state_to_intent_model_v1.csv
context_zone_entry_decision_model_v1.csv
quality_based_execution_decision_v1.csv
execution_intent_unknown_fields_v1.csv
intent_creation_quality_gate_v1.csv
execution_intent_lineage_v1.csv
```

## Proposed Fields

```text
intent_id
intent_candidate_id
scenario_id
zone_id
entry_extreme_id
reason_set_id

four_state_context_id
four_state_zone_id
four_state_entry_id

context_quality_score
zone_quality_score
entry_quality_score
aggregate_quality_score

context_optionality_score
zone_optionality_score
entry_optionality_score
aggregate_optionality_score

context_risk_cost_score
zone_risk_cost_score
entry_risk_cost_score
aggregate_risk_cost_score

intent_created
intent_creation_reason
intent_blocked
intent_block_reason

field_contract_complete
unknown_fields_remaining
requires_broker_validation
requires_safety_gate
```

## Proposed Labels

```text
FRACTAL_FOUR_STATE_VIEW
CONTEXT_LAYER_FROM_FOUR_STATE
ZONE_LAYER_FROM_FOUR_STATE
ENTRY_LAYER_FROM_FOUR_STATE
QUALITY_BASED_TRADE_DECISION
EXECUTION_INTENT_CANDIDATE
INTENT_CONTRACT_INCOMPLETE
BROKER_VALIDATION_REQUIRED
DIRECT_ORDER_SEND_FORBIDDEN
```

## Proposed AI Modules

```text
Fractal Four-State Interpreter
Context-Zone-Entry Layer Builder
Layer Quality Scorer
Aggregate Quality Gate
ExecutionIntent Candidate Builder
Intent Contract Completion Assistant
Intent Safety Boundary Checker
```

## Architecture Consequence

ExecutionIntent should not be designed from broker fields first.

It should be designed from NDS lineage first.

Recommended flow:

```text
Fractal Four-State View
→ Context Layer
→ Zone Layer
→ Entry Layer
→ Layer Quality Scores
→ Aggregate Quality Gate
→ ExecutionIntentCandidate
→ Safety/Broker Validation
```

This keeps execution tied to NDS anatomy and prevents raw order-first design.

## Open Questions

1. What exact fields must be mandatory in ExecutionIntent?
2. Which fields belong to NDS and which belong to broker validation?
3. How should structural price and adjusted price be represented?
4. How should spread adjustment be stored?
5. How should stop buffer be stored?
6. Should risk budget be part of the intent or attached by validator?
7. Should volume be in the intent or computed later?
8. Should split orders be child intents or child orders?
9. Should cancel, replace, and missed rules be inside the intent or linked by policy IDs?
10. What exact condition makes an intent unsafe?
11. Should the first implementation be an `ExecutionIntentCandidate` only?
12. Should all incomplete fields be explicitly marked as unknown rather than guessed?

## Attachment Index

No images were provided for this answer.
