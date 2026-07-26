---
id: UCPS-1F7260DE9AC4
title: "UC-03 Part 2 Target Topology and Move Waves"
type: contract
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-25
updated: 2026-07-25
tags:
  - consolidation
  - uc03
  - topology
  - migration-wave
---
# UC-03 Part 2 Target Topology and Move Waves

## Physical boundaries

```text
src/engine/packages/                 importable historical Python packages
src/engine/legacy/                   shared code awaiting UC-04 consolidation
src/engine/tooling/strategy_factory/ Strategy Factory orchestration tooling
contexts/legacy/                     Context and experiment source assets
tests/legacy/                        migrated validation and regression assets
mql5/legacy/                         laboratory MQL5 source
mql5/Tests/                          MQL5 test programs
adapters/legacy/                     external integration implementations
configs/legacy/                      historical runtime configuration
ops/                                 CI and deployment operations
releases/history/                    non-active program and artifact history
```

## Move waves

1. Strategy Factory Python packages and shared core code.
2. ACL, runtime, market and plugin reference implementations.
3. Contexts, experiments, hypotheses and observation assets.
4. Unit, validation, migration and fixture corpora.
5. Laboratory MQL5 and explicit MQL5 test assets.
6. Infrastructure adapters, configuration, CI and deployment assets.
7. Historical program artifacts and empty-shell cleanup.

## Non-goals

- no semantic owner selection;
- no duplicate capability merge;
- no behavior retirement;
- no live/runtime/order/capital authority;
- no final deletion authorization.
