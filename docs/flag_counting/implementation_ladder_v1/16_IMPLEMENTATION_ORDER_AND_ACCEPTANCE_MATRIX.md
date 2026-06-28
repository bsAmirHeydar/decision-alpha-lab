# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine. The ladder is intentionally layered so that lower layers become frozen foundations before higher layers are allowed to depend on them.

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

This file is the execution checklist. It prevents jumping into renderer or Hook patches before foundations are locked.

## Order

### Step 01 — Freeze types and config

Files:

```text
FP_Types.mqh
```

Acceptance:

- all required fields exist;
- config defaults match clean main chart;
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
- audit node dump possible.

### Step 03 — Freeze identity layer

Files:

```text
FP_Types.mqh
FP_Audit.mqh
```

Acceptance:

- structural id;
- visual id;
- phase id;
- chain id;
- hidden reason.

### Step 04 — Build Hook/ND audit only

Files:

```text
FP_HookEngine.mqh
```

Acceptance:

- bounded contexts;
- unlimited branches;
- branch max <=4 at accepted L;
- 2-node branch not ND;
- broken cycle start invalidates;
- no renderer dependency.

### Step 05 — Build flag body audit only

Files:

```text
FP_FlagBodyEngine.mqh
```

Acceptance:

- O/A/W/B correct;
- Leg2 strict break;
- waist strict invalidation only;
- pre-internal extension absorbed.

### Step 06 — Build internal count audit only

Files:

```text
FP_InternalCountEngine.mqh
```

Acceptance:

- valid 1/2 detected;
- branches preserved;
- pre-internal extension not confirmation.

### Step 07 — Build F1 only

Files:

```text
FP_SequenceEngine.mqh
```

Acceptance:

- F1 post_flag;
- F1 confirmed;
- F1 invalidated;
- fail-open tagged;
- no F2/F3 yet.

### Step 08 — Build F2 only

Acceptance:

- F2 only after confirmed F1;
- backfill origin correct;
- size condition audited;
- F2 child death does not kill F1.

### Step 09 — Build F3 only

Acceptance:

- F3 only after confirmed qualified F2;
- OR completion;
- extension;
- opposite lock.

### Step 10 — Build phase ownership

Acceptance:

- no repeated same-direction F1 in same phase main chart;
- reset rules explicit;
- hidden descendant propagation.

### Step 11 — Build canonicalization

Acceptance:

- duplicates across L hidden with reason;
- audit complete;
- main visible list stable.

### Step 12 — Build renderer

Acceptance:

- clean main chart readable;
- audit mode toggles labels only;
- curves use index sampling;
- stale objects removed.

### Step 13 — Build validation suite

Acceptance:

- golden ranges defined;
- screenshot comparisons archived;
- compile/test report per patch.

## Stop/rework triggers

Return to lower layer if:

- F2 appears before F1 confirmation -> Level 08.
- Multiple F1s in one phase -> Level 10.
- Main chart all gray -> Level 04 or 11.
- No flags -> Level 05/07/10/11.
- Curves broken -> Level 01/12.
- Internal labels leak -> Level 11/12.

## Minimal next coding plan

The next real code work should not edit all modules. It should implement only:

1. types/audit fields if missing;
2. sequence audit dump;
3. clean separation between raw event list and visible event list;
4. then one lifecycle fix at a time.

## Completion definition

Phoenix is implementation-complete when:

- a full raw audit list exists;
- main visible list is derived deterministically;
- all F1/F2/F3 lifecycle rules are passed;
- Hook/ND coverage can be toggled without starving flags;
- renderer toggles do not change logical output.
