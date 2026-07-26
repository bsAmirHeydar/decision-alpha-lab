# Phase01 Limits And Non Goals En

Explicit non-goals: no reference prices, no hunt detection, no divergence, no trading, no statistics, no AI, no model scoring.

## Phase 01 Lock

Phase 01 is a pure time-anatomy layer. It exists to prove that the robot understands the same temporal field as the Strategy Architect.

## Required State

- Broker time.
- UTC time.
- New York time.
- New York trading-day start and end.
- Inside/outside trading-day state.
- Current cycle per enabled CG.
- Previous same-day cycle count per CG.
- Recent previous cycle ranges.
- Partial-final-cycle marker when applicable.

## Exclusion

If a future patch needs reference highs/lows, hunts, divergences, statistics, or trades, it must depend on this time contract rather than creating a second calendar engine.
