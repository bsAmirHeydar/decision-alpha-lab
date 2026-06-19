# Decision Alpha Lab — Execution

Canonical execution root:

```text
mql5/Experts/DecisionAlphaLab/Execution/
mql5/Include/DecisionAlphaLab/Execution/
```

There must not be a nested `decision-alpha-lab/decision-alpha-lab` source copy.

## Current execution adapter

`E0001_ReversalOneToOne.mq5` implements H0005 reversal fixed-R execution.

Current E0001 builds run once per closed candle, resolve the effective reversal/continuation regime from M0002 plus optional human context input, and park spread-aware pending limits on the nearest active reversal nodes:

- 3 nearest buy limits from LOW nodes below market by default.
- 3 nearest sell limits from HIGH nodes above market by default.
- SL is behind the zone.
- TP defaults to the first opposite-node touch; `InpRewardR` is an optional reference/cap when enabled.
- Continuation/non-reversal deletes managed pending orders.
- Optional time filter can block new orders outside the configured session and delete managed pending orders.
- H5 research reporting prints directional memory and fixed-R reversal outcome metrics from the same M0001/M0002 modules so theoretical H5 behavior can be compared against real EA orders.

See `H0005_R1_SIX_SLOT_TOUCH_LEDGER.md` for the exact contract.

## MetaEditor include sync

When compiling from MetaTrader Shared Projects, angle-bracket includes such as:

```mql5
#include <DecisionAlphaLab/Execution/DAL_ExecReversalOneToOne.mqh>
```

are commonly resolved from the terminal-level include tree:

```text
MQL5/Include/DecisionAlphaLab/
```

not only from the repository folder. Use the release installer to copy the updated include files into the terminal include tree before compiling.


## Build 1.20 — strict touch/revisit ledger

This build keeps the H5 original-hypothesis report out of the execution EA. It only changes the execution ledger. A structural setup remains visible to the EA even when the current tick is already inside the touch zone, so the EA can lock that touch episode and avoid planting another limit until price exits the edge by `InpTouchRevisitResetBufferPoints` and later revisits it. Locked touch states are not pruned just because a node temporarily falls out of the 3+3 near-node cache, because that would allow duplicate limits inside the same touch.


### Build 1.21 node-zone lock note

The H5 executor now locks touch state by structural node (`node_id + direction`) and by the touched zone boundaries. A node does not receive a second pending limit while price remains in the same zone episode. Re-arm requires a full exit beyond the zone edge plus `InpTouchRevisitResetBufferPoints`; optional `InpAllowNodeRevisitRearm=false` disables same-node revisits entirely.


## TP policy — first opposite node touch with optional R exit

E0001 build 1.25 and E0002 build 1.03 use the same take-profit rule:

```text
TP = first opposite-node touch by default; optional fixed-R exit only if closer
```

`InpRewardR` is a reference/cap input and defaults to 1.0. By default TP is placed at the first structural opposing touch. If `InpUseFixedRExitIfCloser=true`, the fixed-R target can close earlier only when it is closer than that structural touch. If `InpAllowOppositeTouchBelowRewardR=false`, sub-R opposite-touch setups are skipped.


### Build 1.24 TP correction

E0001 and E0002 now default to TP at the first opposite-node touch. `InpUseFixedRExitIfCloser` is off by default; when enabled, `InpRewardR` can only exit earlier if it is closer than the structural target. `InpAllowOppositeTouchBelowRewardR=false` skips trades whose first opposite-node touch is below the configured R reference. The node touch/revisit lock remains independent from TP selection.


### Build 1.25 performance/compile fix

E0001 build 1.25 and E0002 build 1.03 keep the same H5 entry/TP/touch-lock contract, but use faster defaults and quieter logs. `InpLogMode` now defaults to `DAL_EXEC_LOG_ERRORS`, build-sanity and cycle diagnostics print only when order logging is enabled, and `InpH5ReportEnabled` is off by default in E0001 for execution tests. E0002 also fixes the close-confirmed market TP diagnostic compile error by returning market-entry TP details explicitly from the order helper.

Outside-session pending cleanup is throttled to once per bar instead of every tick. E0002 is pure market execution, so it no longer scans/deletes managed pending orders on every closed-candle signal pass; startup and session-close guards handle leftovers.
