# 01 - Source SRS Extraction

This file is a factual English extraction from `STC Expert Advisor SRS.pdf`. It does not add trading assumptions beyond the source. Implementation interpretations and unresolved questions are handled in later files.

## 1. Project identity

- Expert Advisor name: `STC Expert Advisor`.
- Purpose: automate the STC strategy based on SMT divergence between two tradable indices.
- The strategy must only use information from the current trading day.
- No prior-day information should be used in decision-making after the daily reset.

## 2. General architecture

- The EA is attached only once, on one chart.
- The chart symbol does not affect EA logic.
- All analysis is performed only on two input symbols.
- All trade management is also limited to those two symbols.

## 3. STC trading day

- STC trading day starts at New York 20:00.
- STC trading day ends at New York 15:30 the next day.
- At New York 15:30:
  - all open trades are closed;
  - all strategy states are reset;
  - all counters are reset to zero;
  - all recorded divergences are removed;
  - the next trading day will begin at New York 20:00.

## 4. Time management

- All strategy times are defined in New York time.
- The EA must handle New York DST automatically.
- The user only enters the broker UTC offset.

## 5. M cycles

The PDF prints the M cycle ranges in a right-to-left visual order. The normalized chronological interpretation is:

| M cycle | Start NY | End NY |
| --- | --- | --- |
| M1 | 20:00 | 02:00 |
| M2 | 03:00 | 09:00 |
| M3 | 09:30 | 15:30 |

There are intentional or unspecified gaps:

- 02:00 to 03:00.
- 09:00 to 09:30.

These gaps require explicit implementation behavior.

## 6. W cycles

### M1 W cycles

| W cycle | Start NY | End NY |
| --- | --- | --- |
| M1.W1 | 20:00 | 21:30 |
| M1.W2 | 21:30 | 23:00 |
| M1.W3 | 23:00 | 00:30 |
| M1.W4 | 00:30 | 02:00 |

### M2 W cycles

| W cycle | Start NY | End NY |
| --- | --- | --- |
| M2.W1 | 03:00 | 04:30 |
| M2.W2 | 04:30 | 06:00 |
| M2.W3 | 06:00 | 07:30 |
| M2.W4 | 07:30 | 09:00 |

### M3 W cycles

| W cycle | Start NY | End NY |
| --- | --- | --- |
| M3.W1 | 09:30 | 11:00 |
| M3.W2 | 11:00 | 12:30 |
| M3.W3 | 12:30 | 14:00 |
| M3.W4 | 14:00 | 15:30 |

## 7. Inputs

| Input | Default or allowed values |
| --- | --- |
| Symbol1 | `SPXUSD` |
| Symbol2 | `NDXUSD` |
| Entry STC | `ON` |
| Partial | `ON` |
| Hedging | `OFF` |
| Final Reward | `10` |
| Risk Percent | user-defined |
| Candle Check | `1m`, `3m`, `5m`, `10m`, `15m`, `30m` |
| Contract Size | `10` |
| Broker UTC Offset | user-defined |

## 8. SMT divergence definition

- Divergence is defined only between the two configured symbols.
- A valid divergence exists when only one of the two symbols hunts the high or low of one of the previous W cycles in the same M cycle.
- Hunt condition: touch is sufficient.
- Candle close is not required for the hunt.

## 9. Divergence formation rules

The PDF states:

- The current W is never compared with itself.
- Comparison is only against previous W cycles inside the same M.
- The printed matrix is:
  - `W2 <- W1`
  - `W1 or W3 <- W2`
  - `W1 or W2 or W4 <- W3`
- The same rule applies to M1, M2, and M3.

This matrix is not fully implementation-clear because the arrow direction and the phrase "previous W" can conflict depending on how the text is read. See `08_open_questions.md`.

## 10. Divergence confirmation

After a divergence forms:

- The EA waits until the selected check candle closes.
- If the divergence still exists at the candle close, entry is executed.
- If the divergence disappears before the candle close, no entry is executed.
- Entry occurs immediately after that check candle closes.

## 11. Entry rules

- Each divergence can be traded only once.
- If the same divergence remains valid in later candles, no new entry is allowed.
- Maximum trades per M cycle: 3.
- If hedging is off:
  - the first trade inside an M cycle determines the allowed direction;
  - until the end of that M, only same-direction trades are allowed;
  - opposite-direction trades are not allowed.
- If hedging is on:
  - both buy and sell trades are allowed;
  - the 3-trades-per-M limit still applies.
- If buy and sell divergences are confirmed at the same time, no trade is executed.

## 12. Trade symbol selection

- If SPX hunts but NDX does not, the trade is executed on NDX.
- If NDX hunts but SPX does not, the trade is executed on SPX.

Generalized rule:

- Trade the symbol that did not hunt.

## 13. Stop-loss

- Stop-loss is placed exactly on the low or high of the referenced W.
- No buffer is added.
- If several W references are available, the closest W by time is selected.

## 14. Position sizing

- Position size is calculated using:
  - Risk Percent;
  - Equity;
  - Contract Size.
- No limit is applied even if calculated volume becomes very large.

## 15. Take-profit

- Every trade has a TP.
- TP is calculated from Final Reward.
- The EA does not modify TP after the trade is opened.

## 16. Partial close

- If Partial is off, no partial close is performed.
- If Partial is on, at the end of W4 of each M:
  - all trades opened in the same M are checked;
  - if they have not reached TP yet, approximately 50% of the volume is closed.
- If volume is 1.01, close 0.51.
- If volume is 0.01, close the whole trade.
- Each trade can be partially closed only once.

## 17. End-of-day behavior

At New York 15:30:

- all open trades are closed without exception;
- all counters are reset;
- all states are reset;
- all recorded divergences are deleted;
- all partial-close state is reset;
- all entry state is reset.

## 18. Entry STC toggle

- If Entry STC is off, the STC strategy does not issue new signals.
- Management of already-open trades continues.
- This toggle is intended to allow other strategies to be added later.

## 19. Future development rules

- Architecture must be modular.
- Every strategy must have its own independent ON/OFF switch.
- Money management, position management, time management, and trade management should be shared across all strategies.

## 20. Design principles

The EA must:

- be independent of the chart timeframe;
- be independent of the chart symbol;
- use only Symbol1 and Symbol2;
- inspect only current trading-day information;
- retain no previous-day information after the new-day reset;
- prevent repeated trades for the same divergence;
- execute the strategy exactly according to the source SRS.
