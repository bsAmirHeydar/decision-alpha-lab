
---
type: source_card
source_path: "papers/001_atomic_live_regime_framework.md"
source_ext: ".md"
source_size: 3273
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Atomic No-Sample", "Decision Node", "Execution / Risk", "Known-Time Causality", "Path Smoothness", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0005", "M0001"]
---

# Source Card — 001_atomic_live_regime_framework.md

## Source

[[papers/001_atomic_live_regime_framework|papers/001_atomic_live_regime_framework.md]]

## Summary

This paper describes a research framework for structural market regimes that avoids a common source of bias: completed-sample sequencing. The framework replaces sample order with raw-event known-time batches and requires… Market research often produces convincing results that cannot be traded. The reason is not always overfitting. Sometimes the report answers the wrong temporal question. A completed event sample may contain information that was not available when an entry would have been made. If this sample is later used as if it were known in real time, the report becomes subtly biased. Decision Alpha Lab encountered this problem in regime memory and directional memory research. The solution was to move from sample-centric analysis to atomic live replay. The framework begins with structural nodes and zones. Price creates nodes, revisits them, hunts them, breaks them, and resolves them

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0005, M0001

## Headings

- Atomic Live Regime Framework
  - Abstract
  - 1. Motivation
  - 2. Structural events
  - 3. Known-time ordering
  - 4. Atomic no-sample replay
  - 5. Reversal and continuation
  - 6. R multiple discipline
  - 7. Validation
  - 8. Conclusion

## Related Source Documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `26`
- [[README|README.md]] — score `26`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] — score `24`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `24`
- [[lab/02_hypotheses/H0005_directional_memory_atomic|H0005_directional_memory_atomic.md]] — score `24`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `22`
- [[docs/architecture|architecture.md]] — score `21`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `21`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `21`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `20`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
