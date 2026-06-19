# E0004 — Continuation Heikin Ashi Flip Executor

`E0004_ContinuationHeikinAshiFlip.mq5` is the fourth execution adapter for Decision Alpha Lab.
It is intentionally separate from E0001, E0002, and E0003.

## Contract

E0004 only searches for entries when the effective regime is `CONTINUATION`.
On each new closed candle it calculates Heikin Ashi candles from the same closed-bar stream used by the existing M0001/M0002 modules.

A signal exists when:

1. The current closed Heikin Ashi candle has a non-doji color.
2. The previous closed Heikin Ashi candle has the opposite non-doji color.
3. The current Heikin Ashi color is in the inferred continuation direction.

The continuation direction is inferred from the most recent structural close-hunt:

- close above a confirmed HIGH node means bullish continuation direction.
- close below a confirmed LOW node means bearish continuation direction.

## Orders

- Bullish HA flip in bullish continuation direction: Buy Market.
- Bearish HA flip in bearish continuation direction: Sell Market.

Default risk/reward is fixed `1:2`:

- Buy stop: signal Heikin Ashi low.
- Sell stop: signal Heikin Ashi high.
- TP: `InpRewardR × risk`, default `2.0R`.

Unlike E0003, E0004 does not exit on regime change by default. It uses its own fixed TP/SL.
The regime gate only controls new entries.

## Simultaneous trades

`InpAllowSimultaneousTrades` controls whether multiple E0004 positions may coexist.

- `true`: every valid continuation-direction HA flip can open a new trade.
- `false`: E0004 skips new signals while it already has an open managed position.

## Minimal inputs

- `InpSymbol`, `InpTimeframe`, `InpBars`
- `InpL`, `InpZoneRatio`, `InpExitGap`, `InpConsumeMode`
- `InpRegimeBasis`, `InpHumanContextSignal`
- `InpUseTradingSessionFilter`, session start/end
- `InpMagicNumber`, `InpRiskCash`, `InpRewardR`
- `InpAllowSimultaneousTrades`
- `InpContinuationBreakBufferPoints`

## Notes

The Expert reuses the same M0001/M0002 source-of-truth pipeline as the other execution adapters.
It should be tested independently from the reversal executors.


## Build 1.01 stop update

The stop is no longer only the signal Heikin Ashi candle edge. For buys, E0004 uses the lower/farther stop from the signal HA low and the last-three-candle low. For sells, it uses the higher/farther stop from the signal HA high and the last-three-candle high, then adds the current spread to the sell stop. This makes risk sizing and the 2R target use the wider protective stop.
