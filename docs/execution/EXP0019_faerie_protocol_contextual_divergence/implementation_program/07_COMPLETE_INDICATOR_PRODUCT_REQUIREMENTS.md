---
title: "Complete Indicator Product Requirements"
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
# Complete Indicator Product Requirements

## Indicator identity

Canonical product name:

```text
EXP0019_FaerieProtocol_Context
```

The indicator is the primary observable product of the context engine. It must be complete enough for discretionary analysis, historical audit, debugging, and future EA parity verification.

## Functional requirements

### Data and context

- Resolve the two configured symbols and verify trade-session/history availability.
- Build all context from canonical M1 data.
- Resolve the host confirmation timeframe at initialization and include it in configuration identity.
- Display current New York date, session, week, and DST regime.
- Report coverage separately for each symbol and each required window.

### Sessions and references

- Draw A, L, N session boxes with independent visibility and styles.
- Draw New York week boundaries and optional weekly range boxes.
- Draw symbol-local high/low references for enabled relations.
- Distinguish active, protected-consumed, expired, missing, and neutralized references.
- Provide calendar-day offset labels for historical N references.

### Signals

- Render raw Hunt, Candidate, Confirmed, Invalidated, Neutralized, Suppressed, Eligible, Reserved, and Consumed states.
- Render Hunter and Protected symbol roles.
- Display relation code, direction, reference window, check window, confirmation time, reason code, and signal sequence.
- Never hide a valid suppressed signal in audit mode.
- Keep confirmed visual evidence immutable; later policy changes add status overlays rather than rewriting history.

### WW context

- Display active WW direction and source week.
- Display older active/neutralized WW records in audit history.
- Show newest-active resolution and why a downstream signal is aligned, opposed, or unrestricted.
- Show direct WW setup eligibility separately from its gate role.

### Quota and arbitration

- Show pair-global session quota state.
- Show the earliest M1 Hunt winner.
- Show later confirmed signals as suppressed-by-first-entry rather than deleting them.
- Clearly mark the open live quota-consumption policy in diagnostic mode.

### Alerts

- Optional popup, sound, push, and email alerts.
- Alert types selectable by relation, direction, and lifecycle state.
- Alert deduplication keyed by signal ID and alert type.
- Historical rebuild must not replay old alerts unless explicitly requested.

### Export

- Optional append-only CSV or JSONL event export.
- Export includes context/config hash, signal ID, relation, direction, roles, times, levels, state, reason codes, WW state, and quota state.

## Non-functional requirements

- No full-history rescan per tick/timer.
- No flicker from delete-and-recreate rendering.
- No object-name collision across charts, instances, symbols, or configurations.
- No order API imports.
- Clean deinitialization and instance-scoped cleanup.
- Same semantic ledger as the diagnostic and execution products.
