---
title: "Any positive partial fill triggers fill-based consumption"
status: accepted
phase: FP-I15
---
# Any positive partial fill triggers fill-based consumption

## Decision

Any positive partial fill triggers fill-based consumption. The decision is encoded in the FP-I15 public contracts, golden fixtures, MQL5 mirror, and authority tests.

## Context

Paper execution must exercise real geometry, quota, lifecycle, and reconciliation behavior without claiming that the unresolved live quota-consumption choice has been answered.

## Consequences

The behavior is deterministic, replayable, and safe for synthetic research. Any incompatible change requires a phase or contract version bump. Live broker mutation remains outside this decision.
