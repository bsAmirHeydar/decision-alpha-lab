---
title: "Phase 55 — Exact Acceleration and Maximum-Speed Contract"
tags: [nds, hook, phase55, performance, strategy-tester, exact-acceleration]
status: implemented_reference_external_mt5_benchmark_pending
doc_version: 1.2.0
last_updated: 2026-07-16
---
# Exact Acceleration and Maximum-Speed Contract

## Problem

The PARITY tester intentionally owns 5000 closed bars and all eight canonical scales:

```text
2, 3, 5, 8, 13, 21, 34, 55
```

Before v1.2, every new bar rebuilt all of the following even when their outputs could not affect the current decision:

```text
Timebase
→ complete F1/F2/F3 graph
→ Phase01 nodes
→ Phase02 Hook sequences
→ Phase03 Y records
→ Phase04 closure records
→ 86.4 evidence
→ execution lifecycle
```

The same rebuild also occurred while an 86.4 pending order or fixed-1R position already owned the strategy. That work was deterministic but decision-irrelevant.

## Non-negotiable accuracy invariant

Exact acceleration does **not** change:

- requested bars;
- closed-bar-only semantics;
- scale list;
- node, Hook, F1/F2/F3, Phase03 or Phase04 thresholds;
- `x_count` authority;
- Phase04 50% closure authority;
- first-touch handling, including same-bar fail-closed behavior;
- tick model, spread, commission, order model, SL, TP or 1R geometry;
- one-attempt persistence or single-exposure ownership;
- new-bar invocation schedule.

No approximation, sampling, bar truncation, reduced scale set, future data, heuristic cache or relaxed gate is introduced.

## Acceleration layers

### 1. Broker-owned exposure fast path

Before loading 5000 bars, the tester inspects existing strategy exposure.

The complete structural stack is skipped only when the execution result is owned entirely by current broker state:

- managed pending order lifecycle;
- 86.4 fixed-R position with broker-attached SL/TP;
- managed position on another symbol;
- multiple-position invariant block;
- foreign-position guard;
- disabled strategy.

A same-symbol `TERMINAL_F123` position is not eligible for the complete broker-only fast path because its exit requires the canonical post-entry F3 event graph. It uses a narrower F-only path: Timebase and F detection run, while Phase01/02 Hook and Phase03/04 closure rebuilds are skipped because the open position no longer consumes entry structure.

### 2. Demand-driven F context

For a new 86.4 setup, Phase01/02 Hook truth is built first without the F graph. Phase02 already supplies canonical Hook-after-Hook ownership.

The expensive F1/F2/F3 graph is built only when at least one sequence:

- is structurally valid and alive;
- is confirmed and mature/capped;
- has `x_count ∈ {3,4}`;
- has valid crown-to-origin 86.4 geometry;
- is not already admitted by an enabled Hook-after-Hook family;
- could become executable only through canonical opposing-F3 ownership.

If no such sequence exists, F events cannot alter the executable candidate set and are deferred exactly.

### 3. Candidate-scoped Phase03/04

Phase03 and Phase04 receive only sequences that already pass all pre-closure hard gates. Phase04 can decide closure/death; it cannot repair an invalid Hook, missing crown, wrong node count, disabled family or invalid entry geometry.

`InpBTExactAcceleration=false` sends the complete Phase02 sequence set through Phase03/04 and remains the full reference path.

### 4. Indexed evidence access

Phase04 evidence now provides:

- an exact binary lower bound at `x_closure_time` before scanning first arrival;
- a `sequence_id` hint for common-case lookup;
- mandatory structural identity revalidation;
- full structural fallback when sequence indexes differ or collide.

`sequence_id` remains audit metadata, not authority.

### 5. Single-pass funnel and selection

The 86.4 execution core previously traversed all sequences once for the diagnostic funnel and again for latest-candidate selection, repeating evidence searches. v1.2 owns both outputs in one deterministic pass.

### 6. Parallel repository QA

The bounded Python/static commands are independent read-only processes. The runner executes them concurrently, captures every result, prints output in deterministic command order and never hides later failures through fail-fast cancellation.

Troubleshooting remains available through:

```powershell
python .\tools\flag_counting\run_nds_hook_864_cycle_r1_tests.py --serial
```

## Operator configuration

Maximum exact speed:

```text
InpBTProfile = PARITY
InpBTTradeProfile = HOOK_864_CYCLE_R1
InpBTExactAcceleration = true
```

Full reference comparison:

```text
InpBTProfile = PARITY
InpBTTradeProfile = HOOK_864_CYCLE_R1
InpBTExactAcceleration = false
```

The two runs must use the same symbol, timeframe, date interval, deposit, leverage, tick model and all remaining inputs.

## Performance telemetry

Every run reports:

```text
exposure_fast
exposure_reason
f_required
f_built
f_deferred
p04_scoped
p04_candidates
elapsed_us
```

The session summary aggregates exposure fast paths, F builds/deferments, candidate counts and runtime microseconds.

## Verification boundary

Repository QA proves source contracts and deterministic reference logic. It cannot measure the actual speedup of a specific MT5 agent, broker history or CPU. MetaEditor clean compilation and paired Strategy Tester benchmarks with `exact=true/false` remain external acceptance evidence.

## Rollback

Restore the v1.1.1 versions of the files listed in the v1.2 patch index, or revert the v1.2 commit. No data/schema migration is required.

## Paired parity benchmark

For auditable comparison, set `InpBTPrintEveryNRuns=1` and execute the same test twice: once with acceleration enabled and once disabled. Save both tester logs, then run:

```powershell
python .\tools\flag_counting\compare_nds_hook_864_acceleration_logs.py `
  ".\exact.log" `
  ".\reference.log" `
  --json ".\acceleration-parity.json"
```

The comparator requires equality of canonical action, status, setup key and Entry/SL/TP geometry for every printed run. Diagnostic funnel text and elapsed time may differ. Any decision or geometry mismatch returns a non-zero exit code.
