# VAL0017 — H6 Fast Accurate Optionality

Goal: keep H0006 standalone and atomic/no-sample while reducing runtime and improving execution realism.

## What changed

1. Default anchor is `NEXT_OPEN`, not the known candle close.
2. Stress can run in fast mode using mean excursion and Tail2 hit-rate instead of full quantile sorting.
3. Edge map can run in core mode instead of full bucket mode.
4. Fast/main/slow horizons can be enabled independently.

## Recommended quick run

- `InpH6StressMode=1`
- `InpH6EdgeMapLevel=1`
- `InpH6ReportFastHorizon=true`
- `InpH6ReportMainHorizon=true`
- `InpH6ReportSlowHorizon=false`
- `InpH6EntryAnchorMode=1`

## Recommended final run

- `InpH6StressMode=2`
- `InpH6EdgeMapLevel=2`
- all horizons enabled
- `InpPermutationIterations=500`

## Interpretation

This validation does not ask whether reversal has a better win rate. It asks whether reversal known-time batches mark fatter optionality tails compared with continuation and with shuffled labels.
