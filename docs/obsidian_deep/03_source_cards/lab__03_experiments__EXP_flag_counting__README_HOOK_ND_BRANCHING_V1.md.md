
---
type: source_card
source_path: "docs/releases/legacy_migration/general/40b0c8ecc98c_README_HOOK_ND_BRANCHING_V1.md"
source_ext: ".md"
source_size: 977
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Hook", "UI / React"]
entities: []
---

# Source Card — README_HOOK_ND_BRANCHING_V1.md

## Source

[[docs/releases/legacy_migration/general/40b0c8ecc98c_README_HOOK_ND_BRANCHING_V1|docs/releases/legacy_migration/general/40b0c8ecc98c_README_HOOK_ND_BRANCHING_V1.md]]

## Summary

This experiment now has a dedicated Hook / ND branch-sequence specification. Read these documents before modifying Hook / ND code: `docs/flag_counting/phoenix_rebuild/hook_nd_branching/README.md` `docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1.md` `docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1.md` `docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1.md` `docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_IMPLEMENTATION_CHECKLIST_V1.md` The key correction is that Hook / ND is not a raw 3-node or 4-node window. A Hook can contain many internal branch sequences. The branch count is unlimited. The internal counted nodes inside each branch must be reduced t…

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- Hook / ND Branching V1

## Related Source Documents

- [[lab/03_experiments/EXP_flag_counting/README|README.md]] — score `17`
- [[docs/ai_execution/README|README.md]] — score `16`
- [[docs/debug/E0007/README|README.md]] — score `16`
- [[docs/debug/E0008/README|README.md]] — score `16`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `16`
- [[docs/flag_counting/engineering_pack_v5/README|README.md]] — score `16`
- [[docs/flag_counting/implementation_ladder_v1/README|README.md]] — score `16`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1|HOOK_ND_BRANCH_ALGORITHM_V1.md]] — score `16`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1|HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1.md]] — score `16`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_IMPLEMENTATION_CHECKLIST_V1|HOOK_ND_IMPLEMENTATION_CHECKLIST_V1.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
