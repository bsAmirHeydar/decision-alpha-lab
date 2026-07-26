# Phase 23 Compile Fix — Grouped Semicircle Visual Helper

## Issue

MetaEditor reported that `FP_HookP02CreateArcBetweenPoints` was undeclared and also rejected local reference variables such as:

```mql5
const FP_HookPhase02Sequence &seq = sequences[i];
```

## Fix

- Adds the missing `FP_HookP02CreateArcBetweenPoints` helper before `FP_HookP02CreateCycleArc`.
- Replaces invalid local reference aliases with value copies:

```mql5
FP_HookPhase02Sequence seq = sequences[i];
FP_HookPhase02Sequence seed = sequences[i];
```

## Behavior

No visual semantics changed. The grouped Hook semicircle remains:

- one arc per Hook-origin group
- start at origin
- end at directional group extreme
- dim gray envelope arc
