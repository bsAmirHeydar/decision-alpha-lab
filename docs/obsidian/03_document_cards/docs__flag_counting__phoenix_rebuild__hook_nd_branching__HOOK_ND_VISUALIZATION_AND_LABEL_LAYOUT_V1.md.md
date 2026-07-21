---
title: "Hook / ND Visualization and Label Layout V1"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "6246"
concepts:
  - "AI Agent Layer"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# Hook / ND Visualization and Label Layout V1

**Source:** [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1|docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_VISUALIZATION_AND_LABEL_LAYOUT_V1.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `6246` bytes

## خلاصه

This document defines how Hook / ND structures and Flag Counting labels must be rendered on the chart. The main visual failures observed so far were: 1. labels overlap and become unreadable; 2. ND labels are drawn for raw/developing structures that are not true ND; 3. multiple branch states are dumped directly on the main chart; 4. Hook arcs do not clearly show which branch or Hook context they belong to. This contract separates semantic rendering from debug rendering. The renderer must not create Hook, ND, F1, F2, or F3 structures. It only draws events emitted by the engine. Semantic view is the default chart view. It should show: confirmed and active structures; meaningful developing struc

## Headings

- Hook / ND Visualization and Label Layout V1
-   1. Purpose
-   2. Rendering principles
-     2.1 Renderer is not a detector
-     2.2 Semantic view versus audit view
-   3. Hook / ND visual objects
-     3.1 Hook arc
-     3.2 ND label
-     3.3 Branch number labels
-     3.4 Developing branches
-   4. Label layout contract
-     4.1 Labels must be stacked

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/principles|Research Principles]] — `core_docs`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1|Hook / ND Branch Algorithm V1]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1|Hook / ND Branch-Sequence Contract V1]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_IMPLEMENTATION_CHECKLIST_V1|Hook / ND Implementation Checklist V1]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/README|Hook / ND Branch-Sequence Documentation Pack]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
