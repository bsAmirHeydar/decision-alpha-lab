# D0005 — H5 No-Future Walk-Forward Audit

D0005 is a diagnostic Expert Advisor for H0005/M0001/M0002 live-validity debugging.

The goal is to detect and prevent look-ahead leakage in H5 regime and node logic. The audit does not build one full historical array at startup for decisions. Instead, it replays history candle by candle. On each simulated candle, it requests only the prefix ending at that candle and then rebuilds M0001 nodes, M0001 events, and M0002 branch regime from that prefix only.

## Strict no-future contract

For every simulated step:

1. The cursor is a closed candle.
2. The EA calls `CopyRates` only for `oldest_time -> cursor_time`.
3. No candle after `cursor_time` is copied into the working `DALBar` array.
4. Structural nodes are accepted only when their `active_from_index` is not in the future relative to the cursor.
5. M0002 regime is derived from events computed on the same prefix.
6. The output row logs the latest live-available regime at that cursor.

This makes D0005 different from a full-array research report. Full-array reports are useful for exploration, but they can accidentally behave as if a pivot node was known before its right-side confirmation bars existed. D0005 is designed to expose that difference.

## Main outputs

The EA prints:

- `DAL_D0005_AUDIT_START`
- `DAL_D0005_WF_STEP`
- `DAL_D0005_AUDIT_SUMMARY`
- `DAL_D0005_LIVE_STEP`

The most important fields are:

- `futureNodeViolations`: should be `0`.
- `passNoFuture`: should be `true`.
- `last`: latest prefix-only regime outcome.
- `reversalSteps` and `continuationSteps`: how often the live-available H5 regime was in each state.
- `regimeChanges`: number of live-detected regime changes.

If `InpWriteCsv=true`, the audit also writes a CSV file under the terminal `MQL5/Files` directory.

## Recommended first run

Use a moderate window first:

```text
InpReplayClosedBars = 1500
InpWarmupClosedBars = 250
InpPrintEveryNSteps = 100
InpPrintOnlyOnRegimeChange = false
InpWriteCsv = true
```

For very strict visual debugging:

```text
InpPrintOnlyOnRegimeChange = true
InpProbeLiveOnNewClosedBar = true
```

## Interpretation

If the summary reports:

```text
futureViolationSteps=0
pass=true
```

then the stepwise prefix audit did not detect an obvious future-node availability leak.

If `futureViolationSteps` is non-zero, H5/M0001 is exposing nodes whose `active_from_index` is after the simulated cursor. That means execution or reporting code must be fixed before trusting H5 live validity.

## Important distinction

D0005 validates the data-availability contract. It does not prove that an H5 edge is profitable. Profitability still requires separate execution-level reports, costs, robustness tests, symbol/timeframe splits, and Monte Carlo or permutation checks.
