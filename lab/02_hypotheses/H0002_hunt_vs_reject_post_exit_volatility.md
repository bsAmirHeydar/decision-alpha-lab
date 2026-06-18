# H0002 — Hunt vs Reject Post-Exit Volatility Concentration

## Hypothesis

After a confirmed structural-node territory exit, the future volatility expansion may not be evenly distributed. It may concentrate more in one of two post-exit branches:

1. `HUNT_AFTER_EXIT`: after the confirmed exit, price later hunts the original node price.
2. `REJECT_AFTER_EXIT`: after the confirmed exit, price does not hunt the node within the configured lookahead window.

## Research question

Is post-exit volatility expansion concentrated more in the hunt branch, more in the reject branch, or mixed across both?

## Measurement

The module measures branch-level logRTV:

```text
branchRTV = mean(post-outcome abs(log(high/low))) / mean(pre-entry abs(log(high/low)))
branchLog = log(branchRTV)
```

M0002 reuses M0001 nodes and events, then separates confirmed exits into hunt/reject branches.

## Validation

Each branch is compared to matched random baselines with the same sample length.
The branch distributions are also compared directly with HUNT-vs-REJECT statistics.

## MQL module

```text
mql5/Experts/DecisionAlphaLab/M0002/M0002_HuntRejectExitVolatility.mq5
```
