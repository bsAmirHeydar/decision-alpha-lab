# LEVEL 18 — STC SMT Real Hard Close Finalizer

Patch scope: add the final real broker hard-close layer for EXEC001 STC SMT Cycles.

This level is disabled by default. When explicitly enabled, it retries closing only Symbol1/Symbol2 positions with the configured STC magic number after 15:30 New York. It audits every attempt and verifies whether positions remain after each close request.

Main implementation file:

`mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_RealHardClose.mqh`

Main EA:

`mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5`

Primary output:

`dal/stc/EXEC001_STC_SMT_Cycles/stc_level18_real_hard_close_finalizer.csv`
