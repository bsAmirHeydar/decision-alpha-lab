
---
type: source_card
source_path: "lab/02_hypotheses/H0005_directional_memory.md"
source_ext: ".md"
source_size: 1231
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0005", "M0001"]
---

# Source Card — H0005_directional_memory.md

## Source

[[lab/02_hypotheses/H0005_directional_memory|lab/02_hypotheses/H0005_directional_memory.md]]

## Summary

**Hypothesis:** branch regimes have structural directional memory. Reversal regimes should travel toward the next opposite structural node/zone destination. Continuation regimes should keep moving from the last zone brea… Default detector: `LAST_ONLY`. Context and consensus modes are available for comparison and confidence, but the hypothesis does not assume that context should hard-filter direction. Reversal paths now distinguish a simple zone-edge invalidation from a hunted zone that later reclaims and reverses. The default reversal stop is the farther of: the far edge of the frozen M0001 zone, and the most adverse hunt extreme reached beyond that edge before the path locks/reclaims. This keeps a valid reversal hunt from being treated as immediate failure while still measuring the actual stop-loss distance needed by the structure. MFE/MAE remain stopped at path exit. Additional diagnos

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0005, M0001

## Headings

- H0005 — Directional Memory
  - v1.01 refinement — adaptive reversal stop and R diagnostics

## Related Source Documents

- [[lab/02_hypotheses/H0001_structural_highs_lows_as_decision_nodes|H0001_structural_highs_lows_as_decision_nodes.md]] — score `21`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `21`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `20`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `20`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `20`
- [[papers/001_atomic_live_regime_framework|001_atomic_live_regime_framework.md]] — score `20`
- [[README|README.md]] — score `20`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `19`
- [[lab/02_hypotheses/H0005_directional_memory_atomic|H0005_directional_memory_atomic.md]] — score `19`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `19`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
