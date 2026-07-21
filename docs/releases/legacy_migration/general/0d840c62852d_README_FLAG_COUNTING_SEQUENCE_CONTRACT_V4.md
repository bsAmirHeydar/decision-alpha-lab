# EXP Flag Counting — Sequence Contract V4

Sequence Contract V4 remains the active semantic contract, but it is subordinate to the current canon:

```text
docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md
```

Use V4 for the F1/F2/F3 and Hook/ND semantic rules after reading the current canon.

Active implementation path:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
mql5/Include/FlagCountingPhoenix/
```

Important V4 rules retained by the current canon:

- Nodes come from the existing project node logic.
- L is the existing left/right candle clearance definition.
- The algorithm uses high/low nodes only.
- Equality does not count as break.
- F1 starts from a phase boundary unless fail-open diagnostic recovery is explicitly used.
- F2 starts only after F1 confirmation and uses strict-window backfill.
- F3 starts only after F2 confirmation and uses strict-window backfill.
- F2 is size-compared to F1 only.
- F3 uses OR qualification against F2: Leg1 L ratio or flag size ratio.
- Hook/ND detection is branch-based.
- ND is 3 or 4 nodes only; 2 is not ND.
- F3 locks on the first confirmed opposite F1.
- Locked F3 never disappears.
