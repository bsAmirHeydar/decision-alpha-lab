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

This layer counts internal post-flag adverse nodes. It is the bridge between a completed body and confirmation. F1 confirms only after valid internal 1/2 or more exists and Leg2 is broken again.

## Owned source module

```text
mql5/Include/FlagCountingPhoenix/FP_InternalCountEngine.mqh
```

## Scope

Internal counts are built after a flag body has reached Leg2.

Bullish flag:

```text
count adverse LOW nodes after Leg2
```

Bearish flag:

```text
count adverse HIGH nodes after Leg2
```

Opposite-side nodes between adverse nodes may be used as intermediate context but are not the counted adverse sequence itself.

## F1-specific middle-node rule

For F1, the middle opposite node between internal 1 and 2 must not break Leg2 before the valid 1/2 is formed. After a valid 1/2 exists, later 3/4 logic does not carry that same restriction unless explicitly documented.

## Branching

Multiple internal 1 candidates may exist. They can resolve into shared later nodes. The engine must preserve branches in audit and expose canonical count used by lifecycle.

## Count thresholds

```text
0 counted nodes => post_flag only
1 counted node  => developing internal
2 counted nodes => minimum confirmation-ready internal state
3/4 counted nodes => extended internal state
```

## Relationship to Leg2 extension

If Leg2 is broken again before a valid internal 1/2 exists, that break is extension. It is not confirmation.

## Required fields

```text
body_id
internal_pack_id
counted_nodes[]
branch_id
count
has_valid_1_2
first_valid_1_2_index
middle_opposite_node
middle_opposite_breaks_leg2
pre_internal_leg2_extension_node
```

## Acceptance tests

### Test 01 — No 1/2 no confirmation

A flag body with no valid two adverse nodes cannot confirm even if Leg2 extends.

### Test 02 — Pre-internal extension

A Leg2 break before valid 1/2 updates extension state and does not create a new F1.

### Test 03 — Multiple 1s one 2

The audit output must preserve multiple branch candidates, while lifecycle chooses deterministic canonical confirmation branch.

### Test 04 — F1 middle rule

If middle opposite node violates F1's rule before 1/2 is valid, that branch cannot confirm F1.

## Failure symptoms

- F1 confirmations too early.
- F1 repetitions in a trend leg.
- Internal labels appear on main chart when detailed labels are off.
- F2/F3 created from post_flag parents.

## Freeze condition

This layer is frozen when internal packs can be produced and audited for any body without invoking F1/F2/F3 lifecycle or renderer.
