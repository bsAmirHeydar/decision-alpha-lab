# Time and Causality Contract

## Canonical unit

All cross-module ordering uses signed 64-bit UTC epoch milliseconds. MQL5 `datetime` values are converted to milliseconds. Python timezone-aware datetimes are converted to UTC before serialization.

## Three anatomy times

- `event_time`: when the underlying market occurrence happened.
- `known_time`: the first instant the system could legitimately know the event.
- `confirmation_time`: when the event satisfies the trading or research confirmation contract.

Required ordering:

```text
event_time <= known_time <= confirmation_time
```

This ordering is a hard validation rule. Violations fail closed.

## Source lineage

A timestamp also carries source timezone ID, source UTC offset, source clock ID, and precision. This does not change ordering; it allows DST, broker clock, feed clock, and exchange-time audits later.

## Forbidden patterns

- naive Python datetime;
- terminal-local time with no offset lineage;
- use of final candle state before candle close;
- full-day features in an intraday decision;
- assigning same-candle events an invented sequence;
- folding samples by confirmation time while their labels extend into test data.

## Later use

Phase 07 will build the market-clock and timezone conversion services around this primitive. Phase 12 will purge folds by label horizon. This phase freezes only the transport and ordering semantics.
