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

# Level 08 — F2 Lifecycle Engine

## Purpose

F2 is the second flag in a chain. It is not a new F1 and it is not authorized by a post_flag F1. It is authorized only by confirmed F1.

## Owned source module

```text
mql5/Include/FlagCountingPhoenix/FP_SequenceEngine.mqh
```

## Authorization

F2 may be searched only after parent F1 is confirmed.

```text
parent.f_level == F1
parent.status == confirmed
```

No other parent state authorizes F2.

## Backfill origin

F2 origin is backfilled from the deepest adverse correction after F1 flag body and before F1 confirmation.

Bullish chain:

```text
deepest LOW after F1 Leg2 and before F1 confirmation
```

Bearish chain:

```text
highest HIGH after F1 Leg2 and before F1 confirmation
```

## Size contract

F2 must compare by size against F1.

```text
F2 flag size >= F1 flag size
```

If F2 has not reached size condition, it is not necessarily rejected; it may remain candidate/qualified pending extension depending on body state. However, undersized F2 must not authorize F3.

## Invalidation

F2 invalidates at its own Origin, not at its Waist.

If F2 breaks its Waist but not Origin, the branch is not dead. It may create a waist-break internal branch.

## Parent survival

If an F2 candidate dies, parent F1 remains alive and can search for a new F2 from the same post-F1 correction context.

## Required fields

```text
f_level = F2
parent_f1_id
backfill_origin_node
backfill_window_start
backfill_window_end
size_ratio_to_f1
size_condition_met
can_authorize_f3
invalidated_at_origin
waist_break_branch
```

## Acceptance tests

### Test 01 — F2 only after confirmed F1

F2 cannot be emitted from F1 `post_flag` or `internal_ready` parent.

### Test 02 — Backfill window

F2 origin must come from the adverse correction between F1 Leg2 and F1 confirmation, not after confirmation unless documented as extension.

### Test 03 — F2 origin invalidation

F2 candidate dies only when its own origin is strictly broken.

### Test 04 — F2 small cannot create F3

Undersized F2 may be audited but cannot become parent of F3.

## Failure symptoms

- F2 labels appear next to post_flag F1 labels.
- Several F2s appear before F1 confirmation index.
- F2 disappears and kills F1 context.
- F3 is built from an undersized or unconfirmed F2.

## Freeze condition

F2 lifecycle is frozen when F2 candidates and confirmations can be audited from confirmed F1 only, including failure and parent survival cases.
