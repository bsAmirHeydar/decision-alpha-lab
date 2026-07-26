---
title: "FlagCounting Phoenix"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "mql5/Include/FlagCountingPhoenix/README_FlagCountingPhoenix.md"
source_ext: ".md"
category: "mql5_docs"
source_size_bytes: "31761"
concepts:
  - "AI Agent Layer"
  - "Convexity"
  - "Execution"
  - "F-Counting"
  - "Hook"
  - "Licensing"
  - "MQL Native"
  - "NDS Anatomy"
  - "Validation"
---


# FlagCounting Phoenix

**Source:** [[mql5/Include/FlagCountingPhoenix/README_FlagCountingPhoenix|mql5/Include/FlagCountingPhoenix/README_FlagCountingPhoenix.md]]

**Category:** `mql5_docs`  
**Status:** ok  
**Size:** `31761` bytes

## خلاصه

Phoenix must be implemented and audited from: That file is the source of truth. This README is an implementation index only. Phoenix is a clean rebuild of the Flag Counting engine. It intentionally does not include, reuse, or depend on any earlier `FlagCounting`, `FlagCountingVNext`, or `FlagCountingV6` implementation. 1. Node logic is copied conceptually from the original project rule: a node is a candle high/low level that has at least `L` candles on both sides that do not reach that price. 2. Equality is not a break. Equal highs/lows form one plateau node. 3. Open, close, candle body, and candle color are ignored by the structural logic. 4. A flag body is always `Origin -> Leg1 -> Waist -

## Headings

- FlagCounting Phoenix
-   Current canon
-   Core principles
-   Files
-   Level 01 candle stream
-   Level 02 node engine
-   Level 03 identity layer
-   Level 04 Hook / ND context engine
-   Level 05 Flag Body engine
-   Level 11.5 Raw audit export
-   Expert
-   Recommended first run

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Convexity|Convexity]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/F-Counting|F-Counting]]
- [[docs/obsidian/04_concepts/Hook|Hook]]
- [[docs/obsidian/04_concepts/Licensing|Licensing]]
- [[docs/obsidian/04_concepts/MQL_Native|MQL Native]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|Flag Counting Current Canon]] — `flag_counting_docs`
- [[docs/flag_counting/README|Flag Counting Documentation]] — `flag_counting_docs`
- [[docs/flag_counting/implementation_ladder_v1/README|Phoenix Flag Counting Implementation Ladder V1]] — `flag_counting_docs`
- [[docs/debug/MARKET_LANGUAGE/README|DAL Market Language — Nodes, Cycles, Hooks, Rallies, Flags, 123 Flags, and Open 1/2s]] — `debug_docs`
- [[docs/experience_capture/questions/README|Quant Lab Experience Capture Questionnaire]] — `experience_capture_docs`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|EXP0016 Astro Meta Learner]] — `experiment`
- [[lab/03_experiments/EXP_flag_counting/README|EXP Flag Counting]] — `experiment`
- [[docs/debug/E0008/README|E0008 — MTF Purple Extreme Executor]] — `debug_docs`
- [[docs/flag_counting/engineering_pack_v5/README|Flag Counting Engineering Pack V5]] — `flag_counting_docs`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|EXP0013 - Astro Feature Store]] — `experiment`
- [[README|Decision Alpha Lab]] — `readme`
- [[tools/astro_live_bridge/README|EXP0013 Astro Live Bridge V2]] — `tool_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
