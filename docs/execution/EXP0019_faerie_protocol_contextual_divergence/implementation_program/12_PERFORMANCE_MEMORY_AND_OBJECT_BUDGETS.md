---
title: "Performance, Memory, and Object Budgets"
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
# Performance, Memory, and Object Budgets

## Runtime objectives

The indicator must remain responsive with long calendar-day and weekly lookbacks while processing two symbols and multiple relation families.

## Budget categories

| Budget | Initial engineering target | Evidence |
|---|---:|---|
| steady-state timer work | bounded to new M1/events only | latency histogram |
| full-history scans after ready | zero | diagnostic counter |
| duplicate semantic events | zero | ledger uniqueness check |
| object recreate rate | zero for unchanged projections | render telemetry |
| active object count | bounded by display-depth policy | object inventory |
| checkpoint size | bounded and versioned | file telemetry |
| restart parity | exact signal/event IDs | replay hash |

Exact millisecond and memory thresholds must be measured on the target terminal and machine; they are release evidence rather than guessed universal constants.

## Incremental state

- Per-symbol M1 cursor.
- Active A/L/N/W windows.
- Immutable completed-window cache.
- Indexed calendar-day selector.
- Active reference/hunt/candidate maps.
- WW stack.
- append-only signal ledger plus compact lookup indexes.
- dirty projection set.

## Degradation behavior

If rendering exceeds budget:

1. preserve semantic processing;
2. batch or defer noncritical projections;
3. reduce historical display depth within configured policy;
4. report degraded visual health;
5. never drop ledger events or silently change detection.
