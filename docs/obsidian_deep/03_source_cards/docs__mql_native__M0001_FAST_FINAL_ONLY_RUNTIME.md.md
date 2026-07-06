
---
type: source_card
source_path: "docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME.md"
source_ext: ".md"
source_size: 1733
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "Validation / Audit", "Zone / RTV"]
entities: ["M0001"]
---

# Source Card — M0001_FAST_FINAL_ONLY_RUNTIME.md

## Source

[[docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME|docs/mql_native/M0001_FAST_FINAL_ONLY_RUNTIME.md]]

## Summary

Version: 1.59 The fast default keeps the research loop light while preserving the final chart drawings. On each intra-candle tick: When a new candle opens: No heavy full-history recomputation happens during the run when `InpRuntimeVisuals=false`. `OnDeinit` computes the complete state once: The same computed arrays are used for: final `DAL_M0001_FINAL_NODES` report, final `DAL_M0001_FINAL_RANDOM` report, final restored chart drawings. This avoids duplicate logic and prevents drift between the final report and the chart. structural node arrows, local node price labels, live/revisited/consumed zones, true revisit labels, pending/live/revisited/consumed state labels, consumed markers, optional event boxes through `InpShowEvents`, optional final RTV labels through `InpShowRTV`, optional extreme audit links through `InpShowExtremes`, final summary label. Objects are kept after test finish whe

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

M0001

## Headings

- M0001 Fast Final-Only Runtime
  - Default inputs
  - What happens during the run
  - What happens at shutdown
  - What is restored visually
  - What did not change

## Related Source Documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `19`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `19`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `18`
- [[docs/mql_native/M0001_FINAL_VISUALS_AND_LOGIC_LOCK|M0001_FINAL_VISUALS_AND_LOGIC_LOCK.md]] — score `18`
- [[docs/mql_native/M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY|M0002_REVERSAL_CONTINUATION_EXIT_VOLATILITY.md]] — score `18`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `18`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `17`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `17`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `17`
- [[lab/03_validation/VAL0022_h6_reaction_box_zones/README|README.md]] — score `17`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
