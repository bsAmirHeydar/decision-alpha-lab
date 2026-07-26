
---
type: source_card
source_path: "docs/mql_native/M0001_LOGRTV_RANDOM_NULL_COMPARISON.md"
source_ext: ".md"
source_size: 1644
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native", "Rally", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_LOGRTV_RANDOM_NULL_COMPARISON.md

## Source

[[docs/mql_native/M0001_LOGRTV_RANDOM_NULL_COMPARISON|docs/mql_native/M0001_LOGRTV_RANDOM_NULL_COMPARISON.md]]

## Summary

Raw RTV is useful for interpretation, but it is naturally bounded below and unbounded above. Statistical comparison is therefore done on: This makes a 2x expansion and a 0.5x contraction symmetric: The node sample uses final M0001 events only: For every ready node event, a matched random reference window is generated: This creates a parallel random baseline using the same measurement structure. All extra per-bar prints are disabled by default. The EA prints one compact line only when the node-vs-random logRTV result changes: The line contains: The huge multi-line distribution report and the standard per-bar status print are disabled. The compact result is throttled by signature, so it only prints when ready RTV statistics actually change. `M0001_LiveVisualLab.mq5` version: `1.54`.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 LogRTV Random Null Comparison
  - Purpose
  - Node sample
  - Random null sample
  - Journal output
  - Performance
  - Version

## Related Source Documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `21`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|report.md]] — score `21`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|report.md]] — score `19`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `17`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `16`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `16`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `16`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `16`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `16`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
