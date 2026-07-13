---
type: strategy-factory-reference
status: canonical
title: "New Anatomy Implementation Packet — Complete Checklist"
tags:
  - strategy-factory
  - runbook
  - onboarding
  - reference
---

# New Anatomy Implementation Packet — Complete Checklist

## Goal

This packet is the exact work required to connect a new market view to the Strategy Factory. It is deliberately small compared with a standalone strategy project. Complete the packet in order; do not begin training or live execution before the earlier artifacts exist.

## A. Doctrine packet

Provide:

- strategy ID, owner, and semantic version;
- one-sentence thesis and null hypothesis;
- entities and object identity;
- states and transitions;
- direction semantics;
- event, known, and confirmation time;
- reference lifecycle and freshness;
- invalidation and expiration;
- duplicate and simultaneity policy;
- timeframe/symbol ownership;
- parent/child lineage;
- market-event clustering rule;
- explicit unknown and ambiguous cases;
- kill criteria.

Deliver `ANATOMY_DOCTRINE.md` and a hypothesis hash.

## B. Ten-to-twenty golden examples

Include normal long/short events, boundary times, same-candle events, missing references, stale references, invalidated objects, duplicate candidates, cross-day cases, DST/session transitions, and visual counterexamples. For each example, record expected event payload and why.

## C. Adapter implementation

Implement canonical event emission and feature snapshot. Use a CSV adapter first if direct engine integration would slow validation. Add stable IDs and source hashes. Ensure replay produces identical events. Add tests for all golden examples and future-feature rejection.

## D. Feature contract

For every feature, define type, unit, source, availability time, null policy, transformation, range, version, and prohibited derivation. Separate shared execution context from anatomy-specific state. Start with the smallest set that represents the hypothesis; do not expose every internal engine variable automatically.

## E. Candidate packet

Select a bounded set of entries, stops, exits, expiries, and cost model. Recommended first screen:

- two entry families: immediate and location/pullback;
- two stop families: exact invalidation and buffered invalidation;
- two or three exits: fixed R, structural/time, and optional runner later.

Define compatibility, fill rules, gap behavior, tick rounding, and maximum candidates. Hand-calculate several outcomes.

## F. Label and outcome packet

Declare primary net-R label, secondary classification/regression/ranking labels, label horizon, censoring, intrabar ambiguity, cost version, and no-fill handling. Materialize `label_end_time_utc`.

## G. Baselines and nulls

At minimum:

- always-trade fixed policy;
- simple time/session or trend baseline;
- anatomy-removed confirmation baseline;
- matched random/placebo appropriate to the theory.

State what outcome would demonstrate incremental information.

## H. Validation packet

Declare purged walk-forward folds, cluster key, embargo, minimum clusters, trial family, selection metric, confidence method, FDR, reality check, Deflated Sharpe/PBO, cost/delay stress, best-trade removal, parameter topology, and cross-feed/market plan.

## I. First vertical run

Produce:

```text
events
snapshots
candidates
outcomes
model_dataset
statistics
anti_overfit
QA report
```

Review event counts and several full traces before trusting aggregate results.

## J. AI packet

Only after baseline validation, define task, feature list, model ladder, threshold utility, calibration, fallback, model card, and challenger plan. A first model should be logistic/ridge or a conservative boosted tree. Include `skip` in decisions.

## K. Paper packet

Connect live adapter output to snapshots, candidates, model/rule decisions, risk gate, paper broker, persistence, restart, and monitoring. Compare every live event with historical semantics. Paper runs until forward evidence and operational coverage requirements are met.

## L. Promotion packet

Collect all artifacts, gate results, residual risks, approved symbols/sessions, risk cap, rollback, and review date. Promotion advances one state. A semantic change after promotion creates a new version.

## Expected marginal effort

After the factory is integrated, a clear anatomy should require:

- doctrine and manifest: hours to one day;
- adapter and fixtures: one to three days;
- candidate/outcome integration: one to two days;
- full historical run: mostly compute/data time;
- AI baseline: one to three days;
- paper integration: small if MQL5 bridge is already connected.

Ambiguous anatomy will still take longer because ambiguity is domain work, not engineering overhead.
