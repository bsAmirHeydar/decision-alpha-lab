
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/25_level_04_w_level_builder.md"
source_ext: ".md"
source_size: 3318
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 25_level_04_w_level_builder.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/25_level_04_w_level_builder|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/25_level_04_w_level_builder.md]]

## Summary

Level 04 adds the first structural market object required by STC: the closed 90-minute W high/low levels for both symbols. This level is still non-trading. It does not detect SMT, confirm signals, simulate entries, draw objects, open positions, partial-close positions, or hard-close positions. It only builds and audits W levels after each W… STC does not compare raw prices between SPX and NDX. It compares each symbol against its own W reference levels. Therefore the system needs a deterministic W-level layer before SMT can exist. The locked owner rule is: each symbol has its own W high and W low; the comparison is structural, not price-shared; W1 gives no signal; W2 may later compare only with W1; W3 may later compare with W2 and W1; W4 may later compare with W3, W2 and W1; no W compares with itself; W high/low is the high/low of the whole 90-minute synthetic candle; the construction tim

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Level 04 — W Level Builder
  - Status
  - Why this level exists
  - Output file
  - W serial map
  - Completeness rule
  - Reference role
  - Level 04 acceptance criteria

## Related Source Documents

- [signals.yaml](../../registry/signals.yaml) — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03_cycle_calendar.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/05_execution_and_risk|05_execution_and_risk.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals|13_data_model_and_journals.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/16_implementation_checklist|16_implementation_checklist.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|17_implementation_plan.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|18_module_breakdown.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|19_patch_build_sequence.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
