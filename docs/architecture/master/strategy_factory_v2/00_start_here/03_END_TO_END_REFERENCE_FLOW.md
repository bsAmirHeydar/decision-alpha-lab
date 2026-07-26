---
title: "End-to-End Reference Flow"
domain: strategy-factory-v2
status: canonical
language: en
version: 2.0.0
tags:
  - alpha-lab
  - strategy-factory
  - anatomy-to-decision
---

# Reference flow

## Stage 0 — Doctrine freeze

The anatomy has a written definition, examples, counterexamples, known-time semantics, invalidation, lifecycle, and kill criteria.

## Stage 1 — Event production

The anatomy engine emits a canonical event. The adapter maps domain-specific fields into stable identity, direction, references, timestamps, cluster identity, and metadata.

## Stage 2 — Context construction

Feature providers form a dependency DAG. At startup the graph is topologically sorted. At decision time only dirty providers recompute; fresh cached outputs are reused. Each FeatureValue carries source, version, known time, and availability.

## Stage 3 — Candidate construction

The compiled plan contains a bounded list of candidate templates. Entry, stop, and exit policy callables are resolved once. Runtime does not create a Cartesian product.

## Stage 4 — Decision inference

Each candidate receives context plus candidate-specific numeric fields. Approved local models emit probability, expectancy, MFE, MAE, uncertainty, or other promoted outputs. Calibrators transform raw scores. Utility weights rank candidates.

## Stage 5 — Abstention

The engine abstains when critical context is missing, probability or expectancy is too low, uncertainty is too high, candidate margin is insufficient, the event is duplicated, latency budgets are breached under a strict policy, or model/schema versions mismatch.

## Stage 6 — Risk authorization

A separate gate checks risk per thesis, correlated cluster exposure, symbol and strategy limits, daily losses, open risk, account state, kill switches, and lifecycle state.

## Stage 7 — Execution

Paper and live adapters consume the same intent. Broker preflight validates tick size, stops level, volume step, session state, margin, duplicate orders, expiration, and mode.

## Stage 8 — Trace and reconciliation

Every request, response, fill, modification, partial fill, rejection, cancellation, close, and reconciliation event is linked to the original anatomy event, candidate, decision, plan, and model hashes.

## Stage 9 — learning loop

Forward outcomes are appended to a versioned observation store. They do not mutate the active model automatically. Retraining creates a challenger artifact that must pass the full promotion process.
