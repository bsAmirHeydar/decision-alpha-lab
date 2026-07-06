---
title: "Hook / ND Branch-Sequence Documentation Pack"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/phoenix_rebuild/hook_nd_branching/README.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "1691"
concepts:
  - "AI Agent Layer"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
---


# Hook / ND Branch-Sequence Documentation Pack

**Source:** [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/README|docs/flag_counting/phoenix_rebuild/hook_nd_branching/README.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `1691` bytes

## خلاصه

This package defines the Hook / ND component used by the Flag Counting Phoenix engine. It is intentionally separated from the F1/F2/F3 sequence documents because Hook / ND is not a simple label or a single visual marker. It is a structural container that can hold multiple internal branch sequences. The purpose of this package is to remove ambiguity before implementation. The engine must not treat every three or four raw nodes as ND. A Hook / ND exists only when the branch-sequence rules defined here are satisfied. `HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1.md` Canonical conceptual and engineering contract for Hook / ND. `HOOK_ND_BRANCH_ALGORITHM_V1.md` Step-by-step deterministic algorithm for extr

## Headings

- Hook / ND Branch-Sequence Documentation Pack
-   Files
-   Core idea

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1|Hook / ND Branch Algorithm V1]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1|Hook / ND Branch-Sequence Contract V1]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_IMPLEMENTATION_CHECKLIST_V1|Hook / ND Implementation Checklist V1]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1|Hook / ND Visualization and Label Layout V1]] — `flag_counting_docs`
- [[docs/ai_execution/README|AI Execution Docs]] — `ai_execution_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/engineering_pack_v5/README|Flag Counting Engineering Pack V5]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
