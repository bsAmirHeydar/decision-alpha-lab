---
title: "D0007 — H5 Causal Live Replay Audit"
type: document_card
generated_by: alpha_lab_obsidian_builder
generated_at: 2026-07-06
source_path: "docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md"
source_ext: ".md"
category: "debug_docs"
source_size_bytes: "2119"
entities:
  - "D0007"
  - "H0004"
  - "H0005"
  - "M0004"
concepts:
  - "AI Agent Layer"
  - "Execution"
  - "Known-Time Causality"
  - "NDS Anatomy"
  - "Structural Nodes"
  - "Validation"
---


# D0007 — H5 Causal Live Replay Audit

**Source:** [[docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT|docs/debug/D0007_H5_CAUSAL_LIVE_REPLAY_AUDIT.md]]

**Category:** `debug_docs`  
**Status:** ok  
**Size:** `2119` bytes

## خلاصه

D0007 is the root live-validity validator for H0005. It exists because the old `DAL_M0005_FINAL_*` report is a structural path report, not a live execution proof. D0007 enforces four rules: 1. **Prefix-only decision data** — at every simulated decision step the engine loads only closed candles up to that cursor. 2. **Known-time regime state** — regime is not ordered by arbitrary sample id or entry order. Samples that become known on the same candle are processed as a single batch. 3. **Same-candle batch policy** — if a candle confirms several highs/lows, those events are simultaneous. If the batch contains both reversal and continuation labels, the regime is ambiguous and can be skipped. 4.

## Headings

- D0007 — H5 Causal Live Replay Audit
-   Contract
-   Why this matters
-   Families audited
-   Key outputs

## Entities

`D0007`, `H0004`, `H0005`, `M0004`

## Concepts

- [[docs/obsidian/04_concepts/AI_Agent_Layer|AI Agent Layer]]
- [[docs/obsidian/04_concepts/Execution|Execution]]
- [[docs/obsidian/04_concepts/Known-Time_Causality|Known-Time Causality]]
- [[docs/evidence/nds_anatomy/6a11c75733b2_NDS_Anatomy|NDS Anatomy]]
- [[docs/obsidian/04_concepts/Structural_Nodes|Structural Nodes]]
- [[docs/obsidian/04_concepts/Validation|Validation]]

## Related documents

- [[docs/mql_native/H0005_CONTEXTUAL_BRANCH_REGIME_STATE|H0005 — Contextual Branch Regime State]] — `mql_native_docs`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010 — H4 Atomic No-Sample Regime Audit]] — `debug_docs`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007 — Flag Counting / F1 Start Structure]] — `mql_native_docs`
- [[docs/reports/2026-06-20_h4_h5_gold_m10_report|Report — H4/H5 GOLD M10 Review, 2026-06-20]] — `core_docs`
- [[docs/evidence/h0004_branch_regime_memory/45fad849057f_H0004_branch_regime_memory_atomic|H0004 — Branch Regime Memory]] — `hypothesis`
- [[lab/02_hypotheses/H0005_contextual_branch_regime_state|H0005 — Contextual Branch Regime State]] — `hypothesis`
- [[README|Decision Alpha Lab]] — `readme`
- [[docs/mql_native/H0001_H0002_ALGORITHM_AND_HYPOTHESIS_README|H0001 / H0002 Algorithm and Hypothesis README]] — `mql_native_docs`
- [[docs/mql_native/H0001_H0004_RESEARCH_LOCK|H0001-H0004 Research Lock]] — `mql_native_docs`
- [[docs/mql_native/H0004_BRANCH_REGIME_CLUSTERING|H0004 — Reversal/Continuation Branch Regime Clustering]] — `mql_native_docs`
- [[docs/mql_native/MODULE_MAP|MQL Module Map]] — `mql_native_docs`
- [[docs/research_lessons_and_failure_modes|Research Lessons and Failure Modes]] — `core_docs`

## Recommended Obsidian use

- این card را به نوت‌های concept، hypothesis، experiment یا ADR مربوط link کن.
- اگر این سند source of truth است، در MOC مربوطه بالاتر از اسناد legacy قرارش بده.
- اگر این سند report/validation است، نتیجه نهایی آن را به registry مربوط sync کن.
