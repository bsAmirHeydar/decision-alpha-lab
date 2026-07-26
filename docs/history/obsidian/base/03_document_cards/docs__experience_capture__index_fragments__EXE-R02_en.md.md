---
title: "Index Fragment — EXE-R02"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/index_fragments/EXE-R02_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "920"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Rally"
  - "Structural Nodes"
  - "Validation"
---


# Index Fragment — EXE-R02

**Source:** [[docs/experience_capture/index_fragments/EXE-R02_en|docs/experience_capture/index_fragments/EXE-R02_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `920` bytes

## خلاصه

Path: Summary: In NDS, broker validation and send-gate handling are mechanical execution constraints with clear deterministic rules. They do not belong to scenario, zone, entry, or AI reasoning. The broker validator should only check whether an ExecutionIntentCandidate is mechanically valid for the broker, normalize prices and volumes when safe, split or adjust only when structural meaning is preserved, and veto when broker constraints would make the intent unsafe or structurally invalid. Main derived architecture requirements:

## Headings

- Index Fragment — EXE-R02
-   EXE-R02 — Broker Validator and Send Gate

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/experience_capture/questions/remaining_v2/by_code/EXE-R02|EXE-R02 — Pending Order Cancel and Replace Policy]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/ENT-R01_en|Index Fragment — ENT-R01]] — `experience_capture_docs`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI Algorithm Layer Map for Extreme Engine — نقشه الگوریتم‌های هوش مصنوعی برای اکستریم L2]] — `ai_execution_docs`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI Native Execution Roadmap — نقشه راه هوش مصنوعی، بک‌تست و پل اگزکیوت]] — `ai_execution_docs`
- [[docs/ai_execution/EXTREME_L2_NODE_CYCLE_LIMIT_ENTRY_FA|Extreme L2 Node Cycle Limit Entry — تعریف رسمی اکستریم، نود L2 و ورود لیمیت]] — `ai_execution_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/answers/BASE-02/answer_normalized_en|BASE-02 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-02/notes_en|BASE-02 — Notes and Open Questions]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-04/answer_normalized_en|BASE-04 — Normalized Interpretation]] — `experience_capture_docs`
- [[docs/experience_capture/answers/BASE-05/answer_normalized_en|BASE-05 — Normalized Interpretation]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
