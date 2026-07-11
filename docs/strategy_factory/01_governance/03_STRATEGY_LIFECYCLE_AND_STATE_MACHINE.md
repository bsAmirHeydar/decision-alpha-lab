---
type: strategy-factory-document
status: canonical
title: "Strategy Lifecycle and State Machine"
tags:
  - strategy-factory
---

# Strategy Lifecycle and State Machine

Every strategy moves through the same state machine. The state is evidence-based, versioned, and may move forward only one gate at a time.

## States

`DRAFT → ANATOMY_DEFINED → DATASET_READY → BASELINE_TESTED → OOS_VALIDATED → PAPER_READY → PAPER_RUNNING → MICRO_LIVE → LIVE_APPROVED → SCALED → RETIRED`

Retirement is available from any state. A strategy version that changes its event definition, candidate universe, primary label, or cost model returns to an earlier state; it does not inherit the promotion of the previous version.

## Gate semantics

A gate contains machine-verifiable requirements and a signed architectural decision. Examples include minimum unique clusters, leakage audit pass, positive cluster-level lower confidence bound, uplift over a simple baseline, paper/research reconciliation, maximum latency, and live slippage tolerance. Passing a gate does not imply certainty; it means the evidence is sufficient for the next bounded risk level.

## Demotion and quarantine

Schema mismatch, missing features, drift, feed discontinuity, repeated broker rejections, unexplained paper/live divergence, or a hard risk incident can demote a strategy automatically to `PAPER_READY` or quarantine it entirely. Scaling is never sticky. The system must prefer a false negative—skipping a valid opportunity—over unauthorized risk.

## Version behavior

A strategy identity is stable, but each semantic change creates a new version. Historical reports keep the old version. Model artifacts declare the exact strategy, feature, label, fold, and candidate versions they were trained against. A live runner refuses mismatched versions.

