---
id: UCPS-4E6E07D61F82
title: "Artifact Classes and Storage Boundaries"
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
# Artifact Classes and Storage Boundaries

## Classes

| Class | Authoritative location | Versioned in Git? |
|---|---|---|
| Authored source | `src/`, `contexts/`, `adapters/`, `contracts/`, `schemas/`, `policies/` | Yes |
| Tests and fixtures | `tests/`, Context-local fixtures | Yes |
| Generated build output | `.alpha/generated/` | No, except approved golden fixtures |
| Runtime and research output | `.alpha/runs/`, artifact store | No |
| Operational configuration | `configs/`, `ops/` | Yes, without secrets |
| Canonical docs | `docs/` | Yes |
| Historical release evidence | immutable release store or `releases/` index | selectively |
| Large immutable evidence | content-addressed store or Git LFS | by policy |

## Boundary rule

A file has one primary class. A generated file may not silently become authored source. A runtime receipt may not be edited as documentation. A historical file may not be used as current authority without re-adoption.

## Required metadata

Every generated artifact records producer, source digest, compiler version, schema version, creation time, lineage and immutability status. Every runtime artifact records run identity and environment identity.
