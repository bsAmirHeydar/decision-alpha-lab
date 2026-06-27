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

## Child origin invalidation and parent continuity

A developing child F has its own independent Origin: F2 starts from the parent F1 internal-2 node, and F3 starts from the parent F2 internal-2 node. If the child touches or crosses its own Origin before it completes a coherent body/continuation, only that child candidate is invalidated and removed from rendering. The parent remains alive unless the parent’s own invalidation level is hit.

This rule is semantic, not only visual: an event whose own leg start has been consumed must not remain as an orphan line on the chart, and later movement must not be attached back to that dead child origin.
