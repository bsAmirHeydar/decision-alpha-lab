# 06 — Execution and Risk Contract

## 1. Execution objective

When a confirmed CG divergence occurs and trading is enabled for that CG, the EA enters a market trade on the clean symbol.

The clean symbol is the symbol that did not hunt the relevant reference level.

## 2. Trade direction

| Divergence | Hunt side | Trade direction | Trade symbol |
|---|---|---|---|
| Bullish | Low hunt asymmetry | Buy | Clean symbol |
| Bearish | High hunt asymmetry | Sell | Clean symbol |

## 3. Entry timing

Entry is evaluated only after a chart timeframe candle closes.

Recommended MQL5 implementation:

```text
OnTick:
    detect new closed bar on chart timeframe
    if new closed bar:
        run CG detection for all enabled CGs
        register confirmed signals
        send trade if allowed
```

No entry should be generated from an open candle.

## 4. Entry price

Entry is market-based.

For buy:

```text
entry_price = current Ask on clean symbol
```

For sell:

```text
entry_price = current Bid on clean symbol
```

Backtest approximations should use available tester price at signal execution time.

## 5. Stop-loss

The stop-loss is set using the reference level on clean symbol.

### Buy stop

```text
SL = clean_symbol_reference_low
```

### Sell stop

```text
SL = clean_symbol_reference_high
```

No default buffer is used.

Safety check:

```text
For buy, SL must be below entry.
For sell, SL must be above entry.
```

If not true, skip trade and log invalid risk geometry.

## 6. Target model

The target is time-based:

```text
scheduled_exit_time = current_cycle_end_time
```

There is no baseline take-profit price.

The EA must close the position at or immediately after scheduled exit time.

This means a position lifecycle object is required:

```text
position_ticket
symbol
side
cg_name
cycle_index
entry_time
sl
scheduled_exit_time
signal_key
```

## 7. Risk percent

Risk per trade:

```text
1% of current equity
```

Input:

```cpp
input double InpRiskPercentEquity = 1.0;
```

Risk money:

```text
risk_money = AccountInfoDouble(ACCOUNT_EQUITY) * InpRiskPercentEquity / 100.0
```

## 8. Volume calculation

Required values from broker symbol specification:

```text
SYMBOL_TRADE_TICK_SIZE
SYMBOL_TRADE_TICK_VALUE
SYMBOL_VOLUME_MIN
SYMBOL_VOLUME_MAX
SYMBOL_VOLUME_STEP
```

General formula:

```text
price_distance = abs(entry_price - stop_loss)
loss_per_lot = (price_distance / tick_size) * tick_value
raw_lots = risk_money / loss_per_lot
normalized_lots = floor_to_step(raw_lots, volume_step)
```

Then clamp:

```text
lots = max(volume_min, min(normalized_lots, volume_max))
```

If `loss_per_lot <= 0`, skip trade.

If clamping to `volume_min` would risk more than allowed, recommended first version should skip the trade rather than force minimum lot.

## 9. Trade permissions

A signal can trade only if:

```text
InpEnableTrading == true
CG trade input == true
inside current NY trading day
not duplicate signal
valid clean symbol
valid stop geometry
valid volume
market is tradable
```

## 10. Same-cycle target close

If signal confirms very near cycle end, there may be little time before the scheduled exit.

Baseline behavior:

```text
If confirmation time >= current_cycle_end_time:
    no trade
Else:
    enter and schedule close at cycle end
```

Optional future safety input:

```cpp
input int InpMinSecondsBeforeCycleEndForEntry = 30;
```

Baseline docs recommend adding this in code for practical safety, but it is not part of the user's required core logic.

## 11. Position conflict policy

Because many CGs can signal simultaneously, conflict handling must be explicit.

Baseline recommendation:

```text
InpOnePositionPerSymbol = true
```

If true:

- do not open a new trade on a symbol if an existing EXP0017 position is already open on that symbol;
- still draw/log the signal.

If false:

- allow multiple CG positions on same symbol only if broker account mode and margin rules permit it.

## 12. Magic number

All trades should use a dedicated magic number:

```cpp
input int InpMagicNumber = 170017;
```

Only positions with this magic number are managed by the EA.

## 13. Scheduled exits

The EA should run a position manager every tick:

```text
For every open EXP0017 position:
    if broker_time >= scheduled_exit_time:
        close position
```

If the EA was off at the exact scheduled exit:

```text
On next startup or next tick, close expired positions immediately.
```

This matches the time-target rule.

## 14. End-of-day boundary

At 17:00 NY:

- no new trades from the expiring day;
- close any expired positions;
- reset same-day detection memory for next 18:00 NY day;
- do not carry unconfirmed signals into the next day.

## 15. Audit requirements

Every trade attempt should log:

```text
signal_key
cg_name
side
hunter_symbol
clean_symbol
entry_symbol
entry_price
stop_loss
risk_money
computed_lots
scheduled_exit_time
trade_enabled
trade_result
error_code
```

The audit log is essential because multi-CG systems can produce dense signal clusters.

## Phase 14 owner-approved backtest profile override

The original baseline above remains historical doctrine. For `EXP0017_CG_Raw_Execution_Backtest.mq5`, the Strategy Architect explicitly approved a separate execution profile:

```text
entry = market on first tick after confirmation candle close
trade leg = protected or hunter by input; protected by default
stop = behind selected trade symbol confirmation candle
target = ATR multiple; default ATR(14) * 1.0
CG defaults = cg_3m enabled, all others disabled
```

The authoritative implementation contract for that profile is [[phase14_raw_execution_backtest/PHASE14_EXECUTION_CONTRACT]].

