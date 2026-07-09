# Touch-Only Hunt and Candle-Close Confirmation

## Hunt

A hunt is level touch or level breach.

High hunt:

```text
current_high >= reference_high
```

Low hunt:

```text
current_low <= reference_low
```

## Equality

Equal high is hunt.
Equal low is hunt.

There is no tolerance layer in the baseline model.

## Confirmation

The touch itself can happen intrabar, but divergence is not valid until the relevant chart timeframe candle closes.

Therefore:

```text
open candle = no confirmed divergence
closed candle = eligible for divergence check
```

## MQL5 implication

Use the last closed bar, not the current forming bar.

```text
bar shift 1 = confirmation candidate
bar shift 0 = forbidden for trade signal confirmation
```

