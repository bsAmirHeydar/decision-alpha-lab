
---
type: source_card
source_path: "lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility.md"
source_ext: ".md"
source_size: 3227
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0001", "H0002", "M0001"]
---

# Source Card — H0002_reversal_vs_continuation_post_exit_volatility.md

## Source

[[lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility|lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility.md]]

## Summary

Status: active / fact-layer validation Given a valid completed M0001 structural-node event, does the completed exit side create different volatility regimes? H0002 uses the exact event stream created by H0001/M0001. It does not create a separate event builder. A valid H0002 sample must be: The node lifecycle, hunt/touch consume behavior, revisit reset, baseline logic, warmup handling, and exit-gap logic are inherited from M0001. The M0001 event exit is side-agnostic. A completed exit candle can be fully above or fully below the frozen event territory. The touch is confirmed only after `exit_gap` consecutive fully-outside candles. Exit is not equal to reversal. At the completed exit candle: The primary measurement is locked to the original M0001 event RTV: The branch label must not change the sample window. The branch model is not only a comparison of two means. It has four observed dimen

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0001, H0002, M0001

## Headings

- H0002 — Reversal vs Continuation Node-Exit Volatility Model
  - Research question
  - Event source
  - Exit logic
  - Branch classifier
  - Measurement
  - Current working model
    - 1. Frequency
    - 2. Intensity
    - 3. Tail
    - 4. Post-event memory
  - Acceptance signature

## Related Source Documents

- [[lab/02_hypotheses/H0002_reversal_vs_continuation_post_exit_volatility_deep_audit|H0002_reversal_vs_continuation_post_exit_volatility_deep_audit.md]] — score `28`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `27`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `27`
- [[docs/mql_native/H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING|H0003_CONTINUATION_INERTIA_MEMORY_CLUSTERING.md]] — score `27`
- [[docs/mql_native/H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM|H0003_INERTIA_MEMORY_RESULTS_AND_ALGORITHM.md]] — score `27`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `27`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `27`
- [[docs/mql_native/M0002_DEEP_AUDIT_AND_STABILITY|M0002_DEEP_AUDIT_AND_STABILITY.md]] — score `27`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `27`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `27`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
