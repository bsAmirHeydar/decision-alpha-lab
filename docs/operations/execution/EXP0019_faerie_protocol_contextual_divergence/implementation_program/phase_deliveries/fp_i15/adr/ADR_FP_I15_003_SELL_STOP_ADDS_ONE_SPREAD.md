---
title: "Apply exactly one quote spread before sizing"
status: accepted
phase: FP-I15
---
# Apply exactly one quote spread before sizing

## Decision

Apply exactly one quote spread before sizing. The decision is encoded in the FP-I15 public contracts, golden fixtures, MQL5 mirror, and authority tests.

## Context

Paper execution must exercise real geometry, quota, lifecycle, and reconciliation behavior without claiming that the unresolved live quota-consumption choice has been answered.

## Consequences

The behavior is deterministic, replayable, and safe for synthetic research. Any incompatible change requires a phase or contract version bump. Live broker mutation remains outside this decision.
