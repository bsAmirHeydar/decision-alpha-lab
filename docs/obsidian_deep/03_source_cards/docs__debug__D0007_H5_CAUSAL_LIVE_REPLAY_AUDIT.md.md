
---
type: source_card
source_path: "docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md"
source_ext: ".md"
source_size: 2119
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Decision Node", "Execution / Risk", "Known-Time Causality", "Validation / Audit", "Zone / RTV"]
entities: ["D0007", "H0004", "H0005", "M0004"]
---

# Source Card — D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md

## Source

[[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md]]

## Summary

D0007 is the root live-validity validator for H0005. It exists because the old `DAL_M0005_FINAL_*` report is a structural path report, not a live execution proof. D0007 enforces four rules: **Prefix-only decision data** — at every simulated decision step the engine loads only closed candles up to that cursor. **Known-time regime state** — regime is not ordered by arbitrary sample id or entry order. Samples that become known on the same candle are processed as a single batch. **Same-candle batch policy** — if a candle confirms several highs/lows, those events are simultaneous. If the batch contains both reversal and continuation labels, the regime is ambiguous and can be skipped. **Post-entry measurement only** — future candles are used only after a causal candidate is activated and after a touch/break entry is triggered. In M0004/H0004 and H0005, several highs/lows can be confirmed on th

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Decision_Node|Decision Node]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]], [[docs/obsidian_deep/02_concepts/Zone____RTV|Zone / RTV]]

## Entities

D0007, H0004, H0005, M0004

## Headings

- D0007 — H5 Causal Live Replay Audit
  - Contract
  - Why this matters
  - Families audited
  - Key outputs

## Related Source Documents

- [[docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE|H0005_CONTEXTUAL_BRANCH_REGIME_STATE.md]] — score `25`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `22`
- [[README|README.md]] — score `22`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005_contextual_branch_regime_state.md]] — score `21`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README.md]] — score `20`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001_H0004_RESEARCH_LOCK.md]] — score `20`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004_BRANCH_REGIME_CLUSTERING.md]] — score `20`
- [[docs/mql_native/MODULE_MAP|MODULE_MAP.md]] — score `20`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|2026-06-20_h4_h5_gold_m10_report.md]] — score `20`
- [[docs/research_lessons_and_failure_modes|research_lessons_and_failure_modes.md]] — score `20`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
