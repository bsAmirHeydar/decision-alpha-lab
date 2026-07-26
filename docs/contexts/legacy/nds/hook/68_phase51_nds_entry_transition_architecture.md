# Phase 51 — NDS Entry Transition Architecture

Phase 51 introduces the first NDS-specific bridge from canonical valid Hook structure toward Setup, Trade Plan, and broker-neutral Command Preview objects.

It does not implement the unanswered Zone Canon and does not send orders.

## Pipeline

```text
Hook Phase02 annotated sequence snapshot
→ eligible valid Hook selection
→ Zone adapter
→ Setup gate
→ Trade Plan geometry
→ zero-volume no-send command preview
```

## Safe defaults

```text
profile = PRE_CANON_BLOCKED
direction = UNRESOLVED
order/stop/target = UNRESOLVED
Zone Canon lock = false
trade contract lock = false
command preview only = true
```

## Files

- `FP_NDSStructureSnapshot.mqh`
- `FP_NDSEntryTypes.mqh`
- `FP_NDSEntryRules.mqh`
- `FP_NDSEntryExport.mqh`
- `FP_NDSEntryEngine.mqh`
- `docs/contexts/legacy/nds/entry/`

## Canon boundary

The single future implementation seam is:

```text
FP_NDSBuildCanonicalZoneAdapter
```

No downstream command or risk module may invent Zone boundaries independently.
