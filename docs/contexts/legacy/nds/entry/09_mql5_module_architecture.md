---
title: NDS Entry MQL5 Module Architecture
status: implemented_scaffold
version: 1.0.0
---
# NDS Entry MQL5 Module Architecture

## 1. Dependency chain

```text
FP_HookPhase02Engine
  └─ captures annotated sequences
     into FP_NDSStructureSnapshot

FP_NDSEntryEngine
  └─ FP_NDSEntryExport
      └─ FP_NDSEntryRules
          └─ FP_NDSEntryTypes
              └─ FP_NDSStructureSnapshot
```

## 2. Snapshot cache

`FP_NDSStructureSnapshot.mqh` stores a read-only copy of the annotated Phase 02 sequence array. This prevents another full node/sequence rebuild solely for entry-transition processing.

The cache is cleared before every Phase 02 run and remains invalid when Phase 02 is skipped. This prevents stale structure from leaking across chart modes or failed runs.

## 3. Rule ownership

```text
Types: enums, rows, configs, reset functions
Rules: selection, direction mapping, Zone adapter, state transitions, geometry
Export: CSV serialization only
Engine: orchestration only
Snapshot: Hook-to-entry handoff only
```

## 4. Canon adapter localization

The final Zone implementation should first replace:

```text
FP_NDSBuildCanonicalZoneAdapter
```

It should not modify command code to invent Zone geometry.

## 5. Central EA integration

`FlagCountingPhoenixExperiment.mq5`:

- version `18.30`;
- includes `FP_NDSEntryEngine.mqh`;
- exposes NDS Entry inputs;
- loads `FP_NDSEntryConfig`;
- runs the pipeline after Hook Phase 10;
- remains print-silent by default.

## 6. Coexistence with legacy Level 20–30

The NDS pipeline is parallel to the generic Level 20–30 research stack. It does not silently replace those modules. Future consolidation should occur only after equivalence and migration tests are written.
