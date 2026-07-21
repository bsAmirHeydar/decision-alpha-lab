---
title: "Level 06 — SMT Candidate Engine"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/evidence/level_06_smt_candidate_engine/97fffdd7f422_27_level_06_smt_candidate_engine.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "6096"
concepts:
  - "Execution"
  - "Intermarket Divergence"
  - "Known-Time Causality"
  - "Validation"
---


# Level 06 — SMT Candidate Engine

**Source:** [[docs/evidence/level_06_smt_candidate_engine/97fffdd7f422_27_level_06_smt_candidate_engine|docs/evidence/level_06_smt_candidate_engine/97fffdd7f422_27_level_06_smt_candidate_engine.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `6096` bytes

## خلاصه

Status: implemented as an audit-only layer. Level 06 converts the raw hunt material from Level 05 into explicit SMT candidate rows. It still does not confirm signals, consume signals, simulate entries, open positions, draw objects, or manage trades. The output of this level is a deterministic candidate audit table that later levels can use for confirmation, signal registry, paper execution, and auto-trading. Level 06 is responsible for these operations: 1. Read the closed check-candle context from the Level 03 aggregator. 2. Rebuild the legal previous-W reference set from Level 05. 3. Read raw high/low hunt patterns for every legal reference. 4. Convert exactly-one high hunts into sell-side

## Headings

- Level 06 — SMT Candidate Engine
-   Scope
-   Non-scope
-   Candidate conversion rules
-     High-side SMT
-     Low-side SMT
-   Same-check ambiguity rule
-   Reference selection rule
-   Multiple same-direction candidates
-   Candidate identity
-   Output
-   Expected outputs after attach

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|EXEC001 STC SMT Cycles — Module Breakdown]] — `experiment`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_risk_register/b5f9b48975ee_20_implementation_risk_register|EXEC001 STC SMT Cycles — Implementation Risk Register]] — `experiment`
- [[docs/evidence/02_normalized_strategy_specification/4b26d8673556_02_normalized_strategy_spec|02 - Normalized Strategy Specification]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[docs/evidence/04_smt_divergence_rules_algorithms/5dba5ebb5e42_04_smt_divergence_rules|04 - SMT Divergence Rules and Algorithms]] — `experiment`
- [[docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk|05 - Execution, Risk, Position Management, and Outcomes]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06 - MQL5 Architecture Plan]] — `experiment`
- [[docs/evidence/07_test_plan/ad357cabb5f5_07_test_plan|07 - Test Plan]] — `experiment`
- [[docs/evidence/08_open_questions/18e20583bb82_08_open_questions|08 - Open Questions]] — `experiment`
- [[docs/evidence/09_owner_decisions_pass_1/d64c20e06d5e_09_owner_decisions_pass_1|09 - Owner Decisions Pass 1]] — `experiment`
- [[docs/evidence/11_algorithm_layers/07355f60fef2_11_algorithm_layers|11 - Algorithm Layers]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
