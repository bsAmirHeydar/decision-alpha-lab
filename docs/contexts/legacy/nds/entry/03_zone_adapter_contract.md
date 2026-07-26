---
title: NDS Zone Adapter Contract
status: adapter_ready_canon_pending
version: 1.0.0
---
# NDS Zone Adapter Contract

## 1. Purpose

The Zone Adapter is the single seam where the final Hook/Zone questionnaire will become executable geometry.

```text
FP_NDSBuildCanonicalZoneAdapter(...)
```

Until the Zone Canon is locked, this function deliberately returns:

```text
NDS_ZONE_CANON_ADAPTER_PENDING
```

## 2. Why the adapter is isolated

Zone logic must not be distributed across:

- Hook classification;
- Setup selection;
- risk calculation;
- command construction;
- rendering;
- broker validation.

A single adapter allows the Zone Canon to change without rewriting every downstream layer.

## 3. Required canonical output

The final adapter must populate:

```text
zone_id
source_mode
lower_price
upper_price
width
entry_edge_price
death_edge_price
planned_entry_price
planned_stop_price
planned_target_price
boundaries_valid
directional_geometry_valid
canonical = true
```

## 4. Required future input evidence

The adapter should receive or reconstruct:

```text
Hook origin
Hook crown
Hook terminal
Death boundary
validity family
parent Hook lineage
opposing F3 lineage
sequence nodes
bar-index timestamps
multi-timeframe parent/child context
Zone lifecycle state
```

## 5. Diagnostic manual profile

The code includes:

```text
FP_NDS_ENTRY_PROFILE_DIAGNOSTIC_MANUAL_GEOMETRY
```

This profile accepts manually supplied Zone, entry, stop, and target prices for testing downstream contracts. Every row is marked:

```text
canonical = false
DIAGNOSTIC_MANUAL_GEOMETRY
```

It exists to test state transitions and exports. It is not a substitute for the Zone Canon.

## 6. Canon locks

Canonical operation requires explicit locks:

```text
InpNDSEntryZoneCanonLocked = true
InpNDSEntryTradeContractLocked = true
```

The flags do not themselves make the rules correct. They record that the associated documents and implementation have passed review. A release checklist must verify the referenced Canon version.

## 7. Zone lifecycle not yet implemented

The current adapter does not claim to implement:

```text
birth
activation
touch
consumption
weakening
invalidation
expiration
parent-child refinement
```

These will become a separate `FP_NDSZoneLifecycle` module after questionnaire completion.
