---
title: "Shared-Core Reuse and Compatibility Strategy"
tags: [exp0019, faerie-protocol, implementation-program, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
implementation_program: FP-IMP-001
program_version: 1.0.0
doc_version: 1.0.0
last_updated: 2026-07-13
language: en
---
# Shared-Core Reuse and Compatibility Strategy

## Reuse candidates

The implementation must inspect and reuse compatible semantics from:

- `IntermarketDivergenceExecution/CG` confirmation, divergence, hunt, ledger, and visual patterns;
- `DayeTrader/EXP0018` time, period, relationship, confirmation, lifecycle, replay, render, and session-box patterns;
- `AlphaLab/StrategyFactory/Market` multi-symbol synchronization and time kernel;
- `AlphaLab/StrategyFactory/Economics` cost and maximum-loss primitives;
- `AlphaLab/StrategyFactory/Execution` paper execution and reconciliation;
- `AlphaLab/StrategyFactory/Live` authorization, safety, broker adapter, and kill-switch primitives.

## Reuse classification

| Classification | Meaning | Action |
|---|---|---|
| `DIRECT_REUSE` | Contract and semantics already match | import exact version |
| `ADAPTER_REUSE` | Generic primitive matches but input/output differs | add thin FP adapter |
| `PATTERN_REUSE` | Architecture is useful but semantics differ | reimplement FP module using pattern |
| `NO_REUSE` | Context-specific or conflicting behavior | isolate new module |

## Compatibility harness

Before any FP behavior is merged, create a harness that proves:

- existing Cycle Group results are unchanged;
- existing Daye results are unchanged;
- shared module public contracts have not silently changed;
- FP can consume shared outputs without mutating shared state;
- M1 authority and strict same-session close remain context policies, not global changes unless separately generalized and regression-tested.

## No-fork rule

A new generic primitive may be extracted only if:

1. at least two contexts need the same semantics;
2. the semantic contract is context-independent;
3. old-context golden fixtures pass before and after extraction;
4. the core version is incremented;
5. adapters remain backwards-compatible or migration is explicit.
