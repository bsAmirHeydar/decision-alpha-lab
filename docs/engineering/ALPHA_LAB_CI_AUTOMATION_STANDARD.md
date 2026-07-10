---
id: AIEOS2-7DFFAD4E2B47
title: "Alpha Lab CI and Automation Standard"
type: standard
status: active
domain: engineering
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - engineering
---
# Alpha Lab CI and Automation Standard

## CI Stages

1. Repository and policy structure validation.
2. Obsidian frontmatter/link/ID validation.
3. Language compatibility/static scans.
4. Unit and invariant tests.
5. Dataset/schema/lineage checks.
6. Deterministic smoke/replay tests.
7. Package manifest and archive validation.

## Reproducibility

CI commands must also run locally. Scripts use standard exit codes and machine-readable outputs. Network-dependent tests are isolated and never masquerade as deterministic unit tests.

## Failure Policy

- Errors fail the build.
- Warnings require explicit project policy; new warnings are not silently accepted.
- Missing mandatory inputs fail closed.
- Generated artifacts must not be committed unless the contract designates them as versioned evidence.

## MQL5 Limitation

Where MetaEditor compilation is unavailable in CI, static compatibility checks are advisory substitutes only. Actual MetaEditor compile evidence remains mandatory before release.
