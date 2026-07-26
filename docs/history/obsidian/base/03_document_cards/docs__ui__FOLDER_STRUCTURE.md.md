---
title: "UI Folder Structure"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/ui/FOLDER_STRUCTURE.md"
source_ext: ".md"
category: "ui_docs"
source_size_bytes: "5019"
concepts:
  - "Execution"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# UI Folder Structure

**Source:** [[docs/ui/FOLDER_STRUCTURE|docs/ui/FOLDER_STRUCTURE.md]]

**Category:** `ui_docs`  
**Status:** ok  
**Size:** `5019` bytes

## خلاصه

Owns: replay controls replay speed cursor position frame stepping viewport synchronization Does not own: metric calculation node detection Owns: metric run selector metric parameter display metric event table metric overlays received from API Does not own: metric computation Owns: experiment list experiment details run status experiment outputs Does not own: experiment execution logic Owns: observation tree hypothesis tree experiment linkage validation linkage production signal linkage Owns: selected object details selected candle details selected event details selected node details source traceability React components: Hooks: API functions: Types: Backend schemas: If a future metric require

## Headings

- UI Folder Structure
-   Target Project Layout
-   Frontend Feature Boundaries
-     `features/replay`
-     `features/metrics`
-     `features/experiments`
-     `features/registry`
-     `features/inspector`
-   Naming Conventions
-   Rule

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/ui/README|Quant Lab UI Architecture]] — `ui_docs`
- [[docs/ui/ROADMAP|UI Implementation Roadmap]] — `ui_docs`
- [[docs/ui/VISUAL_REPLAY_PROTOCOL|Visual Replay Protocol]] — `ui_docs`
- [[docs/ui/VISUALIZATION_API|Visualization API Contract]] — `ui_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|04 Algorithms README]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/README|Flag Counting Engineering Pack V5]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/nds_hook_architecture/README|NDS Hook Architecture — Design Pack]] — `nds_hook_architecture_docs`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
