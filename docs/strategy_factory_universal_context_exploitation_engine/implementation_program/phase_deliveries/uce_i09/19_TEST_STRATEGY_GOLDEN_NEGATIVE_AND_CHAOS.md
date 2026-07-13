# Test Strategy: Golden, Negative, and Chaos

Golden tests cover deterministic pair generation, high-quality ranking on separable groups, action-mask compliance, support-aware treatment selection, monotone survival, bounded cumulative incidence, monotone quantiles, conformal interval construction, CVaR ordering, multi-task heads, sparse-regime fallback, and unseen-action prohibition.

Negative tests reject missing groups, no comparable pairs, invalid censoring, empty horizons, quantile endpoints, quantile crossing, unseen actions, mask violations, insufficient support, low propensity, corrupt model state, output-width mismatch, and final-test reuse.

Chaos tests in later phases perturb ordering, drop actions, censor outcomes, increase costs, remove regimes, change horizons, and restart orchestration. Deterministic identity must remain stable when semantics are unchanged and must change when behavior changes.
