# EXP0017 EN CH09 — Clean Symbol Execution Doctrine

## Thesis

The trade candidate is always the clean symbol: the symbol whose corresponding reference has not been hunted.

## Doctrine

- The clean symbol holds the healthy/unhunted reference.
- Buy divergence expresses buying pressure in the clean symbol.
- Sell divergence expresses selling pressure in the clean symbol.
- No additional quality filter exists in the base layer.

## Fields

- `clean_symbol`
- `hunter_symbol`
- `clean_reference_price`
- `trade_symbol`
- `direction`

## Implementation Note

- Execution modules must bind trade_symbol to clean_symbol.
- Drawing modules must still show hunter evidence clearly.
