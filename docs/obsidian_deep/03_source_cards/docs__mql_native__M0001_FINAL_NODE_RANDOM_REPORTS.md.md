
---
type: source_card
source_path: "docs/mql_native/M0001_FINAL_NODE_RANDOM_REPORTS.md"
source_ext: ".md"
source_size: 887
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "MQL Native", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_FINAL_NODE_RANDOM_REPORTS.md

## Source

[[docs/mql_native/M0001_FINAL_NODE_RANDOM_REPORTS|docs/mql_native/M0001_FINAL_NODE_RANDOM_REPORTS.md]]

## Summary

The compact logRTV node-vs-random report is no longer printed during every runtime update. It is printed only when the EA finishes (`OnDeinit`). At the end of the run, exactly two final result prints are produced: The first line is the aggregate for final node/territory events. The second line is the aggregate for matched random reference windows, plus the node-vs-random comparison summary. The following are disabled by default: `M0001_LiveVisualLab.mq5` version: `1.55`.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Final Node/Random Reports
  - Purpose
  - Journal output
  - Disabled noisy prints
  - Version

## Related Source Documents

- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `19`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `17`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `17`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `12`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `12`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `12`
- [[docs/mql_native/M0001_CANDLE_GATED_RUNTIME|M0001_CANDLE_GATED_RUNTIME.md]] — score `12`
- [[docs/mql_native/M0001_CLEAN_REVISIT_LABELS|M0001_CLEAN_REVISIT_LABELS.md]] — score `12`
- [[docs/mql_native/M0001_EXCEL_AUDIT_REPORT|M0001_EXCEL_AUDIT_REPORT.md]] — score `12`
- [[docs/mql_native/M0001_EXTREME_AND_HUNT_ZONE_AUDIT|M0001_EXTREME_AND_HUNT_ZONE_AUDIT.md]] — score `12`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
