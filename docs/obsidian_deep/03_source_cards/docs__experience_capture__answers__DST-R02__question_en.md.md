
---
type: source_card
source_path: "docs/experience_capture/answers/DST-R02/question_en.md"
source_ext: ".md"
source_size: 1440
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "UI / React"]
entities: []
---

# Source Card — question_en.md

## Source

[[docs/experience_capture/answers/DST-R02/question_en|docs/experience_capture/answers/DST-R02/question_en.md]]

## Summary

When several destinations or exit opportunities exist, how should take profit, partial close, runner/tail logic, and trailing behavior be handled? NDS does not treat profit-taking as a single fixed TP. The strategy may have multiple destinations, multiple exit conditions, partial exits, and an optional runner/tail component. Because the broader model prioritizes lo… Please clarify: Should different exit variants be trained and compared? What metrics should decide which exit policy is better? Should the system prioritize potential, open profit path, low cost, or win rate? Is trailing stop allowed or discouraged? Should partial close be favored over trailing? Under what conditions should partial profits be taken? Can several partial exits occur at different logic points? Should a portion remain open for larger profit potential? Is exit policy rule-based, trainable, or both? What should the

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]]

## Entities

—

## Headings

- DST-R02 — Take Profit, Partial Exit, and Multi-Destination Policy
  - Question
  - Why This Question Remains
  - Answer Requirements
  - Expected Output

## Related Source Documents

- [requirements.txt](../../requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_feature_builder/requirements.txt) — score `10`
- [requirements.txt](../../tools/astro_ml/requirements.txt) — score `10`
- [requirements.txt](../../tools/cme_bridge/requirements.txt) — score `10`
- [[docs/evidence/mon001/2cb2a9127709_metrics|metrics.md]] — score `8`
- [[docs/experience_capture/answers/DST-R02/notes_en|notes_en.md]] — score `7`
- [[docs/ai_execution/AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA|AI_ALGORITHM_LAYER_MAP_FOR_EXTREME_ENGINE_FA.md]] — score `6`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `6`
- [[docs/ai_execution/AMIR_STRUCTURAL_EXPERIENCE_MAP_FA|AMIR_STRUCTURAL_EXPERIENCE_MAP_FA.md]] — score `6`
- [[docs/ai_execution/EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA|EXPERIENCE_CAPTURE_LOG_TEMPLATE_FA.md]] — score `6`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
