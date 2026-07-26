---
type: training_contract
title: Hook Validity Dataset Contract
status: canonical_draft
---
# Hook Validity Dataset Contract

Each hook-zone event should include enough fields to test the validity filter.

## Minimal Fields

```text
hook_id
hook_validity
hook_validity_type
previous_hook_id
shared_node_id
f3_id
f3_direction
hook_direction
zone_id
zone_width
entry_price
stop_price
touch_time
mfe
mae
mfe_mae_ratio
time_to_expansion
path_smoothness
invalid_reason
```

## Primary Objective

Measure whether valid hooks generate better zones than invalid hook-like structures.
