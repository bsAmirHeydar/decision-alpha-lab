
---
type: source_card
source_path: "docs/execution/E0002_CLOSE_CONFIRMED_MARKET.md"
source_ext: ".md"
source_size: 5139
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "MQL Native", "UI / React", "Zone / RTV"]
entities: ["E0001", "E0002", "E0003", "E0004", "H0005", "M0001", "M0002"]
---

# Source Card — E0002_CLOSE_CONFIRMED_MARKET.md

## Source

[[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|docs/execution/E0002_CLOSE_CONFIRMED_MARKET.md]]

## Summary

`E0002_CloseConfirmedMarket.mq5` is a separate Expert Advisor from `E0001_ReversalOneToOne.mq5`. It does **not** add a mode to E0001 and does not modify the limit-on-touch executor. E0002 uses the same hypothesis modules as the rest of Decision Alpha Lab: M0001 structural nodes/events are the source of zones and node lifecycle. M0002 completed branch samples are the source of reversal/continuation regime. The optional human-context input can override or block the completed-branch regime gate. On each new closed candle, if the effective regime is reversal, E0002 checks the nearest active H5 reversal nodes: LOW nodes below market are buy candidates. HIGH nodes above market are sell candidates. Default candidate caps are 3 buy-side nodes and 3 sell-side nodes. E0002 does not park pending limits. It waits for a closed candle to touch a node zone and then confirms that the close did not break

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0001, E0002, E0003, E0004, H0005, M0001, M0002

## Headings

- E0002 — H0005 Close-Confirmed Market Executor
  - Execution contract
  - Close-confirmed market entry
    - Buy from LOW node
    - Sell from HIGH node
  - Touch/revisit ledger
  - Session behavior
  - Managed identity
  - Build 1.03 compile and speed fix
  - Minimal input surface
  - Higher-timeframe regime filter

## Related Source Documents

- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `50`
- [[docs/execution/README|README.md]] — score `50`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `48`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `47`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `47`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] — score `44`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] — score `43`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|README.md]] — score `43`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|README.md]] — score `38`
- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `33`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
