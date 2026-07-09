# 10 — Open Questions Before Coding

This file lists decisions that should be clarified before or during the first MQL5 implementation. None of these block the documentation layer, but they affect exact runtime behavior.

## 1. Reference mode

Current baseline:

```text
Compare current cycle against immediately previous completed cycle in same CG.
```

Possible alternatives:

```text
Compare current cycle against all previous cycles of same CG in same day.
Compare against selected previous N cycles.
Compare against highest high / lowest low among previous cycles.
```

Recommendation for first code:

```text
previous-cycle-only
```

Reason:

- deterministic;
- simpler duplicate prevention;
- clean for first backtest;
- can later be extended without rewriting architecture.

## 2. Multiple CG simultaneous signals

Question:

```text
If cg_30m and cg_180m both trigger on the same candle and same clean symbol, should both trade?
```

Recommended baseline:

```text
InpOnePositionPerSymbol = true
```

So only one active EXP0017 position per symbol is allowed. Others are logged/drawn but not traded.

## 3. Same CG buy and sell conflict

Question:

```text
If high-side and low-side divergence both occur in the same CG on the same confirmation candle, should the EA trade both?
```

Recommended baseline:

```text
Skip trading that CG for that candle and mark event as conflict.
```

## 4. Drawing when hunter is not chart symbol

Question:

```text
Should EA open or control a second chart to draw hunter-symbol lines?
```

Recommended baseline:

```text
Do not draw price-scale line if chart symbol != hunter symbol.
Log the event instead.
```

Future version can implement multi-chart drawing.

## 5. New York DST handling

Question:

```text
Should the EA automatically calculate NY daylight saving time?
```

Recommended first version:

```text
Manual InpNewYorkUtcOffsetHours input.
```

Reason:

- transparent;
- less error-prone than fragile custom DST logic;
- user explicitly requested conversion input.

## 6. Target interpretation

User said:

```text
Target is the end of the same cycle in the cycle group.
```

This is interpreted as:

```text
time-based close at cycle end
```

No price TP is attached by default.

Question:

```text
Should a TP price also be set? If yes, how is it computed?
```

Recommended baseline:

```text
No TP price; scheduled time exit only.
```

## 7. Minimum time before cycle end

Question:

```text
Should the EA enter if only a few seconds remain before cycle end?
```

Recommended safety input:

```cpp
input int InpMinSecondsBeforeCycleEndForEntry = 30;
```

But this was not in the user's original required input list.

## 8. Spread and slippage rules

Question:

```text
Should spread filters block entries?
```

Recommended first version:

```text
No strategy-level spread filter unless user requests it.
```

But log spread at entry for audit.

## 9. Broker symbols and contract specs

SPXUSD and NDXUSD differ across brokers. Risk sizing depends on symbol tick value and tick size.

Question:

```text
Should there be custom tick value override inputs?
```

Recommended first version:

```text
Use broker-provided SymbolInfoDouble values.
Skip trade if invalid.
```

## 10. Persistence

The user does not need previous-day data for entry, but live positions need scheduled exits after restart.

Recommendation:

```text
Persist open EXP0017 position lifecycle state to CSV.
```

This is operational persistence, not signal-reference persistence.

