---
title: "V4-37 Delivery 009 — Lot Geometry"
status: accepted-reference
phase: SAED_V4_37
version: 1.0.0
updated: 2026-07-17
tags: [saed-v4, v4-37, portfolio-execution-economics]
---
# SAED V4-37 — Lot Geometry

## Purpose

**Lot Geometry** is a closed engineering slice of the SAED V4-37 Portfolio Execution Economics phase. It converts frozen context opportunities into inspectable cost, liquidity, capacity, portfolio and non-executable scheduling evidence without crossing into live execution authority.

## Contract

Inputs are known-time, content-addressed and schema-closed. Outputs carry deterministic identity, lineage and a research-only authority marker. Unknown fields, future-known observations, invalid currency paths, unbounded cost assumptions, missing liquidity, broken dependence geometry or authority-expanding flags are rejected.

## Engineering invariants

The implementation uses executable-price mathematics, full explicit and implicit cost accounting, bounded participation, depth-aware capacity, contract and lot geometry, cross-currency lineage, dependence-aware portfolio constraints, cash reserves, stress tests and independent review. Baselines remain immutable.

## Validation

Validation includes golden replay, negative fixtures, mutation tests, deterministic hashes, closed schemas, accounting identities, constraint checks, stress scenarios, authority assertions and MQL5 static mirrors. External MetaEditor, terminal, broker and capital evidence are not inferred from repository tests.

## Failure behavior

Any malformed, incomplete, stale, unsupported or authority-expanding input fails closed. The hypothetical allocation is rejected or reduced, the non-executable schedule remains unsubmitted, the baseline is preserved and the issue is escalated for human review.

## Handoff boundary

This artifact may contribute frozen portfolio, cost, capacity and scheduling evidence to V4-38. It transfers no order-submission, capital-activation, runtime-compilation, model-promotion or production authority.
