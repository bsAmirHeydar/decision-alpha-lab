# Phase 06 Signal Audit Ledger Specification

## Objective

The Phase 06 ledger preserves raw final states produced by the closed-candle confirmation layer.

The ledger is not a performance report. It does not know whether the future trade won, lost, stopped out, reached a reward, or produced positive expectancy.

## Included states

The ledger can record:

- `CONFIRMED_TRADEABLE`
- `INVALIDATED_DOUBLE_HUNT`

Both are useful:

- Confirmed states become the primary sample for future outcome study.
- Invalidated double-hunt states show where apparent asymmetry disappeared before permission.

## Duplicate protection

Phase 06 writes only on new closed-candle observations and also provides:

- in-memory duplicate guard
- optional file duplicate guard

The ledger key combines signal identity, status, and confirmation timestamp.

## File location

The file is written through MT5 file APIs using the configured filename:

```text
EXP0017_Phase06_Signal_Audit_Ledger.csv
```

If `InpLedgerUseCommonFiles` is enabled, the ledger uses the terminal common files area.

## Columns

The ledger records signal identity, status, direction, side, CG identity, current and reference cycle numbers, symbols, hunter/clean role, confirmation times, NY trading-day boundaries, cycle windows, reference prices, current extremes, clean stop reference preview, chart symbol, phase name, notes, and created time.
