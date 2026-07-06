
---
type: source_card
source_path: "docs/EXP0015_cme_live_provider_patch.md"
source_ext: ".md"
source_size: 1057
empty: false
generated_at: 2026-07-06
concepts: ["Intermarket Divergence", "Licensing", "Python Brain", "UI / React"]
entities: ["EXP0015"]
---

# Source Card — EXP0015_cme_live_provider_patch.md

## Source

[[docs/EXP0015_cme_live_provider_patch|docs/EXP0015_cme_live_provider_patch.md]]

## Summary

This patch adds a CME-compatible provider layer for EXP0015. The historical poller is intended for closed-bar monitoring and operational simplicity. It does not request the entire history repeatedly. It reads the latest stored bar, requests a small overlapping range, merges by tim… Default command: See `tools/cme_bridge/README.md` for the full operational guide.

## Concepts

[[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

EXP0015

## Headings

- EXP0015 CME Live Provider Patch
  - Implemented provider modes
  - Historical polling

## Related Source Documents

- [[lab/03_experiments/EXP0015_intermarket_time_divergence/README|README.md]] — score `21`
- [[tools/cme_bridge/README|README.md]] — score `21`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/offline_license/README|README.md]] — score `19`
- [[mql5/Experts/IntermarketDivergence/README|README.md]] — score `17`
- [[docs/execution/EXP0016_intermarket_divergence_execution/README|README.md]] — score `14`
- [[lab/09_execution/EXP0016_intermarket_divergence_execution/EXEC001_STC_SMT_Cycles/README|README.md]] — score `14`
- [[mql5/Experts/IntermarketDivergenceExecution/README|README.md]] — score `14`
- [[docs/flag_counting/README|README.md]] — score `14`
- [[lab/03_experiments/EXP0013_astro_feature_store/README|README.md]] — score `14`
- [[lab/03_experiments/EXP0016_astro_meta_learner/README|README.md]] — score `14`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
