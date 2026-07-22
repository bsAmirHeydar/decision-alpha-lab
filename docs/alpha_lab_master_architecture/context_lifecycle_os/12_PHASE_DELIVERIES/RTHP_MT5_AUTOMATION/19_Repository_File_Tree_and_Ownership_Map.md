---
title: RTHP MT5 Automation — Repository File Tree and Ownership Map
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, repository, folders, ownership]
---

# Repository File Tree and Ownership Map

## Documentation

```text
docs/alpha_lab_master_architecture/context_lifecycle_os/
├── 12_PHASE_DELIVERIES/
│   └── RTHP_MT5_AUTOMATION/
└── 13_ATOMIC_CONCEPTS/
    └── RTHP_MT5_AUTOMATION/
```

## Planned context-owned Python package

```text
lab/11_strategy_factory/python/
└── strategy_factory_rthp_mt5_activation_v1/
    ├── __init__.py
    ├── __main__.py
    ├── cli.py
    ├── config.py
    ├── mt5_provider.py
    ├── terminal.py
    ├── symbols.py
    ├── acquire.py
    ├── m1_schema.py
    ├── quality.py
    ├── time_calendar.py
    ├── source_binding.py
    ├── orchestrator.py
    └── verify.py
```

## Planned generated configuration and schemas

```text
lab/11_strategy_factory/generated_contexts/
└── rthp_cross_symbol_cycle_divergence/
    └── mt5_activation/
        └── v1/
            ├── configs/
            ├── schemas/
            ├── fixtures/
            └── generated/
```

## Registry

```text
registry/strategy_factory/contexts/rthp/v1/
├── rthp_mt5_activation_registration.json
├── rthp_mt5_activation_config.schema.json
├── rthp_mt5_m1_bar.schema.json
├── rthp_mt5_symbol_metadata.schema.json
├── rthp_mt5_quality_report.schema.json
└── rthp_mt5_source_binding.schema.json
```

## Tests

```text
lab/11_strategy_factory/tests/
└── rthp_mt5_activation/
```

## Protected paths

The delivery must not modify shared engine packages, canonical Context files, or central ACL/SAED/UCEE registries. Any required shared change is a blocker and requires a separate architecture decision.
