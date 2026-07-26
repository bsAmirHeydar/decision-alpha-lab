
---
type: source_card
source_path: "docs/flag_counting/README.md"
source_ext: ".md"
source_size: 18669
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "MQL Native", "Market Anatomy", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0007"]
---

# Source Card — README.md

## Source

[[docs/flag_counting/README|docs/flag_counting/README.md]]

## Summary

Start here: That file is the final decision source for Phoenix. If any older Flag Counting document conflicts with it, the current canon wins. Phoenix is the only active implementation path. Read in this order: `FLAG_COUNTING_CURRENT_CANON.md` — final decisions and conflict resolver. `FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md` — semantic F1/F2/F3 and Hook/ND contract. `FLAG_COUNTING_ENGINEERING_PACK_V5.md` — engineering package index. `engineering_pack_v5/` — definitions, explanations, algorithms, visualization contracts. `implementation_ladder_v1/` — implementation order, interfaces, freeze gates, validation, audit/export. `phoenix_rebuild/` — Phoenix-specific repair notes, subordinate to the current canon. The following files remain useful as historical context, but must not be used as the decision source for new Phoenix code: M0007, VNext, and V6 are archived/reference implementations onl

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Market_Anatomy|Market Anatomy]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0007

## Headings

- Flag Counting Documentation
  - Active source of truth
  - Active implementation
  - Active canonical documents
  - Legacy/history documents
  - Non-negotiable rule
  - Phoenix Level 11.5 raw audit export
  - Level 12 renderer
  - Phoenix Level 13 validation
  - Level 14 release/debug/rollback layer
  - Level 15 module interface contracts
  - Level 16 acceptance matrix

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `38`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `31`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE|FLAG_COUNTING_LEVEL_19Z_COMPLETE_OBSERVATION_SUITE.md]] — score `31`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN|FLAG_COUNTING_LEVEL_20_ENTRY_BRIDGE_XY_ANCHOR_JOIN.md]] — score `31`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19D_TRANSITION_EVENT_LEDGER|FLAG_COUNTING_LEVEL_19D_TRANSITION_EVENT_LEDGER.md]] — score `29`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_21_PAPER_INTENT_NO_ORDER|FLAG_COUNTING_LEVEL_21_PAPER_INTENT_NO_ORDER.md]] — score `29`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_22_PAPER_LIFECYCLE_CLOSE_ONLY|FLAG_COUNTING_LEVEL_22_PAPER_LIFECYCLE_CLOSE_ONLY.md]] — score `29`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_23_PAPER_PERFORMANCE_CLOSE_ONLY|FLAG_COUNTING_LEVEL_23_PAPER_PERFORMANCE_CLOSE_ONLY.md]] — score `29`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_24_SAFETY_GATE_PRE_BROKER|FLAG_COUNTING_LEVEL_24_SAFETY_GATE_PRE_BROKER.md]] — score `29`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_25_BROKER_DRY_RUN_ONLY|FLAG_COUNTING_LEVEL_25_BROKER_DRY_RUN_ONLY.md]] — score `29`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
