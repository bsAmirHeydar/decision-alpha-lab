---
title: "EXP0015 CME Live Provider Patch"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/EXP0015_cme_live_provider_patch.md"
source_ext: ".md"
category: "core_docs"
source_size_bytes: "1057"
entities:
  - "EXP0015"
concepts:
  - "Intermarket Divergence"
  - "Licensing"
  - "NDS Anatomy"
---


# EXP0015 CME Live Provider Patch

**Source:** [[docs/EXP0015_cme_live_provider_patch|docs/EXP0015_cme_live_provider_patch.md]]

**Category:** `core_docs`  
**Status:** ok  
**Size:** `1057` bytes

## خلاصه

This patch adds a CME-compatible provider layer for EXP0015. The historical poller is intended for closed-bar monitoring and operational simplicity. It does not request the entire history repeatedly. It reads the latest stored bar, requests a small overlapping range, merges by timestamp, and atomically rewrites the canonical DAL CSV files. Default command: See `tools/cme_bridge/README.md` for the full operational guide.

## Headings

- EXP0015 CME Live Provider Patch
-   Implemented provider modes
-   Historical polling

## Entities

`EXP0015`

## Concepts

- [[docs/obsidian/04_concepts/Intermarket_Divergence|Intermarket Divergence]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]

## Related documents

- [[lab/03_experiments/EXP0015_intermarket_time_divergence/README|EXP0015 Intermarket Candle + Session Divergence]] — `experiment`
- [[tools/cme_bridge/README|DAL CME Bridge for EXP0015]] — `tool_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|Offline License Layer - EXEC001 STC SMT Cycles]] — `experiment`
- [[mql5/Experts/IntermarketDivergence/README|Intermarket Divergence Experts]] — `mql5_docs`
- [[docs/execution/EXP0016_intermarket_divergence_execution/README|EXP0016 Intermarket Divergence Execution Documentation]] — `execution_docs`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|EXEC001 STC SMT Cycles]] — `experiment`
- [[mql5/Experts/IntermarketDivergenceExecution/README|Intermarket Divergence Execution Experts]] — `mql5_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[README|Decision Alpha Lab]] — `readme`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
