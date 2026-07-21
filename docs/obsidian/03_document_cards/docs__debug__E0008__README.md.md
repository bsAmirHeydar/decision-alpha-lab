---
title: "E0008 — MTF Purple Extreme Executor"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/E0008/README.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "5482"
entities:
  - "E0007"
  - "E0008"
  - "M0001"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Structural Nodes"
---


# E0008 — MTF Purple Extreme Executor

**Source:** [[docs/debug/E0008/README|docs/debug/E0008/README.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `5482` bytes

## خلاصه

E0008 is the execution template that matches the user objective more directly than E0007: > We do not want every purple zone. > We want purple/source zones that sit inside the correct higher-timeframe context and give a tiny local stop with 50R/100R path potential. Default stack: The default `L=2` is intentional because the purple screenshots were generated with L=2. Each context timeframe builds M0001 node/zone events and searches for a source-like event: This is not yet a full human-grade hook engine, but it is the first testable proxy: No future survival label is required. Oracle/research mode: only zones that already survived 500 bars are used. This is for reverse engineering and must no

## Headings

- E0008 — MTF Purple Extreme Executor
-   Architecture
-   What counts as context
-   Live mode vs oracle purple research
-   Entry modes
-     MICRO_NODE_REVISIT
-     LOCAL_SOURCE_REVISIT
-     LOCAL_SECONDARY_NODE
-     EARLY_LADDER_STEP
-   Stop modes
-   Target modes
-   Suggested tests

## Entities

`E0007`, `E0008`, `M0001`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]

## Related documents

- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|VAL0022 — H6 Reaction Box Zones]] — `validation`
- [[docs/debug/E0007/README|E0007 — Purple Source Extreme Executor Template]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|EXE0001 — H0005 Reversal Fixed-R Executor]] — `execution`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|EXE0002 — Close-Confirmed Market After Touch]] — `execution`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|EXE0003 — Continuation Close-Hunt Market Execution]] — `execution`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_validation/VAL0024_e7_purple_source_extreme/README|VAL0024 — E0007 Purple Source Extreme Execution Validation]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
