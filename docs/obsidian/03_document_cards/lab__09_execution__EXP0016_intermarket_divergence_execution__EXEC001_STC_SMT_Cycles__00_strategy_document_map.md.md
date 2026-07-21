---
title: "00 - Strategy Document Map"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/00_strategy_document_map/7a03efa653e6_00_strategy_document_map.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "2349"
entities:
  - "EXEC001"
concepts:
  - "Convexity"
  - "Execution"
  - "Intermarket Divergence"
---


# 00 - Strategy Document Map

**Source:** [[docs/evidence/00_strategy_document_map/7a03efa653e6_00_strategy_document_map|docs/evidence/00_strategy_document_map/7a03efa653e6_00_strategy_document_map.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `2349` bytes

## خلاصه

This document explains the documentation layers for EXEC001 STC SMT Cycles. STC is not only a signal rule. It is a full execution model that combines time, cycles, two-symbol SMT, confirmation candles, risk sizing, partial management, hard close, restart recovery, and duplicate-instance safety. A single README would become ambiguous. Therefore the strategy is split into layers: 1. Source traceability. 2. Normalized strategy rules. 3. Time and cycle model. 4. SMT divergence model. 5. Execution and risk model. 6. Engineering architecture. 7. Test plan. 8. Persistence and journals. 9. Visualization. 10. Implementation checklist. Each layer should be implementable and testable by itself. Start w

## Headings

- 00 - Strategy Document Map
-   Why this strategy is documented in layers
-   Reading order
-   Source hierarchy
-   What is locked
-   What can still be configured as research knobs

## Entities

`EXEC001`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]

## Related documents

- [[docs/evidence/11_algorithm_layers/07355f60fef2_11_algorithm_layers|11 - Algorithm Layers]] — `experiment`
- [[docs/evidence/02_normalized_strategy_specification/4b26d8673556_02_normalized_strategy_spec|02 - Normalized Strategy Specification]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[docs/evidence/04_smt_divergence_rules_algorithms/5dba5ebb5e42_04_smt_divergence_rules|04 - SMT Divergence Rules and Algorithms]] — `experiment`
- [[docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk|05 - Execution, Risk, Position Management, and Outcomes]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines|12 - State Machines]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals|13 - Data Model and Journals]] — `experiment`
- [[docs/evidence/14_backtest_live_runtime/c31f0574e3ec_14_backtest_live_runtime|14 - Backtest and Live Runtime]] — `experiment`
- [[docs/evidence/16_implementation_checklist/29731b650a84_16_implementation_checklist|16 - Implementation Checklist]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[docs/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/README|EXEC001 STC SMT Cycles — Deployment Profiles]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
