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

# Level 09 — F3 Extension and Lock Engine

## Purpose

F3 is the third flag in a chain. It completes the same-direction sequence and then owns extension until the first opposite confirmed F1 locks it.

## Owned source module

```text
mql5/Include/FlagCountingPhoenix/FP_SequenceEngine.mqh
```

## Authorization

F3 may be searched only after parent F2 is confirmed and size-qualified.

```text
parent.f_level == F2
parent.status == confirmed
parent.can_authorize_f3 == true
```

## Backfill origin

F3 origin is backfilled from deepest adverse correction after F2 flag body and before F2 confirmation.

## Completion OR condition

F3 completes when its body exists and either condition is true:

```text
F3.leg1_L >= ceil(0.80 * F2.leg1_L)
```

or

```text
F3.flag_size > 0.70 * F2.flag_size
```

F3 must not be rejected early simply because it has not yet reached the OR condition. It remains developing until extension, invalidation, or completion.

## Extension

After F3 completes, the rest of the same-direction move is F3 extension. Do not start new same-direction F1/F2 inside that extension unless a phase reset occurs.

## Lock

F3 locks with the first opposite confirmed F1 after F3 completion.

Locked F3 never disappears from historical audit. Main chart may choose a simplified display, but audit persistence is mandatory.

## Required fields

```text
f_level = F3
parent_f2_id
backfill_origin_node
leg1_L_ratio_to_f2
size_ratio_to_f2
completion_reason: L_ratio | size_ratio | none
completed_index
extension_start_index
opposite_lock_f1_id
locked_index
locked_persistent = true/false
```

## Acceptance tests

### Test 01 — F3 only after confirmed qualified F2

No F3 may appear from F2 post_flag, F2 candidate, or undersized F2.

### Test 02 — OR condition

F3 completes if either L ratio or size ratio passes. Both are not required.

### Test 03 — No early rejection

A developing F3 with incomplete OR condition remains alive unless its own invalidation condition is hit.

### Test 04 — Opposite F1 lock

The first opposite confirmed F1 after F3 completion locks F3.

## Failure symptoms

- F3 appears without visible or confirmed F2.
- F3 vanishes after being locked.
- New same-direction F1s appear inside F3 extension.
- Opposite F1 does not lock completed F3.

## Freeze condition

F3 is frozen when completion, extension, and lock are reproducible in audit across replay.
