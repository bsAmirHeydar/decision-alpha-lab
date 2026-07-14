---
title: SAED2-26 — Active Experiment Planning and Institutional Scale
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

Rank research programs by information/economic value, allocate resources, monitor portfolio of research, and formalize continuous evolution.

## Required workstreams

1. **Contracts and schemas** — define closed machine-readable inputs, outputs, lifecycle states, and error semantics.
2. **Reference implementation** — deterministic Python implementation with exact configuration and content addressing.
3. **MQL5/runtime boundary** — where relevant, mirror contracts and certify static and actual parity.
4. **Evidence** — fixtures, negative cases, replay vectors, performance, failure and adversarial tests.
5. **Governance** — ownership, authority, data roles, review, change policy, and rollback.
6. **Obsidian knowledge** — doctrine, architecture, runbooks, ADRs, and traceability.

## Deliverables

Planner; research portfolio dashboard; annual validation and governance cycle.

## Acceptance gates

- All generated artifacts are immutable and hash-addressed.
- Known-time and data-role tests pass.
- Candidate/trial/failure ledgers are complete.
- Negative and adversarial cases fail closed.
- No new execution or promotion authority is introduced.
- Downstream UCEE contracts accept the handoff without semantic translation.
- Evidence classes remain honest: static, fixture, simulated, paper, shadow, and actual are never conflated.

## Exit state

A signed phase-status record enumerates delivered files, open blockers, local-Windows requirements, risks, and the exact handoff to SAED2-27 or operations.
