feat(exp0019): implement FP-I09 semantic ledger and pair-session arbitration

- add append-only hash-chained ledger events and deterministic materialized views
- deduplicate identical signals and fail closed on semantic identity collisions
- arbitrate one pair-global A/L/N reservation across both symbols and all relations
- rank by earliest canonical M1 hunt with versioned non-alpha tie-breaks
- retain WW- and quota-suppressed signals with winner and reason lineage
- support provisional reservation supersession for late earlier evidence and final session sealing
- preserve FP-DEC-012 as UNSET and forbid permanent consumption/release transitions
- add closed checkpoints, restart/rebuild parity, MQL5 mirrors, tests, QA evidence, and Obsidian documentation
