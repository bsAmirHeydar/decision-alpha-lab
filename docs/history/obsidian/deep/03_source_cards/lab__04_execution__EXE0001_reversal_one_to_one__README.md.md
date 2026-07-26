
---
type: source_card
source_path: "lab/04_execution/EXE0001_reversal_one_to_one/README.md"
source_ext: ".md"
source_size: 5389
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Convexity / Optionality", "Decision Node", "Execution / Risk", "UI / React", "Zone / RTV"]
entities: ["E0001", "E0002", "E0003", "E0004", "EXE0001", "H0005", "M0001", "M0002"]
---

# Source Card — README.md

## Source

[[lab/04_execution/EXE0001_reversal_one_to_one/README|lab/04_execution/EXE0001_reversal_one_to_one/README.md]]

## Summary

Build: `1.18` Purpose: execute the H0005 reversal branch as pending limit orders, not market chasing. On each closed candle: Load bars from the configured symbol/timeframe. Exclude the current forming candle by default. Detect structural nodes through the existing L-rule/M0001 modules. Compute M0001 events and the latest completed M0002 branch sample. Resolve the effective regime: last completed branch only, or last branch combined with explicit human context input. If reversal: place/update nearest LOW-node buy limits below market; place/update nearest HIGH-node sell limits above market. If continuation/non-reversal: delete managed pending orders. LOW node buy: HIGH node sell: New H5 reversal setup generation and pending-order management only run inside the configured session. Outside the session, managed pending orders are force-deleted by default, independent of stale-sync protection;

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

E0001, E0002, E0003, E0004, EXE0001, H0005, M0001, M0002

## Headings

- EXE0001 — H0005 Reversal Fixed-R Executor
  - Contract
  - Defaults
  - Geometry
  - Optional time filter
  - H5 comparison report
  - Build 1.20 — strict touch/revisit ledger
    - Build 1.21 node-zone lock note
  - TP policy
  - Build 1.25 performance defaults
  - Minimal input surface
  - Higher-timeframe regime filter

## Related Source Documents

- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `47`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `47`
- [[docs/execution/README|README.md]] — score `47`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `45`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `45`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|README.md]] — score `43`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] — score `41`
- [[docs/execution/E0004_CONTINUATION_HEIKIN_ASHI_FLIP|E0004_CONTINUATION_HEIKIN_ASHI_FLIP.md]] — score `40`
- [[lab/04_execution/EXE0003_continuation_close_hunt/README|README.md]] — score `38`
- [[docs/articles/reversal_vs_continuation_execution|reversal_vs_continuation_execution.md]] — score `33`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
