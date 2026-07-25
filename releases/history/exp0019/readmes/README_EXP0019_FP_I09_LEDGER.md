# EXP0019 FP-I09 Signal Ledger and Pair-Session Arbitration

This patch adds the append-only semantic ledger, deterministic signal deduplication, pair-global A/L/N quota arbitration, provisional reservation supersession, session sealing, closed checkpoints, and restart/rebuild parity.

Canonical policy remains:

- earliest canonical M1 Hunt wins;
- all relations and both symbols share one session pool;
- WW direct setups compete normally;
- suppressed signals remain visible;
- quota consumption policy remains `UNSET`;
- live execution authority remains `NONE`.
