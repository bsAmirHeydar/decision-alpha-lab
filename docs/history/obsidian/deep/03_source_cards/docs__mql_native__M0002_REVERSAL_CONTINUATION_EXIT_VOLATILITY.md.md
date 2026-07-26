
---
type: source_card
source_path: "docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md"
source_ext: ".md"
source_size: 9348
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0001", "H0002", "M0001", "M0002"]
---

# Source Card — M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md

## Source

[[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]]

## Summary

Version: 1.66 M0002 tests the second hypothesis in a separate MQL-native module. It reuses M0001 structural-node extraction, territory geometry, log-range math, random-baseline logic, and validation/reporting utilities. It uses the ex… `M0002_HuntRejectExitVolatility.mq5` remains only as a deprecated compatibility filename and now runs the same reversal/continuation logic. After a structural-node territory touch has completed its strict `exit_gap` window outside the frozen event zone, the completed event is classified only by the completed-exit candle side relative to the original node pri… This module does **not** classify by hunt / non-hunt and it does **not** discard candidate events because the node price was crossed before exit completion. The branch is decided immediately at the completed exit window. H0002 must use M0001 finalized events as its research sample. Node lifetime follo

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, M0001, M0002

## Headings

- M0002 — Reversal vs Continuation After Exit Volatility
  - Central Expert Advisor
  - Include stack
  - Core hypothesis
  - Event construction
  - Branch rules
  - Primary measurement window
  - Optional diagnostic mode
  - Inputs
  - Reports
  - v1.67 EVENT_RTV lock
  - Deep audit repair notes

## Related Source Documents

- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002_DEEP_AUDIT_AND_STABILITY.md]] — score `41`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `37`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `36`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `35`
- [[README|README.md]] — score `34`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `33`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `33`
- [[docs/mql_native/H0002_BRANCH_VOLATILITY_MODEL_ARTICLE|H0002_BRANCH_VOLATILITY_MODEL_ARTICLE.md]] — score `33`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `33`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `33`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
