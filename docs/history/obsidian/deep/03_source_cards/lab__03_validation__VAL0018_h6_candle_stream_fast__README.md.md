
---
type: source_card
source_path: "lab/03_validation/VAL0018_h6_candle_stream_fast/README.md"
source_ext: ".md"
source_size: 706
empty: false
generated_at: 2026-07-06
concepts: ["Convexity / Optionality", "Execution / Risk", "UI / React", "Validation / Audit"]
entities: ["H0006", "VAL0018"]
---

# Source Card — README.md

## Source

[[lab/03_validation/VAL0018_h6_candle_stream_fast/README|lab/03_validation/VAL0018_h6_candle_stream_fast/README.md]]

## Summary

Purpose: validate H0006 optionality using a faster forward candle-stream measurement. Recommended first run: `InpH6CandleStreamMode=true` `InpStressH6Optionality=false` `InpPrintH6EdgeMap=false` `InpH6ReportSlowHorizon=false` `InpH6RequireFullHorizon=true` `InpH6EntryAnchorMode=1` Expected audit: `sampleCalls=0` `branchSamplesBuilt=0` `m0002Calls=0` `h6Engine=CANDLE_FORWARD_STREAM` `measurement=candle_forward_stream_no_prefix_rebuild_no_sample` Escalation run for publication: enable slow horizon set stress mode to 1 first only use stress mode 2 and full edge map after the fast report identifies candidate conditions

## Concepts

[[docs/obsidian_deep/02_concepts/Convexity____Optionality|Convexity / Optionality]], [[docs/obsidian_deep/02_concepts/Execution____Risk|Execution / Risk]], [[docs/obsidian_deep/02_concepts/UI____React|UI / React]], [[docs/obsidian_deep/02_concepts/Validation____Audit|Validation / Audit]]

## Entities

H0006, VAL0018

## Headings

- VAL0018 — H6 Candle-Stream Fast Optionality

## Related Source Documents

- [[lab/03_experiments/EXP0004_mql_native_m0004/report|report.md]] — score `14`
- [[docs/debug/H6_FAST_ACCURATE_OPTIONALITY|H6_FAST_ACCURATE_OPTIONALITY.md]] — score `13`
- [[docs/mql_native/H0007_FLAG_COUNTING_F1_START_STRUCTURE|H0007_FLAG_COUNTING_F1_START_STRUCTURE.md]] — score `13`
- [[lab/03_validation/VAL0017_h6_fast_accurate/README|README.md]] — score `13`
- [[lab/03_experiments/EXP0003_mql_native_m0002/report|report.md]] — score `12`
- [[lab/05_validation/VAL_M0001_MQL_NATIVE/report|report.md]] — score `12`
- [[docs/debug/H6_CANDLE_STREAM_FAST|H6_CANDLE_STREAM_FAST.md]] — score `11`
- [[docs/debug/H6_STANDALONE_OPTIONALITY_EDGE_MAP|H6_STANDALONE_OPTIONALITY_EDGE_MAP.md]] — score `11`
- [[lab/03_validation/VAL0016_h6_standalone_optionality/README|README.md]] — score `11`
- [[lab/03_experiments/EXP0002_mql_native_m0001/report|report.md]] — score `10`

## Obsidian Use

- اگر این سند تعریف رسمی دارد، آن را به یک concept canonical وصل کن.
- اگر این سند نتیجه آزمایش است، آن را به hypothesis و validation وصل کن.
- اگر این سند patch یا compile fix است، آن را به ADR یا patch note وصل کن.
