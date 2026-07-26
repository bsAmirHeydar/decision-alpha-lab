---
id: UCPS-0878B08B4D99
title: "Current State and Problem Statement"
type: assessment
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Current State and Problem Statement

## Audited snapshot

The current combined repository snapshot contains approximately:

| Measure | Current value |
|---|---:|
| Total files | 52,213 |
| Direct root files | 1,485 |
| Markdown files | 27,040 |
| Python files | 5,518 |
| MQL5 sources | 293 `.mq5` and 2,266 `.mqh` |
| Files under `docs/` | 26,115 |
| Files under `lab/` | 10,405 |
| Files under `registry/` | 9,761 |

These counts are diagnostic evidence, not design targets.

## Core problem

The repository currently has a strong architecture and extensive evidence controls, but it lacks one physically and semantically consolidated production platform. Many old systems were classified, wrapped, redirected or represented in registries without being moved, merged, cut over and deleted.

## Observable consequences

- Root-level release artifacts obscure project entry points.
- Production logic exists under `lab/`, `tools/`, phase packages and specialized Context directories.
- Similar primitives such as identity, hashing, registry access, state transitions and evidence packaging have multiple implementations.
- Documentation has multiple authoritative-looking copies and projections.
- RTHP has specialized activation paths instead of proving a universal Context Factory.
- Many historical consumers and MQL5 includes still depend on old locations.
- The repository cannot yet be understood or operated through one lifecycle command.

## Root cause

The previous program optimized for non-destructive preservation. Its claim ceilings prohibited broad source movement, semantic merge and deletion. That was safe, but it cannot be the final operating model.

## Required correction

The next work must produce physical movement, semantic consolidation, consumer cutover and controlled deletion. Reports and registries count only when they govern a real repository change or preserve evidence for an executed change.
