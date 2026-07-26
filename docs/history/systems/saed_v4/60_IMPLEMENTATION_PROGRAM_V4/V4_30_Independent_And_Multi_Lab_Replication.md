---
title: V4-30 Independent And Multi Lab Replication
status: accepted-reference
version: 1.0.0
created: '2026-07-13'
updated: '2026-07-16'
capability_tier: core-production-reference
tags: [saed-v4, implementation, independent-replication, multi-lab, blinded-exchange]
---

# Phase V4-30: Independent And Multi-Lab Replication

## Mission

Create a closed research-control boundary in which the exact V4-29 sealed-evaluation evidence is frozen into a replication package, laboratories are registered under explicit independence rules, protocol and metrics are preregistered before package opening, each eligible laboratory receives a blinded assignment and exactly one deterministic run, and cross-lab agreement is reconciled without granting decision or execution authority.

The reference implementation uses synthetic laboratory identities and local deterministic environments. It validates contracts and failure behavior; it is not evidence of external institutional reproduction.

## Entry gates

- Exact V4-29 certificate and handoff are immutable and hash verified.
- Candidate, dataset commitment, protocol, metric definitions and disclosure policy are frozen.
- Hidden-evaluation token reuse and adaptive final-set tuning remain prohibited.
- Independence dimensions and minimum-lab thresholds are preregistered.
- Laboratory identities, keys, operators, environments and infrastructure relations are declared before assignment.
- Raw protected rows, hidden labels, custody key shares and researcher adaptation paths are unavailable.

## Engineering slices

1. Closed contract and schema freeze for upstream intake, protocol, package, laboratories, environments, assignments and evidence.
2. Stable package identity over candidate, protocol, upstream certificate and aggregate disclosure commitments.
3. Laboratory registration with organization, operator, key, environment, funding, infrastructure and originator-relation declarations.
4. Pairwise independence matrix and deterministic eligibility decision.
5. Blinded package exchange with role-separated sender, receiver, package seal and transport receipt.
6. Immutable preregistration of hypotheses, metrics, tolerances, failure policy and one-run budget.
7. Default-deny environment attestation for network, package installation, clock, shell and mutable dependency access.
8. Exactly one deterministic synthetic run per eligible lab with append-only run accounting.
9. Aggregate-only result envelopes with semantic hashes and policy-approved metrics.
10. Cross-lab semantic hash reconciliation, metric-tolerance reconciliation and coverage analysis.
11. Explicit disagreement taxonomy, quarantine-first adjudication and unresolved-disagreement handling.
12. Append-only registration, preregistration, run, result and adjudication chains.
13. Known-time, future-suffix, leakage, security, model-risk, replay and authority reviews.
14. Restricted handoff to V4-31 formal verification and safety case.

## Acceptance gates

- Every contract is closed and rejects unknown fields.
- V4-29 certificate and handoff hashes match the frozen example exactly.
- Package identity is deterministic and mutation-sensitive.
- At least three synthetic laboratories satisfy all declared independence dimensions.
- No pair shares organization, operator, signing key, environment identity or mutable runtime state.
- Preregistration precedes assignment opening and run start.
- Each laboratory executes exactly once; retries and adaptive reruns fail closed.
- Network, interactive shell, package installation and hidden-row export are denied.
- Every result envelope is aggregate-only and bound to package, laboratory, environment and preregistration identities.
- Semantic output hashes agree across all eligible labs.
- All frozen metrics reconcile within preregistered tolerances.
- Any semantic, metric, identity, ordering, timing or chain disagreement quarantines the bundle.
- Future-suffix mutation cannot change the accepted prefix result.
- All replication ledgers are contiguous, append-only and mutation-sensitive.
- UCEE authority remains unchanged and all operational authority flags remain false.
- Static MQL5 evidence is distinguished from MetaEditor compilation and runtime parity.

## Deliverables

- Python reference package, CLI, synthetic fixtures, tests and deterministic golden generator.
- Closed JSON schemas and exact golden artifacts.
- Synthetic three-lab replication evidence bundle and reconciliation certificate.
- MQL5 static mirrors and compile-oriented harness.
- Modular Obsidian phase delivery and atomic concept libraries.
- QA report, phase status, inventory, file index, SHA-256 ledger and patch manifest.
- Restricted handoff to V4-31.

## Non-goals and claim ceiling

This phase does not claim real laboratory independence, external institutional signatures, physical separation, externally operated infrastructure, real protected-data custody, real alpha, prospective success, promotion authorization, runtime compilation, Python/MQL5 parity, risk allocation, order submission, broker qualification, production authorization, online learning or live trading. External evidence must be attached in a later acceptance process before any such claim is made.
