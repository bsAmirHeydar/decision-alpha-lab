# MQL Module Map

Version: 1.59

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
