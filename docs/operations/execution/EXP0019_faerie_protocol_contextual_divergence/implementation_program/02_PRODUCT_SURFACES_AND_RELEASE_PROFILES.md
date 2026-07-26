---
title: "Product Surfaces and Release Profiles"
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
# Product Surfaces and Release Profiles

## Why multiple products exist

The context engine has one semantic responsibility, while each product has a separate authority boundary. The indicator explains and exposes the model. The diagnostic EA proves event parity and runtime health. The paper EA validates order geometry without broker risk. The live EA is a separately authorized product.

## Complete indicator product

The final indicator must provide:

- A/L/N session boxes and New York week boundaries;
- symbol-local reference highs/lows for all enabled relations;
- Hunter and Protected role markers;
- raw, confirmed, neutralized, invalidated, suppressed, and entry-eligible states;
- AL, AN, LN, NA, NL, NN, and WW labels;
- bullish/bearish direction and relation-specific styling;
- active WW direction, source week, age, and neutralization state;
- pair-session quota status and winning first signal;
- data coverage, synchronization, confirmation timeframe, and health diagnostics;
- historical replay for configured calendar-day/week depth;
- relation/direction/state filters;
- optional popup, sound, push, and email alerts with signal-ID deduplication;
- optional CSV/JSONL audit export;
- deterministic cleanup of objects owned by the indicator instance;
- no order placement.

## Indicator operating modes

| Mode | Purpose | Rendering |
|---|---|---|
| `AUDIT_FULL` | Research and debugging | All raw and suppressed states visible |
| `TRADING_CLEAN` | Daily discretionary use | Confirmed and relevant context emphasized |
| `WW_FOCUS` | Weekly context study | Weekly ranges, active WW, downstream alignment |
| `RELATION_FOCUS` | Isolate one or more relations | Only selected relations prominent |
| `DIAGNOSTIC` | Data/time/sync verification | Health overlays and reason codes |

## Diagnostic EA

The diagnostic EA owns no trade authority. It:

- runs the exact context engine outside indicator lifecycle constraints;
- records event and state snapshots;
- compares incremental processing with full replay;
- exports golden traces;
- provides high-volume test harnesses that would be inappropriate in an indicator.

## Paper EA

The paper EA adds:

- pair-global first-entry arbitration;
- quota reservation using an explicitly labelled temporary profile;
- stop/target geometry;
- SELL stop plus one spread;
- fixed-dollar risk sizing;
- synthetic broker responses and reconciliation.

It may not silently become live-capable.

## Live EA

The live EA is created only after:

- `FP-DEC-012` is owner-confirmed;
- paper execution is stable;
- broker retcodes, partial fills, pending orders, cancellation, and reconnect cases pass;
- authorization, kill switch, and circuit breaker modules are integrated;
- a micro-live release gate is approved.
