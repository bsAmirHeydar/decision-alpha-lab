---
title: NDS Entry Implementation Roadmap
status: active
version: 1.0.0
---
# NDS Entry Implementation Roadmap

## Phase 51 — Entry Transition Scaffold — implemented

- structure snapshot cache;
- valid-Hook source selection;
- explicit direction mapping;
- Zone adapter seam;
- Setup, Trade Plan, Command Preview rows;
- CSV exports;
- safe default blocks;
- static contract QA.

## Phase 52 — Canonical Zone Builder

- implement approved source points;
- boundary construction;
- Zone identity and revision;
- positive/negative symmetry tests;
- Hook-family-specific adapters.

## Phase 53 — Zone Lifecycle Engine

- birth;
- activation;
- touch;
- consumption;
- weakening;
- invalidation;
- expiry;
- persistent ledger.

## Phase 54 — Setup Registry

- retain all eligible Setups;
- deterministic IDs;
- deduplication;
- primary/secondary status;
- multi-timeframe nesting;
- conflict and coexistence policy.

## Phase 55 — Trade Plan Builder

- approved entry models;
- stop/death separation;
- destination and open-tail management;
- plan revisions;
- optionality metrics.

## Phase 56 — Paper Command Lifecycle

- command ledger;
- touch/fill simulation;
- cancel/expire/replace;
- partial lifecycle;
- MFE/MAE and path metrics.

## Phase 57 — Independent Risk Engine

- account-independent risk units first;
- portfolio constraints;
- symbol metadata;
- volume normalization;
- capital authorization interface.

## Phase 58 — Broker Adapter Dry Run

- normalized request;
- tick and stop-level validation;
- duplicate protection;
- transaction-state model;
- still no send.

## Phase 59 — Controlled Paper-Live Rehearsal

- shadow requests;
- broker-state reconciliation;
- restart recovery;
- operator runbook;
- kill switch tests.

## Phase 60 — Real Execution Promotion Gate

Real sending remains prohibited until independent review confirms:

```text
Canon complete
paper evidence adequate
risk engine approved
broker adapter approved
restart recovery tested
kill switch tested
operator profile explicit
```
