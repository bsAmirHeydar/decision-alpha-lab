---
title: "11 - Algorithm Layers"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/11_algorithm_layers.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "5282"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "Intermarket Divergence"
  - "Structural Nodes"
  - "Validation"
---


# 11 - Algorithm Layers

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/11_algorithm_layers|lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/11_algorithm_layers.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `5282` bytes

## خلاصه

This document decomposes the STC strategy into independent algorithms. Inputs: Broker server time. Broker UTC offset input. Optional UTC timestamps from external data. Outputs: New York timestamp. STC trading-day ID. M context. W context. Check-candle context. Hard-close status. Algorithm: 1. Convert all timestamps into UTC. 2. Convert UTC into New York time with DST support. 3. Compute STC trading-day start and end. 4. Reject signal processing outside the active STC day. 5. Assign M, W, gap, and check-candle state. Inputs: Symbol1 bars. Symbol2 bars. Expected interval. Outputs: Complete/incomplete flag. Missing count. Audit reason. Algorithm: 1. For each interval required by the signal engi

## Headings

- 11 - Algorithm Layers
-   Layer 1: Time normalization
-   Layer 2: Data completeness
-   Layer 3: W builder
-   Layer 4: Reference matrix
-   Layer 5: Hunt detector
-   Layer 6: SMT detector
-   Layer 7: Reference selector
-   Layer 8: Confirmation filter
-   Layer 9: Execution/risk
-   Layer 10: Position management
-   Layer 11: Persistence

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/19_patch_build_sequence|EXEC001 STC SMT Cycles — Patch Build Sequence]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/15_visualization_contract|15 - Visualization Contract]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/17_implementation_plan|EXEC001 STC SMT Cycles — Implementation Plan]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/18_module_breakdown|EXEC001 STC SMT Cycles — Module Breakdown]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/21_first_patch_scope|EXEC001 STC SMT Cycles — First Implementation Patch Scope]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/34_level_13_visualization_audit_drawing|Level 13 — Visualization / Audit Drawing]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/40_level_19_validation_pack|Level 19 — Validation Pack / Self-Test Reports]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/41_level_20_operator_manual_deployment_profiles|Level 20 — Operator Manual and Deployment Profiles]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/43_level_21_drawing_audit|Level 21 — Drawing Audit Hardening + HardClose Warning Fix]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/03_cycle_calendar|03 - Cycle Calendar and Time Model]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/06_mql5_architecture_plan|06 - MQL5 Architecture Plan]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
