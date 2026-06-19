# EXE0004 — Continuation Heikin Ashi Flip

Fourth execution adapter for the H0005 continuation side.

## Idea

When the market regime is continuation, use Heikin Ashi color flips as repeated entries in the continuation direction.

## Signal

On each closed candle:

1. regime = continuation;
2. current HA candle color differs from previous HA candle color;
3. current HA color agrees with the inferred continuation direction;
4. enter at market.

## Exit

Fixed reward model:

- SL: opposite edge of the signal Heikin Ashi candle;
- TP: `InpRewardR`, default `2.0R`.

## Simultaneous trades

`InpAllowSimultaneousTrades` decides whether repeated signals can stack positions or whether only one E0004 position can be open at a time.


## Build 1.01 stop update

The stop is no longer only the signal Heikin Ashi candle edge. For buys, E0004 uses the lower/farther stop from the signal HA low and the last-three-candle low. For sells, it uses the higher/farther stop from the signal HA high and the last-three-candle high, then adds the current spread to the sell stop. This makes risk sizing and the 2R target use the wider protective stop.

## Higher-timeframe regime filter

All four execution experts now support an optional higher-timeframe regime gate. The default is off, so existing tests are unchanged.

Inputs:

- `InpUseHigherTimeframeRegimeFilter` — enable/disable the higher-timeframe regime confirmation.
- `InpHigherRegimeTimeframe` — timeframe used for the higher-timeframe M0001/M0002 regime calculation, default `PERIOD_H1`.

Behavior:

- E0001 and E0002 require the higher timeframe to be `REVERSAL` before allowing reversal entries.
- E0003 and E0004 require the higher timeframe to be `CONTINUATION` before allowing continuation entries.
- The higher-timeframe filter is a gate only; it does not change node construction, touch locking, TP policy, or trade management.

