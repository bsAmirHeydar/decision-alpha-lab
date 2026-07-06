
---
type: source_card
source_path: "docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md"
source_ext: ".md"
source_size: 2791
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "MQL Native", "Python Brain", "UI / React", "Validation / Audit"]
entities: ["D0005", "H0005", "M0001", "M0002"]
---

# Source Card — D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md

## Source

[[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]]

## Summary

D0005 is a diagnostic Expert Advisor for H0005/M0001/M0002 live-validity debugging. The goal is to detect and prevent look-ahead leakage in H5 regime and node logic. The audit does not build one full historical array at startup for decisions. Instead, it replays history candle by candle. On each simulat… For every simulated step: The cursor is a closed candle. The EA calls `CopyRates` only for `oldest_time -> cursor_time`. No candle after `cursor_time` is copied into the working `DALBar` array. Structural nodes are accepted only when their `active_from_index` is not in the future relative to the cursor. M0002 regime is derived from events computed on the same prefix. The output row logs the latest live-available regime at that cursor. This makes D0005 different from a full-array research report. Full-array reports are useful for exploration, but they can accidentally behave as if a pivot

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

D0005, H0005, M0001, M0002

## Headings

- D0005 — H5 No-Future Walk-Forward Audit
  - Strict no-future contract
  - Main outputs
  - Recommended first run
  - Interpretation
  - Important distinction

## Related Source Documents

- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `28`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `26`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `25`
- [[README|README.md]] — score `25`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `23`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `23`
- [[docs/execution/README|README.md]] — score `23`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `23`
- [[lab/03_validation/VAL0005_h5_no_future_walk_forward/README|README.md]] — score `23`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `23`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
