---
title: "Risk Reservation Before Selection"
tags: [uce-i17, atomic-concept, portfolio]
status: canonical
doc_version: 1.0.0
---
# Risk Reservation Before Selection

## Definition

Risk Reservation Before Selection is an identity-relevant rule in the UCE-I17 portfolio layer. It must be represented in schemas, code, fixtures, tests, telemetry and runtime evidence rather than being left as an undocumented convention.

## Safety consequence

A violation blocks allocation or activation. Aggregate utility cannot waive reservation, causality, capacity, dependence, reconciliation, stress or authority failures.

## Verification

The I17 test suite contains a positive vector and at least one negative or failure-injection path for this concept. The MQL5 mirror carries only bounded allocation contracts and has no order, broker or network authority.
