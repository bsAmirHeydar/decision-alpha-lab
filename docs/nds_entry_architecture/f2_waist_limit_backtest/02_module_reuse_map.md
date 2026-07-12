# F2 Waist Limit — Module Reuse Map

## Existing authorities reused

| Concern | Reused authority |
|---|---|
| Closed bars | `FP_Timebase.mqh` |
| Scale list | `FP_NodeScaleList.mqh` |
| Canonical nodes | `FP_NodeEngine.mqh` through Sequence Engine |
| F1 body/lifecycle | Phoenix Levels 05–07 |
| F2 body/lifecycle | `FP_F2LifecycleEngine.mqh` |
| Parent resolution | `FP_CanonicalFindParentIndex` |
| Tick normalization | `FP_NDSHookTradeRules.mqh` generic price helper |
| Fixed/risk-cash size | `FP_NDSHookTradeComputeVolume` |
| Symbol trade permissions | `FP_NDSHookTradeCanSend` |

## F2-specific modules

| Module | Responsibility |
|---|---|
| `FP_NDSF2FastDetector.mqh` | Executes approved per-scale F detection without global visual/canonical post-processing |
| `FP_NDSF2WaistTradeTypes.mqh` | Minimal runtime configuration and setup data |
| `FP_NDSF2WaistTradeRules.mqh` | Freshness, pair selection, exact prices, volume and broker request |
| `FP_NDSF2WaistTradeEngine.mqh` | Single-exposure state machine |
| `FP_NDSF2WaistBacktestEngine.mqh` | Closed-bar orchestration |
| `NDSF2WaistLimitBacktest.mq5` | Tester-only entry point |

## Removed from this runtime

- Hook branch scanning
- Hook Phase 02 and Hook validity
- global sequence ownership and visual canonicalization
- renderer and chart objects
- CSV/report export
- performance timing counters
- terminal Global Variable registry
- terminal-wide mutex
- custom runtime prints
- F3 construction
- Zone and AI
