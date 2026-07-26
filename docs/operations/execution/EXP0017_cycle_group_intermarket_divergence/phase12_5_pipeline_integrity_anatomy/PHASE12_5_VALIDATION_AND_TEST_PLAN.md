# Phase 12.5 Validation and Test Plan

## Compile validation

Compile `EXP0017_CG_Pipeline_Integrity_Anatomy.mq5` with all CGPI include files.

Expected: zero errors and zero missing include dependencies.

## Happy-path fixture

Construct a minimal coherent set:

- two Phase 07 outcomes;
- two Phase 10 dataset rows preserving both identities;
- one fold plan;
- one prediction referencing a valid sample and fold;
- matching writer summaries.

Expected: no critical gates fail.

## Negative tests

### Missing column

Delete `sample_id` from the Phase 10 header.

Expected: schema gate blocks Phase 13.

### Duplicate identity

Duplicate a Phase 10 sample row.

Expected: primary-key gate blocks Phase 13.

### Orphan prediction

Set a prediction `sample_id` to an unknown value.

Expected: lineage gate blocks Phase 13.

### Broken fold chronology

Place `test_start` before `train_end`.

Expected: temporal gate blocks Phase 13.

### Semantic contradiction

Set BUY with HIGH side or set hunter equal to clean.

Expected: semantic gate blocks Phase 13.

### Summary mismatch

Set `predictions_written=100` while the file contains 99 rows.

Expected: metric reconciliation fails.

## Large-data test

Run Python audit with at least 200,000 rows and verify deterministic counts and bounded memory behavior.

## Repeatability

Run twice on unchanged files. Every CSV and JSON result must be identical except filesystem timestamps outside the report content.
