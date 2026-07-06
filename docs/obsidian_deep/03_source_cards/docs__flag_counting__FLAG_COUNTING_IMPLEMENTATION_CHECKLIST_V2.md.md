
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2.md"
source_ext: ".md"
source_size: 10360
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "MQL Native", "Path Smoothness", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2.md

## Source

[[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2|docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2.md]]

## Summary

<!-- CURRENT CANON NOTICE This file is retained as historical/context documentation. For current Phoenix implementation decisions, use: docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md If this file conflicts with the current canon, the current canon wins. --> This checklist converts `FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md` into concrete engineering tasks. Every item should be treated as an acceptance criterion for the next implementation pass. Recommended modules: Existing files may be reused, but the internal responsibilities should match these boundaries. [ ] Node extraction uses `high` and `low` only. [ ] No structure rule uses `open`. [ ] No structure rule uses `close`. [ ] No structure rule uses candle body. [ ] No structure rule uses candle color. [ ] Audit explicitly reports that logic is close-agnostic. [ ] Raw nodes are preserved. [ ] Compressed nodes reference raw node ids. [ ]

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Path_Smoothness|Path Smoothness]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Flag Counting Implementation Checklist V2
  - 1. Module boundaries
  - 2. Node engine checklist
    - 2.1 High/low only
    - 2.2 Raw node preservation
    - 2.3 Alternating compressed view
  - 3. ND detector checklist
    - 3.1 ND node count
    - 3.2 Adaptive L
    - 3.3 50% cycle threshold
  - 4. Flag geometry checklist
    - 4.1 Common two-leg body

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `25`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V2|FLAG_COUNTING_SEQUENCE_CONTRACT_V2.md]] — score `25`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `18`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `18`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `18`
- [[lab/03_experiments/EXP_flag_counting/docs/README_FLAG_MARKET_ANATOMY_PHILOSOPHY|README_FLAG_MARKET_ANATOMY_PHILOSOPHY.md]] — score `18`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|FLAG_COUNTING_SEQUENCE_CONTRACT_V3.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
