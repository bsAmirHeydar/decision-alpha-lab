
---
type: source_card
source_path: "tools/astro_feature_builder/README.md"
source_ext: ".md"
source_size: 3958
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Astro ML", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Known-Time Causality", "MQL Native", "Python Brain", "UI / React"]
entities: []
---

# Source Card — README.md

## Source

[[tools/astro_feature_builder/README|tools/astro_feature_builder/README.md]]

## Summary

Python-side deterministic generator for candle-aligned astrological feature stores. Primary runtime architecture: The builder uses `pyswisseph` / Swiss Ephemeris. It does not call APIs and does not require internet during generation once dependencies and ephemeris files are available. Every row is computed at candle open time. This keeps the data causal for Strategy Tester and live execution. The builder can optionally embed a fixed natal or inception chart into every row: When natal inputs are present, the CSV also contains: natal body positions and houses natal ASC / MC / cusps transit-to-natal aspects for Sun..Saturn transit-to-transit and transit-to-natal declination parallels / contra-parallels declination speed and out-of-bounds flags current transit body placement inside natal houses pure astro language fields such as `astro_bias_text`, `astro_path_text`, `astro_signal_text` doctr

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Astro_ML|Astro ML]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- Astro Feature Builder
  - Install
  - Generate CSV + Excel
  - Time contract
  - Natal / inception support
  - Doctrine metadata
  - JSON config
  - MQL5 runtime
  - Excel limit

## Related Source Documents

- [[docs/architecture|architecture.md]] — score `24`
- [metadata.yaml](../../lab/03_experiments/EXP0013_astro_feature_store/metadata.yaml) — score `20`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|README.md]] — score `16`
- [[docs/releases/legacy_migration/general/79a62a424a39_README_FLAG_MARKET_ANATOMY_PHILOSOPHY|README_FLAG_MARKET_ANATOMY_PHILOSOPHY.md]] — score `16`
- [[tools/astro_ml/README|README.md]] — score `16`
- [[docs/ui/ARCHITECTURE|ARCHITECTURE.md]] — score `16`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION|FLAG_COUNTING_LEVEL_19_PHASE4_HOOK_VIEW_PROJECTION.md]] — score `14`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN|FLAG_COUNTING_LEVEL_19_STATE_GATE_IMPLEMENTATION_PLAN.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
