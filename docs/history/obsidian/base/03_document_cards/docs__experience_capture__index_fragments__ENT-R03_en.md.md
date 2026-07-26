---
title: "Index Fragment — ENT-R03"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/index_fragments/ENT-R03_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "951"
concepts:
  - "Convexity"
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# Index Fragment — ENT-R03

**Source:** [[docs/experience_capture/index_fragments/ENT-R03_en|docs/experience_capture/index_fragments/ENT-R03_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `951` bytes

## خلاصه

Path: Summary: In NDS, a pending limit order remains alive only while the reasons that created that trade remain valid. The order is bound to its scenario, zone, entry-level Extreme, reference node, destination, convexity profile, and risk geometry. If those reasons remain intact, the pending order can stay alive. If the reasons are invalidated, the order must be deleted or canceled. This makes pending limit lifecycle a structural reason-integrity problem rather than an arbitrary time-expiration problem. Main derived architecture requirements:

## Headings

- Index Fragment — ENT-R03
-   ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/architecture|System Architecture]] — `core_docs`
- [[docs/experience_capture/questions/remaining_v2/by_code/ENT-R03|ENT-R03 — Higher-Timeframe F3 / Lower-Timeframe 3F Reversal]] — `experience_capture_docs`
- [[docs/ui/ARCHITECTURE|UI System Architecture]] — `ui_docs`
- [[docs/experience_capture/index_fragments/ENT-R01_en|Index Fragment — ENT-R01]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/RSK-R01_en|Index Fragment — RSK-R01]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/RSK-R02_en|Index Fragment — RSK-R02]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/SCN-R02_en|Index Fragment — SCN-R02]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/SCN-R03_en|Index Fragment — SCN-R03]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/DATA-R03_en|Index Fragment — DATA-R03]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/ENT-R04_en|Index Fragment — ENT-R04]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/EXE-R01_en|Index Fragment — EXE-R01]] — `experience_capture_docs`
- [[docs/experience_capture/index_fragments/EXE-R02_en|Index Fragment — EXE-R02]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
