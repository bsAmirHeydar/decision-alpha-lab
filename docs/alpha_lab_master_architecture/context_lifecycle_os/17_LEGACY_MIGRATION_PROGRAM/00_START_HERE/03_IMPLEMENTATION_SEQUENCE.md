---
title: "Implementation Sequence"
status: proposed-reference
version: 2.1.0
updated: 2026-07-21
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
| LCM-09A | Setup Inventory, Family Registry and Canonical Contract Freeze | Yes |
| LCM-09B | Setup Migration, Setup Factory Binding and Behavioral Parity | Yes |
| LCM-10A | Treatment and Execution Capability Inventory | Accepted reference |
| LCM-10B | Treatment Package Extraction and Execution Boundary Construction | Accepted reference; adapters disabled |
| LCM-10C | Dry-Run Parity, Safety Controls and Authority-Negative Closure | No |
| LCM-11A | Visual Object Inventory, Namespace and Lifecycle Contracts | No |
| LCM-11B | Multi-Chart Isolation, Visual Parity and Visualizer Cutover | No |
| LCM-12A | Documentation Authority, Duplicate Analysis and Canonical Mapping | No |
| LCM-12B | Obsidian Reconciliation, Relocation and Documentation Closure | No |
| LCM-13A | Dual-Run Harness and Mismatch Registry | Accepted reference |
| LCM-13B | Controlled Consumer Wave Cutover | Accepted reference; 27 bounded waves |
| LCM-13C | Rollback Drill and Cutover Closure | Accepted reference; LCM-13 closed |
| LCM-14A | Deprecation Registry and Compatibility Redirects | Accepted reference; no quarantine or deletion |
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

[[LCM_14B_QUARANTINE_OBSERVATION_AND_RETIREMENT_ELIGIBILITY|LCM-14B — Quarantine, Observation and Retirement Eligibility]].

## LCM-08 reference closure

LCM-08C closure `CTXWAVECLOSE_D14965CFA16DD2B417DEE789D21AF5C3` completes reference accounting for the frozen Context portfolio and issues the bounded LCM-09A handoff `sha256:060f6785ffdbb8266e7d000b17237c5c1cc8c162fcd96c2fb86202ac811faac3`.


LCM-09A freeze `SETUPFREEZE_8638449DF9A774634FE9B8F9E17EF891` accounts for all 60 LCM-03 Setup identities, records 117 unresolved embedded candidates, freezes 60 blocked reference contracts, and issues bounded LCM-09B handoff `sha256:9010023f1b182049cc9f7e0601689827c062f2dbb15e21a98d652744c625d2fb`.


## LCM-09B accepted reference checkpoint

LCM-09B migration `SETUPMIGRATION_8F5CED333AA143A8F2A798BA01D550D9` materializes all 60 frozen identities as canonical fail-closed reference packages, registers all 60 through the read-only ACL-04 legacy reference port, records 60 blocked parity dispositions with zero hard mismatch waiver, and issues the bounded LCM-10A handoff `sha256:104e4567686811724302be71f49f08f382196bed235c1fd969ebec1e58cd67ac`.

## LCM-10A accepted reference checkpoint

LCM-10A inventory `TREATINV_98D30D63F6B6CA7BEA4ABAC517956B02` closes the baseline Treatment and execution capability accounting without changing source behavior. It issues the bounded LCM-10B handoff `sha256:6f513e66cc269c963e7380429b82ea78e0fba7812a3ec50fde1070e3c9c5c14b`. The next implementation unit is LCM-10B.


## LCM-10B accepted reference checkpoint

LCM-10B migration `TREATMIG_DCC2F1F7B74985D72A783020843C6B51` converts all 1,109 inventoried Treatment atoms into 422 deterministic canonical reference packages, constructs 483 disabled execution-adapter contracts, preserves 382 explicit blockers, and binds all 60 canonical Setups to a Treatment package or blocker. The bounded handoff permits LCM-10C dry-run parity and authority-negative testing only.

## LCM-13C accepted reference closure

LCM-13C closure `CUTOVERCLOSE_0E477DA8D23F1B8DEB35DDD90B925F4F` binds the exact LCM-13B handoff and rehearses rollback plus deterministic forward recovery for all 27 completed waves and all 613 switched consumers. It accounts for six persistent-state planes per wave, retains 189 ordered closure events, leaves all 806 blocked consumers unchanged on legacy, and emits the bounded LCM-14A handoff `sha256:214581770e7d95142944ddb2c4e5bf00f970d38bb38d6cac2af9421dc239a555`. LCM-13 is closed at `LCM_13C_REFERENCE_ONLY`; quarantine and deletion remain forbidden.


## LCM-14A accepted reference checkpoint

LCM-14A deprecation package `DEPRECATION_B53138FCCDFD91CC595A818BD7153132` binds the exact LCM-13C handoff and registers all 613 approved identities. It verifies 136 already-active documentation redirects, installs 477 reference-only consumer-scoped redirect contracts without changing production bindings, freezes 613 actionable warnings, records 12,431 repository reference records across 44,243 scanned files, and leaves external consumer scope explicitly UNKNOWN. It authorizes no quarantine or deletion and emits the bounded LCM-14B handoff `sha256:e6cdd8272af462e3dbf29a148343e6921cadf8c7b6f748c5ce0a0f0d50e8b3f1`.

### LCM-14B implementation closure — 2026-07-22

Quarantine `QUARANTINE_F2B27A6A93EB63C1B264B84DAFA00C2D` packages all 136 approved documentation originals as immutable evidence copies, preserves active redirects and canonical documents, completes two deterministic repository observation cycles and 136 restoration drills, and emits LCM-15A handoff `sha256:beb66a4bb6792692608c4223763f7f88198e62d63a51b217436e1b456ab02cb8`. External consumer evidence remains UNKNOWN and deletion approval remains zero.

### LCM-15A accepted reference checkpoint — 2026-07-22

Deletion proof package `DELCAND_DBF53BE0F1838F171906F990E05930D6` freezes 2,168 exact paths and approves 940 only for non-destructive LCM-15B relocation/reorganization. All 2,168 remain blocked from future deletion because external consumer reachability is UNKNOWN; deletion approval and deletion execution are both zero. Handoff: `sha256:65f12eae61307a4b008bb593e8f5d09466e3839db03e549809bcfeb1584018bd`.
