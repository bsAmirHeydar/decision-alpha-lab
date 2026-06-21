# VAL0018 — H6 Candle-Stream Fast Optionality

Purpose: validate H0006 optionality using a faster forward candle-stream measurement.

Recommended first run:

- `InpH6CandleStreamMode=true`
- `InpStressH6Optionality=false`
- `InpPrintH6EdgeMap=false`
- `InpH6ReportSlowHorizon=false`
- `InpH6RequireFullHorizon=true`
- `InpH6EntryAnchorMode=1`

Expected audit:

- `sampleCalls=0`
- `branchSamplesBuilt=0`
- `m0002Calls=0`
- `h6Engine=CANDLE_FORWARD_STREAM`
- `measurement=candle_forward_stream_no_prefix_rebuild_no_sample`

Escalation run for publication:

- enable slow horizon
- set stress mode to 1 first
- only use stress mode 2 and full edge map after the fast report identifies candidate conditions
