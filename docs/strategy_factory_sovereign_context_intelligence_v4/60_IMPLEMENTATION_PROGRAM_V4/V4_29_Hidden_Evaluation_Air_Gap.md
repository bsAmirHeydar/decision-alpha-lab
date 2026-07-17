---
title: V4-29 Hidden Evaluation Air Gap
status: accepted-reference
version: 1.0.0
created: '2026-07-13'
updated: '2026-07-16'
capability_tier: core-production-reference
tags: [saed-v4, implementation, hidden-evaluation, air-gap, sealed-evaluator]
---

# Phase V4-29: Hidden Evaluation Air Gap

## Mission

Create a closed research-control boundary in which a candidate is frozen before protected evidence is opened, a custodian-controlled evaluator receives exactly one authorization token, evaluation occurs in an isolated deterministic workspace, all access is append-only accounted, and only a policy-approved aggregate disclosure leaves the sealed zone.

This phase closes the architectural gap between repeated research selection and a genuinely protected final evaluation. The local implementation uses a synthetic sealed fixture solely to validate control semantics. It does not claim possession of a real hidden final set or independent institutional custody.

## Entry gates

- The exact SAED V4-28 certificate and handoff are immutable and hash verified.
- The complete search/exposure ledger and online-FDR outcome are frozen.
- Candidate artifact, preprocessing, feature contract, inference entrypoint, evaluation protocol and pass rule are committed before token issue.
- Custodian identities, threshold policy, protected commitment, storage zone and disclosure policy are frozen.
- Network egress, interactive debugging, adaptive retries, raw-row disclosure and researcher key access are denied.

## Implemented engineering slices

1. Closed contract and schema freeze for upstream intake, custody, topology, protocol, disclosure, candidate and sealed fixture.
2. Deterministic canonical hashing, stable identities and append-only chain verification.
3. Protected-custody receipt with threshold-custodian policy and commitment verification.
4. Air-gap topology attestation with explicit zones, allowlisted flows and default-deny transport.
5. Irreversible candidate submission commitment and dependency closure.
6. One-shot token issue, binding, consumption and replay prevention.
7. Sealed evaluator with deterministic inference and aggregate metric calculation.
8. Baseline comparison and precommitted pass-rule evaluation.
9. Aggregate-only disclosure envelope with field allowlist, precision reduction and row-level denylist.
10. Query, token, transport and custody ledgers with contiguous append-only hash chains.
11. Known-time, future-suffix, hidden-label, path, environment, network and side-channel controls.
12. Security, model-risk, authority, certificate, replay and V4-30 handoff artifacts.
13. Golden, negative, mutation, replay, schema, Obsidian and MQL5-static QA.

## Acceptance gates

- Zero unknown fields in every closed contract.
- Exact V4-28 certificate and handoff hash verification.
- Candidate commitment precedes token issue and evaluation time.
- Token is bound to one candidate, one dataset commitment and one protocol; it can be consumed once.
- Research-zone access to hidden labels, plaintext protected rows and custody key shares is zero.
- Evaluator network access, package installation, shell escape and interactive adaptation are denied.
- Result egress is restricted to the frozen disclosure allowlist.
- Query, custody, token and transport chains are contiguous and mutation-sensitive.
- Repeated evaluation, token reuse, post-commit candidate mutation, future-suffix injection and unknown fields fail closed.
- Baseline comparison is preserved and the reference pass rule is evaluated exactly as frozen.
- UCEE authority remains unchanged.
- Static MQL5 evidence remains explicitly distinct from MetaEditor compilation and runtime parity.

## Deliverables

- Python reference package, CLI, tests and reproducible golden generator.
- Closed JSON schemas, examples and exact golden artifacts.
- Synthetic sealed evaluation fixture with explicit non-production classification.
- MQL5 static mirrors and a compile-oriented harness.
- Modular Obsidian phase delivery and atomic concept libraries.
- QA report, phase status, artifact inventory, file index, SHA-256 ledger and patch manifest.
- Restricted handoff to V4-30 independent and multi-lab replication.

## Non-goals and claim ceiling

This reference does not claim real alpha, a real protected final dataset, external custodian independence, cryptographic HSM enforcement, operating-system-level air-gap certification, independent replication, prospective success, promotion authority, runtime compilation, runtime parity, risk allocation, order submission, broker qualification, production authorization, online learning or live trading. Any such claim requires external evidence attached to a later acceptance certificate.
