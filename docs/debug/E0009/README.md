# E0009 — HTF 123 → M1 Hook Counter Executor

This is the intentionally simple model requested after E0008 became too complicated.

## Rule

```text
When a higher timeframe closes a 123,
trade counter-direction on every M1 hook.
```

No purple atlas.  
No second hook requirement.  
No heavy MTF context.  
No tick-by-tick processing.

## 123 definition

E0009 uses the latest confirmed 3-node sequence on the higher timeframe.

### Bullish 123

```text
LOW → HIGH → LOW
```

The 3rd point is a confirmed LOW. Counter-direction trade is:

```text
SELL on every M1 HIGH hook
```

### Bearish 123

```text
HIGH → LOW → HIGH
```

The 3rd point is a confirmed HIGH. Counter-direction trade is:

```text
BUY on every M1 LOW hook
```

## M1 hook entry

### BUY hook

```text
latest M1 LOW node after HTF 123 close
entry = M1 hook zone upper + spread
SL = hook node price
```

### SELL hook

```text
latest M1 HIGH node after HTF 123 close
entry = M1 hook zone lower
SL = hook node price + spread
```

## Exit

Default:

```text
InpExitMode = DAL_E0009_EXIT_FIXED_R
InpFixedR = 50
```

Alternative:

```text
DAL_E0009_EXIT_HTF_POINT_2
```

This uses HTF 123 point 2 as TP.

## Performance

The EA runs only on a new execution-timeframe candle:

```text
InpExecutionTF = PERIOD_M1
```

On each new M1 candle:

1. Refresh HTF 123 only if the HTF candle changed.
2. Rebuild a small M1 node map.
3. If a fresh hook exists, place/plan the limit order.

There is no structural processing on every tick.

## First tests

```text
InpTradingEnabled = false
InpHTFTimeframe = PERIOD_M15
InpExecutionTF = PERIOD_M1
InpHTFL = 2
InpM1L = 2
InpExitMode = DAL_E0009_EXIT_FIXED_R
InpFixedR = 50
InpRequireFreshM1HookAfterHTF123Close = true
```
