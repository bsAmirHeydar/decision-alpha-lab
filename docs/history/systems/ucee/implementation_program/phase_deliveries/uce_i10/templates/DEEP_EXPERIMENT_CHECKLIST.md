---
title: "UCE-I10 Deep Experiment Checklist"
tags: [strategy-factory, uce-i10, template, experiment]
status: template
doc_version: 1.1.0
last_updated: 2026-07-13
---
# UCE-I10 Deep Experiment Checklist

## Identity
- [ ] Experiment ID and exact Git commit recorded.
- [ ] Dataset ID/manifest, row universe, folds, target contract, economics contract, and known-time semantics frozen.
- [ ] Candidate descriptor key/version and all behavior-changing parameters serialized.
- [ ] Resource budget, seed set, device, precision, worker count, and dependency versions recorded.

## Admission
- [ ] Effective sample size and dependence clusters meet policy.
- [ ] Event diversity and representation dimensions meet policy.
- [ ] Known-time and future-perturbation audits pass.
- [ ] Accepted classical baseline and metric are attached.
- [ ] Augmentation and ablation policies are hash-addressed.
- [ ] Admission decision is ACCEPT or documented WARN; REJECT stops here.

## Representation
- [ ] Sequence timestamps/masks/layout verified.
- [ ] Raster source/normalization/channels and zero-change pixel audit verified.
- [ ] Graph node time, topology version, canonical edges, and topology hash verified.
- [ ] Regime/novelty reference rows and thresholds are fit without final-test data.
- [ ] Missing-view policy is explicit.

## Training and evaluation
- [ ] At least three unique seeds scheduled.
- [ ] OOF predictions retained for every base model and fusion candidate.
- [ ] Failed runs retained with error codes.
- [ ] Same folds, rows, target, metrics, and economics used for baseline/candidate comparison.
- [ ] Calibration and support diagnostics retained.
- [ ] Per-view and relevant topology/channel ablations completed.

## Fusion and transfer
- [ ] Late fusion evaluated before gated/stacked fusion.
- [ ] Stacking uses OOF base predictions only.
- [ ] Confidence gate and abstention threshold were selected without final-test data.
- [ ] Source/target/final-test transfer intersections pass.
- [ ] Cross-attention is not scheduled without a superseding admission decision.

## Export and runtime
- [ ] Native JSON, ONNX, or approved distilled MQL5 path exists.
- [ ] Export parity threshold passes on retained fixtures.
- [ ] Latency and resource budget pass.
- [ ] Missing dependency/runtime failure has a tested fallback.
- [ ] MQL5 compile log retained locally when applicable.

## Qualification and handoff
- [ ] Multi-seed mean, dispersion, failed-run rate, economics, and calibration reported.
- [ ] Classical uplift and all required ablations pass.
- [ ] Decision is promotable, challenger-only, or rejected with explicit reasons.
- [ ] Final-test remains sealed until candidate and policy are frozen.
- [ ] Artifact inventory, hashes, QA report, limitations, rollback, and I11 handoff generated.
