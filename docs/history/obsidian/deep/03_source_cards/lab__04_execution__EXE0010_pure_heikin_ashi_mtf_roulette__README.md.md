
---
type: source_card
source_path: "lab/04_execution/EXE0010_pure_heikin_ashi_mtf_roulette/README.md"
source_ext: ".md"
source_size: 3462
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native"]
entities: ["E0010", "EXE0010"]
---

# Source Card — README.md

## Source

[[lab/04_execution/EXE0010_pure_heikin_ashi_mtf_roulette/README|lab/04_execution/EXE0010_pure_heikin_ashi_mtf_roulette/README.md]]

## Summary

E0010 is a pure Heikin Ashi execution module. It does not use structural nodes, M-regime labels, or continuation/reversal classifiers. It trades only from: current-forming higher-timeframe Heikin Ashi close/open body direction; completed lower-timeframe Heikin Ashi close/open body direction flip; Roulette risk sizing. Default: The M10 candle is intentionally the **current-forming** Heikin Ashi candle. The M1 trigger is intentionally based only on **closed** candles. The EA does not evaluate entry logic on every tick. It runs the execution decision only once when a new lower-timeframe bar opens. This means the previous M1 candle has just closed, and only that completed candle is allowed to trigger. There is no dependency on chart candle color. Direction is defined only by the Heikin Ashi body: Buy only when: Sell only when: Default: TP is 1:2 by default. Stop is derived directly from the

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]]

## Entities

E0010, EXE0010

## Headings

- EXE0010 — Pure Heikin Ashi MTF Roulette
  - Purpose
  - Timeframes
  - Execution clock
  - Heikin Ashi body direction
  - Buy rule
  - Sell rule
  - Risk and target
  - Corrected Roulette logic
  - Files

## Related Source Documents

- [[docs/ai_execution/AI_NATIVE_EXECUTION_ROADMAP_FA|AI_NATIVE_EXECUTION_ROADMAP_FA.md]] — score `10`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `10`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `10`
- [[docs/execution/README|README.md]] — score `10`
- [[docs/experience_capture/answers/EXT-10/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/experience_capture/answers/NDS-R01/answer_normalized_en|answer_normalized_en.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_CURRENT_CANON|FLAG_COUNTING_CURRENT_CANON.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2|FLAG_COUNTING_IMPLEMENTATION_CHECKLIST_V2.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS|FLAG_COUNTING_LEVEL_19_PHASE11_ENTRY_BRIDGE_READINESS.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP|FLAG_COUNTING_LEVEL_19_PHASE12_EXTREME_CANDIDATE_MAP.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
