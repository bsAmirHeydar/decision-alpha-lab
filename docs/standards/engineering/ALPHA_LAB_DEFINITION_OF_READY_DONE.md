---
id: AIEOS2-974EC73CDCD8
title: "Alpha Lab Definition of Ready and Done"
type: standard
status: active
domain: engineering
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - engineering
---
# Alpha Lab Definition of Ready and Done

## Definition of Ready for Coding

- Authoritative intent and owner identified.
- Current/desired behavior and non-goals documented.
- Domain terms and ambiguities resolved or registered.
- State/events/invariants/time semantics defined.
- Architecture and ownership boundaries approved.
- Exact files and compatibility risks known.
- Acceptance tests and rollback planned.
- No critical unknown is disguised as an implementation detail.

## Definition of Done for a Patch

- Scope implemented without unrelated behavior changes.
- Target compiler/runtime accepts the code.
- Relevant tests/replay/visual/schema checks pass.
- Warnings and skipped checks are disclosed.
- Documentation, contracts, MOCs, changelog, and registry are updated.
- Install and rollback are executable.
- Exact files are staged and commit is atomic.
- Residual risks have owners.

## Not Done

Compilation alone, a screenshot alone, generated prose alone, or a model score alone is not completion.
