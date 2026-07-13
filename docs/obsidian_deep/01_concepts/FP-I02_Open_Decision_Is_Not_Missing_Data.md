---
title: "FP-I02 Open Decision Is Not Missing Data"
tags: [atomic-concept, exp0019, fp-i02]
status: canonical
---
# FP-I02 Open Decision Is Not Missing Data

## Definition

FP-DEC-012 is explicitly QuotaConsumptionPolicy.UNSET. It is a governance state that blocks live consumption, not an absent field to default.

## Why it matters

Faerie Protocol is implemented across Python research/validation surfaces and MQL5 indicator/EA surfaces. Explicit identity and closed contracts prevent the same economic event from being represented differently after restart, chart changes, visual changes, or data repair.

## Operational consequence

- Include every behavior-bearing field in semantic identity.
- Keep projection and operational fields outside signal identity.
- Reject unknown enum, reason, relation, version, or transition.
- Preserve source and parent lineage.
- Rebuild under a new identity after data/config revision.

## Related implementation

- `fp_i02_kernel/contracts.py`
- `fp_i02_kernel/identity.py`
- `fp_i02_kernel/config.py`
- `fp_i02_kernel/registry.py`
- [[../../execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i02/00_FP_I02_DELIVERY_MOC|FP-I02 Delivery MOC]]
