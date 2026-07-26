---
id: UCPS-UC01-LOGIC-58E6F3A7
title: "Logic, Symbol and Authority Surface Baseline"
type: implementation_standard
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - logic
  - symbols
  - authority
---
# Logic, Symbol and Authority Surface Baseline

## Python surface

The scanner parses each Python source with the standard AST and records modules, classes, functions, async functions, signatures, decorators, bases, visibility, line ranges, owner domain, critical domains and a source-surface fingerprint. Syntax and read failures are explicit records; production-candidate failures are blocking.

## MQL5 surface

The scanner records classes, structs, enums, functions, inputs, macros, external imports and include edges. It also records potential authority surfaces including trade classes, order submission, position mutation, pending orders, network requests, DLL imports, filesystem writes and terminal global-state mutation.

## Claim ceiling

Static discovery does not prove runtime semantic equivalence. It creates the preservation map required for later characterization, parity, consolidation and retirement decisions.
