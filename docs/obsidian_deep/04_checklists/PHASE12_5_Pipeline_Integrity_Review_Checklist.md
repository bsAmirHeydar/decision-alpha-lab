# Phase 12.5 Pipeline Integrity Review Checklist

## Files and schema

- [ ] All required Phase 07–11 files exist.
- [ ] Every required column is present.
- [ ] No file is empty or unreadable.

## Identity

- [ ] `outcome_id` is non-empty and unique.
- [ ] `sample_id` is non-empty and unique.
- [ ] `fold_id + sample_id` is unique in predictions.

## Lineage

- [ ] Phase 07 outcomes reconcile to Phase 10.
- [ ] Phase 11 has no orphan sample IDs.
- [ ] Phase 11 has no orphan signal IDs.
- [ ] Every prediction and bucket model uses a declared fold.

## Semantics

- [ ] BUY is LOW-side; SELL is HIGH-side.
- [ ] Hunter and clean symbols differ.
- [ ] Complete/model-ready rows have positive risk distance.
- [ ] Label classes and binary labels agree.
- [ ] Prediction outcome flags agree with actual R.

## Time and metrics

- [ ] Train/embargo/test ordering passes for every fold.
- [ ] Writer summaries match CSV row counts.
- [ ] Phase 07 COMPLETE count matches Phase 08 overall sample count.

## Gate

- [ ] Readiness is reviewed by the architect.
- [ ] `BLOCKED_FOR_PHASE13` defects are repaired upstream.
- [ ] No readiness result is interpreted as live-trading permission.
