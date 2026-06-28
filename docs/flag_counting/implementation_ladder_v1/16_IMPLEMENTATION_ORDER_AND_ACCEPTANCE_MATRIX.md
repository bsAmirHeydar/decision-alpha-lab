# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine.

Global non-negotiables:

- All structural decisions use candle `high` and `low` only.
- `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs.
- Equality is not a break. A level is broken only by a strict pass beyond it.
- The renderer is non-authoritative. It may only draw logical objects emitted by engines.
- Main-chart rendering and audit rendering are separate products.
- Every layer must expose enough audit fields to prove why an object exists.
- A higher layer may never silently repair a lower-layer defect.

# Implementation Order and Acceptance Matrix

## Purpose

This file is the execution checklist. It prevents jumping into renderer or broad Hook/F lifecycle patches before foundations are locked.

The current decision source is:

```text
docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md
```

## Order

### Step 00 — Freeze current canon

Files:

```text
docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md
docs/flag_counting/README.md
lab/03_experiments/EXP_flag_counting/README.md
```

Acceptance:

- active implementation path is Phoenix only;
- VNext/V6/M0007 marked legacy/reference only;
- ambiguity decisions are resolved;
- patch policy requires canon file reference.

### Step 01 — Freeze Level 01 candle stream and timebase

Files:

```text
FP_BarSnapshot.mqh
FP_TimebaseTypes.mqh
FP_SeriesContract.mqh
FP_Timebase.mqh
FlagCountingPhoenixExperiment.mq5 # wiring only
```

Acceptance:

- Phoenix has exactly one `CopyRates` gateway;
- `InpBarsToScan` means requested closed bars in default closed-only mode;
- current forming live candle is dropped by default;
- canonical arrays are `ArraySetAsSeries(false)`;
- index 0 is oldest and newer bars have higher indices;
- duplicate/reversed time and invalid OHLC fail before detection when strict mode is on;
- `FP_LEVEL01` sanity line proves the stream contract before node detection.

### Step 01.5 — Freeze types and config

Files:

```text
FP_Types.mqh
```

Acceptance:

- active structs match interface contract;
- all required identity, status, visibility, reason, and parent-child fields exist;
- config defaults match current canon;
- no module-specific hidden state is missing.

### Step 02 — Freeze NodeEngine

Files:

```text
FP_NodeExtractTypes.mqh
FP_NodePlateau.mqh
FP_NodeClearance.mqh
FP_NodeCanonicalizer.mqh
FP_NodeScaleList.mqh
FP_NodeAudit.mqh
FP_NodeEngine.mqh
FP_Types.mqh
FlagCountingPhoenixExperiment.mq5 # wiring only
```

Acceptance:

- Level 02 consumes only Level 01 canonical bars and never calls `CopyRates`;
- plateau nodes are merged and anchored deterministically at the last equal touch;
- equality is not a break and does not count as L clearance;
- strict high/low pass is the only clearance rejection break;
- confirmed and pending nodes are explicitly separated by `confirmed`, `is_confirmed`, `is_live_pending`, and `source`;
- raw node extraction and canonical alternating compression each emit standalone audit logs;
- Hook/F layers consume canonical `FP_Node` arrays, not renderer objects;
- `FC-GC-001` baselined or marked as blocking before freeze.

### Step 03 — Freeze identity layer

Files:

```text
FP_Identity.mqh
FP_IdentityAudit.mqh
FP_Types.mqh
FP_NodeCanonicalizer.mqh
FP_SequenceEngine.mqh
FP_Audit.mqh
FlagCountingPhoenixExperiment.mq5 # wiring only
```

Acceptance:

- nodes have deterministic structural and visual ids after extraction, sorting, and canonical compression;
- Hook/ND branches have structural, visual, phase, audit, source, rank, and visibility fields;
- F events have structural, visual, phase, chain, audit, source, rank, visibility, and hidden-reason fields;
- identity is assigned before ownership/canonical pruning and normalized again after pruning;
- same visual geometry may merge only inside the same phase;
- hidden events always have non-empty `hidden_reason`;
- `FP_LEVEL03` reports identity sanity before renderer output is trusted.

### Step 04 — Build Hook/ND audit only

Files:

```text
FP_HookAudit.mqh
FP_HookContext.mqh
FP_HookEngine.mqh
FP_Types.mqh
FP_SequenceEngine.mqh # wiring/counters only
FlagCountingPhoenixExperiment.mq5 # inputs only
```

Acceptance:

- bounded same-side contexts are reported through `FP_LEVEL04`;
- unlimited internal branch scans are allowed, but accepted current-L ND branches have max length <=4;
- 1-node and 2-node branches are counted as developing context and never emitted as ND;
- any branch length >4 rejects the whole current-L context and increments adaptive-L rejection audit;
- strict cycle-start break before resolve invalidates the Hook context; equality does not invalidate;
- retracement rejection is explicit and counted;
- Hook objects expose side, cycle_start, extreme, resolve, max_branch_len, nd_qualified, seeds_visible_f1, visible, and hidden_reason;
- no renderer dependency;
- `FP_LEVEL04_SEED` reports Hook/F1 connection after canonical event pruning;
- `FC-GC-002` baselined or marked as blocking before freeze.

### Step 05 — Build flag body audit only

Files:

```text
FP_FlagBodyRules.mqh
FP_FlagBodyAudit.mqh
FP_FlagBodyEngine.mqh
FP_Types.mqh # body fields/counters only
FP_InternalCountEngine.mqh # records absorbed Leg2 extensions on the body
FP_SequenceEngine.mqh # Level 05 report wiring/counters only
FlagCountingPhoenixExperiment.mq5 # Level 05 inputs only
```

Acceptance:

- Origin/Leg1/Waist/Leg2 correct;
- Leg2 strict break;
- equal Leg1 touches are audited and are not Leg2;
- body invalidation uses strict passage only;
- Waist equal to Origin is accepted and audited;
- pre-internal extension is absorbed into Leg2 and increments `leg2_extension_count`;
- `FP_LEVEL05` reports body attempts, complete/invalid/live body stages, strict break counts, equal touch counts, and absorbed extension counts;
- renderer is not involved;
- `FC-GC-003` baselined or marked as blocking before freeze.

### Step 06 — Build internal count audit only

Files:

```text
FP_InternalCountRules.mqh
FP_InternalCountAudit.mqh
FP_InternalCountEngine.mqh
FP_Types.mqh # Level 06 internal-pack fields/counters/config only
FP_SequenceEngine.mqh # Level 06 report wiring only
FP_Audit.mqh # FP_SUMMARY / FP_EVENT internal fields only
FlagCountingPhoenixExperiment.mq5 # Level 06 inputs only
```

Acceptance:

- valid 1/2 detected and recorded through `valid12`, `has_valid12`, `first_valid12_pos`, and `first_valid12_node`;
- pre-internal Leg2 extension is recorded and never confirmation;
- extension absorption increments `leg2_extension_count` when enabled;
- F1 middle-node rule rejects invalid 1/2 branches and increments `f1_mid_rejected`;
- F2 invalidation uses strict Origin break, not Waist break;
- F3 can be body-only complete without requiring post-body internal count;
- `internal_pack_id` and `branch_id_text` are deterministic;
- `FP_LEVEL06` reports count distribution, valid12, confirmation-ready state, invalidations, extensions, and branch rejections;
- renderer is not involved.

### Step 07 — Build F1 lifecycle only

Files:

```text
FP_F1LifecycleRules.mqh
FP_F1LifecycleAudit.mqh
FP_F1LifecycleEngine.mqh
FP_Types.mqh # lifecycle fields/counters/config only
FP_SequenceEngine.mqh # F1 orchestration and report wiring only
FP_Audit.mqh # FP_SUMMARY / FP_EVENT lifecycle fields only
FlagCountingPhoenixExperiment.mq5 # Level 07 inputs only
```

Acceptance:

- F1 lifecycle is built by the Level 07 facade, not inferred by renderer or generic sequence code;
- F1 carries `lifecycle_id`, `lifecycle_status`, phase-gate, body-ready, internal-ready, F2-ready, scan range, and lifecycle reason;
- F1 confirms only through valid internal 1/2 and a later strict Leg2 re-break;
- Leg2 break before internal 1/2 is extension and never confirmation;
- F1 invalidates only by strict Waist break before confirmation;
- fail-open roots are tagged and reported separately from Hook/phase-boundary roots;
- F2 can only be attempted when `lifecycle_can_spawn_f2=true`;
- `FP_LEVEL07` reports attempts, phase/fail-open roots, gate pass/reject, body missing/complete, candidate/post-flag/confirmed/invalidated/extended counts, F2-ready parents, duplicate rejections, and emitted roots;
- `FC-GC-004` baselined or marked as blocking before freeze.

### Step 08 — Build F2 lifecycle only

Files:

```text
FP_F2LifecycleRules.mqh
FP_F2LifecycleAudit.mqh
FP_F2LifecycleEngine.mqh
FP_SequenceEngine.mqh
```

Acceptance:

- F2 parent gate requires Level 07 `lifecycle_can_spawn_f2=true`;
- F2 origin is strict-window backfill from deepest adverse node between F1 Leg2 and F1 confirmation;
- F2 body is still Level 05 O/A/W/B, not a lifecycle shortcut;
- F2 size gate is audited through `f2_size_gate_passed` and `f2_parent_size_ratio`;
- undersized F2 cannot set `f2_can_spawn_f3=true`;
- F2 invalidates only on strict Origin break, not Waist break;
- failed or undersized F2 does not mutate or kill parent F1;
- `FP_LEVEL08` reports parent/origin/body/size/internal/visibility/F3-ready counters;
- `FC-GC-005` baselined or marked as blocking before freeze.

### Step 09 — Build F3 only

Files:

```text
FP_SequenceEngine.mqh
```

Acceptance:

- F3 only after confirmed qualified F2;
- strict-window backfill origin correct;
- OR completion;
- extension/developing state does not die merely because OR is not reached;
- opposite confirmed F1 locks completed F3;
- `FC-GC-006` baselined or marked as blocking before freeze.

### Step 10 — Build phase ownership

Files:

```text
FP_SequenceEngine.mqh
```

Acceptance:

- no repeated same-direction F1 in same phase main chart;
- strict reset rules explicit;
- hidden descendant propagation;
- lower-L local beats high-L umbrella when semantic quality is equal;
- `FC-GC-007` baselined or marked as blocking before freeze.

### Step 11 — Build canonicalization

Files:

```text
FP_SequenceEngine.mqh
FP_Audit.mqh
```

Acceptance:

- duplicates across L hidden with reason;
- raw event list and visible event list are distinguishable;
- main visible list is stable and deterministic;
- every hidden object has reason.

### Step 11.5 — Build raw audit export/report

Files:

```text
FP_Audit.mqh
FlagCountingPhoenixExperiment.mq5 # wiring only
```

Acceptance:

- raw/visible/hidden counts emitted separately;
- hidden reason is never empty;
- fail-open tag is exported/logged;
- renderer can be disabled while audit still works;
- output field names match `11_5_LEVEL_11_5_RAW_AUDIT_EXPORT.md`.

### Step 12 — Build renderer

Files:

```text
FP_Renderer.mqh
```

Acceptance:

- clean main chart readable;
- audit mode toggles labels only;
- renderer settings do not change logical output;
- curves use index sampling;
- stale objects removed;
- `FC-GC-008` and `FC-GC-009` baselined or marked as blocking before freeze.

### Step 13 — Build validation suite

Files:

```text
docs/flag_counting/VALIDATION_CASE_REGISTRY.md
lab/03_experiments/EXP_flag_counting/validation_cases/
```

Acceptance:

- mandatory cases `FC-GC-001` through `FC-GC-010` exist;
- each frozen level has at least one baselined positive and negative test;
- screenshot and audit export archived per case;
- expected counts are baselined, not guessed.

## Stop/rework triggers

Return to lower layer if:

- F2 appears before F1 confirmation -> Level 08.
- Multiple F1s appear in one phase main chart -> Level 10.
- Main chart all gray -> Level 04 or 11.
- No flags -> Level 05/07/10/11.
- Curves broken -> Level 01/12.
- Internal labels leak -> Level 11/12.
- Renderer changes event counts -> Level 11.5/12.
- Hidden object has no reason -> Level 11/11.5.

## Minimal next coding plan

The next real code work should not edit all modules. It should implement only:

1. missing type/audit fields if any;
2. sequence audit dump and raw/visible separation;
3. one lifecycle fix at a time after audit proves where the defect lives;
4. renderer changes only after audit/export is stable.

## Completion definition

Phoenix is implementation-complete when:

- a full raw audit/export list exists;
- main visible list is derived deterministically;
- all F1/F2/F3 lifecycle rules are passed;
- Hook/ND coverage can be toggled without starving flags;
- renderer toggles do not change logical output;
- validation cases `FC-GC-001` through `FC-GC-010` are baselined.
