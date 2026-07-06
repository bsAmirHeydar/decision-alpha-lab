---
title: "Astro Execution"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "mql5/Experts/AstroExecution/README.md"
source_ext: ".md"
category: "mql5_docs"
source_size_bytes: "5603"
entities:
  - "EXP0013"
concepts:
  - "Astro ML"
  - "Convexity"
  - "Execution"
  - "Licensing"
  - "MQL Native"
  - "Validation"
---


# Astro Execution

**Source:** [[mql5/Experts/AstroExecution/README|mql5/Experts/AstroExecution/README.md]]

**Category:** `mql5_docs`  
**Status:** ok  
**Size:** `5603` bytes

## خلاصه

This folder contains astro-only Expert Advisors for EXP0013. They read the deterministic astro CSV through `DAL_AstroExcelCandleReader.mqh`. They use `DAL_AstroPureAstrologySignals.mqh`. They can journal paper actions through `DAL_AstroExecutionJournal.mqh`. They do not use market-structure, indicators, ATR, volume, or execution-family context. They emit pure astrology entry and exit language from transit, natal activation, and doctrinal astro metrics. They now read a hierarchical timing stack: macro field -> meso gate -> micro trigger -> minute window. They can load doctrine-owned threshold defaults from `DAL_AstroFamilyThresholds.mqh`. The pure signal layer now includes sect-aware doctrine

## Headings

- Astro Execution
-   Contract
-   Execution families
-     A0001 - Transit Trend Pulse
-     A0002 - Natal Resonance
-     A0003 - Friction Polarity
-     A0004 - Sect Benefic Pressure
-     A0005 - Moon Timing Window
-     A0006 - Angular Activation
-     A0007 - Station Transition
-     A0090 - Live Order Shell
-   Usage

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[tools/astro_live_bridge/README|EXP0013 Astro Live Bridge V2]] — `tool_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/finalization/README|EXP0013 Finalization Snapshot]] — `experiment`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[tools/astro_ml/README|Astro ML Tools]] — `tool_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[tools/astro_feature_builder/README|Astro Feature Builder]] — `tool_docs`
- [[tools/astro_validation/README|Astro Signal Validator]] — `tool_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0014_ICT/README|EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab]] — `experiment`
- [[lab/03_validation/VAL0023_e6_all_zone_touch_limit/README|E0006 — All-Zone Touch Limit Fixed-R Executor]] — `validation`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
