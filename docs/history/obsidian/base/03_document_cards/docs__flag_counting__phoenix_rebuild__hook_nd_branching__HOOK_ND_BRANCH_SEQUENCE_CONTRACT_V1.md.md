---
title: "Hook / ND Branch-Sequence Contract V1"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "12566"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Rally"
  - "Structural Nodes"
  - "Validation"
---


# Hook / ND Branch-Sequence Contract V1

**Source:** [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1|docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `12566` bytes

## خلاصه

This document defines the exact Hook / ND logic for the Flag Counting Phoenix engine. The previous failure mode was that ND was treated as a raw marker produced from local 3-node or 4-node windows. That is incorrect. A valid Hook / ND is a structured phase container. It is built from same-side nodes, can contain multiple internal branch sequences, and must be normalized by the project `L` rule so that no internal branch sequence exceeds four counted nodes. The Hook / ND engine is part of the phase-boundary layer. It helps decide where an F1 root can start and explains ranges where the market is not yet expressing a clean F1/F2/F3 chain. It is not merely a visual annotation. A node is the pro

## Headings

- Hook / ND Branch-Sequence Contract V1
-   1. Purpose
-   2. Terminology
-     2.1 Node
-     2.2 Same-side nodes
-     2.3 Low-side Hook
-     2.4 High-side Hook
-     2.5 Hook origin boundary
-     2.6 Internal branch sequence
-     2.7 ND
-     2.8 Cycle retracement rule
-   3. Core invariants

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|EXT-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|Flag Counting Sequence Contract V3]] — `flag_counting_docs`
- [[docs/nds_hook_architecture/06_build_phases|06 — Build Phases]] — `nds_hook_architecture_docs`
- [[docs/releases/legacy_migration/general/0b9f38e7e2fd_README_FLAG_OPTIONALITY_XY_STATE_PHILOSOPHY|Flag Project Philosophy II: Optionality, X/Y State Reading, and Multi-Regime Market Anatomy]] — `experiment`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_ALGORITHM_V1|Hook / ND Branch Algorithm V1]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_IMPLEMENTATION_CHECKLIST_V1|Hook / ND Implementation Checklist V1]] — `flag_counting_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
