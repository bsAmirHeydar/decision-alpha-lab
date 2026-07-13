---
title: "FP-I02 Public Contract Reference"
tags: [fp-i02, contract-reference]
status: normative
---
# FP-I02 Public Contract Reference

## Reference table

| Contract area | Normative meaning |
|---|---|
| `SymbolPair` | Pair display order and order-invariant pair identity. |
| `WindowKey` | Canonical A/L/N/W interval identity. |
| `WindowRecord` | Symbol-local range and completeness evidence. |
| `ReferenceSideKey/Record` | Side-specific reference identity and lifecycle. |
| `HuntFact` | M1-aligned touch/hunt fact. |
| `DivergenceCandidate` | Pre-confirmation asymmetric setup. |
| `ConfirmationEvent` | Closed host-candle result. |
| `ConfirmedSignal` | Immutable confirmed event identity. |
| `WWContextRecord` | Weekly lifecycle evidence. |
| `QuotaKey/Record` | Pair-session entitlement state. |
| `ReasonEvidence` | Reason-code-bearing child evidence. |
| `HealthStatus` | READY/DEGRADED/BLOCKED evidence. |
| `ContextManifestRecord` | Context epoch root identity. |


## Versioning rule

All keys are exact-version contracts. Unknown versions fail closed. Any field-set or meaning change requires a new version, migration function, schema, MQL5 mirror, golden vector, and downstream handoff update.

## Authority rule

These contracts describe evidence only. They do not grant history, drawing, order, broker, position, or network authority.

## Navigation

- [[../00_FP_I02_DELIVERY_MOC|FP-I02 Delivery MOC]]
