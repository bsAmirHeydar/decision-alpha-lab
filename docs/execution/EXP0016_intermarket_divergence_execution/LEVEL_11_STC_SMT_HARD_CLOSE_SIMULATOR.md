# Level 11 STC SMT Hard Close Simulator

Level 11 adds paper-only 15:30 New York hard-close accounting for EXEC001 STC SMT Cycles.

It extends Level 10 by adding:

- a new hard-close audit file,
- 15:30 New York end-of-day paper close logic,
- delayed hard-close recovery,
- remaining-volume close after W4 partial,
- full-volume close when no partial happened,
- no real broker orders.

The implementation file is:

`mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_HardClose.mqh`

The main EA remains:

`mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5`

Output file:

`dal/stc/EXEC001_STC_SMT_Cycles/stc_level11_hard_close_actions.csv`
