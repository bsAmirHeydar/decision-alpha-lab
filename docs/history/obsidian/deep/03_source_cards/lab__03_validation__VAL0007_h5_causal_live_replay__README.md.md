
---
type: source_card
source_path: "lab/03_validation/VAL0007_h5_causal_live_replay/README.md"
source_ext: ".md"
source_size: 1387
empty: false
generated_at: 2026-07-06
concepts: ["Decision Node", "Execution / Risk", "Known-Time Causality", "UI / React", "Validation / Audit", "Zone / RTV"]
entities: ["H0005", "VAL0007"]
---

# Source Card — README.md

## Source

[[lab/03_validation/VAL0007_h5_causal_live_replay/README|lab/03_validation/VAL0007_h5_causal_live_replay/README.md]]

## Summary

This validation replaces path-first H5 interpretation with live-style replay. When H0005 has a known regime state at candle `t`, and that state was knowable using only data up to `t`, do later zone touches or structural breaks produce positive post-entry movement? Old H5 reports can be useful for structural research, but they are not strict live execution proof. VAL0007 treats regime confirmation as a time-stamped event and processes all samples confirmed on the same candle as one batch. If multiple highs/lows are confirmed on the same candle, they do not form a chronological sequence. They are simultaneous. A mixed reversal/continuation batch is marked ambiguous by default. Reversal: regime energy must be REVERSAL; live-visible untouched node zones are activated after the regime is known; entry only occurs if a future candle touches the zone. Continuation: regime energy must be CONTINUA

## Concepts

[[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

H0005, VAL0007

## Headings

- VAL0007 — H5 Causal Live Replay
  - Hypothesis under test
  - What is different from old H5 reports?
  - Simultaneous breaks
  - Entry definitions
  - Measurement

## Related Source Documents

- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `17`
- [[papers/001_atomic_live_regime_framework|001_atomic_live_regime_framework.md]] — score `17`
- [[README|README.md]] — score `17`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `16`
- [[docs/debug/D0006_H5_LIVE_TOUCH_REPLAY_AUDIT|D0006_H5_LIVE_TOUCH_REPLAY_AUDIT.md]] — score `15`
- [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md]] — score `15`
- [[docs/execution/H0005_R1_SIX_SLOT_TOUCH_LEDGER|H0005_R1_SIX_SLOT_TOUCH_LEDGER.md]] — score `15`
- [[docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE|H0005_CONTEXTUAL_BRANCH_REGIME_STATE.md]] — score `15`
- [[docs/mql_native/H0005_DIRECTIONAL_MEMORY|H0005_DIRECTIONAL_MEMORY.md]] — score `15`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] — score `15`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
