fix(nds): integrate Hook 86.4 with Phase04 closure and trade funnel

Correct the no-trade execution path for the canonical Hook 86.4 x3/x4 fixed-R
profile without introducing parallel structure or broker engines.

Root-cause fixes:
- default the dedicated tester to HOOK_864_CYCLE_R1 instead of TERMINAL_F123
- default rare-entry diagnosis to PARITY history/scales instead of FAST
- consume canonical Phase03 Y and Phase04 50% X-closure/death lifecycle
- replace terminal-retracement proxy with closed-bar post-closure first arrival
- include closure candle and fail closed on same-bar closure plus 86.4 touch
- bind Phase02 and Phase04 through stable structural identity, not local index
- add full structural/execution candidate funnel and session counters

Integration:
- preserve Phase02 Hook/family/x-count authority
- preserve Phase52 terminal/F123 behavior and compatibility wrappers
- preserve one-attempt, one-exposure, restart ownership and fixed-1R protection
- preserve existing sizing, price normalization, broker gates and order adapter
- add tester-log analyzer for zero-trade root-cause classification

Evidence:
- 43 deterministic Python tests passed
- nine bounded QA stages passed
- 359 PASS and zero FAIL source/static records
- engineering policy passed with zero errors and warnings
- modified Python files passed py_compile

MetaEditor, MT5 Strategy Tester and broker evidence remain external and pending.
No profitability or live activation claim is made.
