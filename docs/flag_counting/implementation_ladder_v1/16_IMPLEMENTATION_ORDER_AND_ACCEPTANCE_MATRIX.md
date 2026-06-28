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

### Step 01 — Freeze types and config

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
FP_NodeEngine.mqh
```

Acceptance:

- plateau nodes correct;
- equality not break;
- confirmed vs pending separated;
- audit node dump possible;
- `FC-GC-001` baselined or marked as blocking before freeze.

### Step 03 — Freeze identity layer

Files:

```text
FP_Types.mqh
FP_Audit.mqh
```

Acceptance:

- structural id;
- visual id derivation or deterministic object naming contract;
- phase/sequence id;
- chain id;
- visible/hidden reason.

### Step 04 — Build Hook/ND audit only

Files:

```text
FP_HookEngine.mqh
```

Acceptance:

- bounded contexts;
- unlimited branches with accepted branch max <=4 at selected L;
- 2-node branch not ND;
- broken cycle start invalidates;
- no renderer dependency;
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
