---
title: "Market Source Extension Guide"
status: implemented
phase: PHASE_03
language: en
tags:
  - strategy-factory
  - phase03
  - mql5
  - market-services
---

# Interface

A new source implements `ISF03MarketSource`:

```text
EnsureSymbol
ReadLatestTick
ReadClosedBars
ReadSymbolSpec
SourceId
```

# Candidate sources

- MetaTrader terminal;
- frozen CSV/JSONL replay;
- vendor futures data;
- broker audit feed;
- synthetic test generator.

# Requirements

A source must:

- provide exact terminal or canonical symbol identity;
- state its clock semantics;
- return closed bars ordered oldest to newest;
- create valid Phase 01 records;
- never embed strategy logic;
- expose source failures explicitly;
- avoid silent timezone assumptions.

# Alternative feeds

A canonical ES/NQ futures source may later coexist with broker CFD data. Different feeds should not be merged before their source identities, contract specifications, and time mappings are preserved.

# Validation

Every source requires contract tests using the same fixture suite. The terminal adapter is not exempt merely because it is the default.
