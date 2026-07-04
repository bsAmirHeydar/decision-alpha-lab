# Index Fragment — ENT-R02

## ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy

Path:

```text
docs/experience_capture/answers/ENT-R02/
```

Summary:

ENT-R02 defines the practical entry geometry after an Entry-Level Extreme. Entry is limit-based. The stop goes behind the relevant node. A small extra buffer behind the node may improve results and must be trained rather than guessed. Buy limit entry price is adjusted upward by spread. For sell limit trades, stop loss and take profit are adjusted upward by spread. If requested volume exceeds max lot, the order must be split into multiple trades. These rules should produce an ExecutionIntent for validation, not direct order sending.

Main derived architecture requirements:

```text
limit_entry_policy_v1.csv
stop_geometry_model_v1.csv
entry_buffer_policy_v1.csv
spread_adjustment_policy_v1.csv
fill_missed_replace_policy_v1.csv
execution_intent_contract_v1.csv
max_lot_split_policy_v1.csv
broker_validation_request_v1.csv
```
