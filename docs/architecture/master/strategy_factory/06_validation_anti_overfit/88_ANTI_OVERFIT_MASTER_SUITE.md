---
type: strategy-factory-reference
status: canonical
title: "Anti-Overfit Master Suite — Complete Gate Reference"
tags:
  - strategy-factory
  - anti-overfit
  - validation
  - reference
---

# Anti-Overfit Master Suite — Complete Gate Reference

## Philosophy

Overfitting is not one problem. It can arise from future leakage, repeated rule changes, dependent rows, broad parameter search, model complexity, favorable period selection, feed artifacts, unrealistic fills, or publication of the best result. The master suite attacks each path separately. A strategy is not considered robust because it passes one famous test.

## Gate 1 — provenance and trial accounting

Before performance is evaluated, verify source data hash, strategy/anatomy version, feature and candidate versions, label and cost versions, fold plan, and trial registration. Count every materially related attempt. If true trial count is unknown, use a conservative estimate and tag selection risk as unresolved.

## Gate 2 — causal feature audit

For every feature, prove its availability time. Automated checks reject outcome names and timestamps later than the snapshot. Manual review targets completed-session values, eventual object validity, future reference consumption, cross-symbol synchronization, and data revisions. Label-shuffle and feature-time-shift tests should destroy predictive performance.

## Gate 3 — sample independence

Construct `market_event_cluster_id` before outcomes. Keep the entire cluster in one fold. Calculate row, event, cluster, day, and week counts. Use cluster and moving-block bootstrap. If conclusions change materially between row and cluster intervals, use the cluster result and investigate duplication.

## Gate 4 — purged walk-forward

Outer folds are chronological. Remove training samples whose label horizons reach the test start. Apply embargo after purge. Fit normalization, category vocabularies, imputation, feature selection, hyperparameters, thresholds, and calibration inside training only. Preserve fold artifacts.

## Gate 5 — matched baselines

Compare with a baseline that retains easy structure: same session, holding period, direction distribution, volatility, and costs. For divergence, compare confirmation-only and no-divergence events. For zones, compare matched random levels. For time cycles, shift boundaries and use session-only seasonality. The anatomy must add incremental value.

## Gate 6 — null and placebo tests

Recommended suite:

- within-day event-time permutation
- direction/role randomization
- reference time shift
- paired-symbol placebo
- anatomy object placebo
- random feature injection
- outcome label permutation
- session-matched random entry
- no-anatomy confirmation

A placebo that performs similarly indicates the proposed mechanism is unnecessary or the simulator contains bias.

## Gate 7 — multiple testing

Create a family of all related candidates, buckets, filters, models, and targets. Apply Benjamini-Hochberg for discovery and a stricter confirmation rule where appropriate. Report raw and adjusted results. A strategy may proceed on economic and replication evidence even when classical significance is limited, but the uncertainty must cap risk and claims.

## Gate 8 — selection-aware performance

Use:

- **White-style reality check** across candidate return columns;
- **Deflated Sharpe** using trial count and distribution shape;
- **PBO** using combinatorial symmetric cross-validation;
- nested outer folds for the complete model/policy selection process.

The purpose is to estimate whether the research process reliably selects winners rather than whether one fixed historical column looks good.

## Gate 9 — parameter topology

Map performance around selected parameters: reward R, stop buffer, reference age, time tolerance, session boundary, model threshold, and feature window. Prefer stable plateaus. A sharp optimum is treated as fragile and requires a simpler nearby parameter, independent confirmation, or retirement.

Suggested topology report:

| Parameter | Chosen | Neighbor range | Positive neighbors | Worst neighbor | Interpretation |
|---|---:|---:|---:|---:|---|

## Gate 10 — cost and fill stress

Run normal, 1.5x, 2x, and severe spread/slippage; one-bar delay; skipped fills; worse-side ambiguity; price rounding; minimum stop; gap; and lower fill rate. State the cost multiplier and delay at which lower-bound expectancy becomes unacceptable. This becomes a live kill threshold.

## Gate 11 — tail dependence

Remove best 1%, 5%, and 10% trades; best days/weeks/clusters; and the single strongest regime. For convex strategies, do not demand tail independence, but require recurrence across independent periods and a coherent payoff mechanism. Scale risk based on expected drought and tail uncertainty.

## Gate 12 — cross-feed and cross-market replication

Use canonical futures/exchange data when available and target-broker data for realism. Reconcile event definitions first. Test alternate feeds, symbol pairs, periods, and related markets. A broker-specific edge may be real, but it is classified as microstructure/feed-specific and monitored accordingly.

## Gate 13 — fold and regime stability

Show every fold, year, session, direction, symbol, and volatility regime. Define acceptable heterogeneity. A strategy can be regime-specific if the regime is causally identifiable and the classifier is stable. One hidden favorable period is not a strategy.

## Gate 14 — confirmation freeze

Hash the complete research specification before untouched confirmation. Run once. Any change creates a new version and future confirmation. Do not repeatedly expose the same test interval through dashboards, manual review, or model selection.

## Gate 15 — paper and live reconciliation

Even strong historical evidence can fail operationally. Compare live event counts, features, model decisions, candidate prices, fill rates, costs, and outcomes. Paper/live divergence beyond tolerance blocks promotion. Live results enter monitoring, not automatic model updates.

## Suggested promotion matrix

| Evidence | Dataset ready | OOS validated | Paper ready | Micro-live | Scaled |
|---|---:|---:|---:|---:|---:|
| causality audit | pass | pass | pass | pass | pass |
| unique clusters | minimum | higher | higher | forward minimum | broad regimes |
| matched baseline | defined | beaten | beaten | monitored | stable |
| FDR/selection tests | planned | pass/qualified | pass | unchanged | reviewed |
| cost stress | preliminary | pass | pass | actual costs | capacity pass |
| cross-feed | planned | at least one | required for sensitive strategies | monitored | stable |
| execution fidelity | n/a | n/a | rehearsal pass | pass | pass |

## Implementation notes

The patch supplies reference implementations. For an official high-capital decision, independently review formulas and use robust scientific libraries where needed. Preserve the same input/output artifacts so stronger implementations are interchangeable. The suite is a gate framework, not a magic certificate.
