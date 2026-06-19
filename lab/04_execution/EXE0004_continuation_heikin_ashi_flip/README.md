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
