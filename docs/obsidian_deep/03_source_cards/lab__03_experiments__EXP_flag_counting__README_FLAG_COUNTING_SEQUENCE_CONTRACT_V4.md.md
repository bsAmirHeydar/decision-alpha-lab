
---
type: source_card
source_path: "lab/03_experiments/EXP_flag_counting/README_FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md"
source_ext: ".md"
source_size: 1169
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Flag Counting", "Hook", "MQL Native"]
entities: []
---

# Source Card — README_FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md

## Source

[[lab/03_experiments/EXP_flag_counting/README_FLAG_COUNTING_SEQUENCE_CONTRACT_V4|lab/03_experiments/EXP_flag_counting/README_FLAG_COUNTING_SEQUENCE_CONTRACT_V4.md]]

## Summary

Sequence Contract V4 remains the active semantic contract, but it is subordinate to the current canon: Use V4 for the F1/F2/F3 and Hook/ND semantic rules after reading the current canon. Active implementation path: Important V4 rules retained by the current canon: Nodes come from the existing project node logic. L is the existing left/right candle clearance definition. The algorithm uses high/low nodes only. Equality does not count as break. F1 starts from a phase boundary unless fail-open diagnostic recovery is explicitly used. F2 starts only after F1 confirmation and uses strict-window backfill. F3 starts only after F2 confirmation and uses strict-window backfill. F2 is size-compared to F1 only. F3 uses OR qualification against F2: Leg1 L ratio or flag size ratio. Hook/ND detection is branch-based. ND is 3 or 4 nodes only; 2 is not ND. F3 locks on the first confirmed opposite F1. Locke

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]

## Entities

—

## Headings

- EXP Flag Counting — Sequence Contract V4

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `16`
- [metadata.yaml](../../lab/03_experiments/EXP_flag_counting/metadata.yaml) — score `9`
- [[lab/03_experiments/EXP_flag_counting/README|README.md]] — score `9`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `8`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/experience_capture/answers/BASE-04/answer_raw_en|answer_raw_en.md]] — score `8`
- [[docs/experience_capture/answers/BASE-05/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/experience_capture/answers/DST-R03/answer_normalized_en|answer_normalized_en.md]] — score `8`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
