---
id: UCPS-6E0B0A0B3BFA
title: "Architecture Constitution and One Product Boundary"
type: execution-record
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-24
updated: 2026-07-24
tags:
  - consolidation
  - uc02
  - authority-freeze
---
# Architecture Constitution and One Product Boundary

## Constitutional decision

The repository is the Alpha Lab product boundary. No nested product directory named `alpha_lab` is permitted. Shared production logic converges under `src/engine`, while authored Context packages remain under `contexts`.

## One-authority rule

Every production capability has exactly one canonical owner. A system may provide an implementation or extension, but it cannot independently own identity, registry, lifecycle, authority, evidence, runtime or capital semantics.

## Separation of concerns

- the kernel owns universal primitives;
- market owns observations and clocks;
- Context owns occurrence meaning;
- treatment owns executable treatment definitions;
- research owns experiments and model discovery;
- evidence owns protected evaluation and promotion evidence;
- runtime consumes approved artifacts;
- execution interfaces with terminals and brokers;
- monitoring observes deployed behavior.

## Change control

A shared-platform change requires an ADR, contract version, migration plan, verification and rollback. A Context may evolve through its closed Context contract and extension manifests without changing shared internals.

## Safety boundary

All destructive, runtime, order, broker and capital authority flags remain false throughout UC-02.
