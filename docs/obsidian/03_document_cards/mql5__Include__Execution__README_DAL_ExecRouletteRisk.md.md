---
title: "DAL_ExecRouletteRisk — Roulette Execution Risk Model"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "mql5/Include/Execution/README_DAL_ExecRouletteRisk.md"
source_ext: ".md"
category: "mql5_docs"
source_size_bytes: "4243"
concepts:
  - "Execution"
  - "MQL Native"
  - "NDS Anatomy"
---


# DAL_ExecRouletteRisk — Roulette Execution Risk Model

**Source:** [[mql5/Include/Execution/README_DAL_ExecRouletteRisk|mql5/Include/Execution/README_DAL_ExecRouletteRisk.md]]

**Category:** `mql5_docs`  
**Status:** ok  
**Size:** `4243` bytes

## خلاصه

`DAL_ExecRouletteRisk` is a reusable MQL5 execution-risk module. It returns **money risk** only. It does not send orders, decide entries, or decide exits. Each cycle stores: Default inputs: At cycle start: Example: If the account moves down but stays inside the protected band: risk remains fixed: Example: The risk does not shrink on every small loss. If balance breaks below the protected floor, the base account used for lot calculation must update downward. Rule: Example: The cycle re-locks: This is the corrected rule: the base does not follow every loss, but it does follow the account down after the protected floor is broken. The cycle becomes profit-active only after balance rises above th

## Headings

- DAL_ExecRouletteRisk — Roulette Execution Risk Model
-   Core state
-   Losing-side floor band
-   Downside floor break
-   Profit-active rule
-   Profit cluster then loss re-lock
-   Final behavior summary
-   Safety contract

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0012_distributional_cluster_miner/README|EXP0012 — Distributional Cluster Miner]] — `experiment`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0014_ICT/README|EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/validation_cases/README|Phoenix Flag Counting Validation Cases]] — `experiment`
- [[lab/03_validation/VAL0006_h5_live_touch_replay/README|VAL0006 — H5 live-valid touch-entry replay]] — `validation`
- [[lab/03_validation/VAL0008_h4_causal_batch/README|VAL0008 — H4 Causal Batch Validation]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
