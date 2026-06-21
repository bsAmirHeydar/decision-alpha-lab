# H6 Candle-Stream Fast Optionality

Release 108 changes the standalone H0006 report from a heavy batch/edge-map workflow into a fast forward candle-stream workflow by default.

## Contract

- Still atomic and no-sample.
- Still uses raw M0001 known-time batches.
- Still treats same-known-time events as simultaneous.
- Mixed reversal/continuation batches remain ambiguous and are skipped from pure H6 measurements.
- The H6 measurement starts only after the batch is known.

## Engine

Default engine: `CANDLE_FORWARD_STREAM`.

For each pure known-time batch at bar `k`, H6 opens an observation at `k+1` using `NEXT_OPEN` by default. Then the engine walks candles forward once, updates active observations with each bar's high/low, and closes them when their horizon matures.

This avoids repeated horizon scans for optionality and avoids strict prefix rebuilds. It is candle-forward/live-style measurement, not M0002 sample replay.

## Speed defaults

Daily default inputs are intentionally light:

- stress off
- edge map off
- slow horizon off
- full-horizon-only on
- forward stream on

Use the heavier settings only for final research reports.

## Key audit fields

Look for:

- `h6Engine=CANDLE_FORWARD_STREAM`
- `measurement=candle_forward_stream_no_prefix_rebuild_no_sample`
- `fullHorizonOnly=1`
- `opened`, `closed`, `leftOpen`, `skippedIncomplete`, `maxActive`
