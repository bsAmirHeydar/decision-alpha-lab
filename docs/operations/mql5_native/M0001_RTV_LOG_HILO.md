# M0001 RTV — Log High/Low Volatility

## Formula

For each candle:

```text
candle_vol = abs(log(high / low))
```

For each event/revisit:

```text
rtv_inside = average(candle_vol over the RTV sample)
rtv_before = average(candle_vol over the same number of candles before entry)
RTV = rtv_inside / rtv_before
```

## Exit-gap exclusion

When a touch is confirmed by `exit_gap` consecutive candles outside the frozen
event zone, those final outside confirmation candles are not counted in the RTV
inside sample.

```text
event_length = exit_index - entry_index + 1
rtv_sample_length = event_length - exit_gap
```

So if:

```text
entry = 100
exit confirmation = 112
exit_gap = 6
```

then:

```text
full event bars = 100..112
RTV inside bars = 100..106
RTV before bars = 93..99
```

The outside confirmation bars `107..112` confirm that the event is over, but they
are not part of the volatility sample being measured inside the territory event.

## HUNT before confirmation

If a node is hunted before touch confirmation, no exit-gap exclusion is applied:

```text
rtv_sample_length = event_length
```

## Visual

`InpShowRTV` controls RTV labels:

```text
InpShowRTV = true
```

Labels:

```text
RTV 1.42
RTV n/a
```

`RTV n/a` appears when there are not enough baseline candles before entry.

## Version

`M0001_LiveVisualLab.mq5` version: `1.48`.
