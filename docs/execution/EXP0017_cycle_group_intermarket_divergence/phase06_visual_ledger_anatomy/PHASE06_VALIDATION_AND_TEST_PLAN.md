# Phase 06 Validation and Test Plan

## 1. Compile test

Compile:

```text
EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

Expected result:

- no syntax errors
- no missing include errors
- no order-trading calls

## 2. Object-prefix test

Attach the expert and verify all created objects start with:

```text
EXP0017_P06_
```

Detach with `InpClearPhase06ObjectsOnDeinit=true` and verify only Phase 06 objects are removed.

## 3. Hunter-chart-only test

Set:

```text
InpDrawOnlyWhenChartIsHunterSymbol=true
```

Attach to SPXUSD and NDXUSD charts separately.

Expected:

- SPXUSD chart draws only SPX hunter events.
- NDXUSD chart draws only NDX hunter events.

## 4. Confirmed drawing test

When Phase 05 produces `CONFIRMED_TRADEABLE`, Phase 06 should draw a line and label if drawing is enabled.

## 5. Invalidated drawing test

When Phase 05 produces `INVALIDATED_DOUBLE_HUNT`, Phase 06 should draw the invalidated state only if `InpDrawInvalidatedDoubleHunts=true`.

## 6. Ledger write test

With ledger enabled, wait for a new closed candle that produces final states.

Expected:

- CSV file is created.
- Header is written once.
- New signal rows are appended.
- Duplicate rows are blocked on repeated timer pulses.

## 7. No-execution test

Search the Phase 06 files for order execution calls. Expected: none.

## 8. Handoff test

The ledger must contain enough event fields for Phase 07/08 to compute outcomes later without recomputing original signal identity.
