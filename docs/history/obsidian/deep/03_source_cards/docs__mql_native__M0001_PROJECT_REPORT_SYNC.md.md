
---
type: source_card
source_path: "docs/mql_native/M0001_PROJECT_REPORT_SYNC.md"
source_ext: ".md"
source_size: 1208
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "MQL Native", "Python Brain", "Validation / Audit"]
entities: ["M0001"]
---

# Source Card — M0001_PROJECT_REPORT_SYNC.md

## Source

[[docs/mql_native/M0001_PROJECT_REPORT_SYNC|docs/mql_native/M0001_PROJECT_REPORT_SYNC.md]]

## Summary

MQL5 file writing is sandboxed. The expert cannot reliably write directly into the repository working tree from Strategy Tester. So the expert now writes reports to a project-relative path inside the MT5 file sandbox: Then the sync script copies the generated files into the same folder inside this repository: CSV journals still use the same prefix. If you do not know the exact tester agent folder, the script also searches under: `M0001_LiveVisualLab.mq5` version: `1.35`.

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0001

## Headings

- M0001 Project Report Sync
  - Why
  - Expert inputs
  - Sync command
  - Output files
  - Version

## Related Source Documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `21`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `21`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `21`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `18`
- [[docs/architecture|architecture.md]] — score `17`
- [[docs/M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE|M0001_SINGLE_SOURCE_LIVE_ARCHITECTURE.md]] — score `17`
- [[docs/MQL_LIVE_ALL_IN_ONE_APPLY|MQL_LIVE_ALL_IN_ONE_APPLY.md]] — score `17`
- [[docs/mql_visual_lab|mql_visual_lab.md]] — score `17`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `16`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
