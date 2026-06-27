# EXP_flag_counting — Sequence Contract V2 Index

This experiment should follow the English Flag Counting Sequence Contract V2.

Primary documents:

```text
docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md
docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2.md
docs/flag_counting/FLAG_COUNTING_STATE_MACHINE_V2.md
```

Implementation goal:

```text
Replace sliding-window F detection with a chained high/low-only sequence engine.
```

Core chain:

```text
F1 -> F2 -> F3 -> locked sequence
```

Core high-level rules:

```text
1. Use high/low nodes only.
2. Preserve all raw highs/lows.
3. Compress contextually with adaptive L.
4. F1 starts after ND or opposite sequence end.
5. F1 invalidation is waist.
6. F2 starts only after confirmed F1.
7. F2 invalidation is origin, not waist.
8. F3 completes with the two-leg body.
9. After F3, sequence locks and remains on chart.
10. Rejected structures are logged but not shown on the main chart.
```

Next safe implementation path:

```text
1. Build audit-first node compression.
2. Build ND detector independent of F detector.
3. Build common two-leg flag geometry.
4. Build F1 state machine.
5. Build F2 parent-child state machine.
6. Build F3 lock/extension logic.
7. Only then rebuild renderer.
```

Do not continue patching only the renderer while the detector still behaves like a local four-node scanner.
