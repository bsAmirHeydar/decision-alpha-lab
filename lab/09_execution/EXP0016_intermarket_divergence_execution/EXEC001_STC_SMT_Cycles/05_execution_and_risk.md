# 05 - Execution and Risk Rules

## 1. Entry toggle

`Entry STC` controls new entries only.

If `Entry STC = OFF`:

- do not create new STC entries;
- continue managing already-open STC positions.

## 2. Entry timing

After a raw SMT divergence appears:

1. Wait for the configured check candle to close.
2. If divergence is still valid at close, enter immediately.
3. If not valid, do nothing.

## 3. Trade symbol

Trade the symbol that did not hunt.

| Hunted | Not hunted | Entry symbol |
| --- | --- | --- |
| SPX | NDX | NDX |
| NDX | SPX | SPX |

Generalized:

```text
entry_symbol = clean_symbol
```

## 4. Direction

| Divergence | Hunted level | Entry |
| --- | --- | --- |
| Bullish SMT | reference W low | BUY clean symbol |
| Bearish SMT | reference W high | SELL clean symbol |

## 5. Per-M trade limit

Each M cycle allows at most 3 trades.

```text
max_trades_per_m = 3
```

## 6. Hedging OFF

If hedging is disabled:

- the first trade inside an M locks that M direction;
- later trades inside that M must be same direction;
- opposite-direction trades are skipped.

Example:

```text
M2 first trade = BUY
M2 later SELL divergence confirms
SELL is skipped because M2 direction is locked to BUY
```

## 7. Hedging ON

If hedging is enabled:

- BUY and SELL are both allowed;
- the 3-trade limit per M still applies.

## 8. Simultaneous buy and sell

If a buy SMT and sell SMT confirm at the same time:

```text
No trade.
```

## 9. Stop-loss

Stop-loss is placed exactly at the selected reference W level.

### BUY

```text
SL = referenced W low
```

### SELL

```text
SL = referenced W high
```

No buffer is added.

If multiple references exist:

```text
Use the closest W by time.
```

## 10. Take-profit

Every trade receives a TP.

The source says TP is calculated from `Final Reward`.

Implementation candidate:

```text
risk_distance = abs(entry_price - stop_loss)
target_distance = risk_distance * FinalReward
take_profit = entry_price + target_distance for BUY
take_profit = entry_price - target_distance for SELL
```

This must be confirmed because the source does not spell out the exact TP formula beyond `Final Reward`.

## 11. Position sizing

Source inputs:

```text
Risk Percent
Equity
Contract Size
```

Implementation candidate:

```text
risk_cash = equity * (risk_percent / 100)
stop_distance_points = abs(entry_price - stop_loss)
volume = risk_cash / (stop_distance_points * contract_size)
```

The source SRS says no volume cap is applied, even if the result becomes very large.

## 12. Partial close

If Partial is OFF:

```text
No partial close.
```

If Partial is ON:

- At the end of W4 for each M, inspect trades opened in that M.
- If a trade has not reached TP, close approximately 50% of volume.
- If volume is 1.01, close 0.51.
- If volume is 0.01, close the full trade.
- Each trade is partially closed at most once.

## 13. End of day

At New York 15:30:

- close all open positions without exception;
- reset strategy state.

## 14. Recommended journal fields

For every trade or skipped signal, log:

```text
run_id
stc_day_id
m_id
w_id
reference_w_id
symbol_1
symbol_2
hunted_symbol
clean_symbol
entry_symbol
side
reference_level
entry_price
stop_loss
take_profit
risk_percent
equity_snapshot
contract_size
calculated_volume
m_trade_count_before
m_trade_count_after
hedging_enabled
m_direction_lock
entry_stc_enabled
partial_enabled
status
skip_reason
created_at_ny
confirmed_at_ny
entered_at_ny
closed_at_ny
close_reason
```

