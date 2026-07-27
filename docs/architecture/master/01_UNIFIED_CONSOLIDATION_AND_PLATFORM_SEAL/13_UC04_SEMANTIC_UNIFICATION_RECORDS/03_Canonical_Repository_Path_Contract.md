---
id: UCPS-821CCDB2C5B8
title: "Canonical Repository Path Contract"
type: contract
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-27
updated: 2026-07-27
tags:
  - consolidation
  - uc04
  - paths
---
# Canonical Repository Path Contract

## Authority

`tools/repository_paths.py` is the dependency-light path authority shared by production packages, migration tooling, tests and operator scripts.

Repository discovery accepts either:

1. a Git checkout containing `.git` and `src/engine`; or
2. a source archive containing `README.md`, `src/engine` and the accepted UC-03 handoff record.

This removes the previous dependency on historical `lab/` roots and allows clean ZIP verification.

## Resolution order

1. use an existing direct path;
2. resolve an exact source-to-destination mapping from accepted UC-03 receipts;
3. use an explicit, bounded legacy-prefix fallback;
4. fail explicitly when a required target is still missing.

Resolution is cycle-safe and depth-bounded. It never scans arbitrary similarly named directories and never guesses a context identity.

## Canonical roots

| Concern | Root |
|---|---|
| Source | `src/engine` |
| Packages | `src/engine/packages` |
| Strategy Factory tooling | `src/engine/tooling/strategy_factory` |
| Authored contexts | `contexts/legacy/strategy_factory/authored` |
| Generated contexts | `contexts/legacy/strategy_factory/generated` |
| Historical registry | `registry/history` |
| Schemas | `schemas` |
| Program documentation | `docs/architecture/master` |
| Release evidence | `releases` |
| Repository-local runtime output | `.alpha/runs` |

## Boundary invariant

An operator may provide a historical path for compatibility, but active production code must resolve it through this contract before reading or writing. Repository-local runtime output outside `.alpha/runs` is rejected.

The machine-readable contract is `registry/consolidation/uc04/w0/path_contract.json`.
