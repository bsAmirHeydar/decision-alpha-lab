
---
type: source_card
source_path: "mql5/Experts/ICT/README.md"
source_ext: ".md"
source_size: 296
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "MQL Native", "Python Brain"]
entities: ["EXP0014"]
---

# Source Card — README.md

## Source

[[mql5/Experts/ICT/README|mql5/Experts/ICT/README.md]]

## Summary

Batch expert for EXP0014 ICT: L-node sweep -> FVG in sweep path -> IFVG -> CISD -> RR filter -> CSV journal. The expert is intentionally not tick-driven. `OnTick()` is empty. By default it runs once on init, writes CSV files, and removes itself.

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]]

## Entities

EXP0014

## Headings

- ICT Experts
  - ICT001_SweepIFVGCISDExecutor

## Related Source Documents

- [[lab/03_experiments/EXP0014_ICT/README|README.md]] — score `11`
- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `6`
- [[docs/architecture|architecture.md]] — score `6`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] — score `6`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `6`
- [[docs/debug/H4_FAST_ATOMIC_MAIN_REPORT|H4_FAST_ATOMIC_MAIN_REPORT.md]] — score `6`
- [[docs/experience_capture/answers/BASE-04/notes_en|notes_en.md]] — score `6`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `6`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE|FLAG_COUNTING_LEVEL_19_CLEAN_ISOLATED_STATE_GATE.md]] — score `6`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT|FLAG_COUNTING_LEVEL_19_PHASE10_PANEL_LINE_CONTRACT.md]] — score `6`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
