# Status and Lifecycle Definition

## Recommended Status Enum

```text
SEED
BODY_CANDIDATE
LIVE_BODY
POST_FLAG_COUNTING
QUALIFYING
CONFIRMED
COMPLETED
EXTENDING
LOCKED
INVALIDATED
REJECTED
HISTORICAL_HIDDEN
```

## SEED

A partial structure that has not yet formed a complete body.

F1 seed is hidden on main chart.

F2/F3 seed may be displayed because it belongs to an existing confirmed parent context and helps debug stage progression.

## BODY_CANDIDATE

A possible body under construction.

May have Origin/Leg1/Waist but no Leg2 yet.

## LIVE_BODY

A complete two-leg body exists.

```text
Origin -> Leg1 -> Waist -> Leg2
```

For F1, this is the earliest display stage.

## POST_FLAG_COUNTING

The body exists and the engine is tracking post-flag internal numbering.

This is where 1/2/3/4 and ND/Hook may appear.

## QUALIFYING

A child F object has a body but is waiting for size/scale qualification.

F2 may wait for:

```text
F2_size >= F1_size
```

F3 may wait for either OR condition:

```text
F3 Leg1 L >= 0.8 * F2 Leg1 L
OR
F3 size >= 0.7 * F2 size
```

## CONFIRMED

F1 or F2 only.

F1 confirms after post-flag internal numbering and Leg2 re-pass without Waist invalidation.

F2 confirms after internal numbering or waist-break branch and Leg2 re-pass without Origin invalidation.

## COMPLETED

F3 only.

F3 completes after body plus qualification. It does not require post-flag internal numbering.

## EXTENDING

F3 after completion while same-direction movement continues before opposite F1 lock.

## LOCKED

F3 after first confirmed opposite F1 appears.

Locked F3 is persistent.

## INVALIDATED

A live candidate whose own invalidation boundary was passed.

Default display: hidden.

Audit: retained.

## REJECTED

A structure that failed to become the intended object.

Example:

- F2 candidate origin passed before qualification/confirmation.
- F1 candidate Waist passed before confirmation.

Default display: hidden.

## HISTORICAL_HIDDEN

A valid historical object not shown in a clean current-state view due to input.

For confirmed F1/F2 persistence:

```text
InpKeepConfirmedF1F2AfterBoundaryBreak = false
```

Default may hide them after later relevant boundary break, while audit remains.

## Lifecycle Summary

```text
F1:
SEED -> LIVE_BODY -> POST_FLAG_COUNTING -> CONFIRMED
     -> INVALIDATED/REJECTED if Waist passed before confirmation

F2:
SEED -> BODY_CANDIDATE -> LIVE_BODY -> QUALIFYING -> POST_FLAG_COUNTING -> CONFIRMED
     -> INVALIDATED/REJECTED if Origin passed

F3:
SEED -> BODY_CANDIDATE -> LIVE_BODY -> QUALIFYING -> COMPLETED -> EXTENDING -> LOCKED
```
