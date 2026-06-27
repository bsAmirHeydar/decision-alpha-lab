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

## ND / Hook Detection Contract

The VNext implementation now detects ND / Hook phases as first-class text-only events, not only as gaps left after F rendering. For each active scale, the detector scans consecutive compressed node windows of 3 or 4 nodes and accepts a provisional ND when the final high/low node reaches at least 50% toward the active extreme of that node window. This follows the documented rule that an ND does not need a 90% return; a minimum 50% high/low extreme ratio is enough for research visibility.

Important inputs:

- `InpScanND`: enables ND detection.
- `InpDetectAllND`: when true, scan all valid 3/4-node ND windows in each scale; when false, only unowned gaps are marked as ND.
- `InpMaxNDPerScale`: caps ND labels per scale for visual control.
- `InpNDMinNodes`: default 3.
- `InpNDMaxNodes`: default 4.
- `InpNDMinExtremeRatio`: default 0.50.

ND is rendered as text only (`ND`) so it explains the partition without adding more body lines to the chart. Peak-side ND labels are placed above peaks and valley-side ND labels are placed below valleys using the same stacking system as F labels.

### ND high/low-only contract

ND / Hook detection is close-agnostic. It does not care whether a candle closed beyond a level or not. The whole flag-counting grammar currently treats the market through swing highs and swing lows only. ND windows are therefore evaluated from compressed high/low nodes:

- valid ND windows use 3 or 4 alternating high/low nodes;
- the final ND node must reach the configured side of the window by at least `InpNDMinExtremeRatio`;
- `InpNDMinExtremeRatio = 0.50` means the last swing node is at least in the relevant half of the high-low range of that ND window;
- candle open, candle close, candle body, and candle color are not part of the ND definition.



## Origin identity and live-root display contract

The renderer must show coherent live roots by default. A root F1 body does not need to be hidden until internal `1/2` and confirmation; otherwise the chart becomes artificially empty and the research view loses the developing structures. Strict root filters remain optional audit inputs, but their defaults are off.

Orphan control comes from origin identity: if a candidate touches or crosses its own Origin / start of leg, that candidate is invalid and must not be drawn or extended. If it is a child, only the child dies; the parent remains alive unless its own invalidation is hit.

Each rendered F body keeps a traceable identity through `F#/L#/Q#` labels and an `O` origin label, so the chart shows which flag/scale/sequence owns each body and where its first leg starts. ND remains high/low-node based and close-agnostic.
