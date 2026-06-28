# LEVEL 10 — STC SMT Partial Close Simulator

This level adds paper partial-close accounting for EXEC001 STC SMT Cycles.

The EA remains no-order. It writes `stc_level10_partial_actions.csv` and simulates only what should happen at the W4 endpoint of M1 and M2.

M3 partial is intentionally disabled because M3 W4 ends at 15:30 New York, where the hard-close rule takes priority.

Compile:

`mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5`

New module:

`mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Partial.mqh`

New output:

`dal/stc/EXEC001_STC_SMT_Cycles/stc_level10_partial_actions.csv`
