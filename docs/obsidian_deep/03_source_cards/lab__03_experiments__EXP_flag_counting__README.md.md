
---
type: source_card
source_path: "lab/03_experiments/EXP_flag_counting/README.md"
source_ext: ".md"
source_size: 2060
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "UI / React", "Validation / Audit"]
entities: ["M0007"]
---

# Source Card — README.md

## Source

[[lab/03_experiments/EXP_flag_counting/README|lab/03_experiments/EXP_flag_counting/README.md]]

## Summary

This experiment studies fractal, multi-scale, multi-sequence F-counting. Start from the current canon: That file resolves all Flag Counting implementation decisions. If older VNext/V6/M0007 documents conflict with it, the current canon wins. Phoenix is the only active implementation path for this experiment. Read in this order: `docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md` `docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md` `docs/flag_counting/FLAG_COUNTING_ENGINEERING_PACK_V5.md` `docs/flag_counting/engineering_pack_v5/` `docs/flag_counting/implementation_ladder_v1/` `docs/flag_counting/phoenix_rebuild/` The old VNext, V6, sequence V2/V3, checklist V2/V3/V4, and M0007 documents remain research history. They must not be used as the decision source for new code. The active model is: Core rules: high/low only; strict break only; equality is not break; L-based node streams; bra

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

M0007

## Headings

- EXP Flag Counting
  - Active source of truth
  - Active implementation path
  - Core documents
  - Legacy documents
  - Experiment grammar
  - Default visibility policy
  - Recommended first Phoenix run

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `29`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V4|FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]] — score `22`
- [[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]] — score `21`
- [[docs/flag_counting/README|README.md]] — score `21`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `21`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `19`
- [[docs/flag_counting/FLAG_COUNTING_VNEXT_IMPLEMENTATION|FLAG_COUNTING_VNEXT_IMPLEMENTATION.md]] — score `19`
- [[mql5/Include/M0007/README_M0007_FlagCountingF1|README_M0007_FlagCountingF1.md]] — score `19`
- [metadata.yaml](../../lab/03_experiments/EXP_flag_counting/metadata.yaml) — score `18`
- [[lab/03_experiments/EXP_flag_counting/README_FLAG_COUNTING_PHOENIX|README_FLAG_COUNTING_PHOENIX.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
