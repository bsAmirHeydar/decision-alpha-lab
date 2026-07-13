---
title: "FP-I02 Identity Field Matrix"
tags: [fp-i02, contract-reference]
status: normative
---
# FP-I02 Identity Field Matrix

## Reference table

| Contract area | Normative meaning |
|---|---|
| `Context epoch` | Decision set, profile, pair, semantic/dependency/registry hashes, authority, open decisions, resolved timeframe. |
| `Window` | Context, pair, kind/scope, day/week, interval, offset, timezone, data revision. |
| `Candidate` | Epoch, relation, direction, roles, windows, side, hunt time, deadline, timeframe, offset, revision. |
| `Signal` | Candidate, confirmation, relation/direction/roles, times, semantic config. |
| `Projection` | Signal, projection config, object role, chart instance. |


## Versioning rule

All keys are exact-version contracts. Unknown versions fail closed. Any field-set or meaning change requires a new version, migration function, schema, MQL5 mirror, golden vector, and downstream handoff update.

## Authority rule

These contracts describe evidence only. They do not grant history, drawing, order, broker, position, or network authority.

## Navigation

- [[../00_FP_I02_DELIVERY_MOC|FP-I02 Delivery MOC]]
