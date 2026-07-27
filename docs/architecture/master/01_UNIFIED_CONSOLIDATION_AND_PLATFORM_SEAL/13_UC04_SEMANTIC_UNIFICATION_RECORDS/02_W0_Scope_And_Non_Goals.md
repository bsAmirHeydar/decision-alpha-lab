---
id: UCPS-D9F11BCF8459
title: "UC04-W0 Scope and Non-Goals"
type: scope
status: accepted
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-27
updated: 2026-07-27
tags:
  - consolidation
  - uc04
  - recovery
---
# UC04-W0 Scope and Non-Goals

## Bounded intent

W0 restores a trustworthy execution floor after the accepted UC-03 physical relocation. It fixes infrastructure and bindings required to start semantic unification; it does not perform semantic unification of a trading capability itself.

## Included

- one canonical repository discovery and migration-aware path resolver;
- source-archive support where `.git` is absent;
- deterministic repository-local run boundary under `.alpha/runs`;
- repository-wide Pytest collection recovery using importlib mode and explicit package identity;
- migration-aware UC-01 and UC-03 evidence continuity;
- canonical ACL and RTHP context, registry, generated-artifact, train and MT5 activation paths;
- UC-04 schemas, registry records, verifier, tests, CI workflow, release controls and Obsidian records;
- correction of root status surfaces that contradicted accepted stage evidence.

## Explicit non-goals

W0 does not change:

- RTHP definitions, polarity, stale-data doctrine or confirmation semantics;
- feature, task, label, model, fold or promotion behavior;
- the Train Engine algorithm;
- MQL5 entry, execution, stop, target, risk or session logic;
- order, runtime or capital authority;
- consumer implementation for a new shared primitive;
- legacy deletion or semantic retirement.

## Acceptance principle

A green W0 proves that the repository can be discovered, collected, validated and exercised through the RTHP boundary after UC-03. It does not prove that all 9,732 collected tests pass or that UC-04 is complete.
