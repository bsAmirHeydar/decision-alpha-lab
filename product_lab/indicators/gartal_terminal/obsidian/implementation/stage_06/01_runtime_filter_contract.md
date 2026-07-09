# Runtime Filter Contract

Stage 06 separates boot configuration from runtime control.

```text
GT_Config      = immutable boot preset
GT_FilterState = mutable dashboard/session state
GT_NewsStore   = canonical event data
```

The filter engine may mutate `GT_FilterState` only. It must not delete, rewrite, or reorder events.

## Mutable Fields

- `currencies_csv`
- `show_low`
- `show_medium`
- `show_high`
- `show_holiday`
- `show_speech`
- `show_tentative`
- `show_breaking`
- `show_past_events`
- `only_symbol`

## Non-Mutable Fields

- source data;
- parsed event time;
- impact rank;
- release values;
- broker GMT config.
