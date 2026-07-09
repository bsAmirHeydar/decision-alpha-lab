# Candle Close as Confirmation Boundary

## Definition

Candle close is the moment where the active market unit becomes complete enough to judge.

## Role in EXP0017

The strategy uses intrabar highs and lows to identify hunts. But it uses candle close to confirm whether the hunt produced a valid intermarket divergence.

## Important Distinction

Candle close does not mean:

- close beyond the reference,
- close with strong body,
- close with rejection,
- close in a particular candle color.

It means:

> the time unit has ended.

## Why It Exists

The market relationship between SPXUSD and NDXUSD is still alive during the open candle. Until the candle closes, the clean symbol can still hunt and cancel the divergence.

## Related

- [[Temporal_Close_Not_Price_Filter]]
- [[Potential_Divergence_Versus_Confirmed_Divergence]]
- [[Close_Is_Not_Late_Doctrine]]
