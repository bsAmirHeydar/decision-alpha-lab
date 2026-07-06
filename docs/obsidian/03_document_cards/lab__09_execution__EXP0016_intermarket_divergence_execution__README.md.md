---
title: "EXP0016 Intermarket Divergence Execution"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/README.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "1089"
entities:
  - "EXEC001"
  - "EXP0016"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Validation"
---


# EXP0016 Intermarket Divergence Execution

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/README|lab/09_execution/EXP0016_intermarket_divergence_execution/README.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `1089` bytes

## خلاصه

This experiment group contains execution models built on intermarket divergence. The first execution model is: `EXEC001_STC_SMT_Cycles` EXEC001 is now documented as a locked, layered, English specification. It is ready for research/paper implementation. `EXEC001_STC_SMT_Cycles/` - STC SMT cycle strategy from the provided SRS and owner clarifications. Although the current implementation target is EXEC001 only, the folder is organized so future divergence execution strategies can reuse the same architectural ideas: Source SRS extraction. Normalized specification. Cycle calendar. Divergence rules. Execution and risk rules. Architecture plan. Test plan. Data model and journals. Visualization con

## Headings

- EXP0016 Intermarket Divergence Execution
-   Strategy folders
-   Common principles
-   Current build order

## Entities

`EXEC001`, `EXP0016`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/README|EXEC001 STC SMT Cycles — Deployment Profiles]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|Offline License Layer - EXEC001 STC SMT Cycles]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[tools/astro_ml/README|Astro ML Tools]] — `tool_docs`
- [[mql5/Experts/IntermarketDivergenceExecution/README|Intermarket Divergence Execution Experts]] — `mql5_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/experience_capture/questions/remaining_v2/sections/02_context_zone_destination/README|Context, Zone, Destination, and Invalidation]] — `experience_capture_docs`
- [[docs/flag_counting/engineering_pack_v5/04_algorithms/README|04 Algorithms README]] — `flag_counting_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
