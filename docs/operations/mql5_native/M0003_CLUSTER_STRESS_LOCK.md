# M0003 Cluster Stress Lock

This update hardens H0003 from a simple continuation-memory diagnostic into a full cluster-stress suite.

## Changes

- Split M0003 inertia output into short non-truncated reports.
- Added per-horizon memory reports for each configured horizon.
- Added memory AUC and carry AUC summary.
- Added direct cluster comparison between reversal and continuation.
- Added deterministic Fisher-Yates lag-shuffle stress for lag-1 and lag-2 serial memory, with empirical p-values.
- Added direct branch-label permutation stress to test whether continuation-specific cluster memory survives label randomization.
- Added contiguous block cluster stress.
- Added configurable high-volatility run percentile.
- Added high-run iid expectation and run-over-iid ratio.
- Added high-run Fisher-Yates shuffle stress with empirical p-values.
- Added half-life status to shared H0001/H0002 horizon reports so `halfLifeH=0` is not misread as immediate decay.

## Build targets

- M0002 Reversal/Continuation: build 1.75
- M0003 Continuation Inertia Memory: build 1.04
