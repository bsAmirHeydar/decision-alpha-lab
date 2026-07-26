---
type: strategy-factory-reference
status: canonical
title: "Complete Test Matrix — Data, Research, Models, and Execution"
tags:
  - strategy-factory
  - testing
  - reference
---

# Complete Test Matrix — Data, Research, Models, and Execution

## Purpose

This matrix turns the platform's invariants into executable tests. A future anatomy plugin should select all applicable cases and add domain-specific fixtures. Compilation alone is never sufficient.

## Data and clock tests

| ID | Test | Expected failure behavior |
|---|---|---|
| D01 | required schema/type | quarantine file/run |
| D02 | UTC timezone aware | reject row or source |
| D03 | DST transition | exact session mapping |
| D04 | out-of-order bars | sort only if policy permits; warn/hash |
| D05 | duplicate symbol/time | reject duplicate ambiguity |
| D06 | missing bars | reason-coded gap, no silent forward fill |
| D07 | invalid OHLC geometry | reject |
| D08 | bid > ask | reject |
| D09 | nonfinite/zero prices | reject |
| D10 | cross-symbol skew | enforce tolerance |
| D11 | feed correction | new data version |
| D12 | futures roll | explicit contract policy |

## Anatomy tests

- deterministic replay produces identical payload and hash;
- renderer or chart-object changes do not change events;
- event/known/confirmation ordering;
- no current-bar use when closed-bar doctrine applies;
- reference freshness and retirement;
- duplicate and one-signal-per-event;
- simultaneous events remain simultaneous;
- parent/child ownership;
- cross-day/session reset;
- invalidation transition;
- partial history and unavailable paired symbol;
- stable IDs after restart.

## Feature tests

- each feature known time ≤ snapshot time;
- unique names and registered types;
- forbidden outcome feature rejected;
- training-only transform fit;
- unknown category behavior;
- missing reason and fallback;
- feature range/OOD flag;
- future time shift causes rejection;
- label permutation destroys performance;
- source version appears in lineage.

## Candidate tests

- deterministic Cartesian product;
- bounded maximum and explicit pruning;
- compatibility exclusions;
- long/short symmetry;
- entry/stop/target geometry;
- risk distance/tick rounding;
- expiry later than eligibility;
- market, limit, stop, gap, and creation-bar fill;
- no duplicate candidate ID;
- multiple candidates share event/cluster;
- scale-in respects parent risk.

## Outcome tests

Create hand-calculated bars for:

- target only;
- stop only;
- target and stop same bar under all ambiguity policies;
- market gap beyond stop;
- unfilled limit expiry;
- stop-entry gap;
- time exit;
- data end;
- partial exit and runner;
- break-even transition;
- costs and slippage;
- MFE/MAE exact values;
- label end time.

## Validation tests

- random split prohibited in official manifest;
- train/test row disjoint;
- cluster disjoint;
- label horizon purged;
- embargo applied;
- transformers fit on train only;
- inner selection does not access outer test;
- fold artifact deterministic;
- cluster/block bootstrap reproducible with seed;
- BH q-values monotonic in ranked order;
- PBO and reality-check probabilities bounded;
- trial count included in DSR;
- placebo and shuffled labels fail.

## Model tests

- deterministic prediction for fixed artifact;
- test-vector parity between Python and MQL5/inference runtime;
- probability within `[0,1]`;
- missing/OOD fallback;
- feature order and type mismatch rejected;
- model hash mismatch rejected;
- calibration table valid;
- ranker never selects undeclared candidate;
- `skip` available;
- threshold frozen;
- challenger cannot overwrite champion.

## Risk tests

- per-intent limit;
- daily reserved risk;
- daily realized loss lock;
- portfolio, symbol, strategy, and cluster limits;
- concurrent position cap;
- allowlist;
- stale intent;
- kill switch;
- partial fill reservation;
- cancellation release;
- restart reconstruction;
- negative/zero volume and risk rejected.

## Broker tests

- symbol unavailable;
- market closed;
- stale quote;
- min/max/step volume;
- stops/freeze level;
- margin rejection;
- timeout with eventual acceptance;
- duplicate retry;
- partial fill;
- manual cancellation/modification;
- unknown broker position;
- netting/hedging account behavior;
- request/response trace completeness.

## Monitoring tests

- event-rate anomaly;
- feature missing spike;
- score distribution drift;
- latency breach;
- repeated reject circuit breaker;
- slippage/cost breach;
- state mismatch;
- alert routing;
- incident artifact capture;
- rollback to previous model/config.

## Acceptance evidence

For each release, publish test command, environment, result count, skipped tests, MQL5 compile evidence where applicable, replay fixture hashes, and known untested broker conditions. A passed automated suite does not replace demo and micro-live rehearsal.
