# Level 14 — STC SMT Paper Live Alerts

Level 14 adds no-order paper-live alerts for EXEC001 STC SMT Cycles.

It monitors newly created signal registry rows, paper entries, paper outcomes, partial actions, and hard-close actions. It can print, popup, push, or sound alerts in `PAPER_LIVE` and `AUTO_TRADE` runtime modes.

It remains audit-only:

- no broker orders,
- no broker partial close,
- no broker hard close,
- no strategy decision changes.

Output:

- `stc_level14_paper_live_alerts.csv`

Main lab document:

- `lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/35_level_14_paper_live_alerts.md`
