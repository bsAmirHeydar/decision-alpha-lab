
---
type: source_card
source_path: "docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md"
source_ext: ".md"
source_size: 21545
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Flag Counting", "Hook", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0007"]
---

# Source Card — 16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md

## Source

[[docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX|docs/flag_counting/implementation_ladder_v1/16_IMPLEMENTATION_ORDER_AND_ACCEPTANCE_MATRIX.md]]

## Summary

This document is part of the implementation ladder for the Phoenix Flag Counting engine. Global non-negotiables: All structural decisions use candle `high` and `low` only. `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs. Equality is not a break. A level is broken only by a strict pass beyond it. The renderer is non-authoritative. It may only draw logical objects emitted by engines. Main-chart rendering and audit rendering are separate products. Every layer must expose enough audit fields to prove why an object exists. A higher layer may never silently repair a lower-layer defect. This file is the execution checklist. It prevents jumping into renderer or broad Hook/F lifecycle patches before foundations are locked. The current decision source is: Files: Acceptance: active implementation path is Phoenix only; VNext/V6/M0007 marked legacy/referen

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Flag_Counting|Flag Counting]], [[docs/obsidian_deep/02_concepts/Hook|Hook]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0007

## Headings

- Phoenix Flag Counting Implementation Ladder V1
- Implementation Order and Acceptance Matrix
  - Purpose
  - Order
    - Step 00 — Freeze current canon
    - Step 01 — Freeze Level 01 candle stream and timebase
    - Step 01.5 — Freeze types and config
    - Step 02 — Freeze NodeEngine
    - Step 03 — Freeze identity layer
    - Step 04 — Build Hook/ND audit only
    - Step 05 — Build flag body audit only
    - Step 06 — Build internal count audit only

## Related Source Documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `35`
- [[docs/flag_counting/README|README.md]] — score `35`
- [[docs/debug/MARKET_LANGUAGE/README|README.md]] — score `29`
- [[lab/03_experiments/EXP_flag_counting/README|README.md]] — score `29`
- [[docs/flag_counting/implementation_ladder_v1/README|README.md]] — score `29`
- [[docs/flag_counting/VALIDATION_CASE_REGISTRY|VALIDATION_CASE_REGISTRY.md]] — score `28`
- [[docs/flag_counting/implementation_ladder_v1/11_5_LEVEL_11_5_RAW_AUDIT_EXPORT|11_5_LEVEL_11_5_RAW_AUDIT_EXPORT.md]] — score `27`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `25`
- [[docs/debug/E0008/README|README.md]] — score `24`
- [[docs/experience_capture/questions/README|README.md]] — score `24`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
