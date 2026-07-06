---
title: "Phase 26 — Doc-Aligned Hook / ND Branch Rebuild"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/37_phase26_doc_aligned_hook_rebuild.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "4048"
concepts:
  - "AI Agent Layer"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Phase 26 — Doc-Aligned Hook / ND Branch Rebuild

**Source:** [[docs/nds_hook_architecture/37_phase26_doc_aligned_hook_rebuild|docs/nds_hook_architecture/37_phase26_doc_aligned_hook_rebuild.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `4048` bytes

## خلاصه

The earlier Phase 17–25 visual work treated each strict sequence as if it could be rendered as an independent Hook. That contradicted the Hook / ND documentation: Hook / ND is a structured phase container. Internal branch sequences are counted inside that container. Numbered branch nodes are same-side adverse nodes only. Low-side / positive Hook uses lows / valleys. High-side / negative Hook uses highs / peaks. Branches are built end-backward and then labelled old-to-new. Branches with more than four counted nodes are not valid readable output. Labels must be collected and stacked deterministically. The semantic chart view must not draw straight sequence wiring. `docs/flag_counting/engineeri

## Headings

- Phase 26 — Doc-Aligned Hook / ND Branch Rebuild
-   Why
-   Source documents used as authority
-   Root fixes
-     1. Branch builder
-     2. Branch length
-     3. Minimum 1/2 validation
-     4. Opposite extreme / Hook crown
-     5. Semantic minimal renderer
-     6. Label placement
-   Remaining limitation

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1|Hook / ND Branch Algorithm V1]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1|Hook / ND Branch-Sequence Contract V1]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1|Hook / ND Visualization and Label Layout V1]] — `flag_counting_docs`
- [[docs/nds_hook_architecture/03_sequence_builder|03 — Sequence Builder]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/05_visualization_and_diagnostics|05 — Visualization and Diagnostics]] — `nds_hook_architecture_docs`
- [[docs/flag_counting/engineering_pack_v5/02_definitions/ND_HOOK_DEFINITION|ND / Hook Definition]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/HOOK_BRANCH_ENGINE_ALGORITHM|Hook Branch Engine Algorithm]] — `flag_counting_docs`
- [[docs/nds_hook_architecture/02_cyclehook_object_model|02 — CycleHook Object Model]] — `nds_hook_architecture_docs`
- [[docs/flag_counting/engineering_pack_v5/03_explanations/ND_HOOK_BRANCHING_EXPLAINED|ND / Hook Branching Explained]] — `flag_counting_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/nds_hook_architecture/08_phase01_node_source_adapter_implementation|08 — Hook Phase 01 Implementation: Node Source Adapter]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/09_phase02_cyclehook_sequence_builder_implementation|09 — Hook Phase 02 Implementation: CycleHook Object and X-Sequence Builder]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
