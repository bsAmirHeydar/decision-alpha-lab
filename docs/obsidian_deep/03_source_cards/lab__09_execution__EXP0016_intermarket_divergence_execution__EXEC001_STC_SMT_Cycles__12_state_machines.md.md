
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines.md"
source_ext: ".md"
source_size: 2992
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 12_state_machines.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/12_state_machines.md]]

## Summary

States: `BEFORE_STC_DAY` `ACTIVE_DAY` `HARD_CLOSE_DUE` `HARD_CLOSE_RECOVERY` `DAY_RESET_DONE` Transitions: At 20:00 New York, enter `ACTIVE_DAY`. At 15:30 New York, enter `HARD_CLOSE_DUE`. If all STC positions close successfully, enter `DAY_RESET_DONE`. If any close fails or EA restarts after 15:30 with open STC positions, enter `HARD_CLOSE_RECOVERY`. After successful recovery, reset state for next day. States: `NOT_STARTED` `ACTIVE` `GAP_AFTER_M` `ENDED` M state carries: M ID. Trade count. Direction lock. Opened trade IDs. Partial due time. On M start: Trade count = 0. Direction lock = none. On first opened trade when Hedging OFF: Direction lock = trade side. On M end: No more entries allowed. Partial may become due for M1/M2. M3 hands control to hard close. States: `BUILDING` `COMPLETED` `REFERENCE_ELIGIBLE` `CURRENT_W` W1 never signals. W2/W3/W4 can be current W for candidate detectio

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- 12 - State Machines
  - 1. Strategy day state
  - 2. M state
  - 3. W state
  - 4. Candidate state
  - 5. Trade state
  - 6. Partial state
  - 7. Hard-close state

## Related Source Documents

- [signals.yaml](../../registry/signals.yaml) — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/02_normalized_strategy_spec|02_normalized_strategy_spec.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03_cycle_calendar.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/04_smt_divergence_rules|04_smt_divergence_rules.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/05_execution_and_risk|05_execution_and_risk.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/07_test_plan|07_test_plan.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/09_owner_decisions_pass_1|09_owner_decisions_pass_1.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/11_algorithm_layers|11_algorithm_layers.md]] — score `9`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals|13_data_model_and_journals.md]] — score `9`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
