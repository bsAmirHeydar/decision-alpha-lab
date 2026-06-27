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

## Clean-All Visualization Update

The renderer should not hide accepted sequences by default. Instead, it makes every visible sequence easier to read:

- All F body lines use the same thin width by default (`InpFixedLineWidth = 1`).
- Larger scales no longer become visually heavier by line width; scale remains available through labels, logs, and sequence identity.
- Each sequence receives a subtle shade variation inside its own direction/status color family (`InpUseSequenceColorShades = true`).
- Bullish, bearish, live, confirmed, F3 terminal, and ND color families remain distinct, but individual sequence shades help separate overlapping paths.
- ND / Hook phases are text-only labels (`ND`) and do not draw additional body lines. This keeps the chart informative without adding line noise.
- The visual objective is to show all accepted/provisional structures while preventing scale thickness and repeated labels from overwhelming the price chart.

Relevant inputs:

- `InpScanND`
- `InpDrawND`
- `InpMaxNDPerScale`
- `InpUseSequenceColorShades`
- `InpFixedLineWidth`
- `InpNDColor`

