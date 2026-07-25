---
id: UCPS-2A081205DEA7
title: "Naming, Versioning, Identity and Path Standard"
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
# Naming, Versioning, Identity and Path Standard

## Naming

- directories and Python modules use `snake_case`;
- Python classes use `PascalCase`;
- constants use `UPPER_SNAKE_CASE`;
- MQL5 shared symbols use the `AL_` prefix;
- Context slugs are stable lower-case identifiers;
- canonical filenames describe the concept, not delivery history.

Names such as `final`, `latest`, `fixed`, `copy`, `new2` and phase-number suffixes are forbidden for canonical artifacts.

## Versioning

Version belongs in metadata and registries. Filename versioning is allowed only when an external standard or side-by-side compatibility requirement makes it necessary. Breaking contract changes require a major version and migration path.

## Identity

Stable IDs such as `CTX_`, `TRT_`, `TASK_`, `BATCH_`, `MODEL_`, `EVD_`, `RUNTIME_` and `RUN_` remain lineage anchors. Path is location, not identity.

## Paths

Paths are canonical, case-stable and forward-slash normalized in machine records. Relocation records map old path, new path, old digest, new digest, consumer rewrite and retirement status.
