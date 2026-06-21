# H0006 — Reversal Explosive Optionality

## Claim

Reversal regimes may not necessarily have better win rate, but they may identify more convex/option-like points: locations where future movement has fatter tails, larger absolute excursion, and stronger burst potential.

## Why this exists

H0004 proves short-term regime memory over atomic known-time batches. H0005 tries to convert regime state into direction and execution. H0006 asks a different question: which state marks more valuable optionality points?

This matters because an alpha can exist even without high directional hit-rate if the selected points produce unusually large tails that can be harvested by asymmetric exits, volatility expansion, or optionality-like trade design.

## Atomic contract

H0006 must use the same atomic/no-sample contract:

- no M0002 branch samples
- no outcome-sorted sequence
- no internal ordering of same-time events
- pure known-time batches only
- all future excursion measurement starts after the known candle

## Metrics

For each horizon, normalized by ATR at the known candle:

- absolute optionality excursion: `max(high-entry, entry-low) / ATR`
- directional MFE in the batch direction
- adverse excursion
- p90/p95/p99 absolute excursion
- hit rate above ATR thresholds
- top 10% tail share
- reversal minus continuation mean and tail differences
- label-shuffle null over fixed known times and fixed future excursions

## Interpretation

A positive H0006 result is not a trading strategy by itself. It means reversal-known-time batches identify stronger optionality points. Execution still requires a separate trade design such as fixed-R reversal, volatility capture, breakout-after-compression, straddle-like logic, or dynamic trailing.
