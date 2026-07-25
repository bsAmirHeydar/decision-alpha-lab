---
id: UCPS-64C486213A85
title: "Complete Logic Inventory and Symbol Graph"
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
# Complete Logic Inventory and Symbol Graph

## Inventory depth

File classification is insufficient. UC-01 extracts Python modules, classes, functions, commands, schemas and registry writers; MQL5 Experts, Indicators, Scripts, Includes, functions, enums, structs, inputs and buffers; and PowerShell entry points and environment dependencies.

## Capability graph

Symbols are grouped by semantic capability, not only by path similarity. The graph records calls, imports, includes, runtime loading, generated-code relationships and documentation references.

## Ownership and risk

Each production symbol has owner, current system, consumers, side effects, time semantics, authority, test coverage, target capability and disposition.

## Unknown handling

Unresolved dynamic imports, reflection, terminal includes or external automation remain explicit blockers. Absence from static search is not proof of no consumer.
