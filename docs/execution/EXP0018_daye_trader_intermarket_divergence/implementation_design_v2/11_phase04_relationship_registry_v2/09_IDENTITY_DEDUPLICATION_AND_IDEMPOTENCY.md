---
id: EXP0018-P04-IDENTITY
title: "P04 Identity, Deduplication, and Idempotency"
type: identity-contract
status: active
project: EXP0018
phase: P04
---
# Identity and Deduplication

Opportunity identity:

```text
EXP0018|P04|<RELATIONSHIP_ID>|<CURRENT_PERIOD_INSTANCE_ID>|<REFERENCE_PERIOD_INSTANCE_ID>
```

No price, bar index, processing timestamp, or random value is part of identity. Reprocessing the same store yields the same IDs. Duplicate opportunity IDs are critical failures and terminate resolution rather than being silently overwritten.
