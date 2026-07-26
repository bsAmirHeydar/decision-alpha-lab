
---
type: source_card
source_path: "docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER.md"
source_ext: ".md"
source_size: 12549
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "Rally", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["E0001", "E0002", "E0003", "E0004", "H0005", "M0001", "M0002"]
---

# Source Card — H0005_R1_SIX_SLOT_TOUCH_LEDGER.md

## Source

[[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]]

## Summary

This document is the execution contract for `E0001_ReversalOneToOne.mq5`. The strategy is evaluated once per closed candle by default: `InpRefreshSetupsOnNewBarOnly = true` `InpManageOrdersEveryTick = false` `InpUseClosedBarsOnly = true` The current forming candle is excluded from structural/regime calculations so the touch zone is not mutated by the same candle that is about to trade it. Execution does not invent its own market logic. It reuses the hypothesis modules: M0001 builds node territories and node consumption/hunt state. M0002 builds the last completed branch outcome: reversal or continuation. E0001 only translates the active H0005 reversal state into pending limit orders. `InpRegimeBasis` has two modes: `E0001_REGIME_LAST_COMPLETED_BRANCH` Trade only when the latest completed M0002 branch outcome is `REVERSAL_AFTER_EXIT`. `E0001_REGIME_HUMAN_CONTEXT_COMBINED` `InpHumanContextS

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Rally|Rally]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0001, E0002, E0003, E0004, H0005, M0001, M0002

## Headings

- H0005 Reversal Structural-Target-Capped Execution — Build 1.25
  - Execution cadence
  - Source of truth
  - Regime input modes
  - Node selection
  - Spread-aware order geometry
  - Trading-session filter
  - Reversal exit
  - Consumption
  - Diagnostics
  - H0005 research report
    - Directional memory

## Related Source Documents

- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `50`
- [[docs/execution/README|README.md]] — score `50`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `48`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `47`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `47`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] — score `44`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] — score `43`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|README.md]] — score `43`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|README.md]] — score `38`
- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `35`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
