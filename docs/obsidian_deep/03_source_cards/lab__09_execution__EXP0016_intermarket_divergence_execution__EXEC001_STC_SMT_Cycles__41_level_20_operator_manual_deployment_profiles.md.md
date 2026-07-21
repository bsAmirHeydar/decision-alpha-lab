
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles.md"
source_ext: ".md"
source_size: 9925
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "Intermarket Divergence", "Licensing", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: []
---

# Source Card — 41_level_20_operator_manual_deployment_profiles.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles.md]]

## Summary

Level 20 is a documentation and deployment-control layer for `EXEC001_STC_SMT_Cycles`. It does not add new signal logic, does not change SMT detection, does not change risk geometry, does not change paper outcomes, and does not send broker orders by itself. Its purpose is to make the existing Level 01 thro… The strategy now has many independent safety switches. That is intentional, but it also means the operator needs a precise runbook. Level 20 defines that runbook. The STC strategy is not a simple indicator. It contains: New York time conversion. STC trading-day state. M/W cycle classification. Check-candle aggregation. W high/low construction. Previous-W reference matrix. Touch-only hunt detection. SMT candidate generation. Signal confirmation and consumption. No-late-entry protection. Paper entry and risk modeling. Paper outcome simulation. Paper partial and hard-close simulation. Re

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

—

## Headings

- Level 20 — Operator Manual and Deployment Profiles
  - Scope
  - Why this layer exists
  - Canonical operating principle
    - 1. Research layer
    - 2. Paper-live layer
    - 3. Auto-trade layer
  - Golden rules
  - Deployment readiness gates
  - Runtime modes
    - Research Backtest
    - Paper Live

## Related Source Documents

- [[docs/evidence/level_20_deployment_profile_matrix/97ecd654ebb6_42_level_20_profile_matrix|42_level_20_profile_matrix.md]] — score `21`
- [[docs/evidence/val_m0001_mql_native/454e81f9f0b3_report|report.md]] — score `18`
- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `17`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `17`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|README.md]] — score `17`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `16`
- [[docs/flag_counting/README|README.md]] — score `16`
- [[mql5/Include/FlagCountingPhoenix/README_FlagCountingPhoenix|README_FlagCountingPhoenix.md]] — score `16`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `16`
- [signals.yaml](../../registry/signals.yaml) — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
