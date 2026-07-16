---
title: V4-21 Robust Optimization And Regret
status: implemented-reference
version: 1.0.0
created: '2026-07-13'
updated: '2026-07-16'
capability_tier: research-reference
tags: [saed-v4, implementation, robust-optimization, regret, distributional-robustness]
---
# Phase V4-21: Robust Optimization And Regret

## Mission
V4-21 consumes the immutable, research-only V4-20 decision-focused treatment-selection evidence and adds a closed-contract robust-optimization and regret-analysis layer. The phase freezes ambiguity assumptions before evaluation, compiles bounded synthetic scenario families, evaluates pure and bounded-mixture treatment allocations, applies baseline non-inferiority, computes max/mean/dynamic regret, and emits a content-addressed research certificate.

## Authority boundary
This phase has no runtime authority, execution authority, promotion authority, production treatment-selection authority, or live risk-allocation authority. Every recommendation is synthetic and research-only. Fail-closed behavior resolves to the canonical `SKIP` allocation.

## Implemented engineering slices
1. Closed upstream intake and immutable hash verification.
2. Closed ambiguity, scenario, optimization, regret, baseline, and budget contracts.
3. Deterministic native and shocked scenario compiler.
4. Deterministic ambiguity-distribution vertex compiler.
5. Pure and two-treatment bounded allocation enumeration.
6. Maximin, minimax-regret, distributionally robust, robust-CVaR, and lexicographic objectives.
7. Manual baseline and skip preservation.
8. Bounded adversarial stress and leave-one-scenario-out stability.
9. Content-addressed certificate, replay receipt, budget ledger, and V4-22 handoff.
10. Python tests, closed schemas, Obsidian documentation, static MQL5 mirror, QA, inventory, and SHA-256 ledger.

## Evidence ceiling
The attached evidence establishes only a deterministic synthetic reference implementation. It does not establish real alpha, real policy value, prospective success, MetaEditor compilation, Python/MQL5 runtime parity, broker qualification, production authorization, or live trading safety.

## Handoff
The next phase is [[V4_22_Generative_Path_Stress_Lab|V4-22 Generative Path Stress Lab]]. It may consume only the signed research artifacts and must preserve all authority denials.
