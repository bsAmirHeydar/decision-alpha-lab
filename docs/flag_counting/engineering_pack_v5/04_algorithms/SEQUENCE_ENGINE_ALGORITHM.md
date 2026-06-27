# Sequence Engine Algorithm

## Purpose

Own the F1 -> F2 -> F3 chain.

Prevent sliding-window behavior.

## Chain States

```text
WAIT_F1_BOUNDARY
BUILD_F1
TRACK_F1_POST_FLAG
F1_CONFIRMED_BUILD_F2
TRACK_F2_POST_FLAG
F2_CONFIRMED_BUILD_F3
F3_COMPLETED_EXTENDING
F3_LOCKED_CLOSED
```

## Phase Boundary Detection

A new F1 may start only from:

- ND/Hook terminal extreme;
- opposite sequence end;
- confirmed opposite F1 that locks previous F3;
- explicitly emitted phase boundary.

If there is already an active F1/F2 in same direction/context, do not start another same-direction F1 unless phase boundary rules permit it.

## F1 Flow

1. Receive phase boundary.
2. Start F1 origin from boundary extreme.
3. Build F1 body.
4. Display only after body complete.
5. Track post-F1 context.
6. If Waist passed before confirmation, reject F1 candidate.
7. If valid internal 1/2 exists and Leg2 is passed again, confirm F1.
8. Authorize F2 and backfill origin from post-F1 context.

## F2 Flow

1. After F1 confirmation, use stored post-F1 deepest adverse correction as F2 origin.
2. Build F2 body.
3. Display seed/leg development for debugging.
4. Wait for size >= F1 size; allow extension.
5. Track post-F2 context.
6. If F2 origin passed, kill F2 candidate only.
7. Keep F1 context and rebuild/search F2 again from owned post-F1 context.
8. If internal 1/2 or waist-break branch exists and Leg2 is passed again, confirm F2.
9. Authorize F3 and backfill origin from post-F2 context.

## F3 Flow

1. After F2 confirmation, use stored post-F2 deepest adverse correction as F3 origin.
2. Build F3 body.
3. Wait for OR qualification; allow extension.
4. When qualified, mark F3 completed.
5. Same-direction movement becomes F3 extension.
6. Listen for first confirmed opposite F1.
7. Lock F3 and close chain.
8. Let the opposite F1 own the new opposite chain.

## Parent/Child Death Rule

Child death does not kill parent context.

```text
F2 dies -> F1 context remains.
F3 candidate dies -> F2 context remains.
```

The dead child identity must not be reused.

## Active Opposite Direction

Opposite direction may produce F1 that locks F3.

Before a chain reaches F3, avoid starting opposite/same arbitrary chains unless phase boundary logic emits them.

## Chain Emissions

The SequenceEngine emits logical objects:

```text
FObject
HookEvent
PhaseBoundary
AuditEvent
```

Renderer consumes these emissions only.
