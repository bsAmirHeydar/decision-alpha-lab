
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_V6_IMPLEMENTATION_NOTES.md"
source_ext: ".md"
source_size: 10555
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Flag Counting", "Hook", "MQL Native", "Path Smoothness", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_V6_IMPLEMENTATION_NOTES.md

## Source

[[docs/flag_counting/FLAG_COUNTING_V6_IMPLEMENTATION_NOTES|docs/flag_counting/FLAG_COUNTING_V6_IMPLEMENTATION_NOTES.md]]

## Summary

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This patch adds a new implementation namespace: `FlagCountingV6`. V6 is not a patch over the old scanner. It is a modular implementation intended to follow the engineering documentation pack: L-rule node extraction from candle highs/lows. Equal high/low plateau merge. Alternating node view per L. Two-leg flag body construction. F1/F2/F3 post-flag state evaluation. Backfilled F2/F3 child origins from the parent post-flag correction context. Branch-based ND/Hook extraction. Diagnostic renderer that only draws emitted logical objects. The node engine follows the project L-rule: High/low only. Equal price is not a break. A node becomes

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting V6 Implementation Notes
  - Compile target
  - Important implementation choices
    - Node definition
    - Flag body
    - F1
    - F2
    - F3
    - ND / Hook
    - Renderer
  - Compile caveat
  - V6.1 semantic visibility and ownership repair

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `25`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `18`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V3|FLAG_COUNTING_CONCEPT_SPEC_V3.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2|FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
