---
title: "FP-I02 Reason and State Reference"
tags: [fp-i02, contract-reference]
status: normative
---
# FP-I02 Reason and State Reference

## Reference table

| Contract area | Normative meaning |
|---|---|
| `Reason registry` | 35 exact codes with category, severity, terminal, execution-blocking, and visual metadata. |
| `Candidate machine` | OBSERVED → RAW → terminal confirmed/cancelled/expired/invalid. |
| `Reference machine` | FRESH → HUNTER_SEEN → consumed/expired/superseded. |
| `WW machine` | RAW → CONFIRMED → neutralized/expired. |
| `Quota machine` | AVAILABLE → RESERVED → consumed/released; consumed blocked while Q12 is UNSET. |


## Versioning rule

All keys are exact-version contracts. Unknown versions fail closed. Any field-set or meaning change requires a new version, migration function, schema, MQL5 mirror, golden vector, and downstream handoff update.

## Authority rule

These contracts describe evidence only. They do not grant history, drawing, order, broker, position, or network authority.

## Navigation

- [[../00_FP_I02_DELIVERY_MOC|FP-I02 Delivery MOC]]
