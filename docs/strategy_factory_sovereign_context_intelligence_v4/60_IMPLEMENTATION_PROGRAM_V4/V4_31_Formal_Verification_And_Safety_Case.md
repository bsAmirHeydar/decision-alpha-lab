---
title: V4-31 Formal Verification And Safety Case
status: canonical
version: 1.0.0
created: '2026-07-16'
updated: '2026-07-16'
capability_tier: core-production-reference
tags:
  - saed-v4
  - formal-verification
  - safety-case
  - research-only
---

# Phase V4-31: Formal Verification And Safety Case

## Mission

V4-31 converts the accepted V4-30 replication reference into a closed, deterministic and independently reviewable formal-verification and safety-case evidence package. The phase defines a finite transition-system semantics, a frozen invariant catalog, bounded temporal properties, explicit proof obligations, mutation adequacy, counterexample preservation, hazard-control traceability, residual-risk accounting and a GSN-compatible assurance case. All results remain evidence for research governance; they are not permission to promote, allocate risk, compile a runtime, submit an order or release production software.

## Authority boundary

UCEE remains the sole authority for promotion, runtime policy, portfolio allocation and execution. Every V4-31 authority flag is false. A failed obligation, surviving mutation, uncontrolled hazard, incomplete traceability edge, non-deterministic replay, unknown contract field or unsupported upstream artifact causes rejection or quarantine. No manual override is represented in the reference state machine.

## Contract

The formal domain is a finite synthetic state machine with closed variable domains, an explicit initial state, unique actions and authority-free transitions. Expressions are parsed through an AST allowlist; function calls, attribute access, imports, subscripts, arithmetic side effects and builtins are unavailable. Reachability uses deterministic breadth-first exploration, making reported reachable counterexample traces minimal in transition count. Temporal semantics are intentionally bounded and declared; this phase does not claim full unbounded LTL/CTL model checking.

Artifacts are closed JSON contracts with `additionalProperties=false`, deterministic identities and SHA-256 content binding. Exact golden/schema pairs are generated for the upstream receipt, model, graph, property catalogs, verification reports, mutation and counterexample ledgers, proof registry and discharge ledger, hazard and mitigation artifacts, assurance case, traceability, reviews, authority boundary, evidence bundle, certificate and handoff.

## Formal method

The reference verifier explores every reachable state in the finite declared model. State invariants are checked over all reachable states. Transition properties are checked over every reachable transition instance. Bounded `leads_to_within` properties use graph search from every trigger state. Terminality and reachability are explicit property kinds. The verifier never silently treats a bounded result as a general proof.

The mutation suite injects authority acquisition, missing qualification preconditions, counterexample suppression, unsupported-evidence acceptance, missing fail-closed paths, inconsistent evidence flags and post-decision mutation. Every seeded defect must be killed by one or more predeclared detectors. Surviving mutations block the proof ledger and certificate.

## Safety case

The hazard register combines STPA-style unsafe-control-action statements with bounded FMEA-style severity, likelihood and detectability scores. Each hazard binds to explicit controls and proof obligations. Control effectiveness is a synthetic reference parameter used only to exercise residual-risk accounting. Residual-risk thresholds are not production risk acceptance criteria.

The assurance case is a closed directed acyclic graph using GSN-compatible goal, strategy, context, assumption, justification and solution nodes. Every node must be reachable from the root. Every goal or strategy must have outgoing support. Every declared evidence key must resolve to a deterministic content hash. Missing evidence, cycles or disconnected nodes fail closed.

## Verification

Acceptance requires all invariants and bounded temporal properties to pass, a 100 percent seeded mutation score, preservation of every counterexample, discharge of every proof obligation, complete hazard-control coverage, bounded residual risk within synthetic thresholds, a valid assurance graph, complete evidence traceability, closed contracts, known-time review, security review, deterministic replay, exact logical reproduction and zero authority.

Python tests include positive reference acceptance, per-property checks, per-mutation checks, proof-obligation checks, hazard and assurance checks, schema-pair validation, unknown-field rejection, hostile expression tests, upstream authority violations, graph cycles, missing evidence and repeated deterministic runs. MQL5 files are static research mirrors only and contain no order-placement surface.

## Claim ceiling

The accepted certificate means only that the bundled finite synthetic reference model satisfies the bundled closed properties under the implemented bounded semantics and that the bundled safety case is structurally complete. It does not prove arbitrary Python or MQL5 code, a deployed runtime, real-market correctness, real alpha, prospective performance, external theorem-prover certification, MetaEditor compilation, broker behavior or production safety.

## Handoff

V4-32 may use the hash-bound formal constraints, proof obligations, hazard controls and authority boundary when defining the Multi-Agent Research Constitution. No agent may inherit promotion, runtime, risk, execution, production, online-learning or live-trading authority from this handoff.
