
---
type: source_card
source_path: "docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE.md"
source_ext: ".md"
source_size: 1509
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_FINAL_ONLY_WARMUP_AND_PRUNE.md

## Source

[[docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE|docs/mql_native/M0001_FINAL_ONLY_WARMUP_AND_PRUNE.md]]

## Summary

Runtime distribution calculations were removed. During live-stream processing the EA only updates a lightweight runtime comment. The node-vs-random logRTV statistics are computed once in `OnDeinit`. A new input seeds the live stream with closed historical bars before the test/live stream begins: Warmup bars are used to reconstruct old structural nodes and their consumed/live state. The research sample is filtered by `analysis_start`, which is set to the first newly appended bar after warmup, so final reports inc… This allows old nodes to be available for touches inside the test period without contaminating the report with pre-test events. Random reference entries are also restricted to the same analysis period, while their before-window can use warmup bars when needed. This keeps the random baseline aligned with the node sample. The following old MQL files were not used by the main EA an

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Final-Only Research Report, Warmup, and MQL Prune
  - Final-only statistics
  - Warmup input
  - Random baseline fairness
  - Removed dead MQL files
  - Version

## Related Source Documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `21`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|report.md]] — score `21`
- [[docs/evidence/exp0002_mql_native_m0001_runtime/319a21879dae_report|report.md]] — score `19`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `16`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `16`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `16`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `16`
- [[docs/evidence/m0001_excel_audit/ff999bc7279e_M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `16`
- [[docs/evidence/m0001_json_audit/2e8468dd6e0a_M0001_JSON_AUDIT_REPORT|M0001_JSON_AUDIT_REPORT.md]] — score `16`
- [[docs/mql_native/M0001_LOGRTV_RANDOM_NULL_COMPARISON|M0001_LOGRTV_RANDOM_NULL_COMPARISON.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
