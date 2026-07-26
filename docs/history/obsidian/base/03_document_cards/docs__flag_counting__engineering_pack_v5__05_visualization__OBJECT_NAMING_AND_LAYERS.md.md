---
title: "Object Naming and Layers"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/05_visualization/OBJECT_NAMING_AND_LAYERS.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "1478"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
  - "Validation"
---


# Object Naming and Layers

**Source:** [[docs/flag_counting/engineering_pack_v5/05_visualization/OBJECT_NAMING_AND_LAYERS|docs/flag_counting/engineering_pack_v5/05_visualization/OBJECT_NAMING_AND_LAYERS.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `1478` bytes

## خلاصه

Chart objects must be deletable, refreshable, and traceable. Never create anonymous trendlines. Use one prefix for all Flag Counting objects: Recommended draw order: 1. historical/locked F3 extension background arcs; 2. ND/Hook arcs; 3. flag body lines; 4. origin markers; 5. internal numbers; 6. F labels; 7. panel/status objects. Default: Avoid scale-based thickness by default. Use deterministic shade from sequence id: Use shade inside semantic color family. Renderer receives current render object ids. On refresh: 1. build set of desired object names; 2. update/create desired objects; 3. delete old FCN_ objects not desired unless locked persistence requires retention; 4. never delete non-FCN

## Headings

- Object Naming and Layers
-   Naming Goals
-   Prefix
-   Suggested Names
-   Layer Order
-   Width
-   Shades
-   Stale Object Cleanup
-   Locked Persistence
-   Tooltip / Description

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/05_visualization/DEBUG_VIEWS|Debug Views]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-06/answer_normalized_en|BASE-06 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/answer_normalized_en|EXT-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|NDS-R01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/notes_en|NDS-R01 — Notes and Open Questions]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
