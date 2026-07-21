
---
type: source_card
source_path: "docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS.md"
source_ext: ".md"
source_size: 4159
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_PROFESSIONAL_VALIDATION_METRICS.md

## Source

[[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS.md]]

## Summary

This document locks the professional validation layer added to the M0001 MQL-native research engine. The node, territory, touch, HUNT, revisit, RTV, logRTV, warmup, and candle-gated runtime semantics are unchanged. The EA remains candle-gated during runtime: The professional statistics are intentionally final-only. They are not recalculated on every candle. Earlier reports embedded `histRaw` into the main NODES/RANDOM lines. Long histograms could be truncated by the MetaTrader Journal, hiding the important `COMPARE` section. v1.60 fixes this by default: The main final lines are compact and the histogram is printed only as separate optional `DAL_M0001_FINAL_HIST_*` lines. Each node event can now be compared against multiple matched random windows: For each valid node event, the engine builds a deterministic random baseline with the same RTV sample length and a valid pre-entry before-windo

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Professional Validation Metrics — v1.60
  - Final-only validation design
  - Compact report bug fix
  - Random baseline K
  - Core outputs
    - NODES / RANDOM
    - COMPARE
    - QUANT_TAIL
    - ROBUST
    - SESSION_REGIME
    - AUDIT
  - Optional parameter robustness grid

## Related Source Documents

- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|report.md]] — score `25`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `22`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|report.md]] — score `21`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `21`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `20`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `20`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `20`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `20`
- [[docs/mql_native/MQL_NATIVE_ARCHITECTURE|MQL_NATIVE_ARCHITECTURE.md]] — score `20`
- [[docs/architecture|architecture.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
