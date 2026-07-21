
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/37_level_16_real_auto_entry_router.md"
source_ext: ".md"
source_size: 6665
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — 37_level_16_real_auto_entry_router.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/37_level_16_real_auto_entry_router|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/37_level_16_real_auto_entry_router.md]]

## Summary

Level 16 is the first layer that can convert an already-confirmed STC SMT signal into a real broker entry order. It does not change the strategy logic. It only mirrors the Level 08 paper entry geometry into broker orders… The layer remains disabled by default. The router preserves the existing STC rules: the EA uses only `Symbol1` and `Symbol2`; the chart symbol does not drive the strategy; SMT is structural per symbol; high-side SMT maps to a sell on the clean symbol; low-side SMT maps to a buy on the clean symbol; entry is attempted only at the next check-candle open after signal confirmation; no delayed entry is allowed after the grace window expires; Entry STC OFF creates audit rows only and no later real entry; simultaneous buy and sell in one check candle is forgotten; each M cycle allows at most three real entries across both symbols; with hedging OFF, direction lock applies only

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Level 16 — Real Auto Entry Router
  - Status
  - Non-negotiable locked rules preserved
  - What Level 16 adds
  - Safety gates
  - New inputs
  - Split order behavior
  - Real order geometry
  - No late entry rule
  - Output
  - Acceptance criteria
  - Still deferred

## Related Source Documents

- [signals.yaml](../../registry/signals.yaml) — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03_cycle_calendar.md]] — score `11`
- [[docs/evidence/05_execution_risk_position_management_outcomes/e6e53a81ed12_05_execution_and_risk|05_execution_and_risk.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06_mql5_architecture_plan.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/13_data_model_and_journals|13_data_model_and_journals.md]] — score `11`
- [[docs/evidence/16_implementation_checklist/29731b650a84_16_implementation_checklist|16_implementation_checklist.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `11`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `11`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|21_first_patch_scope.md]] — score `11`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
