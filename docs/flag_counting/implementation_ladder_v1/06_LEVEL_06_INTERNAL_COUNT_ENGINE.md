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

# Level 06 — Internal Count Engine

## Purpose

This layer counts internal post-flag adverse nodes after a completed Level 05 body. It is the bridge between a completed body and lifecycle confirmation, but it does not own F1/F2/F3 creation, F2/F3 authorization, phase reset, main-chart ownership, or rendering.

A completed body is:

```text
Origin -> Leg1 -> Waist -> Leg2
```

After Leg2, Level 06 builds a post-body internal pack:

```text
internal 1 -> internal 2 -> optional 3 -> optional 4
```

The lifecycle layer may later use that pack to confirm F1/F2, but the pack itself is only evidence.

## Owned source modules

```text
mql5/Include/FlagCountingPhoenix/FP_InternalCountRules.mqh
mql5/Include/FlagCountingPhoenix/FP_InternalCountAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_InternalCountEngine.mqh
```

`FP_InternalCountRules.mqh` owns pure predicates and identity helpers.

`FP_InternalCountAudit.mqh` owns structured reporting, counters, and optional samples.

`FP_InternalCountEngine.mqh` owns the public facade and event-pack wiring.

## Input

```text
FP_Node canonical_nodes[]
FP_FlagEvent body_event
FP_Config config
```

The body event must already have valid Level 05 evidence:

```text
body_id
body_status
origin
leg1
waist
leg2
pos_origin
pos_leg1
pos_waist
pos_leg2
```

## Output

```text
FP_InternalPack
```

The event receives the pack through:

```text
event.internal_pack
```

Level 06 also exposes `FP_LEVEL06` logs and totals in `FP_SUMMARY`.

## Directional count rule

Bullish body:

```text
count adverse LOW nodes after Leg2
```

Bearish body:

```text
count adverse HIGH nodes after Leg2
```

Opposite-side nodes between adverse nodes may be used as middle context, but they are not counted as the internal sequence.

## Count thresholds

```text
0 counted nodes => body exists, no post-flag count
1 counted node  => developing internal
2 counted nodes => valid 1/2 exists
3 counted nodes => extended internal branch
4 counted nodes => maximum tracked internal branch
```

Counts above four are not tracked inside this pack. Higher-L compression or later lifecycle logic must handle larger structures instead of silently extending this layer.

## Strict-break confirmation support

A body is not confirmation-ready merely because Leg2 exists.

Confirmation support requires:

```text
valid internal 1/2 exists
then favorable strict break beyond Leg2 appears
```

The pack records this evidence as:

```text
valid12
has_valid12
first_valid12_pos
first_valid12_node
confirm_pos
```

The lifecycle layer may then decide whether the event becomes confirmed.

## F1 middle-node rule

For F1 only, the best opposite-side middle node between internal 1 and internal 2 must not itself break Leg2 before valid 1/2 is formed.

Bullish F1:

```text
middle HIGH between internal LOW 1 and LOW 2 must not break Leg2 high
```

Bearish F1:

```text
middle LOW between internal HIGH 1 and HIGH 2 must not break Leg2 low
```

The pack records:

```text
middle_opposite_node
has_middle_opposite_node
middle_opposite_breaks_leg2
```

Branches rejected by this rule are counted in:

```text
FP_LEVEL06 f1_mid_rejected
```

## Pre-internal Leg2 extension rule

If Leg2 is broken again before valid internal 1/2 exists, that break is **extension**, not confirmation.

Level 06 records the first such break as:

```text
pre_internal_leg2_extension_node
has_pre_internal_leg2_extension
pre_internal_leg2_extension_pos
```

When `InpAbsorbPreInternalExtensions=true`, the extension is folded back into the same body as the new Leg2 and `leg2_extension_count` increments.

This prevents repeated F1 creation inside one trend leg before a true post-body internal 1/2 exists.

## Invalidation boundary

Level 06 only records pre-confirmation invalidation evidence:

```text
F1 invalidates at strict Waist break
F2 invalidates at strict Origin break
F3 does not require post-body internal count in this layer
```

Equality does not invalidate.

Recorded fields:

```text
invalid_pos
status
reason
```

## Required fields now present

```text
internal_pack_id
branch_id
branch_id_text
count
valid12
has_valid12
first_valid12_pos
first_valid12_node
middle_opposite_node
middle_opposite_breaks_leg2
pre_internal_leg2_extension_node
pre_internal_leg2_extension_pos
confirm_pos
invalid_pos
scan_start_pos
scan_end_pos
status
reason
```

## Audit output

`FP_LEVEL06` reports:

```text
bodies
f1_bodies
f2_bodies
f3_bodies
attempts
packs
count0/count1/count2/count3/count4
valid12
confirm_ready
confirms
invalidations
pre_ext_seen
pre_ext_absorbed
f1_mid_rejected
missing_mid_rejected
non_deeper_rejected
max_ext
max_count
f3_body_only
```

Optional samples are controlled by:

```text
InpPrintInternalSamples
InpInternalSampleLimit
```

## Forbidden dependencies

Level 06 must not:

- create F1, F2, or F3;
- authorize F2/F3 parents;
- lock F3;
- prune duplicate roots;
- decide main-chart visibility;
- draw internal labels;
- read candle open/close/body/color;
- call `CopyRates`.

## Acceptance tests

### Test 01 — No 1/2 no confirmation

A flag body with no valid two adverse nodes cannot confirm even if Leg2 extends.

Expected audit:

```text
valid12=0
confirm_ready=0
pre_ext_seen>=1 if favorable extension appears before 1/2
```

### Test 02 — Pre-internal extension

A Leg2 break before valid 1/2 updates extension state and does not create a new F1.

Expected fields:

```text
has_pre_internal_leg2_extension=true
pre_internal_leg2_extension_node != none
leg2_extension_count increments when absorption is enabled
```

### Test 03 — Multiple 1s one 2

The audit output must preserve rejected or skipped branch evidence while lifecycle chooses deterministic canonical confirmation branch.

Expected audit:

```text
non_deeper_rejected or missing_mid_rejected can be non-zero
internal_pack_id remains deterministic
```

### Test 04 — F1 middle rule

If the middle opposite node violates the F1 rule before 1/2 is valid, that branch cannot confirm F1.

Expected audit:

```text
f1_mid_rejected>=1
valid12 does not increment for that rejected branch
```

### Test 05 — F2 invalidation boundary

F2 must invalidate on strict Origin break, not Waist break.

Expected audit:

```text
invalidations increments only on strict origin break for F2
```

## Failure symptoms

- F1 confirmations too early.
- F1 repetitions in a trend leg.
- F2/F3 created from post_flag parents.
- Internal labels appear on the main chart when detailed labels are off.
- `FP_SUMMARY internal_valid12` disagrees with visible confirmations.
- `pre_ext_seen` exists but `leg2_extension_count` stays zero while absorption is enabled.

## Freeze condition

This layer is frozen when internal packs can be produced and audited for any body without invoking F1/F2/F3 lifecycle decisions or renderer behavior.
