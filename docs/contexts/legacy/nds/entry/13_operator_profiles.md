---
title: NDS Entry Operator Profiles
status: active
version: 1.0.0
---
# NDS Entry Operator Profiles

## Profile 0 — Pre-Canon Observation — default

```text
ContractProfile = PRE_CANON_BLOCKED
DirectionPolicy = UNRESOLVED
OrderModel = UNRESOLVED
StopModel = UNRESOLVED
TargetModel = UNRESOLVED
ZoneCanonLocked = false
TradeContractLocked = false
CommandPreviewOnly = true
```

Purpose: verify that valid Hook structure reaches the pipeline and that all unresolved contracts block explicitly.

## Profile 1 — Diagnostic Manual Geometry

```text
ContractProfile = DIAGNOSTIC_MANUAL_GEOMETRY
DirectionPolicy = explicitly selected
OrderModel = explicitly selected
StopModel = MANUAL_DIAGNOSTIC or selected research model
TargetModel = MANUAL_DIAGNOSTIC or selected research model
RequireTradeContractLocked = false
Manual Zone/entry/stop/target = supplied
CommandPreviewOnly = true
```

Purpose: test downstream Setup, Plan, CSV, and Command contracts. Never interpret as canonical or tradable.

## Profile 2 — Canonical Adapter — reserved

```text
ContractProfile = CANONICAL_ZONE_ADAPTER
ZoneCanonLocked = true
TradeContractLocked = true
CommandPreviewOnly = true
```

This profile remains blocked until `FP_NDSBuildCanonicalZoneAdapter` is implemented and validated.

## Profile 3 — Future execution

Not implemented in this package. Live execution must use a separate EA deployment profile and independent broker/risk authorization.
