---
type: strategy-factory-reference
status: canonical
title: "Canonical Schema Reference"
tags:
  - strategy-factory
  - contracts
  - schema
  - reference
---

# Canonical Schema Reference

## Contract philosophy

The schema is the stable bridge among MQL5 anatomy engines, Python research, machine learning, paper execution, and live broker integration. Strategy-specific vocabulary belongs in namespaced metadata or registered features. Shared columns retain identical meaning across all strategies.

## AnatomyEvent

| Field | Type | Required | Meaning and invariant |
|---|---|---:|---|
| `event_id` | string | yes | deterministic semantic identity |
| `strategy_id` | string | yes | stable family ID |
| `strategy_version` | semver string | yes | anatomy semantics version |
| `symbol` | string | yes | execution or primary symbol |
| `reference_symbol` | string/null | no | paired/reference market |
| `direction` | long/short/neutral | yes | anatomy direction, not trade permission |
| `event_time_utc` | timestamp | yes | time underlying action occurred |
| `known_time_utc` | timestamp | yes | earliest deterministic knowledge time |
| `confirmation_time_utc` | timestamp | yes | earliest candidate eligibility time |
| `reference_price` | float | yes | canonical price anchor |
| `invalidation_price` | float/null | no | anatomy failure boundary |
| `timeframe` | string/null | no | source timeframe/cycle |
| `session` | string/null | no | canonical session ID |
| `parent_event_id` | string/null | no | lineage |
| `market_event_cluster_id` | string/null | expected | underlying episode identity |
| `anatomy_state` | string | yes | approved lifecycle state |
| `source_hash` | string | expected | source-content identity |
| `metadata` | map | no | namespaced anatomy fields |

Hard time invariant:

```text
event_time_utc <= known_time_utc <= confirmation_time_utc
```

Neutral events may be used as context or vetoes but cannot generate directional candidates without a separate directional decision contract.

## FeatureValue and FeatureSnapshot

Each `FeatureValue` contains name, value, known time, source, version, and missing reason. The snapshot contains event ID, decision timestamp, schema version, producer version, and a unique list of features.

Hard invariant:

```text
feature.known_time_utc <= snapshot.snapshot_time_utc
```

Recommended metadata registry for every feature:

| Attribute | Example |
|---|---|
| name | `divergence_strength` |
| type | float32 |
| unit | normalized ATR |
| source | EXP0017 adapter |
| availability | confirmation close |
| null policy | explicit missing category |
| range | `[0, 5]` |
| transformation | train-only robust scaler |
| version | `1.2.0` |
| prohibited derivation | no future reference retirement |

Snapshot rows must be immutable. Later joins may add outcomes but may not alter the feature artifact.

## TradeCandidate

| Field | Meaning |
|---|---|
| `candidate_id` | hash of event + policies + parameters + manifest |
| `event_id` | source event |
| `entry_policy_id` | registered entry behavior |
| `stop_policy_id` | registered initial risk behavior |
| `exit_policy_id` | registered management behavior |
| `eligible_from_utc` | earliest order eligibility |
| `expires_at_utc` | order/thesis expiry |
| `entry_type` | market, limit, stop, or approved composite |
| `entry_price` | normalized pre-cost price |
| `stop_price` | initial hard invalidation/risk price |
| `target_price` | optional target |
| `risk_distance` | absolute entry-stop distance |
| `max_holding_seconds` | time horizon |
| `cost_model_id` | explicit execution assumptions |
| `policy_parameters` | immutable parameter map |

Long geometry requires stop below entry and target, if present, above entry. Short geometry is symmetric. `risk_distance` must exactly match absolute entry-stop distance within tick tolerance.

## OutcomeRecord

Outcome records are candidate-level and preserve no-fill outcomes.

Required economic fields:

- filled and fill timestamp/price
- exit timestamp/price/reason
- gross R and net R
- MFE R and MAE R
- spread, slippage, commission in R
- holding duration
- ambiguous-bar count
- label end time
- lifecycle metadata

`label_end_time_utc` is the last timestamp used to determine any target label. It drives purging and is not optional for official ML datasets.

## ModelDecision

A model decision stores model identity/version/hash, event and candidate, decision time, action, probability, expected net/MFE/MAE, confidence tier, feature schema, and explanations. It does not store volume. A trade action must reference an existing candidate. `skip` is a valid and often preferred action.

## ExecutionIntent

Intent is the only object accepted by an execution bridge. It contains candidate geometry, volume, risk dollars, strategy/version, optional model decision, creation time, and expiry. It is created only after decision and before risk evaluation. A risk-approved intent may be reserved and submitted. Rejected intents remain in the audit log.

## ExecutionTrace

Trace stores request/response times, adapter, broker order/deal/position IDs, state, fill, volume, slippage, reject reason, and metadata. Traces are append-only state transitions. Broker truth can supersede local expectation but cannot alter the original intent.

## RunManifest

A run manifest should include:

```json
{
  "run_id": "...",
  "git_commit": "...",
  "strategy_id": "...",
  "strategy_version": "...",
  "manifest_hash": "...",
  "source_data_hash": "...",
  "dataset_hash": "...",
  "feature_set_hash": "...",
  "candidate_set_hash": "...",
  "label_set_hash": "...",
  "fold_plan_hash": "...",
  "model_hash": "...",
  "cost_model_version": "...",
  "simulation_policy_version": "...",
  "random_seed": 7,
  "status": "research_complete"
}
```

## Recommended table keys

- bars: `(feed_id, symbol, timeframe, timestamp_utc)`
- events: `event_id`
- snapshots: `snapshot_id`, unique `event_id` for one decision point
- candidates: `candidate_id`
- outcomes: `candidate_id + simulation_version`
- decisions: `decision_id`
- intents: `intent_id`
- traces: `(intent_id, transition_sequence)`

## Schema evolution

Adding nullable metadata is usually minor. Changing time semantics, identity fields, units, candidate geometry, label definition, or cost interpretation is major. Major versions require new artifacts and cannot share model compatibility with earlier versions.

## Serialization rules

Use UTC ISO-8601 in JSON/CSV and timezone-aware timestamp in Parquet. Use finite numeric values; represent unavailable values as null plus missing reason. Do not serialize enums using language-specific ordinal integers. Maps are canonicalized with sorted keys before hashing.

## Reconciliation rules

MQL5 and Python event payloads should produce a common canonical hash. Any mismatch is reported by field. Candidate price differences are checked after symbol tick normalization. Research and live model decisions must match model hash, feature hash, and candidate hash.
