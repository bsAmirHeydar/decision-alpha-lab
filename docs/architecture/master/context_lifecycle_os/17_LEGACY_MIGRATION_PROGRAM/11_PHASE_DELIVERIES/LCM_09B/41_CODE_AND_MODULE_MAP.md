---
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-09b, setup-migration]
phase_id: LCM-09B
claim_ceiling: LCM_09B_REFERENCE_ONLY
---
# Code and Module Map

## Production package

`tools/strategy_factory/lcm/lcm_09b/`

| Module | Responsibility | Forbidden responsibility |
|---|---|---|
| `constants.py` | phase IDs, claim ceiling, bound roots, invariant lists | domain semantics |
| `canonical.py` | canonical serialization, IDs, object/file digests | persistence policy |
| `io.py` | atomic UTF-8 JSON/JSONL publication | network or legacy execution |
| `models.py` | typed states and immutable snapshot/state records | orchestration |
| `expressions.py` | closed deterministic expression language | arbitrary Python evaluation |
| `contracts.py` | package and authority validation | waiver decisions |
| `evaluator.py` | pure Setup decision evaluation over caller-supplied Context | clocks, brokers, charts, persistence |
| `adapters.py` | normalize supplied legacy evidence | import or execute legacy code |
| `parity.py` | exact trace comparison and blocked disposition | aggregate-score waiver |
| `factory_bridge.py` | read-only Factory reference registry | candidate promotion |
| `restart.py` | digest-bound checkpoint and restore | wall-clock reconstruction |
| `provenance.py` | source-to-package graph | semantic approval |
| `artifact_manifest.py` | byte inventory and manifest digest | self-referential receipt inclusion |
| `schema_validation.py` | Draft 2020-12 schema checks | implicit coercion |
| `static_validation.py` | deny order, chart, network, process surfaces | runtime execution |
| `handoff.py` | bounded LCM-10A permission artifact | LCM-10 execution |
| `verify.py` | package and installation integrity | test suppression |
| `qa.py` | aggregate bounded QA result | unsupported compiler claims |
| `service.py` | deterministic orchestration and publication | invented Setup rules |
| `cli.py` | operator entry points | hidden defaults |

## ACL-04 extension

`tools/strategy_factory/acl_os/acl_04/legacy_reference.py` exposes the LCM reference port through the existing Factory namespace. This extension does not modify the normal ACL-04 compilation or selection path. Its only operation is to load and list authority-negative registrations.

## Registry surfaces

- `registry/history/lcm/lcm_09b/schemas/v1/`: closed machine contracts;
- `registry/history/lcm/lcm_09b/policies/v1/`: versioned non-negotiable policy records;
- `registry/history/lcm/setup_package_migrations/<migration_id>/`: immutable generated phase evidence.

## Test surfaces

- `lab/11_strategy_factory/migration/tests_lcm_09b/`: phase-direct unit, contract, replay, parity, provenance, and package tests;
- `lab/11_strategy_factory/acl_os/tests_acl_04/test_legacy_reference_port.py`: bounded Factory regression.

## Dependency direction

The dependency direction is one-way:

`LCM-09A frozen evidence -> LCM-09B package service -> generated registries -> ACL-04 read-only reference port -> LCM-10A dependency inventory`

No dependency points back into legacy MQL5 source, no Setup package imports ACL-04 candidate internals, and no generated registry becomes doctrine.
