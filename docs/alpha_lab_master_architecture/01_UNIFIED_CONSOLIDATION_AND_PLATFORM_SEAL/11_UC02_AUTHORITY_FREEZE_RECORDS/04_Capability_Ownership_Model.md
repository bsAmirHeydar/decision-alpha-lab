---
id: UCPS-AF9FDFB54F42
title: "Capability Ownership Model"
type: execution-record
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-24
updated: 2026-07-24
tags:
  - consolidation
  - uc02
  - authority-freeze
---
# Capability Ownership Model

## Exact ownership

Every discovered Python and MQL5 symbol is assigned to one canonical domain. Cross-domain use is implemented through a contract; it does not create duplicate ownership.

## Canonical domains

`kernel`, `market`, `context`, `treatment`, `research`, `evidence`, `policy`, `capital`, `portfolio`, `runtime`, `execution`, `monitoring`, `memory`, `adapters`, `contracts`, `schemas`, `registry`, `configuration`, `mql5`, `testing`, `documentation`, `engineering`, `operations`, `products`, `examples`, `release_history` and `historical_archive`.

## Ownership evidence

The capability ledger records language, source path, symbol identity, symbol kind, source system, canonical owner, target and migration action. Package-level summaries show mixed legacy packages explicitly rather than pretending a package already has coherent ownership.

## No semantic loss

A capability may move, split or merge only after characterization evidence identifies its observable behavior. Different semantics remain versioned strategies or extensions instead of being silently collapsed.

## Blocking condition

An unowned production capability or a capability assigned to multiple canonical owners blocks UC-03.
