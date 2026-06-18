# MQL Module Map

Version: 1.66

| Module | Purpose |
|---|---|
| `Common/DAL_Common.mqh` | shared enums and small helpers |
| `Common/DAL_Math.mqh` | log range, safe division, high/low zone intersection |
| `Common/DAL_ChartObjects.mqh` | chart object creation, deletion, arrows, rectangles, labels |
| `Market/DAL_Bars.mqh` | MT5 candle loading in chronological order |
| `Market/DAL_LiveBarStream.mqh` | warmup seeding and append-latest-closed-candle stream |
| `StructuralNodes/LRule/DAL_LRuleTypes.mqh` | confirmed L-rule node data model |
| `StructuralNodes/LRule/DAL_LRuleDetector.mqh` | left/right L-rule HIGH/LOW detector |
| `StructuralNodes/DAL_StructuralNodeEngine.mqh` | stable facade for confirmed structural nodes |
| `M0001/DAL_M0001Config.mqh` | M0001 parameters and consume-mode helpers |
| `M0001/DAL_M0001Types.mqh` | final event model and RTV fields |
| `M0001/DAL_M0001Engine.mqh` | event lifecycle, frozen event geometry, RTV/log-range samples |
| `M0001/DAL_M0001AuditState.mqh` | per-node final visual/audit state, live/revisited/consumed state |
| `M0001/DAL_M0001Visual.mqh` | restored final chart drawings: nodes, zones, revisits, state, optional events/RTV |
| `M0001/DAL_M0001RtvNullComparison.mqh` | final-only node-vs-random logRTV distribution and comparison report |
| `Experts/DecisionAlphaLab/M0001/M0001_LiveVisualLab.mq5` | EA entry point, candle gate, warmup, final reports, final visuals |
| `M0002/DAL_M0002Types.mqh` | M0002 branch outcome model: REVERSAL_AFTER_EXIT vs CONTINUATION_AFTER_EXIT |
| `M0002/DAL_M0002Engine.mqh` | uses exact M0001 completed-exit events with hunt/touch consumption preserved, classifies close-vs-node at exit completion, and creates EVENT_RTV branch samples by default |
| `M0002/DAL_M0002Reports.mqh` | prints branch-vs-random and REVERSAL-vs-CONTINUATION final reports |
| `Experts/DecisionAlphaLab/M0002/M0002_ReversalContinuationExitVolatility.mq5` | H0002/M0002 EA entry point with candle-gated final-only reports |
| `M0003/DAL_M0003Reports.mqh` | H0003 continuation inertia/memory/cluster reports over exact M0002 branch samples |
| `Experts/DecisionAlphaLab/M0003/M0003_ContinuationInertiaMemory.mq5` | H0003/M0003 EA entry point for volatility-memory and cluster-stress reports |
| `M0004/DAL_M0004Reports.mqh` | H0004 branch-label regime clustering reports: transition matrix, same-branch lift, run clustering, permutation stress, block concentration stress, and segmented inertia |
| `Experts/DecisionAlphaLab/M0004/M0004_BranchRegimeClustering.mq5` | H0004/M0004 EA entry point using exact M0001/M0002 branch labels sorted chronologically |

Removed legacy layers are intentionally not part of the active runtime:

```text
Excel export layer
JSON report layer
old validation-journal script
old verbose distribution module
Python/UI bridge runtime
```

## v1.60 Professional Validation Metrics

The M0001 MQL-native engine now includes a final-only professional validation layer: compact NODES/RANDOM reports, explicit effect-size metrics, paired validation, bootstrap confidence intervals, sign-flip permutation p-values, distribution-distance metrics, quantile/tail metrics, chronological split-stability metrics, optional parameter robustness, and an integrity audit. Histograms are optional (`InpPrintHistogram=false` by default) so Journal lines no longer truncate the core `COMPARE` metrics.

See `docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS.md`.

## v1.66 M0002 Neutral Reversal/Continuation EVENT_RTV Branch Lab

M0002 is isolated from M0001 at the EA and include-folder level. It reuses M0001 structural-node, territory, log-range, and reporting modules, but uses the exact M0001 event lifecycle so H0002 is not inflated by post-consumption node recycling. Its default EVENT_RTV mode answers whether the original M0001 event-window volatility expansion is concentrated in reversal outcomes, continuation outcomes, or mixed across both branches. Optional POST_OUTCOME_FIXED mode is diagnostic only.

See `docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md`.


## Logic repair v1.70

H0002 now uses `DAL_M0001ComputeEvents()` directly. Node consumption is preserved exactly as in H0001/M0001; no reversal/continuation calculation is created after a node has been consumed.


## v1.00 M0004 Branch-Regime Clustering

M0004 studies the chronological sequence of exact M0002 branch labels. It preserves the observed reversal/continuation counts and tests whether the label order has same-branch inertia, Markov-like transition dependence, run clustering, and block-level branch concentration beyond shuffled-label nulls.

See `docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING.md`.
