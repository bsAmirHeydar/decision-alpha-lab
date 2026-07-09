# EXP0017 EN CH14 — Statistical Testing and Performance Metrics

## Thesis

The research engine must test win rate, expectancy, stop behavior, outcome windows, and multiple performance measures over a meaningful sample.

## Doctrine

- Win rate matters as an early health filter because fewer stop-outs matter.
- Expectancy matters as a result layer.
- All metric families should be tested independently.
- A minimum initial study of roughly 400 trading days is appropriate.
- Stop streaks and very bad win rate are major red flags.

## Fields

- `win_rate`
- `stop_rate`
- `expectancy`
- `r_outcome`
- `pip_outcome`
- `max_intraday_reward`
- `stop_streak`

## Implementation Note

- Do not rely only on cycle-end target result.
- Calculate multi-window and maximum intraday outcomes.
