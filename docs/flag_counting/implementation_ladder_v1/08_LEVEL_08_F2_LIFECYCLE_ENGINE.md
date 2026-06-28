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

F2 is the second flag in an existing F-chain. It is not a new F1, not a Hook, and not a generic child body. F2 is authorized only by a Level 07 F1 whose lifecycle explicitly allows child construction.

The Level 08 contract is:

```text
confirmed F1 + lifecycle_can_spawn_f2
-> strict F2 origin backfill window
-> F2 body
-> parent-size gate
-> F2 internal confirmation / Origin invalidation
-> f2_can_spawn_f3
```

F2 is therefore the bridge between a confirmed F1 and any possible F3. F3 must never be built from a body-only, undersized, invalidated, or unconfirmed F2.

## Owned source modules

```text
mql5/Include/FlagCountingPhoenix/FP_F2LifecycleRules.mqh
mql5/Include/FlagCountingPhoenix/FP_F2LifecycleAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_F2LifecycleEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_SequenceEngine.mqh
```

`FP_SequenceEngine.mqh` is orchestration only. The F2 lifecycle decision itself belongs to the Level 08 modules.

## Parent authorization

F2 may be attempted only when the parent F1 passes:

```text
parent.level == F1
parent.status == confirmed
parent.has_confirm == true
parent.lifecycle_can_spawn_f2 == true
```

Any other parent state is rejected and counted in `FP_LEVEL08 parent_rejected`.

## F2 origin backfill

F2 origin is backfilled from the deepest adverse correction after F1 Leg2 and before F1 confirmation.

Bullish chain:

```text
deepest LOW in (F1.Leg2, F1.Confirm)
```

Bearish chain:

```text
highest HIGH in (F1.Leg2, F1.Confirm)
```

The window is strict. Nodes after F1 confirmation do not become the F2 origin in Level 08.

## Body dependency

F2 body construction is delegated to Level 05:

```text
Origin -> Leg1 -> Waist -> Leg2
```

Level 08 does not invent body points. It only consumes the body and records whether the body exists.

## Size gate

F2 must reach the parent-size condition before it can be a real sequence child:

```text
F2.flag_size >= InpF2MinParentSizeRatio * F1.flag_size
```

Default:

```text
InpF2MinParentSizeRatio = 1.0
```

If F2 is below the size gate:

- it is counted in audit;
- it does not authorize F3;
- it is hidden from the main chart by default;
- it can be shown for debug with `InpF2ShowSizeRejectedCandidates=true`.

If pre-internal extension absorption increases Leg2 before the internal count is valid, the same F2 candidate is updated and size is recomputed. A duplicate F2 must not be emitted just because Leg2 extended.

## Internal confirmation

After the size gate passes, Level 08 uses Level 06 internal-count evidence.

F2 confirms when:

```text
valid internal 1/2 after F2 Leg2
+ later strict favorable re-break of F2 Leg2
+ no strict F2 Origin break before confirmation
```

F2 does not use the special F1 middle-node restriction. That rule belongs only to F1.

## Invalidation

F2 invalidates at its own Origin, not its Waist.

```text
bullish F2 invalidation = strict break below F2 Origin
bearish F2 invalidation = strict break above F2 Origin
```

Equality is not invalidation.

A Waist break that does not break Origin may still be part of internal branch behavior. It must not kill the F2 lifecycle by itself.

## F3 authorization

F3 may be attempted only when:

```text
F2.status == confirmed
F2.has_confirm == true
F2.f2_size_gate_passed == true
F2.f2_can_spawn_f3 == true
```

This is the Level 08 handoff to Level 09.

## Required fields

`FP_FlagEvent` must carry:

```text
f2_lifecycle_id
f2_lifecycle_status
f2_parent_ready
f2_origin_found
f2_body_complete
f2_size_gate_passed
f2_internal_ready
f2_can_spawn_f3
f2_origin_scan_start_pos
f2_lifecycle_scan_end_pos
f2_parent_size_ratio
f2_lifecycle_reason
```

## Audit

`FP_LEVEL08` must report:

```text
parent_attempts
parent_ready
parent_rejected
origin_scans
origin_found
origin_missing
body_missing
body_complete
size_pass
size_reject
candidate
post_flag
confirmed
invalidated
extended
visible
hidden
f3_ready
emitted_children
duplicate_rejected
max_ext
```

Samples are controlled by:

```text
InpPrintF2Sanity = true
InpPrintF2Samples = false
InpF2SampleLimit = 6
```

Main-chart candidate controls:

```text
InpF2ShowSizeRejectedCandidates = false
InpF2ShowPostFlagCandidates = true
InpF2ShowLiveBodyCandidates = true
```

## Acceptance tests

### Test 01 — F2 only after confirmed F1

No F2 may be emitted from candidate, post-flag, body-only, invalidated, hidden, or fail-open rejected F1 parents.

### Test 02 — Backfill window

F2 origin must be the deepest adverse node between F1 Leg2 and F1 confirmation.

### Test 03 — Size gate

An undersized F2 must not set `f2_can_spawn_f3=true`.

### Test 04 — Origin invalidation

F2 dies only on strict Origin break before confirmation. Waist break alone is not fatal.

### Test 05 — Parent survival

If a child F2 fails, the parent F1 remains a confirmed parent. Sequence ownership may hide or display later states, but Level 08 must not mutate the F1 lifecycle.

### Test 06 — F3 handoff

F3 may only consume an F2 with `f2_can_spawn_f3=true`.

## Failure symptoms

- F2 appears before F1 confirmation.
- F2 uses a node after F1 confirmation as origin.
- An undersized F2 creates F3.
- F2 invalidates on Waist instead of Origin.
- Failed F2 hides or invalidates its parent F1.
- `FP_LEVEL08` reports zero parent attempts while visible F2 exists.

## Freeze condition

Level 08 is frozen when every emitted F2 has a confirmed Level 07 parent, a strict backfilled origin, a recorded size gate result, a Level 06 internal-pack result, and a deterministic `f2_can_spawn_f3` handoff state.
