# Level 12 — Persistence and Restart Recovery

## Scope

Level 12 adds the first persistence layer for `EXEC001_STC_SMT_Cycles`. It does not place real orders, does not close real positions, and does not draw chart objects. Its purpose is to keep the paper/audit engine deterministic across EA restarts during the same STC trading day.

The STC SRS requires the Expert Advisor to avoid duplicate trades for the same divergence and to reset all state at the end of the STC trading day. Owner clarification also locked that missed entries must not be executed late, delayed partial actions must be recovered, delayed hard close must be recovered, and only the current STC trading day may influence the current day. Level 12 is the first implementation layer that preserves those rules across process restarts.

## What is persisted

The snapshot stores the current STC-day processing cursors for every audit/execution layer:

- last closed check-candle audit index
- last closed W-level serial
- last reference-hunt check index
- last SMT-candidate check index
- last signal-registry check index
- last paper-entry check index
- last paper-outcome check index
- last partial-action check index
- last hard-close check index

It also stores the paper execution counters and direction locks needed to preserve the strategy rules after restart:

- paper trade count for M1, M2, and M3
- paper direction lock for M1, M2, and M3
- outcome-simulator trade count and direction lock for M1, M2, and M3
- partial-simulator trade count and direction lock for M1, M2, and M3

The snapshot intentionally does not store yesterday's strategy state as active state. A snapshot is accepted only when its `stc_day_id` equals the current STC trading-day id.

## Snapshot file

The current snapshot is written as a two-column key-value CSV file:

`dal/stc/EXEC001_STC_SMT_Cycles/stc_level12_persistence_snapshot.csv`

The file is overwritten rather than appended. This makes it a compact current-state file and avoids having to scan a long log on every restart.

## Recovery audit file

Every restore attempt and every snapshot write is logged here:

`dal/stc/EXEC001_STC_SMT_Cycles/stc_level12_persistence_recovery.csv`

This file is append-only and records:

- whether a snapshot was found
- whether it matched the active strategy configuration
- whether it matched the current STC trading day
- whether it was restored
- the restored cursors, counters, and direction locks

## Restore validation

A snapshot is restored only if all of these fields match:

- schema is `DAL_STC_LEVEL12_PERSISTENCE_V1`
- strategy id equals `EXEC001_STC_SMT_Cycles`
- `Symbol1` matches the current input
- `Symbol2` matches the current input
- magic number matches the current input
- check-candle size matches the current input
- stored `stc_day_id` equals the current STC trading day id

If any of these checks fail, the EA starts without restoring the snapshot and writes a recovery-audit row explaining why.

## Restore sequence

On initialization:

1. Validate configuration.
2. Create Common Files output folders.
3. Acquire duplicate-instance lock.
4. Build the current time snapshot.
5. Write build sanity and initial runtime event.
6. Attempt to restore the Level 12 snapshot.
7. Run all closed-layer processors from check candles through hard close.
8. Write a fresh Level 12 snapshot after the recovery pipeline.

This ordering is intentional. The snapshot must be restored before closed-layer processors run, otherwise the processors may backfill already-consumed check candles and duplicate paper entry, partial, or hard-close audit rows.

## Snapshot write timing

A snapshot is written:

- after initialization and recovery pipeline
- periodically during timer pulses according to `InpPersistenceSnapshotSeconds`
- on deinitialization

The default interval is 30 seconds.

## Current limitation

Level 12 restores in-memory cursors and paper counters from the snapshot. It does not yet reconstruct real broker positions because real auto-trading is not enabled yet. Later auto-trade levels must extend this module to reconcile broker positions by magic number.

## Acceptance criteria

A Level 12 run is accepted when:

- the EA compiles
- `stc_level12_persistence_snapshot.csv` is written
- `stc_level12_persistence_recovery.csv` is written
- restart inside the same STC trading day restores the previous cursors and counters
- restart with a different symbol pair does not restore the old snapshot
- restart in a new STC trading day does not restore yesterday's snapshot as active state
- no real order is sent
