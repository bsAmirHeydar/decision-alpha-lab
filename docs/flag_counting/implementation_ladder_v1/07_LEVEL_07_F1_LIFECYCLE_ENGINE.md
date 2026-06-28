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

# Level 07 — F1 Lifecycle Engine

## Purpose

F1 is the first two-leg structure after a valid phase boundary or fail-open root. This layer defines F1 states and prevents raw body enumeration from becoming multiple F1 chains inside one phase.

## Owned source modules

```text
mql5/Include/FlagCountingPhoenix/FP_SequenceEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_FlagBodyEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_InternalCountEngine.mqh
```

## Authorized F1 roots

An F1 may start from:

- ND/Hook resolve boundary;
- endpoint/extreme of an opposite structure;
- diagnostic fail-open raw origin when strict boundary coverage would otherwise starve flags.

F1 must not start from the middle of an active same-direction leg.

## F1 states

```text
candidate_body
post_flag
internal_ready
confirmed
invalidated
hidden_duplicate
hidden_phase_loser
```

## F1 display rule

F1 can be displayed after its two-leg body exists. Its label must indicate status if detailed/debug mode is active.

## F1 confirmation rule

F1 confirms only when:

1. two-leg body exists;
2. valid post-flag internal 1/2 or more exists;
3. price strictly breaks Leg2 again after valid internal state;
4. Waist has not been strictly broken before confirmation.

## F1 invalidation rule

Before confirmation, F1 invalidates at Waist.

## Pre-internal extension rule

If price breaks Leg2 again before valid internal 1/2, update Leg2 extension. Do not confirm. Do not create a new F1.

## Phase ownership relationship

Inside one direction/phase, main chart should not display repeated same-direction F1 roots unless a documented phase reset occurred.

Audit may keep all F1 candidates.

## Required fields

```text
f_level = F1
status
root_source
body_id
internal_pack_id
confirmed_index
invalidated_index
phase_id
chain_id
is_phase_owner
hidden_reason
```

## Acceptance tests

### Test 01 — F1 no middle start

If a candidate root is inside an existing same-direction phase after F1 ownership, it cannot become a new main-chart F1 unless phase reset is present.

### Test 02 — F1 confirms only after 1/2

Leg2 break without valid internal 1/2 is extension, not confirmation.

### Test 03 — Waist invalidation

A pre-confirmation strict Waist break invalidates F1.

### Test 04 — Fail-open tag

A fail-open F1 must be visibly/audit-tagged as fail-open and must lose to equivalent phase-boundary roots.

## Failure symptoms

- Several green F1s in one continuous bullish phase.
- F2/F3 appear while parent F1 is only post_flag.
- Fail-open roots dominate Hook-derived roots.
- Main chart changes massively when Hook labels toggle.

## Freeze condition

F1 lifecycle is frozen when F1 can be emitted, confirmed, invalidated, and phase-owned in audit without creating F2/F3.
