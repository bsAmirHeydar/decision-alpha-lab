---
title: "SYS-R01 — Final NDS Architecture and Build Order"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/experience_capture/questions/remaining_v3_split/SYS-R01/question_en.md"
source_ext: ".md"
category: "experience_capture_docs"
source_size_bytes: "1140"
concepts:
  - "Execution"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# SYS-R01 — Final NDS Architecture and Build Order

**Source:** [[docs/experience_capture/questions/remaining_v3_split/SYS-R01/question_en|docs/experience_capture/questions/remaining_v3_split/SYS-R01/question_en.md]]

**Category:** `experience_capture_docs`  
**Status:** ok  
**Size:** `1140` bytes

## خلاصه

چون بعد از ثبت ontology، سناریو، زون، ورود، ریسک، execution، data و AI باید ترتیب ساخت مشخص شود. بدون build order، پروژه سنگین و پراکنده می‌شود. اول object builderها ساخته شوند یا execution layer؟ Canonical State Packet قبل از AI لازم است؟ Event ledger قبل از training لازم است؟ Scenario/Zone/Entry layer قبل از backtest چطور ساخته شود؟ UI لازم است یا بعداً؟ Shadow/Paper/Live gate در چه مرحله‌ای می‌آید؟ کدام بخش‌ها hard rule هستند؟ کدام بخش‌ها trainable هستند؟ کدام بخش‌ها فعلاً فقط مستندسازی شوند؟ Roadmap نهایی ساخت سیستم چیست؟ خیر. پاسخ متنی کافی است. `nds_build_order_v1.csv` `system_architecture_v1.csv` `hard_rule_vs_trainable_policy_map_v1.csv` `deployment_roadmap_v1.csv`

## Headings

- SYS-R01 — Final NDS Architecture and Build Order
-   Purpose
-   Required Clarifications
-   Image Requirement
-   Expected Derived Outputs

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[docs/experience_capture/answers/DATA-R03/question_en|DATA-R03 — Layered Training, Knowledge Consolidation, and Training Granularity]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R01/question_en|ENT-R01 — Entry-Level Extreme Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R02/question_en|ENT-R02 — Limit Entry, Stop Geometry, and Practical Fill Policy]] — `experience_capture_docs`
- [[docs/experience_capture/answers/ENT-R03/question_en|ENT-R03 — Pending Limit Lifecycle: Cancel, Missed, Replace]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXE-R01/question_en|EXE-R01 — ExecutionIntent Contract Finalization]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-01/question_en|EXT-01 — How Exactly Is Extreme Defined Relative to an Untouched Node?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/EXT-09/question_en|EXT-09 — How Do You Understand the Quality of the Anchor Node?]] — `experience_capture_docs`
- [[docs/experience_capture/answers/NDS-R01/question_en|NDS-R01 — Canonical NDS Object Model]] — `experience_capture_docs`
- [[docs/experience_capture/answers/RSK-R01/question_en|RSK-R01 — Risk Budget Across Convex Opportunity Set]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R01/question_en|SCN-R01 — Context Power Scoring]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R02/question_en|SCN-R02 — Potential Zone Definition]] — `experience_capture_docs`
- [[docs/experience_capture/answers/SCN-R03/question_en|SCN-R03 — Scenario Ranking and Multi-Zone Selection]] — `experience_capture_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
