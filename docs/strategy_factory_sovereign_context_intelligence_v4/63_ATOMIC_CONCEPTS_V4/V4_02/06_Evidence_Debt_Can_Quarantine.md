---
title: Evidence Debt Can Quarantine
status: implemented
version: 1.0.0
phase: V4-02
created: '2026-07-13'
updated: '2026-07-13'
tags: [saed-v4, v4-02, atomic-concept]
---
# Evidence Debt Can Quarantine

## Definition

Evidence Debt Can Quarantine is a non-negotiable invariant of the Context Digital Twin Kernel.

## Operational consequence

Any component that violates this invariant must reject, degrade, conflict or quarantine the Twin. It must never silently continue.

## Verification

The invariant is represented in closed schemas, deterministic Python code, negative fixtures, property tests and the limited MQL5 diagnostic mirror.

## Related

- [[00_MOC_V4_02_Context_Digital_Twin_Kernel]]
- [[38_Acceptance_Gates]]
