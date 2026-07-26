# Resource Budgeting and Compute Gates

All trainers inherit UCE-I07 row, feature, output, memory, wall-time, worker, device, precision, and determinism budgets. RBF kernels, k-NN, broad forests, and external boosters require stricter admission gates because their time or memory complexity can dominate a tournament.

The benchmark records fit time, repeat-run time, and peak traced memory. These figures are environment-specific evidence, not universal constants. Search phases must account for total family multiplicity and cumulative resource use rather than only the winning trial.

Single-worker deterministic defaults are used for baseline evidence. Parallel search is admitted only with reproducibility and seed-control proof.
