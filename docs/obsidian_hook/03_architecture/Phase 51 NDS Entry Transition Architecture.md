# Phase 51 NDS Entry Transition Architecture

## Status

```text
implemented scaffold
no-send
Zone Canon pending
```

## Pipeline

```text
Hook Phase02 annotated sequence snapshot
→ valid-Hook eligibility and selection
→ canonical Zone adapter seam
→ Setup gate
→ Trade Plan geometry
→ zero-volume Command Preview
→ CSV audit
```

## Modules

```text
FP_NDSStructureSnapshot.mqh
FP_NDSEntryTypes.mqh
FP_NDSEntryRules.mqh
FP_NDSEntryExport.mqh
FP_NDSEntryEngine.mqh
```

## Default expected result

An eligible valid Hook may reach `STRUCTURE_CAPTURED`. The profile then reports `NDS_ZONE_BLOCKED_PRE_CANON_PROFILE`. This is the intended fail-closed behavior until the questionnaire decisions are locked.

## Full documentation

- [[../../nds_entry_architecture/README|NDS Entry Transition Architecture]]
- [[../00_mocs/NDS_ENTRY_EXECUTION_MOC]]
