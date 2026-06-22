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

Release 101 uses the simple definition requested by the user.

### 123 سقف

```text
سه سقف اخیر تایم بالا، هرکدام بالاتر از قبلی
HIGH1 < HIGH2 < HIGH3
```

Counter-direction trade:

```text
SELL on every M1 HIGH hook
```

### 123 کف

```text
سه کف اخیر تایم بالا، هرکدام پایین‌تر از قبلی
LOW1 > LOW2 > LOW3
```

Counter-direction trade:

```text
BUY on every M1 LOW hook
```

No alternating LOW-HIGH-LOW / HIGH-LOW-HIGH sequence is required anymore.

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

## Release 101

Changed HTF 123 detection from alternating swing triples to the simple rule:

```text
3 recent higher highs -> counter SELL
3 recent lower lows   -> counter BUY
```

Everything else remains candle-based and simple.


## Release 102 — HTF third opposite swing TP

Default exit changed to:

```text
InpExitMode = DAL_E0009_EXIT_HTF_THIRD_OPPOSITE_SWING
InpHTFTpSwingCount = 3
```

This uses the same higher timeframe that created the 123.

### BUY exit

If the trade is BUY after three falling HTF lows:

```text
after the position entry time,
count confirmed HTF HIGH nodes
TP = 3rd HTF HIGH
```

### SELL exit

If the trade is SELL after three rising HTF highs:

```text
after the position entry time,
count confirmed HTF LOW nodes
TP = 3rd HTF LOW
```

TP is usually not known at order placement. The EA leaves TP empty at entry and updates the open position when the required HTF swing node becomes confirmed.

## Release 103 — why no trades were appearing

The first E0009 versions could easily show no trades because:

```text
1. InpTradingEnabled was false by default.
2. Only the latest M1 hook was checked.
3. Only LIMIT orders were supported.
4. If the latest hook was hunted/invalid, every other hook was ignored.
5. Reject reasons were mostly hidden unless reject logs were enabled.
```

Release 103 fixes the execution shell:

```text
InpOrderMode = DAL_E0009_ORDER_AUTO
InpMaxHookCandidatesPerBar = 6
InpPrintRejectLogs = true
```

### Order modes

```text
DAL_E0009_ORDER_LIMIT_REVISIT
DAL_E0009_ORDER_STOP_RECLAIM
DAL_E0009_ORDER_MARKET_ON_CONFIRM
DAL_E0009_ORDER_AUTO
```

`AUTO` chooses:

```text
BUY:
    trigger below Ask  -> BUY LIMIT
    trigger above Ask  -> BUY STOP
    trigger near Ask   -> BUY MARKET

SELL:
    trigger above Bid  -> SELL LIMIT
    trigger below Bid  -> SELL STOP
    trigger near Bid   -> SELL MARKET
```

### Multiple hook scan

Instead of checking only the latest M1 hook, release 103 scans the latest eligible hooks:

```text
InpMaxHookCandidatesPerBar = 6
```

### Debug counters

The audit line now prints:

```text
hookSeen
hookAfterTimeReject
hookAgeReject
hookZoneFail
hookHuntedReject
hookBuilt
geometryReject
riskReject
capReject
duplicateSkip
```

These counters show exactly where the EA is blocking trades.


## Release 104 — compile fix

Fixed one hard compile error and the initialization warnings from release 103:

```text
removed stale c.one_order_per_hook assignment
initialized hh1/hh2/hh3 and ll1/ll2/ll3 before branch use
```

No trading logic changed.
