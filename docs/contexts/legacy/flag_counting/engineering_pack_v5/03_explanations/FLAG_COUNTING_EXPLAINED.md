# Flag Counting Explained

## The Model in One Sentence

Flag Counting treats movement as a sequence of owned two-leg structures, where each structure must have a legitimate origin, phase context, lifecycle role, and post-body behavior.

## Why Sliding Windows Failed

A sliding-window detector sees any local alternating pattern:

```text
Low -> High -> Low -> High
```

and may call it a bullish flag.

This is wrong because it cannot answer:

- Why did the flag start there?
- Which sequence owns it?
- Is it F1, F2, or F3?
- Is it inside a larger active chain?
- Did it begin from ND, opposite sequence end, or arbitrary mid-move noise?
- What invalidates it?
- What does it produce next?

This caused orphan lines that started from the middle of moves.

## Sequence-Based Interpretation

A sequence chain begins at a phase boundary.

```text
Phase Boundary -> F1 -> F2 -> F3 -> Opposite F1 Lock
```

The engine is not allowed to restart F1 at every local opportunity.

After F1 confirms, the system searches for F2 in the same chain.

After F2 confirms, the system searches for F3.

F3 terminates the chain.

## Why Every Movement Should Belong Somewhere

The model tries to avoid idle movement. However, belonging somewhere does not mean becoming a new flag. A movement may be:

- extension of existing Leg2;
- post-flag correction;
- hook/ND;
- child candidate that later dies;
- F3 extension;
- opposite F1 that locks F3;
- part of a parent sequence context.

The system must assign movement to a role, not invent a fresh F1 in the middle.

## The Difference Between Logic and Rendering

Logic emits objects.

Rendering draws them.

If the chart is messy, do not let renderer invent filters that change meaning. Fix object identity, sequence ownership, lifecycle, and label layout.

A clean chart must still be a faithful chart.

## What Makes a Flag Real

A flag is real enough to draw only when it can specify:

```text
Origin
Leg1
Waist
Leg2
Direction
F-level or candidate role
Owning sequence
Status
Invalidation boundary
Next expected phase
```

If those fields are missing, the object should be a hidden seed or audit event, not a chart flag.
