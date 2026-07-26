
---
type: source_card
source_path: "docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md"
source_ext: ".md"
source_size: 6535
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md

## Source

[[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md]]

## Summary

Version: 1.59 This document locks the current M0001 research semantics and runtime contract. It exists so future optimization work does not accidentally change the algorithm. M0001 is candle-based, not tick-based. The optimized default is: That means: no full node/event recomputation on every closed candle, no chart object deletion/redraw loop during the test, final node/random logRTV reports are printed once at shutdown, final chart objects are restored and kept after the run finishes. For visual debugging during a replay, set: This intentionally costs more because the chart state is recomputed and redrawn on each newly closed candle. A confirmed L-rule node at index `i` requires both left and right confirmation windows. The node marker is drawn on the pivot candle. Trading/research logic starts only from `active_from_index`. For LOW nodes, the expansion extreme is the highest high in t

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Final Visuals and Logic Lock
  - Runtime contract
  - Structural node definition
  - Territory formula
  - Event lifecycle
  - HUNT priority
  - TOUCH mode
  - HUNT mode and revisit memory
  - Revisited-live extreme reset
  - Visual rules
  - RTV and logRTV
  - Warmup and analysis period

## Related Source Documents

- [[docs/mql_native/M0001_PROFESSIONAL_VALIDATION_METRICS|M0001_PROFESSIONAL_VALIDATION_METRICS.md]] — score `26`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `21`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `20`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `20`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `20`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `19`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `19`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `19`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|README.md]] — score `19`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `18`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
