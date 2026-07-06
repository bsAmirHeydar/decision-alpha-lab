
---
type: source_card
source_path: "mql5/Include/M0007/README_M0007_FlagCountingF1.md"
source_ext: ".md"
source_size: 7920
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "MQL Native", "Path Smoothness", "UI / React", "Validation / Audit"]
entities: ["M0007"]
---

# Source Card — README_M0007_FlagCountingF1.md

## Source

[[mql5/Include/M0007/README_M0007_FlagCountingF1|mql5/Include/M0007/README_M0007_FlagCountingF1.md]]

## Summary

M0007 counts and draws F1 flag structures on chart for visual/audit research. The detector now uses the actual four-node F1 origin logic. Bullish F1: A bullish F1 is accepted only when: Bearish F1: A bearish F1 is accepted only when: This fixes the earlier schematic problem where the chart origin was synthetic or taken from the wrong side of the structure. The renderer draws only the clean F1 grammar: No horizontal guide levels, no vertical audit lines, and no internal N/R labels are drawn by default. Important inputs: M0007 is visual/audit-only. It does not place orders. The renderer must not invent the origin. `Start` is now a first-class detector node and is stored in every `M0007_F1Event`. Current core: The chart numbers are **not** leg labels. Current numeric count: Default overlay: Removed from the default overlay: Current default F1 confirmation is intentionally stricter: `InpRequ

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0007

## Headings

- M0007 — F1 Flag Counting MQL5 Module
  - Correct F1 topology
  - Visual contract
  - Files
  - Inputs
  - Scope
  - 2026-06 fix — real origin plus post-leg-2 internal 1/2
  - Confirmation contract update
  - Strict confirmation after internal 1/2
  - Live forming / confirmed rendering contract
  - Incremental chart object contract
  - Renderer hotfix: no default `Text` labels

## Related Source Documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `21`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_VNEXT_IMPLEMENTATION|FLAG_COUNTING_VNEXT_IMPLEMENTATION.md]] — score `19`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `19`
- [[docs/flag_counting/README|README.md]] — score `19`
- [[lab/03_experiments/EXP_flag_counting/README|README.md]] — score `19`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `17`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `16`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2.md]] — score `16`
- [[lab/03_experiments/EXP_flag_counting/docs/README_FLAG_MARKET_ANATOMY_PHILOSOPHY|README_FLAG_MARKET_ANATOMY_PHILOSOPHY.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
