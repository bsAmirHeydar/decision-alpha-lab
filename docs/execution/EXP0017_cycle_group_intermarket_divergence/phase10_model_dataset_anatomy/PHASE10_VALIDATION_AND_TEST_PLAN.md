# Phase 10 — Validation and Test Plan

## Compile validation

Compile:

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Model_Dataset_Anatomy.mq5
```

## File validation

Before Phase 10 runs, Phase 07 should have produced:

```text
EXP0017_Phase07_Outcome_Study.csv
```

Phase 09 files are optional, but enrichment requires:

```text
EXP0017_Phase09_Rankings_All.csv
EXP0017_Phase09_Shortlist.csv
```

## Dataset validation

Open `EXP0017_Phase10_Model_Dataset.csv` and verify:

- one row per outcome sample;
- confirmed outcome rows have labels;
- zero-risk or incomplete rows are excluded when inputs require exclusion;
- role keys match Phase 08/09 keys;
- `primary_r` changes when the label window changes;
- `shortlist_match` appears only when Phase 09 shortlist data exists.
