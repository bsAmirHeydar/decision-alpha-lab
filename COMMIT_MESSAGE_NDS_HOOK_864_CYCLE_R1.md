feat(nds): add canonical Hook 86.4 x3/x4 fixed-R execution profile

Implement the requested NDS Hook setup inside the existing Hook and execution
architecture without introducing a parallel detector, node counter, or broker
path.

Setup contract:
- consume canonical Phase02 Hook validity, family, cycle closure and terminal
- require canonical x_count exactly 3 or 4; Origin is not counted
- require confirmed Terminal and untouched Crown-to-Origin 86.4 level
- stage Buy/Sell Limit at crown + 0.864 * (origin - crown)
- derive Stop from canonical death boundary with Origin fallback
- attach broker-normalized fixed 1R Target

Integration and compatibility:
- add explicit HOOK_864_CYCLE_R1 profile; keep TERMINAL_F123 as enum 0/default
- preserve Phase52 terminal entry, no-fixed-TP setup and F123 exit behavior
- retain legacy engine/core wrappers and broker-comment shape
- reuse HH/F3H selection, sizing, broker gates, one-exposure lock, CAS lock,
  persistent one-attempt registry and structural-death cancellation
- stabilize Phase55 setup identity across x3 to x4 with no reprice/duplicate

Lifecycle and safety:
- keep decision and broker-send inputs disabled by default
- recover managed pending/position lifecycle profile after magic ownership
- fail closed on unknown profile comments
- validate broker Entry/SL/TP for fixed-R pending orders and positions
- cancel invalid fixed-R pending protection; block on failed cancellation
- prevent fixed-R positions from entering the Phase52 F123 close path
- route audit rows by recovered profile and record broker protection geometry

Evidence and documentation:
- add dedicated Phase55 CSV ledger schema
- add no-order MQL5 contract self-test and Windows compile evidence script
- add deterministic Python reference, 26 tests, vectors, profile contract and
  acceptance matrix
- add 16-chapter engineering package plus Obsidian architecture, contract,
  state-machine, ledger and operator notes
- update existing NDS entry and Hook MOCs without redefining Hook doctrine

Verification:
- 26 Python tests passed
- 8 bounded regression/static QA stages passed
- 324 PASS and zero FAIL records
- engineering policy passed with zero errors and warnings
- modified Python files passed py_compile
- modified MQL5 sources passed compatibility and delimiter scans

MetaEditor, MT5 Strategy Tester and broker evidence remain external/pending.
Live activation and profitability are not asserted.
