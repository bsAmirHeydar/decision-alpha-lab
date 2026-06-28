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

# Level 05 — Flag Body Engine

## Purpose

This layer detects the invariant two-leg flag body. It is the central object of Phoenix. F1/F2/F3 are all built from the same body shape; their differences come from lifecycle role and post-body behavior.

## Owned source module

```text
mql5/Include/FlagCountingPhoenix/FP_FlagBodyEngine.mqh
```

## Body contract

```text
Origin -> Leg1 -> Waist -> Leg2
```

## Bullish body

- Origin: LOW node.
- Leg1: HIGH node after Origin.
- Waist: deepest LOW after Leg1 that does not strictly break Origin.
- Leg2: HIGH that strictly breaks Leg1.

## Bearish body

- Origin: HIGH node.
- Leg1: LOW node after Origin.
- Waist: highest HIGH after Leg1 that does not strictly break Origin.
- Leg2: LOW that strictly breaks Leg1.

## Equal price rule

- Leg2 must strictly break Leg1.
- Waist must not strictly break Origin.
- Equal to Origin is not invalidation.
- Equal to Leg1 is not Leg2 break.

## Leg2 extension rule

If the market breaks beyond Leg2 before the required post-flag internal count exists, that is still body extension, not confirmation and not a new F1.

This rule prevents repeated F1 creation inside one unfinished flag.

## Output object

```text
body_id
direction
L
origin_node
leg1_node
waist_node
leg2_node
body_status: body_complete | body_extended | invalid
origin_hit_status
leg1_break_status
leg2_extension_count
source_root_mode
```

## Forbidden behavior

- Creating F1/F2/F3 directly without a valid two-leg body.
- Using close/body color to select Leg1 or Leg2.
- Treating a pre-internal Leg2 extension as confirmation.
- Starting a new same-direction F1 from the middle of an unfinished body.

## Acceptance tests

### Test 01 — Basic bullish body

Given LOW O, HIGH A, LOW W above O, HIGH B above A, emit one bullish body.

### Test 02 — Waist breaks origin

If W strictly breaks O before Leg2, reject the body.

### Test 03 — Equal Leg1 touch

If B equals A but does not strictly exceed A, Leg2 is not complete.

### Test 04 — Leg2 extension absorption

If price makes a higher high after Leg2 before internal 1/2 exists, update/extend Leg2. Do not emit a new F1.

## Failure symptoms

- Multiple F1 roots in one one-sided move.
- F1 confirms immediately after body without internal 1/2.
- Large umbrellas and local flags both draw as equal main structures.
- Body starts from Hook cycle boundary instead of intended semantic origin.

## Freeze condition

This layer is frozen when body detection works independently from F-level lifecycle and can output body candidates plus invalidation reasons without drawing them.
