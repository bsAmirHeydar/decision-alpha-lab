# M0001 Pending Touch and Hunt Priority

## Correction

A zone touch is not immediately a confirmed TOUCH consumption.

It is first a pending touch / active event.

```text
first zone touch -> pending touch / event starts
```

During this pending event, the node can still be hunted.

```text
node break before exit_gap confirmation -> CONSUMED:HUNT
exit_gap outside frozen zone without node break -> CONSUMED:TOUCH
```

## Priority

HUNT always has priority over TOUCH while a touch event is pending.

For a LOW node:

```text
bar.low < node_price -> HUNT
```

For a HIGH node:

```text
bar.high > node_price -> HUNT
```

## TOUCH confirmation

TOUCH is confirmed only after:

```text
outside_count >= InpExitGap
```

using the frozen event territory from the first touch candle.

## Why

This keeps the state machine faithful to the intended model:

```text
TRACKING
-> PENDING TOUCH / ACTIVE EVENT
   -> HUNT if node breaks before event confirmation
   -> TOUCH if event exits cleanly for exit_gap candles
-> CONSUMED
```

## Version

`M0001_LiveVisualLab.mq5` version: `1.31`.
