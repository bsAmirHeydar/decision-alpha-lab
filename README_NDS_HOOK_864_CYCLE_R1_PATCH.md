# NDS Hook 86.4 Cycle R1 — Integrated Execution Profile

This patch implements the requested NDS/Flag setup as an explicit profile inside the existing canonical Hook trade stack. It does not add a second Hook detector, a second node counter, or a parallel execution engine.

## Canonical setup

```text
Valid canonical HH/F3H Hook
→ canonical Cycle closed
→ canonical Terminal confirmed
→ canonical x_count exactly 3 or 4
→ Terminal has not reached Crown→Origin 86.4%
→ Buy Limit / Sell Limit at Crown + 0.864 × (Origin − Crown)
→ Stop behind canonical Death boundary, with Origin fallback
→ broker-normalized attached Target at fixed 1R
```

Origin is not counted as X1/X2/X3/X4. `x_count` is consumed directly from `FP_HookPhase02Sequence`.

## Integration boundary

The new profile is `FP_NDS_HOOK_TRADE_PROFILE_HOOK_864_CYCLE_R1`. The existing `TERMINAL_F123` profile remains enum value `0`, remains the default, retains limit entry at `resolve_price`, retains no attached fixed target, and retains the same-direction F123 market-exit lifecycle.

The new profile reuses:

- canonical Hook Phase02 validity, family, cycle closure, crown, Terminal, retracement, and node count;
- the existing selector and HH/F3H family policy;
- existing account/magic single-exposure controls;
- existing compare-and-swap entry lock;
- existing one-attempt persistent registry;
- existing quote, tick, stop-level, freeze-level, volume, and risk-cash logic;
- existing pending cancellation after structural death;
- the same central EA and lightweight Strategy Tester core.

## Safety and lifecycle

- Central decision and broker-send inputs remain `false` by default.
- Ratio `0.864`, node window `3..4`, confirmed-Terminal gate, untouched-level gate, and `1R` are locked. Modified values fail closed.
- The setup key is stable across x3→x4 for the same Hook; an accepted setup is not repriced or duplicated.
- Economic ownership remains symbol plus strategy Magic.
- After ownership is established, the broker comment is used only to recover the immutable lifecycle profile across restart/input changes.
- Unknown profile comments fail closed.
- Fixed-R pending and open-position Entry/SL/TP geometry is revalidated from broker state.
- Invalid fixed-R pending protection is cancelled as a risk-reduction action; failed cancellation blocks the lifecycle for reconciliation.
- Fixed-R positions are never routed through the Phase52 F123 close path.
- Ledger routing follows the recovered exposure profile, not mutable current inputs.

## Main files

- `mql5/Include/FlagCountingPhoenix/FP_NDSHook864CycleR1Rules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeTypes.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeRules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeExecutionCore.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeExport.mqh`
- `mql5/Experts/FlagCounting/NDSHook864CycleR1ContractSelfTest.mq5`
- `tools/flag_counting/nds_hook_864_cycle_r1_reference.py`
- `tests/flag_counting/test_nds_hook_864_cycle_r1_reference.py`
- `docs/nds_entry_architecture/phase55_hook_864_cycle_r1_execution/`

## Repository QA

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\flag_counting\run_nds_hook_864_cycle_r1_tests.ps1
```

At patch construction:

- 26 deterministic Python tests passed.
- 8 bounded regression/static QA stages passed.
- 324 explicit PASS records and zero FAIL records were emitted.
- Engineering policy passed with zero errors and zero warnings.
- Python reference and QA files passed `py_compile`.
- Modified MQL5 files passed delimiter and compatibility scans.
- Static QA emitted 40 existing non-blocking repository advisories; no blocking static finding was present.

## External acceptance still pending

Repository QA is not MetaEditor, MT5 Strategy Tester, or broker proof. The patch deliberately keeps the following pending:

- supported Windows/MetaEditor clean compile;
- MQL5 self-test execution;
- Python/MQL5 vector parity;
- Phase52 tester regression;
- Phase55 tester and visual geometry review;
- demo-broker pending/fill/SL/TP/death-cancel/restart evidence;
- x3→x4 no-reprice evidence;
- broker statement and ledger reconciliation;
- risk and human approval for any live activation.

No profitability, edge, production readiness, or live authority claim is made by this patch.
