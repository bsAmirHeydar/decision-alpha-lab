# Level 12 — STC SMT Persistence and Restart Recovery

Level 12 adds current-day persistence for the paper/audit engine of `EXEC001_STC_SMT_Cycles`.

It writes:

- `stc_level12_persistence_snapshot.csv`
- `stc_level12_persistence_recovery.csv`

It restores only when strategy id, symbol pair, magic number, check timeframe, and current STC day match the saved snapshot.

It is still no-order: no real broker entry, partial, or hard close is executed in this level.
