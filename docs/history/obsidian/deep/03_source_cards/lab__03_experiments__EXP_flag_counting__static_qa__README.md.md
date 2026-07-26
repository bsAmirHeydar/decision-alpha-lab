
---
type: source_card
source_path: "lab/03_experiments/EXP_flag_counting/static_qa/README.md"
source_ext: ".md"
source_size: 872
empty: false
generated_at: 2026-07-06
concepts: ["MQL Native", "Python Brain"]
entities: []
---

# Source Card — README.md

## Source

[[lab/03_experiments/EXP_flag_counting/static_qa/README|lab/03_experiments/EXP_flag_counting/static_qa/README.md]]

## Summary

Level 18 is the compile/static QA hardening layer after the official Level 17 decision lock. Run from repository root: Strict mode fails on warnings too: The scanner checks Phoenix MQL files for: empty `Print()` calls very long multi-argument `Print(...)` calls duplicate EA input names stale `phoenix_level16` / `phoenix_level17` identity pass references in MQL source stale interface contract versions stale short report aliases such as `r.export_forced` missing Level 18 modules The MQL runtime layer prints `FP_LEVEL18`; this Python scanner is the source-side companion for checks that cannot be proven from inside MQL5 at runtime.

## Concepts

[[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]]

## Entities

—

## Headings

- Phoenix Level 18 Static QA

## Related Source Documents

- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `12`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `10`
- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `10`
- [[lab/03_experiments/EXP0000_sample/report|report.md]] — score `8`
- [[lab/03_experiments/EXP0001_structural_highs_lows_importance/report|report.md]] — score `8`
- [[lab/05_validation/VAL001/report|report.md]] — score `8`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `4`
- [[docs/architecture|architecture.md]] — score `4`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] — score `4`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
