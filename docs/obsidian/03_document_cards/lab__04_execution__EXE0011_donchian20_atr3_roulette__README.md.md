---
title: "EXE0011 — Donchian 20 ATR3 Roulette Execution"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/04_execution/EXE0011_donchian20_atr3_roulette/README.md"
source_ext: ".md"
category: "execution"
source_size_bytes: "6078"
entities:
  - "E0011"
  - "EXE0011"
concepts:
  - "Convexity"
  - "Execution"
  - "Known-Time Causality"
  - "MQL Native"
  - "NDS Anatomy"
  - "Rally"
---


# EXE0011 — Donchian 20 ATR3 Roulette Execution

**Source:** [[lab/04_execution/EXE0011_donchian20_atr3_roulette/README|lab/04_execution/EXE0011_donchian20_atr3_roulette/README.md]]

**Category:** `execution`  
**Status:** ok  
**Size:** `6078` bytes

## خلاصه

`E0011_Donchian20Atr3Roulette` is a pure MQL5 execution expert for a simple breakout continuation model: entry from a fresh Donchian 20 breakout stop-loss at 3 ATR take-profit at 2R money risk from the reusable Roulette risk module No Python, no external execution scripts, and no structural-regime dependency are used. The expert does not evaluate on every tick. It evaluates once when a new `InpSignalTimeframe` candle opens. Therefore the signal candle is always the last closed candle, `shift 1`. The Donchian channel is calculated causally. For a period of 20: signal candle = `shift 1` Donchian range for the signal = highs/lows of `shift 2` through `shift 21` previous candle = `shift 2` previ

## Headings

- EXE0011 — Donchian 20 ATR3 Roulette Execution
-   Purpose
-   Default Inputs
-   Execution Clock
-   Donchian Breakout Rule
-     Buy
-     Sell
-   Stop-Loss
-     Buy Stop
-     Sell Stop
-   Take-Profit
-     Buy

## Entities

`E0011`, `EXE0011`

## Concepts

- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Rally|Rally]]

## Related documents

- [[lab/03_experiments/EXP0012_distributional_cluster_miner/README|EXP0012 — Distributional Cluster Miner]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[tools/astro_feature_builder/README|Astro Feature Builder]] — `tool_docs`
- [[tools/astro_ml/README|Astro ML Tools]] — `tool_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/execution/README|Decision Alpha Lab — Execution]] — `execution_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/nds_hook_architecture/README|NDS Hook Architecture — Design Pack]] — `nds_hook_architecture_docs`
- [[lab/03_experiments/EXP0014_ICT/README|EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
