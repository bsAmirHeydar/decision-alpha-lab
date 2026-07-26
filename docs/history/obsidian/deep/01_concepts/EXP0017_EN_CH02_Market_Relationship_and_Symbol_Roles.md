# EXP0017 EN CH02 — Market Relationship and Symbol Roles

## Thesis

SPXUSD and NDXUSD are deeply related, but neither symbol receives permanent leadership status in the base version.

## Doctrine

- The relationship is historical, price-based, relative, and structurally sticky because of shared index composition.
- SPXUSD may represent broader market flow, but this is not a fixed authority rule.
- Both symbols are valid hunters and clean symbols.
- The non-hunting symbol is the trade candidate in every confirmed divergence.

## Fields

- `symbol_pair`
- `hunter_symbol`
- `clean_symbol`
- `cash_session_flag`
- `symbol_role_result`

## Implementation Note

- Compare each symbol only against its own reference.
- Do not compare raw prices between SPXUSD and NDXUSD.
