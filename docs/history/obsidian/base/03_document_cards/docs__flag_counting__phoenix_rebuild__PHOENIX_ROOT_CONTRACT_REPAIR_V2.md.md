---
title: "Phoenix Root Contract Repair V2"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/phoenix_rebuild/PHOENIX_ROOT_CONTRACT_REPAIR_V2.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "5997"
concepts:
  - "AI Agent Layer"
  - "F-Counting"
  - "Hook"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# Phoenix Root Contract Repair V2

**Source:** [[docs/flag_counting/phoenix_rebuild/PHOENIX_ROOT_CONTRACT_REPAIR_V2|docs/flag_counting/phoenix_rebuild/PHOENIX_ROOT_CONTRACT_REPAIR_V2.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `5997` bytes

## خلاصه

This repair brings the Phoenix implementation back to the documented Flag Counting contract after the Hook/ND visual-cycle changes made the main chart gray and starved the colored F1/F2/F3 flag bodies. The guiding rule is simple: > Hook / ND is a phase-boundary and context layer. It must never erase the two-leg flag-body detector. The main chart must show valid F structures first. Hook / ND is drawn as gray context behind those structures, not as a replacement for them. The uploaded project had four coupled problems. `FP_DetectScale()` first collected Hook-derived roots and then built F1 only from those roots unless no Hook-derived root could build a visible F1. That is not safe. A Hook engi

## Headings

- Phoenix Root Contract Repair V2
-   Purpose
-   Root failure found
-     1. Hook-origin filtering was too strong
-     2. Same-direction restart pruning was too aggressive for the research chart
-     3. Hook rendering was not compact enough across scales
-     4. Hook counted-node labels were mixed with main-chart labels
-   Repair decisions
-     1. Always keep fail-open F1 visibility when allowed
-     2. Disable same-direction chain pruning by default
-     3. Compact Hook arcs at renderer level
-     4. Hide Hook counted numbers by default

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/phoenix_rebuild/IMPLEMENTATION_NOTES|Phoenix Implementation Notes]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/PHOENIX_MAIN_CHART_CONTRACT_REPAIR_V3|Phoenix Main-Chart Contract Repair V3]] — `flag_counting_docs`
- [[docs/flag_counting/phoenix_rebuild/PHOENIX_SEQUENCE_OWNERSHIP_REPAIR_V4|Phoenix Sequence Ownership Repair V4]] — `flag_counting_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|BASE-06 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|Flag Counting Level 19 — Clean Isolated State Gate]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|Flag Counting Level 19 — Phase 11 Entry Bridge Readiness]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|Flag Counting Level 19 — Phase 12 Extreme Candidate Map]] — `flag_counting_docs`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|Flag Counting Level 19 — Phase 13 Multi-Timeframe Alignment Map]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
