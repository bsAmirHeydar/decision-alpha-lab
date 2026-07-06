
---
type: source_card
source_path: "docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md"
source_ext: ".md"
source_size: 2270
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Licensing", "MQL Native", "Python Brain", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["D0006", "E0001", "E0005", "H0005", "M0001", "M0002"]
---

# Source Card — D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md

## Source

[[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]]

## Summary

D0006 is the strict live-validity audit for H0005 reversal touch-entry logic. It exists because full-history H5 reports can be useful for discovery, but they are not enough to prove live validity. A live-valid H5 test must separate three times: the time the regime and zones are known, the later time price actually touches the zone and fills the entry, the future path used only for measurement after fill. D0006 enforces this contract: The audit is deliberately separate from E0001–E0005. It is a validator, not an executor. When the latest prefix-only M0002 regime is reversal, D0006 activates live candidates: The entry is not assumed at the signal candle. The candidate must be touched later: Only after that fill does D0006 measure MFE, MAE, reward hit, stop hit, same-bar ambiguity, and realized R. The critical field is: If this is not zero, H5 is still using something that should not be ava

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Licensing|Licensing]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

D0006, E0001, E0005, H0005, M0001, M0002

## Headings

- D0006 — H5 Live Touch Replay Audit
  - Contract
  - Reversal touch model
  - Key summary fields
  - CSV
  - Scientific meaning

## Related Source Documents

- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `32`
- [[docs/execution/E0005_CONTINUATION_CLOSE_BREAK_FIXED_R|E0005_CONTINUATION_CLOSE_BREAK_FIXED_R.md]] — score `31`
- [[docs/execution/E0002_CLOSE_CONFIRMED_MARKET|E0002_CLOSE_CONFIRMED_MARKET.md]] — score `30`
- [[docs/execution/E0003_CONTINUATION_CLOSE_HUNT|E0003_CONTINUATION_CLOSE_HUNT.md]] — score `30`
- [[docs/execution/README|README.md]] — score `30`
- [[lab/04_execution/EXE0002_close_confirmed_market/README|README.md]] — score `30`
- [[README|README.md]] — score `29`
- [[lab/04_execution/EXE0001_reversal_one_to_one/README|README.md]] — score `28`
- [[docs/debug/D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT|D0005_H5_NO_FUTURE_WALK_FORWARD_AUDIT.md]] — score `28`
- [[lab/04_execution/EXE0004_continuation_heikin_ashi_flip/README|README.md]] — score `26`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
