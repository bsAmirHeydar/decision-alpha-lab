# NDS Hook 86.4 — No-Trade Diagnostic Funnel

## Purpose

Use this note when Strategy Tester completes with zero orders. Do not loosen setup rules before identifying the first zero counter.

## Required tester

```text
Expert: NDSHookLimitF123Backtest
InpBTTradeProfile: HOOK_864_CYCLE_R1
InpBTProfile: PARITY
InpBTPrintRunSummary: true
InpBTSendTesterOrders: true
```

The dedicated tester defaults to these values after Phase 55 v1.1. The central Phoenix expert uses a different input name and remains disabled by default.

## Funnel

```text
total
→ canonical
→ family
→ allowed
→ confirmed
→ crown
→ x34
→ mature
→ p04
→ closed
→ alive
→ untouched
→ ready
```

### `no_phase02_sequences`

The selected symbol, timeframe, history window, detector scales, or Hook configuration generated no canonical sequence. Confirm history synchronization and run PARITY before changing doctrine.

### `no_valid_hook_family`

Sequences exist but none satisfy the existing valid HH/F3H family semantics. Inspect Phase02 reports rather than bypassing family validity.

### `no_x3_or_x4_sequence`

Valid families exist but the canonical X count never reached 3 or 4 in the scanned window. Origin is not counted.

### `phase04_evidence_missing`

Phase03/04 did not publish a matching record. Check Phase03 Y availability, Phase04 engine enablement, exact symbol/timeframe context, and sequence identity.

### `phase04_x_not_closed`

A matching Phase04 record exists but the canonical 50% closure has not occurred. This is not an execution error.

### `all_closed_cycles_dead_by_origin_return`

Closure existed, but the origin-return death boundary invalidated every candidate before entry.

### `first_864_arrival_already_consumed`

The 86.4 level was touched on or after the closure candle before the system could place a new first-arrival order. Same-candle closure/touch is deliberately included.

### `runtime_contract_rejected`

All visible funnel gates passed, but an exact identity/config/evidence check rejected the candidate. Read the detailed run reason and MQL5 self-test output.

### `ready_candidate_exists` but no order

The setup layer found a candidate. Inspect downstream gates:

- send authority disabled;
- paper-only action;
- one-attempt registry already consumed;
- managed pending/position exists;
- foreign same-symbol position;
- entry is on the wrong side of Bid/Ask;
- broker stop/freeze distance;
- lot/risk/margin failure;
- unsupported pending/SL/TP capability;
- market/session/account trade restriction.

## Session summary

At test end, review:

```text
no_candidate_runs
ready_runs
paper_ready
limits_sent
pending_held
position_held
cancelled
blocked
p04_closed_total
p04_evidence_total
untouched864_total
```

A zero `limits_sent` is only meaningful when compared with these counters.

## Related

- [[NDS Hook 86.4 Cycle R1 Entry Contract]]
- [[NDS Hook 86.4 Cycle R1 State Machine]]
- [[NDS Hook 86.4 Cycle R1 Operator Checklist]]


## Offline log analysis

```powershell
python .\tools\flag_counting\analyze_nds_hook_864_tester_log.py .\tester-journal.log
```

The output is JSON and does not change the terminal, repository, order state, or setup registry.
