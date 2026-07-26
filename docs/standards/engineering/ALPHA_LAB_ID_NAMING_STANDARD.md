---
id: AIEOS2-C22B1D9B2CD8
title: "Alpha Lab Identity and Naming Standard"
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
# Alpha Lab Identity and Naming Standard

## Artifact Prefixes

| Artifact | Pattern | Example |
|---|---|---|
| Observation | `OBSNNNN` | `OBS0007` |
| Hypothesis | `HNNNN` | `H0012` |
| Experiment | `EXPNNNN` | `EXP0017` |
| Analysis | `ANLNNNN` | `ANL0004` |
| Validation | `VALNNNN` | `VAL0008` |
| Signal | `SIGNNNN` | `SIG0003` |
| Execution | `EXECNNN` | `EXEC014` |
| Monitoring | `MONNNN` | `MON0005` |
| Architecture decision | `ADR-NNNN` | `ADR-0021` |
| Patch | `<scope>-P<NNN>` or hotfix ID | `EXP0017-P006` |

## Rules

- IDs never encode mutable status.
- Renaming titles does not change identity.
- Persistent chart/data IDs derive from stable domain components and time keys.
- File names are ASCII, descriptive, bounded in length, and safe on Windows paths.
- Avoid repeating long hierarchy in every filename; use folders for context.
- Registry status and links are updated atomically with creation/retirement.
