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

Level 07 converts a completed Level 05 body plus Level 06 internal-count evidence into a lifecycle-owned F1 root. This is the first layer allowed to say whether an F1 is merely a candidate, post-flag, confirmed, invalidated, hidden, or allowed to spawn F2.

F1 lifecycle is not a renderer rule and is not a body rule. Body and internal-count layers provide evidence; Level 07 owns the semantic root state.

## Owned source modules

```text
mql5/Include/FlagCountingPhoenix/FP_F1LifecycleRules.mqh
mql5/Include/FlagCountingPhoenix/FP_F1LifecycleAudit.mqh
mql5/Include/FlagCountingPhoenix/FP_F1LifecycleEngine.mqh
mql5/Include/FlagCountingPhoenix/FP_SequenceEngine.mqh # orchestration only
```

## Inputs

```text
canonical FP_Node[]
Hook/ND phase-boundary origin candidates
fail-open raw origin candidates
Level 05 body builder
Level 06 internal-pack builder
FP_Config
```

## Output

```text
FP_FlagEvent level=F1
lifecycle_id
lifecycle_status
lifecycle_phase_gate_passed
lifecycle_body_complete
lifecycle_internal_ready
lifecycle_can_spawn_f2
lifecycle_reason
FP_LEVEL07 audit report
```

## Authorized roots

An F1 may start from:

- a Hook/ND phase-boundary root;
- a diagnostic fail-open raw origin when fail-open is enabled;
- a raw origin only when phase-boundary requirement is explicitly disabled.

When `require_f1_phase_boundary=true`, a non-hook root must be tagged as fail-open or rejected.

## Lifecycle states

```text
candidate      = two-leg body exists, no valid post-body internal evidence yet
post_flag      = body exists and adverse internal count exists / valid12 waits for confirmation
confirmed      = valid internal 1/2 exists and Leg2 breaks again afterwards
invalidated    = strict Waist break before confirmation
extended       = Leg2 was updated by pre-internal extension absorption
hidden         = lifecycle exists but main visibility policy hides it
```

## Confirmation rule

F1 confirms only when all are true:

1. Level 05 body exists: `Origin -> Leg1 -> Waist -> Leg2`.
2. Level 06 valid internal 1/2 exists after Leg2.
3. A favorable strict break beyond Leg2 happens after valid internal 1/2.
4. Waist has not been strictly broken before that confirmation.

A Leg2 break before valid internal 1/2 is extension only. It updates Leg2 when absorption is enabled and never confirms F1.

## Invalidation rule

Before confirmation, F1 invalidates only on strict Waist break. Equality with Waist is not invalidation.

## F2 authorization rule

F2 may only be attempted from an F1 event where:

```text
level == F1
status == confirmed
has_confirm == true
lifecycle_can_spawn_f2 == true
```

No body-only F1, post-flag F1, hidden invalidated F1, or failed phase-gate origin may authorize F2.

## Audit requirements

`FP_LEVEL07` must report:

```text
origin attempts
phase-boundary attempts
fail-open attempts
phase gate pass/reject
body missing
body complete
candidate
post_flag
confirmed
invalidated
extended
visible
hidden
f2_ready
duplicate_rejected
emitted_roots
max_ext
```

Optional samples must expose `lifecycle_id`, phase/fail-open tags, body/internal readiness, F2 authorization, extension count, visibility, hidden reason, and lifecycle reason.

## Acceptance tests

### Test 01 — F2 cannot spawn before confirmed F1

A two-leg F1 body or post-flag F1 without confirmation must never become an F2 parent.

### Test 02 — Leg2 break before internal 1/2 is extension

A favorable break before valid internal 1/2 must increment extension evidence and not confirm F1.

### Test 03 — Waist invalidation

A strict Waist break before confirmation must set F1 invalidated and `lifecycle_can_spawn_f2=false`.

### Test 04 — Fail-open tag

A fail-open F1 must have `from_fail_open=true`, lifecycle identity, and must lose to an equivalent phase-boundary F1 during later canonical pruning.

## Failure symptoms

- F2 appears while the parent F1 is only `live_body` or `post_flag`.
- F1 confirmation appears at the same node as pre-internal Leg2 extension.
- Hidden F1 roots have no lifecycle reason.
- Fail-open roots are indistinguishable from Hook-owned roots.
- Renderer toggles change F1 lifecycle counts.

## Freeze condition

Level 07 is frozen when F1 lifecycle states and F2 authorization are visible in audit through `FP_LEVEL07` and `FP_SUMMARY`, while renderer output remains a pure consumer of emitted events.
