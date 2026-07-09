# Phase 07 Outcome Study Specification

## Purpose

Phase 07 answers the first statistical question:

> After a confirmed EXP0017 divergence appears, what happens next?

It consumes only confirmed tradeable signals from the existing confirmation stack and turns them into measurable outcome rows.

## Entry model

The default entry is a research estimate:

- clean symbol
- confirmation candle close
- no order
- no slippage model
- no spread model
- no broker execution assumption

The entry estimate is intentionally separated from live execution. This prevents the research dataset from pretending that an order was actually sent.

## Stop model

The stop-reference remains the clean symbol reference level:

- BUY divergence: clean reference low
- SELL divergence: clean reference high

Phase 07 measures stop distance and stop-hit behavior but does not place a stop order.

## Outcome windows

For each confirmed signal, Phase 07 studies:

1. result at current CG cycle end
2. result after one forward CG cycle
3. result after two forward CG cycles
4. result after three forward CG cycles
5. result at New York trading-day end
6. maximum favorable excursion until day end
7. maximum adverse excursion until day end
8. whether the clean stop reference was touched before each studied horizon

## Normalized movement

The key normalized index is:

```text
signal points / clean-symbol total daily range points
```

This directly implements the strategy-architect requirement that pip movement relative to total daily movement must become a statistical component.
