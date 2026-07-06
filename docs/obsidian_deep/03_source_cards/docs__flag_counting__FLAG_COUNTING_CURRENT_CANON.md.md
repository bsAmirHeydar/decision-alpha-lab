
---
type: source_card
source_path: "docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md"
source_ext: ".md"
source_size: 37939
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "Licensing", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0007"]
---

# Source Card — FLAG_COUNTING_CURRENT_CANON.md

## Source

[[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md]]

## Summary

Status: **active source of truth for Phoenix implementation**. Scope: docs, code patches, audit, renderer, validation, and future execution modules related to Flag Counting. This document exists to remove decision drift. If any older Flag Counting document conflicts with this file, this file wins. The only active implementation path is Phoenix: Legacy paths are retained only as research history or reference material: Do not start new code from M0007, VNext, V6, old checklists, or old sequence contracts. Use the following hierarchy when implementing or auditing Phoenix: **This file** — final decision source and conflict resolver. `docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md` — semantic sequence contract. `docs/flag_counting/FLAG_COUNTING_ENGINEERING_PACK_V5.md` and `docs/flag_counting/engineering_pack_v5/` — definitions, algorithms, and explanations. `docs/flag_counting/imple

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0007

## Headings

- Flag Counting Current Canon
  - 1. Active implementation target
  - 2. Canon hierarchy
  - 3. Non-negotiable invariants
  - 4. Final resolved decisions
    - 4.1 Phase reset
    - 4.2 F1 root preference
    - 4.3 Fail-open
    - 4.4 Main-chart visibility
    - 4.5 High-L versus lower-L ownership
    - 4.6 Pending nodes
    - 4.7 Backfill window

## Related Source Documents

- [[docs/flag_counting/README|README.md]] — score `30`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `27`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `25`
- [metadata.yaml](../../lab/03_experiments/EXP_flag_counting/metadata.yaml) — score `25`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]] — score `25`
- [[mql5/Include/FlagCountingPhoenix/README_FlagCountingPhoenix|README_FlagCountingPhoenix.md]] — score `24`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `23`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `23`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
