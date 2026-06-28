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
FP_FlagBodyEngine.mqh
```

Acceptance:

- Origin/Leg1/Waist/Leg2 correct;
- Leg2 strict break;
- body invalidation uses strict passage only;
- pre-internal extension absorbed;
- `FC-GC-003` baselined or marked as blocking before freeze.

### Step 06 — Build internal count audit only

Files:

```text
FP_InternalCountEngine.mqh
```

Acceptance:

- valid 1/2 detected;
- branches preserved;
- pre-internal extension not confirmation;
- internal pack fields are complete enough for F1/F2/F3 lifecycle.

### Step 07 — Build F1 only

Files:

```text
FP_SequenceEngine.mqh
```

Acceptance:

- F1 body/live/post-flag status;
- F1 confirmed only through valid internal 1/2 and Leg2 re-break;
- F1 invalidated by Waist strict break;
- fail-open tagged;
- no F2/F3 yet;
- `FC-GC-004` baselined or marked as blocking before freeze.

### Step 08 — Build F2 only

Files:

```text
FP_SequenceEngine.mqh
```

Acceptance:

- F2 only after confirmed F1;
- strict-window backfill origin correct;
- size condition audited;
- undersized F2 cannot authorize F3;
- F2 child death does not kill F1;
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
