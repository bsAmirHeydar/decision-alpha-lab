# Phase 06 Limits and Non-Goals

Phase 06 does not implement:

- order placement
- risk sizing
- stop order placement
- target calculation
- time exit
- MFE/MAE outcome study
- R outcome
- pip outcome
- dollar outcome
- statistical report
- CG ranking
- AI scoring
- rule promotion
- filtered execution

## Known visual limitation

Phase 06 uses the reference-cycle boundary as the line anchor because exact wick timestamps are not yet part of the reference-field contract.

This is acceptable for audit at this stage. A later refinement can store exact reference extreme time and upgrade the drawing anchor.

## Ledger limitation

The Phase 06 ledger is an event ledger, not an outcome ledger.

Rows should not be interpreted as trades, wins, losses, or strategy performance.
