---
title: "Phase Partition and Patch Granularity Standard"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, governance]
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# Phase Partition and Patch Granularity Standard

## Purpose

Define when an LCM master phase is delivered as one, two or three patches, and prevent both unsafe monoliths and administratively fragmented micro-phases.

## Classification

### Light phase — one patch

A light phase is primarily one responsibility, has one rollback semantic, affects a bounded artifact set and can be fully verified in one clean-overlay run.

### Medium phase — two patches

A medium phase contains two responsibilities that must not share rollback, such as authority mapping followed by implementation, or documentation classification followed by relocation.

### Heavy phase — three patches

A heavy phase contains three materially different responsibility classes, typically discovery/contract, implementation/boundary construction and parity/cutover/closure. Three is the default maximum.

## Mandatory reasons to split

- Destructive and non-destructive operations would otherwise share a patch.
- Consumer cutover would share a patch with implementation.
- Repository-wide discovery would share a patch with semantic decisions.
- Authority-capable adapter construction would share a patch with activation or parity evidence.
- Rollback requires different recovery points for different workstreams.
- Direct verification cannot isolate the cause of failure.

## Reasons that do not justify splitting

- A document is long.
- A scanner takes time but has deterministic checkpoints.
- Several artifacts are generated from one closed registry.
- The patch contains many files but one coherent responsibility and rollback.

## Maximum granularity

No planned master phase may exceed three subphases without an ADR. An ADR must show why the current subphase cannot be completed safely using internal checkpoints. It must also identify the new handoff contract and prove that semantic context will not be fragmented.

## Patch acceptance

Every patch must include scope, non-goals, authority, source digest, output digest, exact file index, hashes, QA, direct tests, regression scope, hostile review, rollback and handoff. A patch is rejected if it contains undeclared move, refactor, cutover, quarantine or deletion actions.
