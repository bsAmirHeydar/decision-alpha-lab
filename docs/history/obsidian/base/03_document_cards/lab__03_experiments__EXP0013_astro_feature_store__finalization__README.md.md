---
title: "EXP0013 Finalization Snapshot"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "lab/03_experiments/EXP0013_astro_feature_store/finalization/README.md"
source_ext: ".md"
category: "experiment"
source_size_bytes: "1335"
entities:
  - "EXP0013"
concepts:
  - "Astro ML"
  - "Execution"
  - "MQL Native"
  - "Validation"
---


# EXP0013 Finalization Snapshot

**Source:** [[lab/03_experiments/EXP0013_astro_feature_store/finalization/README|lab/03_experiments/EXP0013_astro_feature_store/finalization/README.md]]

**Category:** `experiment`  
**Status:** ok  
**Size:** `1335` bytes

## خلاصه

This folder records the latest astro-only finalization pass run on: CSV: `data/astro/astro_NAS100_M1_20260622_to_now_nasdaq100_natal_mql.csv` doctrine config: `tools/astro_feature_builder/astro_config.example.json` profile: `pure_strict` tuned candidate: `pure_strict_tuned` tuned override: `min_micro_timing = 54.0` rows scanned: `5736` pure entry bars: `607` probe bars: `62` blocked bars: `5067` final entry windows: `11` direction mix: `long only` in this sample Top veto reasons: `no_direction`: `5015` `low_weight`: `77` `low_family_count`: `62` `micro_timing_low`: `37` pure entry bars: `659` final entry windows: `13` pure entry bars: `698` final entry windows: `13` Current promotion snapsho

## Headings

- EXP0013 Finalization Snapshot
-   Recommended operating profile
-   Final-entry results
-     `pure_strict`
-     `pure_balanced`
-     `pure_probe`
-   Family validation snapshot
-   Notes

## Entities

`EXP0013`

## Concepts

- [[docs/obsidian/04_concepts/Astro_ML|Astro ML]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[mql5/Experts/AstroExecution/README|Astro Execution]] — `mql5_docs`
- [[tools/astro_live_bridge/README|EXP0013 Astro Live Bridge V2]] — `tool_docs`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[tools/astro_ml/README|Astro ML Tools]] — `tool_docs`
- [[tools/astro_feature_builder/README|Astro Feature Builder]] — `tool_docs`
- [[tools/astro_validation/README|Astro Signal Validator]] — `tool_docs`
- [[docs/debug/E0006/README|E0006 — Structural Execution Layer Overview]] — `debug_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0005_mql_native_directional_memory/README|EXP0005 — MQL-native H0005 directional memory]] — `experiment`
- [[lab/03_experiments/EXP0014_ICT/README|EXP0014 — ICT Sweep / FVG / IFVG / CISD Execution Lab]] — `experiment`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
