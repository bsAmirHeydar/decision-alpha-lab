# EXE-R02 — Notes and Open Questions

## Classification

This answer should be treated as:

```text
mechanical broker validator
deterministic send gate
broker constraint checklist
order adjust or veto policy
execution safety boundary
non-NDS mechanical layer
```

## Core Hard Rules

```text
BROKER_VALIDATION_IS_MECHANICAL
BROKER_RULES_ARE_CLEAR_AND_DETERMINISTIC
BROKER_VALIDATOR_IS_NOT_NDS_REASONING
BROKER_VALIDATOR_MUST_NOT_CHANGE_SCENARIO_ZONE_OR_ENTRY_LOGIC
MECHANICAL_ADJUSTMENT_IS_ALLOWED_ONLY_IF_STRUCTURE_REMAINS_INTACT
BROKER_CONSTRAINT_FAILURE_CAN_VETO_INTENT
```

## Core Learnable Policies

Strictly speaking, this layer is not a learning layer.

However, operational thresholds can be configured or empirically reviewed:

```text
max_allowed_spread
max_allowed_cost_drift
safe_rounding_tolerance
safe_volume_adjustment_tolerance
margin_adjustment_policy
```

These are execution configuration policies, not NDS ontology learning.

## Proposed Objects

```text
BrokerConstraintSnapshot
MechanicalExecutionValidator
SendGate
BrokerValidationResult
MechanicalAdjustment
ExecutionVetoReason
ValidatedExecutionRequest
```

## Proposed Datasets

```text
broker_validation_model_v1.csv
send_gate_policy_v1.csv
mechanical_execution_validator_v1.csv
broker_constraint_checklist_v1.csv
order_adjust_or_veto_policy_v1.csv
execution_veto_reason_taxonomy_v1.csv
broker_validation_audit_ledger_v1.csv
```

## Proposed Fields

```text
intent_id
intent_candidate_id
symbol
order_type
direction

structural_entry_price
structural_stop_price
structural_take_profit
adjusted_entry_price
adjusted_stop_price
adjusted_take_profit

digits
tick_size
point_size
price_normalized
price_normalization_delta

volume_requested
volume_normalized
volume_step
min_lot
max_lot
lot_split_required
child_order_count

min_stop_distance
stop_distance_structural
stop_distance_adjusted
stop_valid_after_broker_rules

commission_estimate
spread_current
spread_allowed
spread_vetoed

margin_required
margin_available
margin_valid
margin_adjusted
margin_vetoed

freeze_level
trade_mode
market_session_open
symbol_trade_allowed
order_type_supported
filling_mode_supported
expiration_supported

mechanical_adjustment_applied
mechanical_adjustment_reason
mechanical_adjustment_preserves_structure
send_gate_state
send_gate_veto_reason
validated_request_created
```

## Proposed Labels

```text
BROKER_VALIDATION_MECHANICAL
PRICE_NORMALIZED_TO_TICK
VOLUME_NORMALIZED_TO_LOT_STEP
MAX_LOT_SPLIT_REQUIRED
MIN_STOP_DISTANCE_VALID
MIN_STOP_DISTANCE_VETO
MARGIN_VALID
MARGIN_VETO
SPREAD_VALID
SPREAD_VETO
MARKET_CLOSED_VETO
TRADE_MODE_VETO
FREEZE_LEVEL_VETO
SEND_GATE_APPROVED
SEND_GATE_ADJUSTED
SEND_GATE_VETOED
STRUCTURE_BREAKING_ADJUSTMENT_VETOED
```

## Proposed AI Modules

This layer should not require AI for market reasoning.

Possible non-reasoning modules:

```text
Broker Constraint Reader
Mechanical Validation Engine
Price/Volume Normalizer
Mechanical Adjust-or-Veto Router
Send Gate Auditor
```

## Architecture Consequence

Broker validation should be built after ExecutionIntentCandidate but before any broker request.

Recommended flow:

```text
ExecutionIntentCandidate
→ Safety Boundary Check
→ BrokerConstraintSnapshot
→ MechanicalExecutionValidator
→ Mechanical Adjust or Veto
→ SendGate
→ ValidatedExecutionRequest
```

If adjustment would change NDS structure, the validator should veto instead of silently modifying the trade.

## Open Questions

1. Which broker constraints are mandatory in the first implementation?
2. What is the maximum allowed price normalization drift?
3. What is the maximum allowed volume mismatch due to lot step?
4. Should insufficient margin trigger volume reduction or full veto?
5. What spread threshold should be used initially?
6. Should max-lot split be handled here or earlier in ExecutionIntent?
7. Should all broker constraints be snapshotted for every intent?
8. Should rejected orders feed a separate execution-audit dataset?
9. Should the first implementation be no-send audit-only?
10. How should mechanical validation interact with risk-budget matching from RSK-R02?

## Attachment Index

No images were provided for this answer.
