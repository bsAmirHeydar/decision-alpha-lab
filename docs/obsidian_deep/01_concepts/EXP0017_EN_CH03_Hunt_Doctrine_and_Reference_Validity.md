# EXP0017 EN CH03 — Hunt Doctrine and Reference Validity

## Thesis

A hunt is a high/low touch or break of a reference level; close beyond the level is not required.

## Doctrine

- High hunt: current high >= reference high.
- Low hunt: current low <= reference low.
- Equality counts as a hunt.
- Close beyond the level is not required.
- If both symbols hunt their corresponding references, divergence is invalid.

## Fields

- `reference_price`
- `hunt_side`
- `hunt_symbol`
- `hunt_time`
- `hunt_candle`
- `double_hunt_state`

## Implementation Note

- Use OHLC high/low data, not close-only logic.
- Separate intrabar hunt occurrence from final close confirmation.
