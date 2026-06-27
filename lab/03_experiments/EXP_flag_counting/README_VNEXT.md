# EXP Flag Counting vNext

Use `FlagCountingVNextExperiment.mq5` for the next implementation round.

The old scanner-based experts are considered experimental history. The vNext module implements the current design contract:

- multi-scale node streams,
- parallel sequence registry,
- F1 root,
- mandatory F2 child from F1 Internal 2,
- mandatory F3 child from F2 Internal 2 when available,
- F1 Waist invalidation,
- F2 Origin invalidation,
- F3 terminal body behavior,
- body-only chart rendering,
- audit logging behind an input flag.

Compile target:

`mql5/Experts/FlagCounting/FlagCountingVNextExperiment.mq5`
