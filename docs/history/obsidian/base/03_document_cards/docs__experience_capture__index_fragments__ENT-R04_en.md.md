---
title: "Index Fragment — ENT-R04"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/index_fragments/ENT-R04_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1090"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# Index Fragment — ENT-R04

**Source:** [[docs/experience_capture/index_fragments/ENT-R04_en|docs/experience_capture/index_fragments/ENT-R04_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1090` bytes

## خلاصه

Path: Summary: After a limit entry is filled, the trade becomes an active PositionThread linked to the same scenario, zone, entry extreme, and reason set that created it. While that position is open, the system must not take another duplicate trade with the same reasons. The reason set is locked to the open position until the position is closed or completed. Exits can occur in multiple places according to NDS exit and destination logic. Hedging is a separate topic because it requires separate entry logic and should not be automatically triggered by the existence of an active position or an opposite scenario. Main derived architecture requirements:

## Headings

- Index Fragment — ENT-R04
-   ENT-R04 — After Fill: Scenario-to-Position Transition

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R04|ENT-R04 — Post-F1 Continuation Entry]] — `experience_capture_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/experience_capture/index_fragments/DATA-R03_en|Index Fragment — DATA-R03]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/ENT-R01_en|Index Fragment — ENT-R01]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/ENT-R03_en|Index Fragment — ENT-R03]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/EXE-R01_en|Index Fragment — EXE-R01]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/EXE-R02_en|Index Fragment — EXE-R02]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/RSK-R01_en|Index Fragment — RSK-R01]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/RSK-R02_en|Index Fragment — RSK-R02]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/SCN-R02_en|Index Fragment — SCN-R02]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/SCN-R03_en|Index Fragment — SCN-R03]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
