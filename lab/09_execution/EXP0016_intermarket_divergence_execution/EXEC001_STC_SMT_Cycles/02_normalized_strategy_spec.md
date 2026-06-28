# 02 - Normalized Strategy Specification

This file translates the source SRS into an implementation-oriented strategy contract.

## 1. Scope

`EXEC001_STC_SMT_Cycles` is an intermarket SMT divergence execution strategy.

It is not a general divergence scanner. It is a time-cycle strategy with fixed New York M/W cycles and strict trade-management rules.

## 2. Symbols

| Role | Meaning | Default |
| --- | --- | --- |
| Symbol1 | First analysis/trading symbol | `SPXUSD` |
| Symbol2 | Second analysis/trading symbol | `NDXUSD` |

The EA should not care which chart symbol it is attached to.

## 3. Trading day contract

A strategy day is defined as:

```text
New York 20:00 -> New York 15:30 next day
```

At New York 15:30 the EA must:

1. Close all open positions controlled by the STC strategy.
2. Reset all counters.
3. Reset all M-cycle direction locks.
4. Delete all divergence records.
5. Reset all partial-close flags.
6. Reset all entry-consumed flags.

No previous-day strategy state is allowed to survive the reset.

## 4. Time basis

The canonical strategy time zone is:

```text
America/New_York
```

Implementation layers:

- Python/backtest layer: use timezone-aware timestamps with automatic DST.
- MQL5 layer: use broker-time input offset plus a New York conversion helper.
- CME/CSV layer: prefer UTC timestamps converted into New York time internally.

## 5. Cycle hierarchy

```text
STC Day
  M1
    W1
    W2
    W3
    W4
  M2
    W1
    W2
    W3
    W4
  M3
    W1
    W2
    W3
    W4
```

Every divergence belongs to exactly one M cycle and one active W cycle.

## 6. Reference levels

For each symbol and each W cycle, calculate:

```text
W High
W Low
W Start Time
W End Time
W ID
M ID
STC Day ID
```

Only W levels inside the current STC day should be used.

## 7. Divergence side

### Bullish SMT divergence

A bullish SMT divergence exists when:

- exactly one symbol touches or breaks a prior reference W low inside the same M cycle;
- the other symbol does not touch or break its corresponding reference W low;
- the condition remains valid until check-candle close.

The trade direction is BUY on the symbol that did not hunt.

### Bearish SMT divergence

A bearish SMT divergence exists when:

- exactly one symbol touches or breaks a prior reference W high inside the same M cycle;
- the other symbol does not touch or break its corresponding reference W high;
- the condition remains valid until check-candle close.

The trade direction is SELL on the symbol that did not hunt.

## 8. Hunt definition

Hunt is touch-only:

```text
Bullish hunt: bar low <= reference W low
Bearish hunt: bar high >= reference W high
```

No candle close confirmation is needed for the hunt itself.

## 9. Confirmation

A raw divergence is not traded immediately. It enters a pending state.

The EA waits for the configured check candle to close:

```text
1m / 3m / 5m / 10m / 15m / 30m
```

At the check-candle close:

- If exactly one symbol still has hunted and the other has not, the divergence is confirmed and entered.
- If both symbols have hunted, the divergence is no longer valid.
- If neither symbol has hunted, no divergence exists.
- If both buy and sell divergences confirm at the same time, no trade is entered.

## 10. One trade per divergence

Every divergence needs a stable ID such as:

```text
stc_day + m_id + current_w_id + reference_w_id + side + hunted_symbol + clean_symbol
```

Once that ID has been traded, it must not trigger again.

## 11. M-cycle trade limit

Each M cycle can have at most 3 trades.

When hedging is OFF:

- the first trade in the M cycle locks the M direction;
- all later trades in that M must match the locked direction;
- opposite-direction trades are skipped.

When hedging is ON:

- both BUY and SELL are allowed;
- the 3-trades-per-M limit still applies.

## 12. Symbol selection

Trade the clean/non-hunting symbol.

Examples:

| Hunted symbol | Clean symbol | Trade symbol |
| --- | --- | --- |
| SPX | NDX | NDX |
| NDX | SPX | SPX |

## 13. Stop-loss and take-profit

Stop-loss:

- BUY: stop on referenced W low.
- SELL: stop on referenced W high.
- No buffer.
- If multiple reference W cycles are eligible, use the closest one by time.

Take-profit:

- All trades must have TP.
- TP is calculated from Final Reward.
- TP is not modified after opening.

## 14. Position size

Position size uses:

```text
Risk Percent
Equity
Contract Size
Stop distance
```

The SRS explicitly says no max-volume limitation is applied, even if calculated volume is very large.

Implementation may include a separate safety switch later, but the source strategy contract has no cap.

## 15. Partial close

At the end of W4 for each M cycle:

- inspect trades opened in that M;
- if Partial is ON and trade has not hit TP;
- close approximately 50%;
- mark the trade as partial-closed;
- never partial-close that trade again.

## 16. End-of-day close

At New York 15:30:

- close all open STC trades without exception;
- then reset all state.

## 17. Entry STC switch

If `Entry STC = OFF`:

- no new STC signals are generated;
- already-open trades continue to be managed.

