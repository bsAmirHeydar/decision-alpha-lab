# Glossary

## Decision Node

A structural high or low where the market previously made a visible decision.

## Decision Zone

A finite territory around a node. The project avoids treating structural nodes as infinitesimal points.

## Decision Energy

The observable force associated with a structural event. It may express as rejection, continuation, hunt, break, velocity, or path quality.

## Reversal

A state or event where price interaction with a structural zone is interpreted as self-correcting behavior.

## Continuation

A state or event where price interaction with a structural zone is interpreted as self-reinforcing behavior.

## Regime

The current dominant market state: reversal pressure, continuation pressure, or ambiguity.

## Known Time

The candle/time at which a label or event becomes knowable without future data.

## Known-Time Batch

All events or labels that become knowable on the same candle/time. They are simultaneous and must not be sequenced internally.

## Ambiguous Batch

A known-time batch containing mixed reversal and continuation energy. It is reported and counted but skipped from pure transition statistics by default.

## Classic Sample Report

A report based on completed branch samples. Useful for exploration, but not enough for live claims.

## Causal Batch Report

A report that groups sample labels by known time and prevents fake same-candle transitions.

## Atomic No-Sample Report

A report that does not build branch samples. It derives regime and entry decisions directly from raw events during replay.

## Path-Normalized R

An R-like metric using a structural distance as a denominator. Useful for path comparison, not automatically a trading R.

## Execution R

An R multiple based on a real risk rule used by the trading model.

## MFE

Maximum favorable excursion after entry.

## MAE

Maximum adverse excursion after entry.

## Convexity

A payoff structure where downside is constrained and upside can expand.
