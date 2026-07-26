---
id: UCPS-D5A3CAE8D90E
title: "Naming, Identity, Version and Path Freeze"
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
# Naming, Identity, Version and Path Freeze

## Product and command names

- Product: **Alpha Lab**
- Repository: `decision-alpha-lab`
- Operator command: `alpha`
- Shared production root: `src/engine`
- Public MQL5 prefix: `AL_`

## Naming rules

Python directories, modules, functions and variables use `snake_case`; classes use `PascalCase`; constants use `UPPER_SNAKE_CASE`. Canonical files do not use uncontrolled suffixes such as `copy`, `new`, `latest`, `fixed2` or a phase number as identity.

## Identity rules

Artifact identity is metadata and survives relocation. Existing IDs such as `CTX_`, `SETUP_`, `TRT_`, `TASK_`, `BATCH_`, `MODEL_`, `EVD_`, `POLICY_`, `RUNTIME_`, `RUN_` and `INCIDENT_` remain stable unless an explicit identity migration is approved.

## Version rules

Contract versions follow semantic versioning. Breaking semantics require a major version, compatible additions require a minor version and bounded repairs require a patch version. Path movement alone does not change semantic identity.

## Generated files

Generated outputs must declare their source contract, digest and compiler version and must be rejected when edited by hand.
