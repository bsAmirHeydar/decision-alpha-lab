# EXP Flag Counting - Sequence Contract V4

This experiment must use the V4 contract documents as the implementation authority:

- `docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md`
- `docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V4.md`
- `docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V4.md`

The critical update in V4 is that the detector must become a sequence engine, not a sliding-window scanner.

Important V4 rules:

- Nodes come from the existing project node logic.
- L is the existing left/right candle clearance definition.
- The algorithm uses high/low nodes only.
- Equality does not count as break.
- F1 starts only from a phase boundary.
- F2 starts only after F1 confirms but backfills its origin from the post-F1 correction context.
- F3 starts only after F2 confirms but backfills its origin from the post-F2 correction context.
- F2 is size-compared to F1 only.
- F3 uses OR qualification against F2: Leg1 L ratio or flag size ratio.
- Hook/ND detection is branch-based and may have multiple 1s sharing one 2.
- ND is 3 or 4 nodes only; 2 is not ND.
- If any hook branch exceeds 4 nodes, increase L until all branches are <=4.
- F3 locks on the first confirmed opposite F1.
- Locked F3 never disappears.

Before coding, audit the existing detector for every checklist item in V4.
