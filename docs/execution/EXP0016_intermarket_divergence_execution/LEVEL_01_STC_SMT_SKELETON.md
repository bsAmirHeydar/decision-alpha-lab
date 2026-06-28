# Level 01 — STC SMT Skeleton Patch

This patch adds the first compileable MQL5 shell for `EXEC001_STC_SMT_Cycles`.

The level is deliberately safe: it validates inputs, creates runtime journals, starts a timer, prints locked rules, and prevents duplicate instances. It does not detect signals and it does not trade.

Compile target:

`mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5`

Primary documentation:

`lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton.md`
