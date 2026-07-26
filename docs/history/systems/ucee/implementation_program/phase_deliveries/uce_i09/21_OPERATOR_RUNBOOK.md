# Operator Runbook

1. Validate the UCE-I06 dataset manifest and label task.
2. Freeze action registry, action mask policy, horizon grid, quantile grid, and regime definition.
3. Run the local Engineering Policy and UCE-I09 boundary/static validators.
4. Execute native conformance and cumulative tests.
5. Inspect support audit before treatment or policy training.
6. Inspect censoring and cause distribution before survival training.
7. Inspect ranking group size and pair count before ranking training.
8. Retain all failed, unavailable, rejected, and pruned trials.
9. Compare task families on the same split and economic assumptions.
10. Do not publish a runtime artifact; hand accepted experiments to UCE-I11 and UCE-I12.

Stop immediately on final-test access before selection lock, unseen actions, mask violations, incoherent survival/quantiles, missing evidence hash, or changed economics lineage.
