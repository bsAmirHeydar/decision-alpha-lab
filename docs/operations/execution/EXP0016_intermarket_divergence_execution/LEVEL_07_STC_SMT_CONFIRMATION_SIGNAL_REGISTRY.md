# LEVEL 07 STC SMT Confirmation and Signal Registry

Level 07 adds the first signal registry layer for `EXEC001_STC_SMT_Cycles`.

It confirms Level 06 SMT candidates at the close of their check candle and writes consumed audit-only signal rows to:

`dal/stc/EXEC001_STC_SMT_Cycles/stc_level07_signal_registry.csv`

No paper trade and no real order is created in this level.

Main rules:

- The signal exists only at the exact check-candle close.
- Entry OFF means audit-only and consumed.
- Missed/offline entry moments are never entered later.
- Final M check candles are not entry-eligible.
- Same-check buy and sell are forgotten.
- All signal rows are consumed to prevent duplicate or delayed entries.
