---
title: "Visual Contract"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/05_visualization/VISUAL_CONTRACT.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "2051"
concepts:
  - "AI Agent Layer"
  - "F-Counting"
  - "Hook"
  - "NDS Anatomy"
---


# Visual Contract

**Source:** [[docs/flag_counting/engineering_pack_v5/05_visualization/VISUAL_CONTRACT|docs/flag_counting/engineering_pack_v5/05_visualization/VISUAL_CONTRACT.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `2051` bytes

## خلاصه

Renderer receives render model objects: It does not receive raw bars to infer structures. A flag body uses two visual pieces: All flag lines are thin by default. Do not make larger scale lines thick by default. Use label and shade, not width. The curve must not look like broken angular trendlines. Implementation options: polyline sampled from quadratic Bezier through Waist; arc-like curve with enough sample points; platform curve object if available and stable. Minimum visual rule: The curve does not need to follow every candle. It must show body logic. ND/Hook uses gray arc/semicircle. Do not draw the 50% line by default. Show `O` by default during research. Input: Research default uses det

## Headings

- Visual Contract
-   Rendering Inputs
-   Flag Body Rendering
-   Smooth Arc Requirement
-   ND / Hook Rendering
-   Origin Marker
-   Labels
-   Colors
-   Main Chart Defaults
-   Fidelity Rule

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/05_visualization/DEBUG_VIEWS|Debug Views]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/05_visualization/OBJECT_NAMING_AND_LAYERS|Object Naming and Layers]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/05_visualization/LABEL_STACKING|Label Stacking]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/ai_execution/README|AI Execution Docs]] — `ai_execution_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/answers/BASE-01/answer_normalized_en|BASE-01 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
