---
title: "Trade the protected symbol, never the hunter"
status: accepted
phase: FP-I15
---
# Trade the protected symbol, never the hunter

## Decision

Trade the protected symbol, never the hunter. The decision is encoded in the FP-I15 public contracts, golden fixtures, MQL5 mirror, and authority tests.

## Context

Paper execution must exercise real geometry, quota, lifecycle, and reconciliation behavior without claiming that the unresolved live quota-consumption choice has been answered.

## Consequences

The behavior is deterministic, replayable, and safe for synthetic research. Any incompatible change requires a phase or contract version bump. Live broker mutation remains outside this decision.
