---
title: Compile the Treatment Lattice
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: canonical
tags:
  - saed-v3
  - runbook
  - operations
---

# Mission

Convert payoff, entry, trigger, stop, exit, trail, management, time, cost, and capability primitives into a frozen finite lattice.

## Entry conditions

- Approved primitive registries.
- Context compatibility rules.
- Broker/runtime capability profile.

## Mandatory roles and separation of duties

- Setup researcher.
- Treatment compiler engineer.
- Execution auditor.
- Independent reviewer.

## Procedure

1. Load closed registries.
2. Generate candidate combinations.
3. Apply semantic, temporal, geometry, risk, broker, and runtime constraints.
4. Canonicalize duplicates.
5. Add Skip and Abstain.
6. Freeze lattice and search hierarchy.
7. Run mutation and identity tests.

## Mandatory outputs

- Treatment lattice.
- Constraint rejection ledger.
- Compatibility matrix.
- Lattice hash.

## Stop and escalation conditions

- Unbounded candidate count.
- Unknown unit or capability.
- Action embeds final risk/size.
- Equivalent candidates unresolved.

## Evidence retained

- Compiler version.
- Input/output hashes.
- Rejected candidates.
- Reviewer signoff.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[Treatment_DSL_And_Constraint_Solver]]
- [[Hierarchical_Treatment_Search]]
