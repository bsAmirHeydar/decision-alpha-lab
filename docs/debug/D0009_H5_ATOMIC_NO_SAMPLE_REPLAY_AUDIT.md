# D0009 H5 Atomic No-Sample Replay Audit

D0009 is the strict H5 validator for the "do not build samples first" contract.

It never calls `DAL_M0002CollectBranchSamples` and never creates `DALM0002BranchSample` arrays. The replay path is:

```text
closed bars prefix -> confirmed structural nodes -> raw M0001 events -> raw event regime batch -> candidate activation -> entry trigger -> post-entry measurement
```

## Why this exists

Earlier H5 reports were useful structural/path research, but they could still inherit sample/order bias:

- branch samples were built first;
- samples were sorted by outcome/exit/entry order;
- multiple events known on the same candle could become a fake sequence;
- continuation R was normalized by a structural denominator even when no trading stop existed.

D0009 removes that layer for validation. Regime state is derived directly from raw M0001 events that are already knowable by the current replay candle.

## Regime construction

For every replay step, D0009 loads only the bars available up to that closed candle. It computes M0001 nodes and raw M0001 events on that prefix only.

For each closed/touch-confirmed raw event, D0009 classifies the event directly:

- LOW node: close above node at known candle = reversal; close below = continuation.
- HIGH node: close below node at known candle = reversal; close above = continuation.

All raw events with the same known candle are one simultaneous batch. If a batch contains both reversal and continuation, it is ambiguous and skipped by default.

## Entry model

After the regime is known:

- Reversal candidates are untouched LOW/HIGH node zones on the opposite side of market and fill only on later zone touch.
- Continuation candidates are untouched HIGH/LOW node break zones and fill only on later close-break or intrabar-break depending on input.

## Risk/R measurement

Reversal uses zone-edge structural risk. Continuation can use either:

- ATR risk: default, `InpContinuationRiskMode = DAL_D0009_CONT_RISK_ATR`;
- structural zone risk: diagnostic only.

The output R statistics are therefore tied to an explicit risk mode, not an implicit sample path denominator.

## Key log lines

```text
DAL_D0009_AUDIT
DAL_D0009_SUMMARY_ALL
DAL_D0009_SUMMARY_REVERSAL
DAL_D0009_SUMMARY_CONTINUATION
```

`DAL_D0009_AUDIT` must show:

```text
sampleCalls=0
branchSamplesBuilt=0
contract=no_samples_raw_events_only
```

