---
title: "Alpha Lab Command Center"
type: dashboard
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
status: "active"
---

# Alpha Lab Command Center

این صفحه کنترل پنل انسانی پروژه در Obsidian است: نقشه سریع، مسیر تحقیق، مسیر اجرا، و نقاطی که Agent آینده باید از آنها استفاده کند.

## وضعیت کلی

| بخش | تعداد |
|---|---:|
| اسناد indexed | 862 |
| کارت‌های document تولیدشده | 862 |
| entityهای شناسایی‌شده | 79 |
| conceptهای شناسایی‌شده | 15 |
| registry / metadata YAML | 24 |

## Breakdown by category

| Category | Documents |
|---|---:|
| experience_capture_docs | 265 |
| flag_counting_docs | 144 |
| experiment | 130 |
| mql_native_docs | 72 |
| nds_hook_architecture_docs | 44 |
| core_docs | 36 |
| execution_docs | 31 |
| debug_docs | 29 |
| validation | 24 |
| hypothesis | 14 |
| execution | 10 |
| mql5_docs | 7 |
| ai_execution_docs | 6 |
| tool_docs | 6 |
| ui_docs | 6 |
| infrastructure | 5 |
| analysis | 4 |
| core_component | 4 |
| research_docs | 4 |
| archive | 3 |
| article_docs | 3 |
| documentation | 3 |
| monitoring | 2 |
| paper | 2 |
| production_signal | 2 |
| readme | 2 |
| report | 2 |
| data_docs | 1 |
| license_docs | 1 |

## Navigation

- [[docs/obsidian/01_maps/all_documents_index|All Documents Index]] — فهرست کامل فایل‌ها.
- [[docs/obsidian/01_maps/all_document_relationships|All Document Relationships]] — روابط اتوماتیک document-to-document.
- [[docs/obsidian/01_maps/entity_index|Entity Index]] — H/EXP/VAL/M/CP/SIG/MON/EXE.
- [[docs/obsidian/01_maps/concept_index|Concept Index]] — Hook، Rally، F-counting، Known-Time، Atomic No-Sample و غیره.
- [[docs/obsidian/01_maps/registry_index|Registry Index]] — رجیستری‌ها و metadataهای YAML.
- [[docs/obsidian/01_maps/empty_docs_audit|Empty Docs Audit]] — فایل‌هایی که خالی بودند و با scaffold پر شدند.

## Research pipeline

```mermaid
graph LR
    OBS[Observation] --> HYP[Hypothesis]
    HYP --> EXP[Experiment]
    EXP --> ANL[Analysis]
    ANL --> VAL[Validation]
    VAL --> PROD[Production Signal]
    PROD --> MON[Monitoring]
    MON --> ARCH[Archive / Retirement]
```

## Core architecture links

- [[docs/manifesto|Manifesto]]
- [[docs/principles|Research Principles]]
- [[docs/glossary|Glossary]]
- [[docs/laboratory_architecture|Laboratory Architecture]]
- [[docs/architecture|Architecture]]
- [[docs/research-roadmap|Research Roadmap]]

## High-priority specialist maps

- [[docs/obsidian/02_mocs/flag_counting_moc|Flag Counting / F-Counting MOC]]
- [[docs/obsidian/02_mocs/nds_hook_architecture_moc|NDS Hook Architecture MOC]]
- [[docs/obsidian/02_mocs/mql_native_moc|MQL Native MOC]]
- [[docs/obsidian/02_mocs/ai_execution_moc|AI Execution / Agent MOC]]
- [[docs/obsidian/02_mocs/experiment_validation_moc|Experiment + Validation MOC]]
