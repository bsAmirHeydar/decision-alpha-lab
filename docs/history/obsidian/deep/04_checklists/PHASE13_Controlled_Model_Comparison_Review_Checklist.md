# Phase 13 Controlled Model Comparison Review Checklist

## Gate
- [ ] Phase 12.5 is not blocked.
- [ ] Critical files and fixed folds are present.

## Causality
- [ ] Feature allowlist reviewed.
- [ ] Future outcome fields excluded.
- [ ] Full-day range leakage excluded.
- [ ] Phase 09 full-history enrichment excluded.

## Experiment
- [ ] Same Phase 11 folds used for every model.
- [ ] Encoders fit on train only.
- [ ] Deterministic seed recorded.
- [ ] Bucket baseline included.
- [ ] Threshold baseline included.
- [ ] Logistic and ridge regularization recorded.
- [ ] Ensemble weights fixed before test evaluation.

## Evidence
- [ ] Fold-level metrics reviewed.
- [ ] Calibration reviewed.
- [ ] Regression error reviewed.
- [ ] Worst fold reviewed.
- [ ] Coefficient/feature stability reviewed.
- [ ] Repeated run reproducibility checked.

## Governance
- [ ] No model treated as live permission.
- [ ] No CG disabled automatically.
- [ ] No risk or target changed.
- [ ] Phase 14 receives a versioned evidence package only.
