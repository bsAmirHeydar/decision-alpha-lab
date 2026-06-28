# Level 15 — STC SMT Broker Position Manager

This level adds a magic-only broker position safety layer for `EXEC001_STC_SMT_Cycles`.

It does not enable auto-entry. It only scans real broker positions, audits exposure, detects foreign positions on the configured pair, and optionally hard-closes matching magic-number positions after 15:30 New York when real hard close is explicitly enabled.

Project-local details are documented in:

`lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/36_level_15_broker_position_manager.md`
