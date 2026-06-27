# EXP Flag Counting

This experiment studies fractal, multi-scale, multi-sequence F-counting.

Current implementation path:

- `mql5/Experts/FlagCounting/FlagCountingVNextExperiment.mq5`
- `mql5/Include/FlagCountingVNext/`

Core documents:

- `docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3.md`
- `docs/flag_counting/FLAG_COUNTING_ALGORITHM_BLUEPRINT.md`
- `docs/flag_counting/FLAG_COUNTING_VISUALIZATION_SPEC.md`

Visualization rule:

- draw body only,
- stack labels by scale and F-level,
- keep the strongest label closest to the price structure,
- use larger thickness/fonts for larger scales.
