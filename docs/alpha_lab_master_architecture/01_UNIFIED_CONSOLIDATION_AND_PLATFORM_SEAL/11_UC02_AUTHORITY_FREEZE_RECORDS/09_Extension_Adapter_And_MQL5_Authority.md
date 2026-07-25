---
id: UCPS-D916C2AFCD24
title: "Extension, Adapter and MQL5 Authority"
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
# Extension, Adapter and MQL5 Authority

## Extensions

Permitted extension types are detector, feature, label, treatment, data, model, broker and visualizer plugins. Every extension has a manifest, version, owner, declared capability, typed inputs and outputs, failure semantics, security scope and conformance suite.

## Adapters

Adapters translate external systems into canonical contracts. They do not own doctrine, Context meaning, lifecycle or evidence semantics.

## MQL5

MQL5 is a terminal implementation and execution boundary. It consumes versioned contracts and must provide compiled evidence and parity receipts. MQL5 source does not become the architectural source of truth merely because it is executable.

## Safety

No extension or adapter may escalate runtime, order, broker or capital authority. A broker adapter can expose capabilities only after the upstream runtime artifact and operator authority permit them.

## Load rule

An extension without a valid manifest and conformance suite is not loadable.
