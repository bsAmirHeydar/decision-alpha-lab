
---
type: source_card
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope.md"
source_ext: ".md"
source_size: 3223
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Execution / Risk", "Intermarket Divergence", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: ["EXEC001"]
---

# Source Card — 21_first_patch_scope.md

## Source

[[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope.md]]

## Summary

This document defines the exact scope of the first code patch. The first patch must create a stable execution shell only. It must not implement SMT logic. Create a compilable MQL5 Expert Advisor and include structure that can host the STC SMT Cycles engine. The first patch should prove that the project structure, inputs, timer loop, symbol handling, runtime modes, output folder setup, and build sanity logs are stable. `mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5` `mql5/Include/IntermarketDivergenceExecution/STC/` `DAL_STC_Enums.mqh` `DAL_STC_Types.mqh` `DAL_STC_Config.mqh` `DAL_STC_Utils.mqh` `DAL_STC_Journal.mqh` minimal stub `DAL_STC_Engine.mqh` minimal no-op engine Core inputs: `InpSymbol1` `InpSymbol2` `InpRuntimeMode` `InpEntrySTC` `InpPartial` `InpHedging` `InpFinalReward` `InpRiskPercent` `InpCandleCheckMinutes` `InpContractSize` `InpBrokerUtcOffsetHo

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

EXEC001

## Headings

- EXEC001 STC SMT Cycles — First Implementation Patch Scope
  - 1. Objective
  - 2. Files to Add
    - Expert
    - Include Directory
    - Include Files
  - 3. Inputs to Add
  - 4. Runtime Modes
  - 5. Build Sanity Log
  - 6. Validation Logic
  - 7. Timer Loop
  - 8. Output Folders

## Related Source Documents

- [[docs/evidence/exec001_stc_smt_cycles_implementation_plan/0d054880f96a_17_implementation_plan|17_implementation_plan.md]] — score `20`
- [[docs/evidence/exec001_stc_smt_cycles_module_breakdown/0e4565d59512_18_module_breakdown|18_module_breakdown.md]] — score `20`
- [[docs/evidence/exec001_stc_smt_cycles_build_sequence/f494e5d7db74_19_patch_build_sequence|19_patch_build_sequence.md]] — score `20`
- [[docs/evidence/level_13_visualization_audit_drawing/b5b7350fdc84_34_level_13_visualization_audit_drawing|34_level_13_visualization_audit_drawing.md]] — score `20`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|README.md]] — score `20`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `19`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/22_level_01_skeleton|22_level_01_skeleton.md]] — score `18`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/35_level_14_paper_live_alerts|35_level_14_paper_live_alerts.md]] — score `18`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|40_level_19_validation_pack.md]] — score `18`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
