
---
type: source_card
source_path: "docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_04_STC_SMT_W_LEVEL_BUILDER.md"
source_ext: ".md"
source_size: 3318
empty: false
generated_at: 2026-07-06
concepts: ["Execution / Risk", "Intermarket Divergence", "Python Brain", "UI / React", "Validation / Audit"]
entities: []
---

# Source Card — LEVEL_04_STC_SMT_W_LEVEL_BUILDER.md

## Source

[[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_04_STC_SMT_W_LEVEL_BUILDER|docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_04_STC_SMT_W_LEVEL_BUILDER.md]]

## Summary

Level 04 adds the first structural market object required by STC: the closed 90-minute W high/low levels for both symbols. This level is still non-trading. It does not detect SMT, confirm signals, simulate entries, draw objects, open positions, partial-close positions, or hard-close positions. It only builds and audits W levels after each W… STC does not compare raw prices between SPX and NDX. It compares each symbol against its own W reference levels. Therefore the system needs a deterministic W-level layer before SMT can exist. The locked owner rule is: each symbol has its own W high and W low; the comparison is structural, not price-shared; W1 gives no signal; W2 may later compare only with W1; W3 may later compare with W2 and W1; W4 may later compare with W3, W2 and W1; no W compares with itself; W high/low is the high/low of the whole 90-minute synthetic candle; the construction tim

## Concepts

[[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/Intermarket_Divergence|Intermarket Divergence]], [[docs/obsidian_deep/02_concepts/Python_Brain|Python Brain]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

—

## Headings

- Level 04 — W Level Builder
  - Status
  - Why this level exists
  - Output file
  - W serial map
  - Completeness rule
  - Reference role
  - Level 04 acceptance criteria

## Related Source Documents

- [signals.yaml](../../registry/signals.yaml) — score `14`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_02_STC_SMT_TIME_ENGINE|LEVEL_02_STC_SMT_TIME_ENGINE.md]] — score `11`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR|LEVEL_03_STC_SMT_CHECK_CANDLE_AGGREGATOR.md]] — score `11`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR|LEVEL_05_STC_SMT_REFERENCE_HUNT_DETECTOR.md]] — score `11`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY|LEVEL_08_STC_SMT_RISK_PLAN_PAPER_ENTRY.md]] — score `11`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING|LEVEL_13_STC_SMT_VISUALIZATION_AUDIT_DRAWING.md]] — score `11`
- [[docs/execution/EXP0016_intermarket_divergence_execution/LEVEL_19_STC_SMT_VALIDATION_PACK|LEVEL_19_STC_SMT_VALIDATION_PACK.md]] — score `11`
- [[docs/EXP0015_cme_live_backtest_plan|EXP0015_cme_live_backtest_plan.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP|FLAG_COUNTING_LEVEL_19_PHASE13_MTF_ALIGNMENT_MAP.md]] — score `10`
- [[docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION|FLAG_COUNTING_LEVEL_19_PHASE21_PAPER_REGIME_ATTRIBUTION.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
