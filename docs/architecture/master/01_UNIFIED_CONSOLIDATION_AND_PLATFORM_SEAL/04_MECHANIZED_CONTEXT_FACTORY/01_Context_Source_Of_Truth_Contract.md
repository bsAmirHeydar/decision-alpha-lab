---
id: UCPS-B9E3E96D9295
title: "Context Source-of-Truth Contract"
type: contract
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Context Source-of-Truth Contract

## Authored package

Each Context has one authored package containing `context.yaml`, doctrine, detector or declared detector extension, extension manifest, fixtures and Context-specific tests.

## Required contract domains

- stable identity and version;
- claim, non-claims and invariants;
- instruments, timeframe and market requirements;
- observation, known-time and decision clocks;
- occurrence states, transitions, confirmation, invalidation and expiry;
- synchronization, stale, missing, duplicate and revision policies;
- feature and representation bindings;
- labels, horizons, censoring and embargo;
- permitted research tasks and trial budget;
- Treatment compatibility and prohibited actions;
- falsification and monitoring assumptions;
- explicit authority ceiling.

## Closed-world behavior

Missing mandatory meaning is an error. The compiler does not infer high-impact semantics from prose or prior Contexts. Optional defaults are versioned platform policy and are visible in compiled output.

## Stability

The authored contract is the source of truth. Generated code and docs carry the source digest. Changing the contract creates a new compiled lineage and may invalidate downstream evidence.
