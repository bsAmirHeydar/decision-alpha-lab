
---
type: source_card
source_path: "docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP.md"
source_ext: ".md"
source_size: 2280
empty: false
generated_at: 2026-07-06
concepts: ["AI Agent Layer", "Atomic No-Sample", "Convexity / Optionality", "Known-Time Causality", "MQL Native", "UI / React", "Validation / Audit"]
entities: ["H0004", "H0006", "M0006"]
---

# Source Card — H6_STANDALONE_OPTIONALITY_EDGE_MAP.md

## Source

[[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP.md]]

## Summary

H0006 is separated from H0004. H0004 remains the regime-memory hypothesis. H0006 tests a different question: > Are reversal known-time batches better optionality points for future explosive movement, independent of ordinary win-rate? The standalone expert is: It uses the same atomic no-sample known-time batch contract as H0004: `DAL_H0006_OPTIONALITY_FAST/MAIN/SLOW` compare reversal and continuation batches by future ATR-normalized movement after the known-time candle. The report does not claim win-rate. It measures optionality: absolute future excursion in ATR units directional MFE in ATR units adverse excursion in ATR units p90 / p95 / p99 tails hit rates above configurable ATR thresholds top 10% tail concentration shuffle-label null stress `DAL_H0006_EDGE_BUCKET_FAST/MAIN/SLOW` is the edge-map layer. It asks which sub-conditions are materially edge-like and which are unimportant. Buck

## Concepts

[[docs/obsidian_deep/02_concepts/AI_Agent_Layer|AI Agent Layer]], [[docs/obsidian_deep/02_concepts/Atomic_No-Sample|Atomic No-Sample]], [[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Known-Time_Causality|Known-Time Causality]], [[docs/obsidian_deep/02_concepts/MQL_Native|MQL Native]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

H0004, H0006, M0006

## Headings

- H0006 standalone optionality and edge-map report
  - Reports
  - Materiality labels
  - Why this exists

## Related Source Documents

- [[lab/03_validation/VAL0016_h6_standalone_optionality/README|README.md]] — score `23`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `22`
- [[lab/02_hypotheses/H0004_branch_regime_memory_atomic|H0004_branch_regime_memory_atomic.md]] — score `17`
- [[README|README.md]] — score `17`
- [[lab/03_validation/VAL0017_h6_fast_accurate/README|README.md]] — score `17`
- [[docs/debug/D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT|D0010_H4_ATOMIC_NO_SAMPLE_REGIME_AUDIT.md]] — score `16`
- [[docs/debug/H6_CANDLE_STREAM_FAST|H6_CANDLE_STREAM_FAST.md]] — score `16`
- [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|H6_FAST_ACCURATE_OPTIONALITY.md]] — score `16`
- [validations.yaml](../../registry/validations.yaml) — score `16`
- [[docs/debug/H6_REACTION_BOX_ZONES|H6_REACTION_BOX_ZONES.md]] — score `16`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
