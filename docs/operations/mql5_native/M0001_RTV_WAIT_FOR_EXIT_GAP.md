# M0001 RTV Waits for Exit-Gap Closure

## Rule

RTV is calculated only after the event has actually closed by exit-gap:

```text
high/low must not intersect the frozen event zone
for exit_gap consecutive candles
```

Any candle that intersects the frozen zone resets the outside counter.

## RTV-ready condition

```text
rtv_ready = touch_confirmed && full_baseline_available && mean_before > 0
```

So HUNT-before-confirmation events can still exist for visual audit, but they are
not included in RTV mean/median and are written as non-ready/n/a.

## Sample construction

After exit-gap closure:

```text
event_length = exit_index - entry_index + 1
rtv_sample_length = event_length - exit_gap
inside sample = entry .. entry + rtv_sample_length - 1
before sample = same number of candles immediately before entry
```

The final outside confirmation candles are not included in the inside volatility sample.

## Version

`M0001_LiveVisualLab.mq5` version: `1.50`.
