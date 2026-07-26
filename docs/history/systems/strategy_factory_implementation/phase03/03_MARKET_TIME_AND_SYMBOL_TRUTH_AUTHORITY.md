---
title: "Market, Time, and Symbol Truth Authority"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Authority model

MQL5 owns runtime truth because it receives broker ticks, terminal bars, symbol properties, server time, and execution constraints. Python mirrors the canonical outputs but does not reconstruct live truth.

## Market truth

Market truth includes:

- the latest accepted tick;
- the ordered sequence of closed bars;
- the source and receive times;
- whether a bar series is complete, gapped, stale, or desynchronized;
- the generation of each cached series.

No strategy may silently repair price history. If a gap is observed, quality changes and the decision path fails closed unless a research-only policy explicitly records the exception.

## Time truth

Canonical time is UTC epoch milliseconds. Broker time and New York local time are transformations with explicit lineage. A timestamp without source clock, source offset, and precision is incomplete.

## Symbol truth

Broker symbols are external identifiers, not internal safe IDs. They may contain prefixes and suffixes such as `#US30`, `EURUSD.a`, or `XAUUSD-pro`. Phase 03 therefore separates:

```text
internal identifier grammar
from
terminal symbol grammar
```

Symbol specifications are snapshots. Tick size, tick value, minimum volume, volume step, stops level, freeze level, filling mode, and trade mode may change; material changes increment a specification generation.

## Consumer rule

Anatomy and execution modules consume typed snapshots. They do not call the terminal independently. This gives every downstream event a consistent market, time, and specification lineage.
