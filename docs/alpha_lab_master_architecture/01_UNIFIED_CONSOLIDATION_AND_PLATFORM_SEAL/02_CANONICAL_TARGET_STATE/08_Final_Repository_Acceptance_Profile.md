---
id: UCPS-113FC66AE3BC
title: "Final Repository Acceptance Profile"
type: standard
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Final Repository Acceptance Profile

## Structural targets

- no more than twenty direct root files;
- one production source root: `src/engine/`;
- one test hierarchy;
- one Context root;
- zero production code under `lab/`;
- zero shared engine implementation under `tools/`;
- zero phase release bundles in root;
- zero duplicate canonical documentation trees.

## Logical targets

- one implementation per shared capability;
- zero active imports from retired systems;
- zero Context-specific conditions in shared engine code;
- zero unknown production-file owners;
- zero unresolved required consumers.

## Operational targets

- one repository acceptance command;
- deterministic clean-clone build;
- recovery drill pass;
- three Golden Contexts pass end-to-end;
- MQL5 compile, tester and parity matrices pass;
- platform-seal policies prevent regression.
