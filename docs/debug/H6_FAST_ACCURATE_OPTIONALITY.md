# H6 Fast Accurate Optionality Report

This release makes the standalone H0006 optionality report faster and more execution-realistic without returning to samples.

## Contract

H6 remains atomic and no-sample:

- `sampleCalls=0`
- `branchSamplesBuilt=0`
- `m0002Calls=0`
- sequence is built from raw M0001 known-time batches
- events that become known on the same candle are simultaneous, not sequential

## Accuracy change

The default H6 entry anchor is now `NEXT_OPEN`.

Previously, future optionality used the known candle close as the anchor. The new default measures future excursion from the next candle open, which is closer to what could be acted on after the regime batch becomes knowable.

Set `InpH6EntryAnchorMode=0` to compare against the old known-close anchor.

## Speed controls

H6 stress and edge maps now have levels:

- `InpH6StressMode=0`: no optionality stress.
- `InpH6StressMode=1`: fast null using mean absolute excursion and hit-rate above Tail2. No per-iteration quantile sorting.
- `InpH6StressMode=2`: full null including P90 comparison. Slower.

Edge map level:

- `InpH6EdgeMapLevel=0`: off.
- `InpH6EdgeMapLevel=1`: core buckets only: all, multi-event, 3+ event, run-start, run-continuation.
- `InpH6EdgeMapLevel=2`: full buckets including single-event and buy/sell dominant buckets.

Horizon toggles:

- `InpH6ReportFastHorizon`
- `InpH6ReportMainHorizon`
- `InpH6ReportSlowHorizon`

Turning off slow horizon is the fastest way to reduce work while preserving fast/main diagnostics.

## New audit line

Each horizon prints:

`DAL_H0006_COMPUTE_AUDIT_<FAST|MAIN|SLOW>`

It reports the horizon, valid count, entry anchor, and the one-pass cached measurement contract.
