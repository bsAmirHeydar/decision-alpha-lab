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


## Current root visibility correction

The visual experiment now keeps live coherent F1 roots visible by default. The previous strict defaults made the chart too empty because they required every root to already have internal `1/2` and confirmation before rendering. Those checks are still available as optional inputs, but the default research view is:

- `InpRequireF1Internal12ForRoot = false`
- `InpRequireF1ConfirmedForRoot = false`
- `InpRequireParentConfirmedForNextF = false`

Origin identity is still strict: if a child/candidate touches its own start of leg, only that child dies; the parent remains alive unless its own invalidation is hit.
