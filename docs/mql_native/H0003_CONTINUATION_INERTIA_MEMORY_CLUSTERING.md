# H0003 — Continuation Inertia, Volatility Memory, and Clustering

## Research question

H0003 asks whether the higher volatility created in the node territory has stronger inertia after continuation exits than after reversal exits, and whether that post-event volatility memory is clustered in time.

## Reuse policy

H0003 deliberately reuses M0001 and M0002 modules. It does not create a new event definition. Events come from `DAL_M0001ComputeEvents()`. Branch labels come from M0002 reversal/continuation classification. RTV windows remain `EVENT_RTV_LOCKED`. This keeps the project semantics consistent across H0001, H0002, and H0003.

## Core tests

1. Event inertia: continuation event logRTV should be higher than reversal event logRTV.
2. Horizon memory: continuation horizon deltas should remain higher than reversal deltas over h1/h2/h3/h4 configured horizons.
3. Carry ratio: continuation should preserve a larger fraction of its event volatility into future horizons.
4. Cluster memory: continuation delta logs should remain positive under day/week cluster aggregation.
5. High-volatility run structure: continuation high-delta events are checked for run behavior above the continuation median and p75 thresholds.

## Outputs

The M0003 EA prints:

- `DAL_M0003_FINAL_AUDIT`
- `DAL_M0003_FINAL_SUMMARY`
- `DAL_M0003_FINAL_INERTIA_MEMORY`
- `DAL_M0003_FINAL_REVERSAL_CLUSTER`
- `DAL_M0003_FINAL_CONTINUATION_CLUSTER`
- `DAL_M0003_FINAL_REVERSAL_HIGH_RUNS`
- `DAL_M0003_FINAL_CONTINUATION_HIGH_RUNS`

## Interpretation

If continuation has lower frequency, higher event logRTV, higher horizon deltas, higher carry ratios, positive cluster-robust day/week means, and heavier high-volatility runs, then the hypothesis is strengthened: continuation is not merely a stronger branch inside the event; it is a volatility-memory state.
