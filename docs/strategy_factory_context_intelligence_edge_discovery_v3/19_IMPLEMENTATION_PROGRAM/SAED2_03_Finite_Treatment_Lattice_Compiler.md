---
title: SAED2-03 — Finite Treatment Lattice Compiler
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- implementation
- phase
---

# Mission

Build typed atoms, compatibility graph, dominance pruning, deterministic candidate IDs, and runtime feasibility checks.

## Required workstreams

1. **Contracts and schemas** — define closed machine-readable inputs, outputs, lifecycle states, and error semantics.
2. **Reference implementation** — deterministic Python implementation with exact configuration and content addressing.
3. **MQL5/runtime boundary** — where relevant, mirror contracts and certify static and actual parity.
4. **Evidence** — fixtures, negative cases, replay vectors, performance, failure and adversarial tests.
5. **Governance** — ownership, authority, data roles, review, change policy, and rollback.
6. **Obsidian knowledge** — doctrine, architecture, runbooks, ADRs, and traceability.

## Deliverables

Compiler; treatment universe manifest; pruning ledger; fixtures.

## Acceptance gates

- All generated artifacts are immutable and hash-addressed.
- Known-time and data-role tests pass.
- Candidate/trial/failure ledgers are complete.
- Negative and adversarial cases fail closed.
- No new execution or promotion authority is introduced.
- Downstream UCEE contracts accept the handoff without semantic translation.
- Evidence classes remain honest: static, fixture, simulated, paper, shadow, and actual are never conflated.

## Exit state

A signed phase-status record enumerates delivered files, open blockers, local-Windows requirements, risks, and the exact handoff to SAED2-04 or operations.
