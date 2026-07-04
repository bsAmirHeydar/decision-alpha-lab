# Phase 16 — Sequence Draw Modes

## Reason

Phase 15 made the sequence inspector too strict by hard-capping `SEQUENCE_CYCLE_DEBUG` to a single sequence. That solved clutter, but it also hid the surrounding sequence-counting context.

Phase 16 adds explicit draw modes so the Hook inspector can show more than one sequence without returning to the previous P05/P06/P04 label pileup.

## New Phase 02 input

```text
InpHookPhase02SequenceDrawMode
```

Modes:

```text
FP_HOOK_P02_DRAW_RECENT_N
FP_HOOK_P02_DRAW_LATEST_PER_SCALE_DIRECTION
FP_HOOK_P02_DRAW_BY_SCALE_RECENT_N
FP_HOOK_P02_DRAW_BY_SEQUENCE_ID
```

## Supporting inputs

```text
InpHookPhase02MaxSequencesToDraw
InpHookPhase02SequenceDrawScaleL
InpHookPhase02SequenceDrawDirection
InpHookPhase02SequenceDrawSequenceId
```

Direction filter:

```text
0  = both directions
1  = positive only
-1 = negative only
```

Scale filter:

```text
0  = all scales
5  = only L5
13 = only L13
```

## Recommended views

### Balanced context

```text
InpHookPhase02SequenceDrawMode = FP_HOOK_P02_DRAW_LATEST_PER_SCALE_DIRECTION
InpHookPhase02MaxSequencesToDraw = 6
InpHookPhase02SequenceDrawScaleL = 0
```

### One scale inspection

```text
InpHookPhase02SequenceDrawMode = FP_HOOK_P02_DRAW_BY_SCALE_RECENT_N
InpHookPhase02SequenceDrawScaleL = 5
InpHookPhase02MaxSequencesToDraw = 4
```

### Exact sequence inspection

```text
InpHookPhase02SequenceDrawMode = FP_HOOK_P02_DRAW_BY_SEQUENCE_ID
InpHookPhase02SequenceDrawSequenceId = 931
```

## Phase 07 interaction

`SEQUENCE_CYCLE_DEBUG` no longer hard-caps visible sequences to 1. It uses `InpHookPhase07MaxSequencesToDraw` and Phase 02 draw-mode filters while still hard-disabling P03/P04/P05/P06 drawing.
