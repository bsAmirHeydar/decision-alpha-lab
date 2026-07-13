feat(ucee): implement I11 experiment DAG search scheduling and budget governance

- compile admitted candidates into deterministic experiment DAGs and trial identities
- add baseline-first grid/random/Halton/TPE/halving/Hyperband/evolutionary/Pareto search
- enforce hard trial, time, memory, CPU/GPU, retry, seed, fold, and artifact budgets
- add dependency scheduling, spawn isolation, retry, cancel, timeout, quarantine, cache, and resume
- add hash-chained selection ledger and reproducibility reconciliation
- add 24 closed schemas, vectors, examples, MQL5 contract mirrors, tests, and detailed Obsidian docs
- hand off the complete attempted trial universe to UCE-I12 multiplicity-aware promotion
