---
title: "06 — Build Phases"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/nds_hook_architecture/06_build_phases.md"
source_ext: ".md"
category: "nds_hook_architecture_docs"
source_size_bytes: "4242"
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


# 06 — Build Phases

**Source:** [[docs/nds_hook_architecture/06_build_phases|docs/nds_hook_architecture/06_build_phases.md]]

**Category:** `nds_hook_architecture_docs`  
**Status:** ok  
**Size:** `4242` bytes

## خلاصه

Find the central expert that currently performs F-counting / Rally display. Add display-family inputs, but keep default behavior as Rally-only. Acceptance: Build a Hook node adapter from the existing structural nodes used by F-counting. Acceptance: Implement CycleHook objects for positive and negative directions. Acceptance: Implement positive and negative strict sequence building. Acceptance: Extract X nodes and Y opposite Extremes. Acceptance: Implement: Acceptance: Implement positive and negative A/B/C classification. Acceptance: Add display controls for Hook-only, Rally-only, and both. Acceptance: Add optional audit outputs. Acceptance: Run visual smoke tests on: Once the visual and audi

## Headings

- 06 — Build Phases
-   Phase 0 — Locate Central Expert and Protect Rally
-   Phase 1 — Node Source Adapter
-   Phase 2 — CycleHook Object Model
-   Phase 3 — Multi-Sequence Builder
-   Phase 4 — X/Y Extraction
-   Phase 5 — Closure + ND + Death
-   Phase 6 — Hook Type A/B/C
-   Phase 7 — Visualization Controls
-   Phase 8 — Audit and CSV Export
-   Phase 9 — Smoke Test
-   Phase 10 — Freeze Hook v1

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/nds_hook_architecture/13_phase06_xy_closure_quality_score_implementation|13 — Hook Phase 06 Implementation: X/Y Closure Strength and Quality Score]] — `nds_hook_architecture_docs`
- [[docs/nds_hook_architecture/15_phase08_audit_csv_reconciliation_implementation|15 — Hook Phase 08 Implementation: Audit + CSV Reconciliation]] — `nds_hook_architecture_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|EXT-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/FLAG_COUNTING_SEQUENCE_CONTRACT_V3|Flag Counting Sequence Contract V3]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/hook_nd_branching/HOOK_ND_BRANCH_SEQUENCE_CONTRACT_V1|Hook / ND Branch-Sequence Contract V1]] — `flag_counting_docs`
- [[lab/03_experiments/EXP_flag_counting/docs/README_FLAG_OPTIONALITY_XY_STATE_PHILOSOPHY|Flag Project Philosophy II: Optionality, X/Y State Reading, and Multi-Regime Market Anatomy]] — `experiment`
- [[docs/nds_hook_architecture/07_mql5_integration_contract|07 — MQL5 Integration Contract]] — `nds_hook_architecture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
