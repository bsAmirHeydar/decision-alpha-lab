---
title: Runbook — Build the Counterfactual Outcome Cube
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- runbook
- operations
---

# Purpose

Generate executable, path-aware and cost-aware outcomes for every compatible treatment sibling of each context occurrence without selection bias.

# Entry conditions

- Context and treatment universe hashes are frozen.
- Canonical event data and broker/economics profiles pass quality checks.
- Replay engine version and ambiguity policy are admitted.

# Roles and separation of duties

| Role | Responsibility |
|---|---|
| Replay Engineer | Builds deterministic path and fill simulation. |
| Execution Scientist | Owns spread, slippage, fill, impact and broker semantics. |
| Data Validator | Audits point-in-time lineage and path completeness. |
| Research Owner | Consumes outcomes but cannot edit replay truth. |

# Procedure

## Step 1 — Enumerate occurrences and siblings

**Action**

Materialize each valid context occurrence and compile every compatible treatment plus Skip under one opportunity-cluster ID.

**Mandatory output**

- Occurrence-treatment index.

**Stop conditions**

- Sibling count differs across reruns without a version change.

## Step 2 — Resolve executable path

**Action**

Load bid/ask or approved lower-timeframe path, market status, symbol specifications and event-time revisions.

**Mandatory output**

- Path replay manifest.

**Stop conditions**

- Path resolution is too coarse for stop/target/trail ordering and no conservative ambiguity rule exists.

## Step 3 — Simulate trigger and fill

**Action**

Apply order type, trigger, expiration, queue/fill, partial fill, slippage and adverse-selection rules.

**Mandatory output**

- Fill event ledger.

**Stop conditions**

- Non-fill, missed opportunity or partial fill is discarded.

## Step 4 — Simulate risk and exits

**Action**

Execute stop, target, partial, trail, time exit, context invalidation and management state machines.

**Mandatory output**

- Treatment state-transition ledger.

**Stop conditions**

- Multiple events in one interval cannot be ordered under the declared policy.

## Step 5 — Calculate economics and distributions

**Action**

Compute gross/net R, costs, MFE/MAE, holding, capital occupancy, tail, path and capacity labels.

**Mandatory output**

- Outcome cube partitions.

**Stop conditions**

- Mid-price or zero-cost assumptions silently replace executable economics.

## Step 6 — Certify determinism and lineage

**Action**

Rebuild samples, mutate future suffixes and compare hashes; trace rows to events/code/config.

**Mandatory output**

- Outcome-cube certification.

**Stop conditions**

- Decision-time fields change under future-only mutation.

## Step 7 — Publish immutable cube

**Action**

Write content-addressed partitions, schema, quality, support and known-time reports.

**Mandatory output**

- Signed outcome cube artifact.

**Stop conditions**

- Quality, lineage or ambiguity exceeds registered limits.

# Completion gates

- [ ] All siblings and non-fills retained.
- [ ] Path-dependent styles use sufficient path fidelity.
- [ ] Costs and broker rules are versioned.
- [ ] Future-suffix invariance passes.
- [ ] Cube is content-addressed and reproducible.

# Evidence retained

- `occurrence_treatment_index`
- `path_replay_manifest`
- `fill_event_ledger`
- `treatment_state_ledger`
- `outcome_cube`
- `outcome_cube_certification`

# Failure and escalation matrix

| Condition | Required response |
|---|---|
| Ambiguous intrabar ordering | Use conservative rule or exclude with explicit support loss. |
| Feed revision changes path | Create new data/cube version; preserve old evidence. |
| Broker rule unavailable | Mark unsupported; do not infer permissive behavior. |
| Replay defect discovered | Quarantine all downstream datasets/models via lineage graph. |

# Exit state

Outcome cube becomes eligible for dataset construction, not yet for model selection.

# Related architecture

- [[00_Home]]
- [[End_To_End_Reference_Architecture]]
- [[Adversarial_Anti_Overfit_Red_Team]]
- [[Failure_Modes_Kill_Criteria_And_Recovery]]
