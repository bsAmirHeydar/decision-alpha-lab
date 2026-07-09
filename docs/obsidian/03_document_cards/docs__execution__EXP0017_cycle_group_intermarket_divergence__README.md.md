# Document Card — EXP0017 CG Intermarket Divergence README

## Source

`docs/execution/EXP0017_cycle_group_intermarket_divergence/README.md`

## Summary

Defines EXP0017 as an independent MQL5 expert specification for intermarket divergence across cycle groups anchored at 18:00 New York.

## Key claims

- Independent from previous STC and Flag/NDS systems.
- Uses two symbols, default SPXUSD and NDXUSD.
- Processes multiple CGs from 3m to 720m.
- Trades clean symbol after candle-close confirmation.
- Risk is 1% equity and exit is cycle-end time.

## Links

- [[CG_INTERMARKET_DIVERGENCE_MOC]]
- [[EXP0017 Strategy Specification]]
- [[Cycle Group Calendar Doctrine]]
