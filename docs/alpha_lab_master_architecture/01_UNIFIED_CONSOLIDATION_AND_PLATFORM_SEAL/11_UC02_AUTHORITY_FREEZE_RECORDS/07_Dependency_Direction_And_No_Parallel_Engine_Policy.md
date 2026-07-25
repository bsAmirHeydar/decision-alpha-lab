---
id: UCPS-7BE86ECE199E
title: "Dependency Direction and No-Parallel-Engine Policy"
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
# Dependency Direction and No-Parallel-Engine Policy

## Dependency direction

The permitted direction is from universal primitives toward increasingly operational layers. Kernel has no dependency on Context-specific code. Market may depend on kernel; Context may depend on kernel and market; research may depend on Context and treatment contracts; runtime consumes approved policy and artifacts; execution depends on runtime and adapters.

## Forbidden edges

- kernel to a named Context;
- runtime to a training implementation;
- research to broker or order APIs;
- a Context to private execution internals;
- an adapter mutating doctrine;
- MQL5 becoming architecture authority.

## Parallel-engine definition

A new package is a parallel engine when it independently defines identity, lifecycle, registry, authority, evidence, runtime or capital semantics instead of implementing a versioned extension or adapter contract.

## Enforcement

The differential guard compares proposed paths and packages with the UC-01 baseline. Grandfathered debt remains visible but does not permit new debt. New Strategy Factory, UCEE, ACL, SAED-platform or operating-system package roots fail CI.
