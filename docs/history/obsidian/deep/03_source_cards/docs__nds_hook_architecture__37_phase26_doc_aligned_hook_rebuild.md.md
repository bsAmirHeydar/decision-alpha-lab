
---
type: source_card
source_path: "docs/nds_hook_architecture/37_phase26_doc_aligned_hook_rebuild.md"
source_ext: ".md"
source_size: 4048
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Hook", "MQL Native", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 37_phase26_doc_aligned_hook_rebuild.md

## Source

[[docs/nds_hook_architecture/37_phase26_doc_aligned_hook_rebuild|docs/nds_hook_architecture/37_phase26_doc_aligned_hook_rebuild.md]]

## Summary

The earlier Phase 17–25 visual work treated each strict sequence as if it could be rendered as an independent Hook. That contradicted the Hook / ND documentation: Hook / ND is a structured phase container. Internal branch sequences are counted inside that container. Numbered branch nodes are same-side adverse nodes only. Low-side / positive Hook uses lows / valleys. High-side / negative Hook uses highs / peaks. Branches are built end-backward and then labelled old-to-new. Branches with more than four counted nodes are not valid readable output. Labels must be collected and stacked deterministically. The semantic chart view must not draw straight sequence wiring. `docs/flag_counting/engineering_pack_v5/02_definitions/ND_HOOK_DEFINITION.md` `docs/flag_counting/engineering_pack_v5/03_explanations/ND_HOOK_BRANCHING_EXPLAINED.md` `docs/flag_counting/engineering_pack_v5/04_algorithms/HOOK_BRAN

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Phase 26 — Doc-Aligned Hook / ND Branch Rebuild
  - Why
  - Source documents used as authority
  - Root fixes
    - 1. Branch builder
    - 2. Branch length
    - 3. Minimum 1/2 validation
    - 4. Opposite extreme / Hook crown
    - 5. Semantic minimal renderer
    - 6. Label placement
  - Remaining limitation

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `18`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1|HOOK_ND_BRANCH_ALGORITHM_V1.md]] — score `18`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1|HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1.md]] — score `18`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1|HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1.md]] — score `18`
- [[docs/nds_hook_architecture/05_visualization_and_diagnostics|05_visualization_and_diagnostics.md]] — score `17`
- [[docs/nds_hook_architecture/03_sequence_builder|03_sequence_builder.md]] — score `17`
- [[docs/flag_counting/engineering_pack_v5/02_definitions/ND_HOOK_DEFINITION|ND_HOOK_DEFINITION.md]] — score `16`
- [[docs/flag_counting/engineering_pack_v5/03_explanations/ND_HOOK_BRANCHING_EXPLAINED|ND_HOOK_BRANCHING_EXPLAINED.md]] — score `16`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/HOOK_BRANCH_ENGINE_ALGORITHM|HOOK_BRANCH_ENGINE_ALGORITHM.md]] — score `16`
- [[docs/nds_hook_architecture/02_cyclehook_object_model|02_cyclehook_object_model.md]] — score `15`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
