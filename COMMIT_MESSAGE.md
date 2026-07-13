feat(exp0019): implement FP-I04 multi-symbol M1 data synchronization

- add canonical symbol-pair and closed M1 bar contracts
- align both symbols by exact UTC minute open
- distinguish missing, out-of-coverage, conflict, and revised states
- add coverage, gap, revision, cursor, backfill, and snapshot evidence
- add batch/incremental parity tests and MQL5 contract mirrors
- add detailed FP-I04 Obsidian delivery documentation
