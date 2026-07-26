# EXP0017 EN CH08 — Candle Close Confirmation and Trade Permission

## Thesis

A divergence becomes confirmed and tradeable only after the active chart timeframe candle closes with asymmetry still valid.

## Doctrine

- Hunt can happen intrabar; confirmation waits for candle close.
- If both symbols have hunted by confirmation time, no trade exists.
- Temporal close is not a price filter.
- All confirmed signals should remain visible.

## Fields

- `confirmation_time`
- `confirmation_candle_timeframe`
- `potential_state`
- `confirmed_state`
- `invalid_at_confirmation`

## Implementation Note

- The EA must use closed candle events as the final signal boundary.
- Do not execute on intrabar potential states.
