---
id: EXP0018-P04-REGISTRY-CONTRACT
title: "P04 Canonical Registry Contract"
type: data-contract
status: active
project: EXP0018
phase: P04
---
# Canonical Registry Contract

Each record contains:

```text
schema_version
relationship_id
source_alias
family
selector
current_period_id/code
reference_period_id/code
is_major
chart_label
enabled_by_default
implementation_ready
doctrine_status
blocker_decision_id
source_authority
notes
```

Cardinality is invariant: 22 total, 6 major, 16 minor, 20 implementation-ready, 2 blocked. Duplicate IDs or aliases are critical failures. Registry order is stable and is not used as business identity.
