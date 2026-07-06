---
title: "Offline License Layer - EXEC001 STC SMT Cycles"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "1497"
entities:
  - "EXEC001"
  - "EXP0015"
concepts:
  - "Execution"
  - "F-Counting"
  - "Intermarket Divergence"
  - "Licensing"
  - "MQL Native"
  - "Validation"
---


# Offline License Layer - EXEC001 STC SMT Cycles

**Source:** [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `1497` bytes

## خلاصه

This patch ports the FlagCounting Phoenix offline-license architecture to the divergence / time-cycle execution project. The license is intentionally exposed as neutral strategy/profile fields: By default, the issuer archive is written under: The recipient only receives the `*_recipient_inputs.txt` values. The `*_issuer_audit.json` and `*_full_record.txt` files stay private. `IMDEXEC001_STC_SMT_Cycles.mq5` checks the license before `g_stc_engine.Init()` and before every timer pulse. The two EXP0015 research wrappers check the same license before batch/live-monitor execution. If the license is absent, expired, copied to another account/server, or has wrong gates/signature, init fails or the t

## Headings

- Offline License Layer - EXEC001 STC SMT Cycles
-   MT5 recipient inputs
-   Issuer command
-   Saved files
-   Runtime behavior

## Entities

`EXEC001`, `EXP0015`

## Concepts

- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/deployment_profiles/README|EXEC001 STC SMT Cycles — Deployment Profiles]] — `experiment`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[tools/cme_bridge/README|DAL CME Bridge for EXP0015]] — `tool_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution]] — `experiment`
- [[lab/03_experiments/EXP0015_intermarket_time_divergence/README|EXP0015 Intermarket Candle + Session Divergence]] — `experiment`
- [[mql5/Experts/IntermarketDivergence/README|Intermarket Divergence Experts]] — `mql5_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[mql5/Experts/IntermarketDivergenceExecution/README|Intermarket Divergence Execution Experts]] — `mql5_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
