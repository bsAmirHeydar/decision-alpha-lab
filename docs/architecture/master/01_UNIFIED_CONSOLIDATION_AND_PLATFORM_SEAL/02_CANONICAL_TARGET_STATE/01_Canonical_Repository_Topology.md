---
id: UCPS-5F1C1C1B36B0
title: "Canonical Repository Topology"
type: architecture
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Canonical Repository Topology

## Target tree

```text
decision-alpha-lab/
├── README.md
├── AGENTS.md
├── pyproject.toml
├── uv.lock
├── LICENSE
├── .gitignore
├── .gitattributes
├── src/engine/
├── contexts/
├── adapters/
├── contracts/
├── schemas/
├── policies/
├── registry/
├── configs/
├── mql5/
├── tests/
├── docs/
├── ops/
├── tools/
├── products/
├── examples/
└── releases/
```

## Directory authority

- `src/engine/`: reusable production logic only.
- `contexts/`: authored Context definitions and Context-specific plugins.
- `adapters/`: market data, storage, terminal, broker, model and notification boundaries.
- `contracts/`, `schemas/`, `policies/`: normative machine authority.
- `registry/`: identity, state and lineage records; never general-purpose code.
- `mql5/`: terminal implementation organized by Include, Experts, Indicators, Scripts and Tests.
- `tests/`: unified verification hierarchy.
- `docs/`: architecture, standards, Contexts, operations, decisions and generated projections.
- `ops/`: deployment, scheduled operation and environment automation.
- `tools/`: developer and maintenance utilities only.

## Prohibited roots after seal

Production packages under `lab/`, shared engines under `tools/`, phase bundles at repository root, generated run artifacts in source directories and nested directories that repeat the project identity are prohibited.
