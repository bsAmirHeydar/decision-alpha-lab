
---
type: source_card
source_path: "lab/03_validation/VAL0005_h5_no_future_walk_forward/README.md"
source_ext: ".md"
source_size: 1306
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "MQL Native", "UI / React", "Validation / Audit"]
entities: ["H0005", "M0001", "M0002", "VAL0005"]
---

# Source Card — README.md

## Source

[[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|lab/03_validation/VAL0005_h5_no_future_walk_forward/README.md]]

## Summary

Validation target: H0005 must be evaluated exactly as it would be available live. H5 must not be validated by building a complete historical array once and then asking earlier candles what the future-completed node/regime was. The validation process must advance one candle at a time. Use: The debugger replays history using prefix-only bar arrays. At each cursor candle it reconstructs: M0001 structural nodes M0001 events M0002 latest branch regime The result is the regime that would have existed live at that candle. Primary pass condition: Secondary sanity conditions: Structural nodes need right-side confirmation. If a historical report treats a pivot node as known at the pivot candle instead of at its confirmation candle, the report is using future information. That makes the H5 resu… This validation forces the algorithm to respect node availability time through `active_from_index` and p

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

H0005, M0001, M0002, VAL0005

## Headings

- VAL0005 — H5 No-Future Walk-Forward Validation
  - Rule
  - Implementation
  - Pass condition
  - Why this matters

## Related Source Documents

- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `24`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] — score `23`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `23`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `23`
- [[README|README.md]] — score `23`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `21`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `21`
- [[docs/execution/README|README.md]] — score `21`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `21`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `21`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
