---
title: "Label Stacking"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/flag_counting/engineering_pack_v5/05_visualization/LABEL_STACKING.md"
source_ext: ".md"
category: "flag_counting_docs"
source_size_bytes: "1801"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "Hook"
  - "NDS Anatomy"
---


# Label Stacking

**Source:** [[docs/flag_counting/engineering_pack_v5/05_visualization/LABEL_STACKING|docs/flag_counting/engineering_pack_v5/05_visualization/LABEL_STACKING.md]]

**Category:** `flag_counting_docs`  
**Status:** ok  
**Size:** `1801` bytes

## خلاصه

When all sequences are shown, label collision is unavoidable unless labels are stacked deterministically. Peak labels should be above peaks. Valley labels should be below valleys. This applies to F labels, internal numbers, ND labels, and origin markers when tied to a high/low node. Group labels by approximate chart location: Do not randomly offset each label. Near price to far from price: 1. older sequence first; 2. higher F-level first within same sequence age if needed; 3. confirmed before candidate; 4. ND/internal labels after owning F label unless specifically anchored to same node; 5. deterministic id as final tie-breaker. The user preference is: For a high/peak anchor: For a low/valle

## Headings

- Label Stacking
-   Purpose
-   Anchor Rule
-   Stack Buckets
-   Order Within Stack
-   Peak Placement
-   Valley Placement
-   Vertical Step
-   Avoid Huge Distance
-   Label Identity

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/flag_counting/engineering_pack_v5/05_visualization/OBJECT_NAMING_AND_LAYERS|Object Naming and Layers]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/05_visualization/DEBUG_VIEWS|Debug Views]] — `flag_counting_docs`
- [[docs/flag_counting/engineering_pack_v5/05_visualization/VISUAL_CONTRACT|Visual Contract]] — `flag_counting_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|Amir Structural Experience Map — نقشه تجربه‌های ساختاری امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|Experience Capture Log Template — قالب ثبت تجربه‌های امیر]] — `ai_execution_docs`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|Extreme L2 Node Cycle Limit Entry — تعریف رسمی اکستریم، نود L2 و ورود لیمیت]] — `ai_execution_docs`
- [[docs/ai_execution/README|AI Execution Docs]] — `ai_execution_docs`
- [[docs/debug/E0007/README|E0007 — Purple Source Extreme Executor Template]] — `debug_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
