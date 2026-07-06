
---
type: source_card
source_path: "lab/04_analysis/ANL005_h5_reversal_continuation_path_bias/README.md"
source_ext: ".md"
source_size: 1083
empty: false
generated_at: 2026-07-06
concepts: ["Atomic No-Sample", "Execution / Risk", "UI / React", "Validation / Audit"]
entities: ["ANL005"]
---

# Source Card — README.md

## Source

[[lab/04_analysis/ANL005_h5_reversal_continuation_path_bias/README|lab/04_analysis/ANL005_h5_reversal_continuation_path_bias/README.md]]

## Summary

Which H5 results are tradable, and which are only structural path statistics? The classic H5 report mixed structural path normalization with execution-like R metrics. Reversal fixed-R tests were closer to execution logic. Continuation path PF was not a real trading PF because continuation did not use a real initial stop in the classic report. Reversal showed short reaction behavior but weak full structural path performance. Practical implication: use touch-entry, test R1/R2, account for same-bar ambiguity and spread. Continuation showed large path potential. However, old PF must be retested with explicit risk. Practical implication: use ATR or structural stop, test close-break and intrabar-break separately, test trailing and fixed R separately, distinguish path R from execution R. H5 main reports must default to atomic no-sample replay with explicit risk mode.

## Concepts

[[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

ANL005

## Headings

- ANL005 — H5 Reversal/Continuation Path Bias Review
  - Question
  - Key finding
  - Reversal interpretation
  - Continuation interpretation
  - Research decision

## Related Source Documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `12`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `12`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `10`
- [[lab/05_validation/VAL001/report|report.md]] — score `10`
- [experiments.yaml](../../registry/experiments.yaml) — score `9`
- [[docs/architecture|architecture.md]] — score `8`
- [[docs/atomic_live_research_contract|atomic_live_research_contract.md]] — score `8`
- [[docs/debug/D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT|D0009_H5_ATOMIC_NO_SAMPLE_REPLAY_AUDIT.md]] — score `8`
- [[docs/debug/H4_DEEP_H6_OPTIONALITY_REPORT|H4_DEEP_H6_OPTIONALITY_REPORT.md]] — score `8`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
