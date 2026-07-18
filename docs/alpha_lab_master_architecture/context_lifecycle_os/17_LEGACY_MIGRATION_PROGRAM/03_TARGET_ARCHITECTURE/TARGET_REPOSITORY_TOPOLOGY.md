---
title: "Target Repository Topology"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Target Repository Topology

```text
lab/11_strategy_factory/
  acl_os/                         # protected lifecycle kernel
  contexts/<context_id>/          # canonical Context packages
  setups/<setup_id>/              # canonical Setup packages
  treatments/<treatment_id>/      # canonical Treatment packages
  visualizers/<visualizer_id>/    # deterministic projections
  shared_engines/<engine_id>/     # proven reusable primitives
  adapters/{python,mql5,tradingview}/<adapter_id>/
  migration/
    registry/
    surveys/
    packets/
    parity/
    waves/
    quarantine/

mql5/
  Include/AlphaLab/ContextOS/
    Kernel/
    Shared/
    Contexts/<context_id>/
    Setups/<setup_id>/
    Treatments/<treatment_id>/
    Visualizers/<visualizer_id>/
    Adapters/<adapter_id>/
    Compatibility/<legacy_alias>/
  Experts/AlphaLab/ContextOS/
    Diagnostics/
    Research/
    Paper/
    Tests/

docs/alpha_lab_master_architecture/context_lifecycle_os/
  17_LEGACY_MIGRATION_PROGRAM/

docs/contexts/<context_id>/        # optional human navigation projection
registry/
  legacy_context_migration/
  releases/<program>/<release_id>/
tools/release/powershell/
```

## Placement rule

Canonical domain truth lives in the package and accepted master architecture. MQL5 files are platform implementations or adapters. Generated Obsidian pages are projections. Release files are registry artifacts. Legacy originals live only in active legacy paths during dual run or in migration quarantine after cutover.
