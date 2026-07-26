---
title: "Current-to-Target Path Map"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, project-decision]
---
# Current-to-Target Path Map

## Current source to target decisions

| Current namespace | Initial target | Transition mechanism |
|---|---|---|
| `lab/11_strategy_factory/contexts/_acl_02_template` | retained | canonical Context scaffold |
| experiment-specific Context logic in `mql5/Include/*` | `mql5/Include/AlphaLab/ContextOS/Contexts/<id>` | adapter, parity, compatibility wrapper |
| Setup/trigger logic embedded in Experts/Includes | `lab/11_strategy_factory/setups/<id>` plus MQL adapter | behavioral extraction |
| entry/stop/target logic mixed with Setup | `lab/11_strategy_factory/treatments/<id>` | treatment contract and dry request parity |
| drawing mixed into detectors | `lab/11_strategy_factory/visualizers/<id>` | event projection and object-lifecycle parity |
| repeated time/session/reference primitives | `shared_engines/<id>` | only after equivalence proof |
| direct broker operations | `adapters/mql5/<id>` | capability-guarded execution-last migration |
| old MQL public paths | `ContextOS/Compatibility/<alias>` | thin forwarding wrapper during deprecation |
| experiment normative docs | Context package/source-evidence links | retain authority and add successor mapping |
| exact duplicate architecture docs | master-architecture copy | redirect then deletion gate |
| generated source cards/atomic concepts | generated knowledge namespace | derived marker and rebuild contract |
| root release metadata | `registry/history/releases/<program>/<release>` | locator migration then move |
| root installers | `tools/release/powershell/<program>` | preserved historical command mapping |
| inactive originals | migration quarantine | original bytes, hashes, parity and rollback |

## Move discipline

Each path change is one of three operations: move-only, wrapper/redirect, or semantic refactor. These operations are never combined for the same large artifact in one commit. `git mv` is used where possible, but source identity remains the canonical artifact ID rather than Git rename detection.

## Paths deliberately untouched during early phases

- ACL-OS kernel and fixtures;
- SAED/UCE platform research stack;
- active broker adapters;
- legacy experiment source paths before characterization;
- root release files before locator migration;
- source-authority documents and decision logs.
