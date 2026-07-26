---
id: UCPS-4CBBF025CBF9
title: "Contracts, Schemas, Policies and Registry Authority"
type: architecture
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Contracts, Schemas, Policies and Registry Authority

## Contract authority

Contracts define meaning and interface. Schemas validate representation. Policies constrain allowed action. Registries record identity, lineage and accepted state. Documentation explains these authorities but does not replace them.

## Single-source rule

A field or lifecycle state has one normative definition. Context-local schemas may extend designated extension points but may not redefine universal fields.

## Publication

Contract and schema publication is atomic, versioned and digest-bound. Consumers declare supported versions. Breaking versions require compatibility analysis and explicit migration.

## Registry discipline

Registries are append-aware, reason-coded and auditable. Derived indexes may be regenerated. Manual edits to generated indexes are forbidden. State transitions require evidence references and authority checks.
