
---
type: source_card
source_path: "docs/mql_native/H0005_DIRECTIONAL_MEMORY.md"
source_ext: ".md"
source_size: 3532
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Rally", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0005", "M0005"]
---

# Source Card — H0005_DIRECTIONAL_MEMORY.md

## Source

[[docs/mql_native/H0005_DIRECTIONAL_MEMORY|docs/mql_native/H0005_DIRECTIONAL_MEMORY.md]]

## Summary

H0005 asks whether branch-regime memory becomes usable directional/path memory. The market is not measured by fixed time windows. Direction is tested structurally: **Reversal regime:** the path has an X-axis destination. Entry starts at the next structural zone touch. Success means the opposite node/zone destination is touched before structural stop invalidation. The default stop m… **Continuation regime:** the path has no fixed X-axis target because structural levels are being broken. Entry starts at the break of the last zone, not merely at a node hunt. Exit is the detected regime change. The source of the regime is configurable: `LAST_ONLY` — default; uses the immediately previous branch label. `EWMA_CONTEXT` — uses human-eye EWMA branch context. `EWMA_CONSENSUS` — accepts only when last branch and context agree. `LAST_WITH_CONTEXT_CONFIDENCE` — uses last branch for direction while re

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0005, M0005

## Headings

- H0005 — Directional Memory of Structural Regimes
  - Regime source
  - Path exits
  - Metrics
  - Random and stress checks

## Related Source Documents

- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `21`
- [[docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE|H0005_CONTEXTUAL_BRANCH_REGIME_STATE.md]] — score `20`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `20`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `17`
- [[docs/execution/README|README.md]] — score `17`
- [[lab/02_hypotheses/H0001_structural_highs_lows_as_decision_nodes|H0001_structural_highs_lows_as_decision_nodes.md]] — score `17`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `17`
- [[lab/02_hypotheses/H0005_directional_memory_atomic|H0005_directional_memory_atomic.md]] — score `17`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `17`
- [[papers/001_atomic_live_regime_framework|001_atomic_live_regime_framework.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
