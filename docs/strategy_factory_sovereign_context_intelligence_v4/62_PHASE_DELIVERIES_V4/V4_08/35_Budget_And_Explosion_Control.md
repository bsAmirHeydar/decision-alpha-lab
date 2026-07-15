---
title: Budget And Explosion Control
status: implemented-reference
phase: SAED_V4_08
version: 1.0.0
created: '2026-07-15'
updated: '2026-07-15'
capability_tier: core-production-reference
authority: reference-only
tags:
  - saed-v4
  - v4-08
  - outcome-cube
  - executable-path
---

# Budget And Explosion Control

## Institutional intent

Budget And Explosion Control defines a governed part of the SAED V4-08 Executable Path Outcome Cube. The phase consumes the immutable V4-07 action lattice, a known-time context snapshot, a bounded post-decision market path, an exact-versioned outcome policy and an exact-versioned cost registry. It emits one deterministic counterfactual outcome row for every lattice node without converting structural adjacency into preference, recommendation, capital allocation or execution authority.

## Contract boundary

The implementation is additive. V4-07 node identity, node hash, component hashes, feasibility certificates, Skip and Abstain actions and the upstream handoff hash are preserved. Any missing, duplicated, mutated or unexpected node causes complete-exposure validation to fail closed. Unknown fields are prohibited by JSON Schema Draft 2020-12 contracts with `additionalProperties: false`.

The phase may compile executable path specifications, evaluate deferred predicates using information known no later than the decision timestamp, simulate bounded counterfactual paths, apply frozen gap and ambiguity policies, compute side-aware costs, build path-event ledgers and emit a V4-09 handoff. It may not train a model, rank treatments, select a treatment, allocate risk, activate runtime, send an order or mutate the action lattice.

## Deterministic semantics

Identity is content-addressed from canonical JSON. Floating-point inputs are normalized before hashing. Rows are ordered by `node_id`; path events are chained by the previous event hash; cube integrity is summarized by a row Merkle root. Deterministic partitioning changes work placement only and does not change merge order or cube identity.

The same frozen inputs must reproduce the same execution specification, outcome row, row hash, cube hash, integrity receipt, summary and V4-09 handoff. Any difference is surfaced by semantic diff rather than silently accepted.

## Known-time and leakage controls

Context features with `observed_at_ms` later than `decision_time_ms` are rejected. Market observations belong to the post-decision outcome path and cannot be read by the decision-time compiler. Trigger predicates are evaluated only from the context snapshot. Outcome values are descriptive counterfactual evidence and are never reintroduced into V4-07 structural feasibility or node generation.

## Failure behavior

The implementation fails closed on future features, non-monotonic sequences, invalid OHLC geometry, negative spread, symbol mismatch, unknown cost models, missing reference features, non-positive initial risk, row-budget overflow, path-event overflow, incomplete exposure or upstream hash mismatch. Quarantine records preserve source hashes and reason codes without authorizing recovery through implicit fallback.

## Evidence classification

Python tests, schema validation, deterministic reproduction and MQL5 static validation are repository evidence. They do not constitute MetaEditor compilation, broker parity, real-market calibration, prospective performance, real alpha or production authorization. Those claims remain explicitly pending external evidence.

## Review questions

1. Does every V4-07 node produce exactly one row?
2. Are Skip and Abstain preserved as non-order outcomes?
3. Are decision-time features strictly known-time?
4. Are path observations consumed only after the decision timestamp?
5. Are ambiguity, gap and cost policies exact-versioned and hashed?
6. Does `net_r = gross_r - total_cost_r` hold for every row?
7. Are ranking, selection, capital and execution authority false?
8. Can the result be independently reproduced from indexed files and hashes?

## Related notes

- [[V4_07_V4_08_Handoff]]
- [[V4_08_Outcome_Row]]
- [[V4_08_Complete_Exposure]]
- [[V4_08_V4_09_Handoff]]

## Acceptance statement

This note is accepted when source, schemas, fixtures, tests, QA artifacts, MQL5 diagnostics and the V4-09 handoff agree on the same bounded semantics and when every stronger production claim remains blocked unless external evidence is attached.
