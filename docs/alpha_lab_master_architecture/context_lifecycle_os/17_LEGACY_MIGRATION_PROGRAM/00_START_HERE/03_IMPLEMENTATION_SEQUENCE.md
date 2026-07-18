---
title: "Implementation Sequence"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Implementation Sequence

## Release train

| Phase | Name | Primary result | Destructive action allowed |
|---|---|---|---|
| LCM-00 | Baseline Freeze and Governance | immutable starting point | no |
| LCM-01 | Forensic Repository Survey | complete machine inventory | no |
| LCM-02 | Classification and Ownership | every artifact classified and owned | no |
| LCM-03 | Identity and Alias Registry | canonical IDs and legacy aliases | no |
| LCM-04 | Behavioral Characterization | golden observations and traces | no |
| LCM-05 | Target Topology and Locator | approved destination map | no |
| LCM-06 | Migration Framework | adapters, packet schemas and comparators | no |
| LCM-07 | Shared Engine Extraction | verified reusable primitives | limited, no deletion |
| LCM-08 | Context Package Migration | canonical Context packages | no deletion |
| LCM-09 | Setup Package Migration | canonical Setup packages | no deletion |
| LCM-10 | Treatment and Execution Separation | authority boundaries | no deletion |
| LCM-11 | Visualization Standardization | deterministic visual projections | no deletion |
| LCM-12 | Documentation Reconciliation | canonical knowledge graph | redirect stubs only |
| LCM-13 | Wave Cutover and Dual Run | consumers switched under parity | no deletion |
| LCM-14 | Deprecation and Quarantine | inactive legacy preserved outside runtime paths | move to quarantine |
| LCM-15 | Controlled Deletion and Root Hygiene | proven dead artifacts removed | yes, gated |
| LCM-16 | Full Cutover and Closure | program closure and residual risk | no new deletion beyond approved ledger |

## First implementation train

The first four patches must be limited to governance, inventory, identity and characterization infrastructure. No context code is moved in those patches.

## First pilot migration

After LCM-06, select a read-only, single-timeframe, non-executing family with clear examples. Do not begin with FlagCounting/NDS/Hook, Faerie Protocol or E-series execution modules.
