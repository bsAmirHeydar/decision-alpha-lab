# Phase 02 Limits and Non-Goals

## Limits

Phase 02 depends on M1 history availability for both symbols.

If the broker has not loaded historical M1 bars, recent references may be marked missing.

## No hunt logic

A high/low reference being displayed does not mean it has been hunted.

Hunt requires future comparison of current-cycle high/low against these references.

## No divergence logic

The reference field does not know whether one symbol hunted and the other did not.

That belongs to Phase 04 and Phase 05.

## No execution logic

No reference can become a trade in this phase.

There is no entry, stop, target, risk, position limit, hedge logic, or order placement.

## No ranking

The system does not rank:

- CGs
- reference distances
- reference ages
- symbol roles
- cash-session references
- overlap states

Ranking only becomes valid after statistical evidence.
