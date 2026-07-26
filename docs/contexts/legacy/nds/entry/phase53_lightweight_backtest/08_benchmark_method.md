# Benchmark Method

The lightweight engine records in-memory microsecond timing for every structural run.

At deinitialization it reports:

```text
runs
successful runs
failed runs
Hook rebuild runs
position fast-path runs
average microseconds
maximum microseconds
last-run microseconds
```

## Comparison procedure

1. Use the same symbol, timeframe, date range, deposit, spread model, and tester mode.
2. Run `FlagCountingPhoenixExperiment` with execution enabled and all optional exports disabled.
3. Run `NDSHookLimitF123Backtest` with `PARITY`.
4. Compare trades and F123 exits.
5. Run the lightweight expert with `FAST` and compare elapsed time.
6. Investigate only decision differences, not expected drawing or CSV differences.

## Acceptance

- PARITY must preserve the executable decisions for the same configuration.
- FAST must preserve local-rule behavior and disclose context-window differences.
- No chart objects, timer events, license calls, or research pipelines may appear in the lightweight call path.
