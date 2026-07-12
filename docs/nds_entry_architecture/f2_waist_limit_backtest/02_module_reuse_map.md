# F2 Waist Limit — Module Reuse Map

## Reused canonical modules

| Concern | Existing authority reused |
|---|---|
| Closed-bar data | `FP_Timebase.mqh` |
| Scale list | `FP_NodeScaleList.mqh` |
| F1/F2 anatomy | `FP_SequenceEngine.mqh` |
| F2 lifecycle | `FP_F2LifecycleEngine.mqh` |
| Canonical parent resolution | `FP_CanonicalRules.mqh` through Sequence Engine |
| Price/tick normalization | `FP_NDSHookTradeRules.mqh` generic helpers |
| Fixed/risk-cash sizing | `FP_NDSHookTradeRules.mqh` generic helpers |
| Managed-order counting | Phase 52 trade helpers |
| Managed-position counting | Phase 52 trade helpers |
| Foreign-position guard | Phase 52 trade helpers |
| Terminal-wide entry mutex | Phase 52 trade helpers |
| Duplicate pending reconciliation | Phase 52 trade helpers |

## New modules

| Module | Responsibility |
|---|---|
| `FP_NDSF2WaistTradeTypes.mqh` | F2-specific configuration, setup and report contracts |
| `FP_NDSF2WaistTradeRules.mqh` | F2 selection, F1 parent resolution and exact price geometry |
| `FP_NDSF2WaistTradeEngine.mqh` | Single-exposure execution state machine |
| `FP_NDSF2WaistBacktestTypes.mqh` | Lightweight runtime reports and performance counters |
| `FP_NDSF2WaistBacktestEngine.mqh` | Closed-bar detector/execution orchestration |
| `NDSF2WaistLimitBacktest.mq5` | Dedicated Strategy Tester entry point |

## Explicitly excluded

- Hook Phase 02 validity and sequence classification
- Hook-after-Hook and Hook-after-F3 setup selection
- Zone adapter
- AI/CG scoring
- rendering and chart objects
- CSV ledgers
- production license
- timer and chart-event handlers
- paper broker and release-governance stack

## Internal Hook boundary nuance

`cfg.scan_hooks=true` remains inside the canonical F detector because approved F1 root construction can depend on phase-boundary evidence. No Hook object is passed to the F2 trade rules, and no Hook field can authorize an order.
