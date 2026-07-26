---
id: UCPS-4C9918A3B2E7
title: "UC-03 Part 2 — Code, Context, Test and MQL5 Relocation"
type: execution-record
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-25
updated: 2026-07-25
tags:
  - consolidation
  - uc03
  - physical-relocation
  - code
  - context
  - mql5
---
# UC-03 Part 2 — Code, Context, Test and MQL5 Relocation

## Purpose

Part 2 removes executable and research assets from the historical `lab/` workspace and places them behind the approved repository boundaries. It is a physical relocation wave only. It does not choose canonical algorithms, merge duplicate behavior or retire implementations.

## Principal relocations

- Python package roots move from `lab/11_strategy_factory/python` to `src/engine/packages`.
- Strategy Factory tooling moves from `tools/strategy_factory` to `src/engine/tooling/strategy_factory`.
- shared legacy code moves under `src/engine/legacy` with provenance-preserving subdomains;
- Context, experiment and hypothesis assets move under `contexts/legacy`;
- tests, validation corpora and migration tests move under `tests/legacy`;
- laboratory MQL5 assets move under `mql5/legacy` and MQL5 test programs move under `mql5/Tests`;
- schemas, contracts, configurations, adapters, operations and products move to their declared physical boundaries.

## Preservation rule

Every source file is hashed at runtime immediately before relocation. The destination must match that runtime hash before any permitted reference rewrite. A destination collision is preserved under `releases/history/conflicts/uc03_part2`; it is never overwritten without an archived copy.

## Compatibility rule

Part 2 introduces temporary namespace shims and a repository-local Python path bootstrap. Their only purpose is to keep existing consumers running while physical paths change. They do not create new product authority and must be removed after consumer cutover.

## Exit

An accepted Part 2 authorizes Part 3 only. UC-04 remains forbidden until documentation, registry, consumer and clean-replay closure is complete.
