# Phase 13 Controlled Model Comparison Specification

## Objective

Determine whether any simple model family produces reproducible out-of-sample evidence beyond the Phase 11 bucket baseline.

## Candidate families

1. hierarchical bucket baseline;
2. train-derived one-feature threshold baseline;
3. sparse logistic classifier for win probability;
4. sparse ridge/linear regression for primary R;
5. fixed non-negative constrained ensembles.

## Experimental discipline

- reuse Phase 11 fold boundaries exactly;
- train encoders and models only on each train window;
- never use test outcomes during fitting;
- use deterministic fold-specific seeds;
- retain model-level and sample-level audit outputs;
- compare both classification and R-regression tasks;
- compare calibration and stability, not only headline accuracy;
- preserve the bucket baseline as the minimum reference model.

## Output interpretation

A first-place model is only the best candidate in the current experiment. It is not a production model and does not become a strategy rule automatically.
