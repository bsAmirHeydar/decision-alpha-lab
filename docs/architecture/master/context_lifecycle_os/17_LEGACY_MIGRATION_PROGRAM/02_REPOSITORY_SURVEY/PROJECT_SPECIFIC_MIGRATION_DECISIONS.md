---
title: "Project-Specific Migration Decisions"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration, project-decision]
---
# Project-Specific Migration Decisions

## Decision basis

The repository-wide survey shows that the project is not one legacy strategy. It is a portfolio of domain families, platform kernels, generated knowledge systems, research experiments, execution adapters and historical release artifacts. Migration must therefore be portfolio-based and identity-based rather than folder-based.

## Observed portfolio

| Family | All files | Docs | Python | MQL source | Approx. MQL lines | Program decision |
|---|---:|---:|---:|---:|---:|---|
| ACL-OS kernel | 4,600 | 3,249 | 561 | 0 | 0 | protect; destination OS |
| Strategy Factory / SAED / UCE platform | 8,614 | 47 | 2,614 | 1,562 | 26,516 | protect; interface-only changes |
| EXP0015 intermarket time | 26 | 16 | 1 | 8 | 1,809 | Wave-01 candidate after owner review |
| ICT / Structural Nodes | 25 | 7 | 0 | 10 | 1,561 | Wave-01 shared-primitive review |
| M0001–M0007 | 264 | 225 | 0 | 34 | 24,828 | Wave-02 per identity |
| EXP0018 Daye Trader | 1,577 | 1,363 | 28 | 111 | 18,064 | Wave-03 MTF/session/visual |
| EXP0016 intermarket execution | 277 | 247 | 0 | 29 | 10,434 | Wave-04 split Context/Treatment/Adapter |
| EXP0017 Cycle Group | 1,178 | 1,068 | 0 | 103 | 17,047 | Wave-04 split Context/Setup/Statistics/Execution |
| EXP0019 Faerie Protocol | 2,440 | 1,131 | 551 | 208 | 3,763 | Wave-05 owner-decision preserving |
| FlagCounting / NDS / Hook / Zone | 1,534 | 1,217 | 27 | 226 | 58,065 | Wave-06 critical sub-waves |
| E-series execution | 41 | 5 | 0 | 36 | 19,668 | Wave-07 execution-last |
| Astro research/execution | 279 | 177 | 28 | 33 | 9,572 | separate Wave-07 lane |
| Product Lab | 276 | 220 | 0 | 19 | 5,235 | excluded; separate program |

Counts are structural survey counts. Static contract mirrors and generated artifacts may inflate a family count; LCM-02 resolves active role and reachability.

## Repository-specific architectural decisions

### Preserve ACL-OS as destination kernel

`lab/11_strategy_factory/acl_os`, `tools/strategy_factory/acl_os`, ACL fixtures/tests and accepted master architecture are protected. Context-specific behavior must enter through packages and extensions; migration may not simplify the repository by embedding old strategy rules in the kernel.

### Use the existing ACL Context template

The target for Contexts is the existing `lab/11_strategy_factory/contexts/_acl_02_template`. LCM adds migration evidence to that contract instead of inventing another Context format.

### Add sibling domain libraries

The current repository has Context templates but no equivalent canonical homes for Setup, Treatment and visualization packages. LCM-05 creates sibling libraries under `lab/11_strategy_factory/` and binds them through registries.

### Consolidate MQL only after parity

`mql5/Include/AlphaLab`, `DecisionAlphaLab`, `StrategyFactory`, experiment-specific and research namespaces are not bulk-renamed. New canonical domain implementations land under `AlphaLab/ContextOS`; old public paths receive wrappers during dual run.

### Treat documentation as an authority graph

Exact duplicate namespaces are candidates for consolidation. Large generated systems such as `obsidian_deep` and atomic concepts become derived projections. EXP0017–EXP0019 source and owner-decision documents remain source evidence and are never removed merely because a canonical Context package exists.

### Clean root at the end

The root has 1,069 files. Release metadata and installers will move only after locator migration, historical instruction preservation and reference scans. Early cosmetic cleanup is rejected.

## First pilot recommendation

Do not start with the most complex or commercially important family. Select a read-only, non-order, bounded-state family after LCM-02 ownership review. The pilot must prove packet, trace, parity, redirect, rollback and quarantine mechanics before any EXP0019 or Flag/NDS migration.
