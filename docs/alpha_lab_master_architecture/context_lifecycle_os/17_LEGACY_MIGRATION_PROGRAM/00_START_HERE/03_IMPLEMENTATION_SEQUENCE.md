---
title: "Implementation Sequence"
status: proposed-reference
version: 2.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration]
---
# Implementation Sequence

## Decision

The authoritative lifecycle remains `LCM-00` through `LCM-16`. To prevent monolithic patches from combining incompatible responsibilities, only the heavy phases `LCM-08` through `LCM-16` are divided into two or three implementation subphases. This is the approved balanced partition; further fragmentation requires an ADR demonstrating that the current boundary is unsafe.

## Completed foundation train

| Phase | Result | Status |
|---|---|---|
| LCM-00 | Baseline Freeze and Governance | implemented reference |
| LCM-01 | Forensic Repository Survey | implemented reference |
| LCM-02 | Classification, Ownership and Authority | implemented reference |
| LCM-03 | Canonical Identity, Alias and Locator | implemented reference |
| LCM-04 | Behavioral Characterization and Golden Traces | implemented reference |
| LCM-05 | Target Topology and Repository Locator | implemented reference |
| LCM-06 | Migration Framework and Compatibility Layer | implemented reference |
| LCM-07 | Shared Engine Extraction Evidence | implemented reference; no shared engine materialized without proof |

## Refined implementation release train

| Subphase | Primary result | Destructive action allowed |
|---|---|---|
| LCM-08A | Context Portfolio Freeze, Risk Classification and Pilot Selection | No |
| LCM-08B | Pilot Context Migration, Compatibility Adapter and Behavioral Parity | Accepted reference; no cutover |
| LCM-08C | Context Wave Migration and Context Portfolio Closure | Accepted reference; portfolio accounted with explicit blockers |
| LCM-09A | Setup Inventory, Family Registry and Canonical Contract Freeze | No |
| LCM-09B | Setup Migration, Setup Factory Binding and Behavioral Parity | No |
| LCM-10A | Treatment and Execution Capability Inventory | No |
| LCM-10B | Treatment Package Extraction and Execution Boundary Construction | No |
| LCM-10C | Dry-Run Parity, Safety Controls and Authority-Negative Closure | No |
| LCM-11A | Visual Object Inventory, Namespace and Lifecycle Contracts | No |
| LCM-11B | Multi-Chart Isolation, Visual Parity and Visualizer Cutover | No |
| LCM-12A | Documentation Authority, Duplicate Analysis and Canonical Mapping | No |
| LCM-12B | Obsidian Reconciliation, Relocation and Documentation Closure | No |
| LCM-13A | Dual-Run Harness and Mismatch Registry | No |
| LCM-13B | Controlled Consumer Wave Cutover | No |
| LCM-13C | Rollback Drill and Cutover Closure | No |
| LCM-14A | Deprecation Registry and Compatibility Redirects | No |
| LCM-14B | Quarantine, Observation and Retirement Eligibility | Move to quarantine only |
| LCM-15A | Deletion Candidate Inventory and Reference Proof | No |
| LCM-15B | Root, Release and Documentation Reorganization | Non-destructive moves only |
| LCM-15C | Controlled Deletion and Clean-Clone Verification | Yes, exact approved ledger only |
| LCM-16A | Full Regression, MQL5 Matrix, Parity and Security Audit | No |
| LCM-16B | Recovery Drill, Final Ledger and Program Closure | No |

## Master-phase completion rule

A subphase PASS is not a master-phase PASS. Each master phase has a consolidated gate and final handoff. For example, LCM-08 remains OPEN after LCM-08A and LCM-08B; it closes only when LCM-08C publishes the complete Context portfolio disposition and handoff to LCM-09A.

## Patch-count control

- Light phase: one patch.
- Medium phase: two patches.
- Heavy phase: three patches.
- No master phase may exceed three planned subphases without an approved ADR.
- Emergency hotfixes do not advance lifecycle state unless the phase contract explicitly incorporates their evidence.

## Non-negotiable commit separation

- Inventory and authority changes.
- Move-only changes.
- Semantic implementation/refactor.
- Consumer cutover.
- Quarantine.
- Destructive deletion.

These categories may not be combined merely to reduce patch count.

## Next implementation unit

[[LCM_08A_CONTEXT_PORTFOLIO_FREEZE_RISK_CLASSIFICATION_AND_PILOT_SELECTION|LCM-08A — Context Portfolio Freeze, Risk Classification and Pilot Selection]].

## LCM-08 reference closure

LCM-08C closure `CTXWAVECLOSE_D14965CFA16DD2B417DEE789D21AF5C3` completes reference accounting for the frozen Context portfolio and issues the bounded LCM-09A handoff `sha256:060f6785ffdbb8266e7d000b17237c5c1cc8c162fcd96c2fb86202ac811faac3`.


LCM-09A freeze `SETUPFREEZE_8638449DF9A774634FE9B8F9E17EF891` accounts for all 60 LCM-03 Setup identities, records 117 unresolved embedded candidates, freezes 60 blocked reference contracts, and issues bounded LCM-09B handoff `sha256:9010023f1b182049cc9f7e0601689827c062f2dbb15e21a98d652744c625d2fb`.
