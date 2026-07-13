---
title: "40 - Normative Algorithm Specification"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 40 - Normative Algorithm Specification


## End-to-End Algorithm

### Inputs

- Two-symbol pair descriptor.
- M1 historical/live data for both symbols.
- New York timezone conversion service.
- A/L/N session schedule and New York weekly schedule.
- Calendar-day N lookback depth.
- Resolved host chart confirmation timeframe.
- Seven-relation registry.
- Owner-decision set v2.
- Shared risk/execution services.

### Context Initialization

```text
1. Resolve PERIOD_CURRENT to a concrete timeframe.
2. Validate both symbols, point sizes, tick sizes, history access, and session definitions.
3. Build fp_context_manifest.v2.
4. Compute context_epoch_id from all identity-bearing fields.
5. Verify owner decision set and confirm quota consumption is set or live execution is disabled.
6. Initialize shared core adapters and FP-specific modules.
7. Backfill required M1 coverage and completed windows.
```

### Window Construction

```text
For each M1 close/event:
  a. Convert UTC/broker time to New York time.
  b. Assign trading_day_key and A/L/N session.
  c. Assign New York weekly interval.
  d. Update current symbol-local session and weekly ranges.
  e. Freeze completed windows with provenance hashes.
```

### Historical N Selection

```text
For offset d in [1..lookback_depth]:
  expected_date = current_trading_day_calendar_date - d calendar days
  expected_N = derive N interval for expected_date
  coverage = inspect M1 coverage
  if coverage != COMPLETE:
      emit skipped-offset evidence
      continue  // do not replace with older session
  else:
      expose N high and low references with offset d
```

### Candidate Detection

```text
For each enabled relation and reference side:
  scan canonical M1 contacts for both symbols
  if exactly one symbol has contacted:
      create candidate at first_hunt_m1_time
  if both contact in same M1:
      emit SYMMETRIC_SAME_M1; no ordered candidate
  if second symbol contacts before confirmation:
      cancel candidate
```

### Confirmation

```text
confirmation_tf = resolved host chart timeframe
candidate_session = check-window A/L/N session
confirmation_bar = first eligible closed bar
if confirmation_bar.close_time >= candidate_session.end:
    expire CONFIRMATION_DEADLINE_MISSED
else if asymmetry and data remain valid:
    confirm signal
else:
    cancel with exact reason
```

### Weekly Context

```text
Build previous completed NY week references.
Detect current-week one-sided M1 touch.
Confirm WW using host chart close while asymmetry persists.
If second symbol later touches the same weekly side:
    append WW_NEUTRALIZED.
Active gate = newest confirmed, active, non-neutralized WW.
If no active WW and weekly data complete:
    allow both directions.
```

### Eligibility and Arbitration

```text
raw confirmed signal
  -> relation execution enabled?
  -> data complete?
  -> WW direction compatible or no active WW?
  -> risk/geometry valid?
  -> session quota available?
  -> compare first_hunt_m1_time against all session contenders
  -> reserve pair-session quota for earliest winner
```

### SELL Stop

```text
raw_stop = structural stop from setup
if direction == SELL:
    adjusted_stop = raw_stop + one spread_snapshot
else:
    adjusted_stop = raw_stop
risk_distance = abs(entry - adjusted_stop)
volume = shared_risk_core(risk_amount, risk_distance, symbol_geometry)
```

### Drawing

Every raw/confirmed/suppressed/neutralized outcome is projected to chart. Suppressed states use distinct style and reason code; they are never silently hidden.

## Technical Tie-Break Order

When `first_hunt_m1_time` is equal:

1. earliest `confirmation_close_time`,
2. relation code canonical order (`AL`, `AN`, `LN`, `NA`, `NL`, `NN`, `WW`) only as a technical stable order,
3. direction enum,
4. hunter symbol canonical order,
5. signal ID lexical order.

This tie-break has no quality meaning and must not be used as a performance ranking.

## Fail-Closed Conditions

- Unresolved New York time or DST.
- Missing pair data for required observation.
- Incomplete source reference.
- Unknown relation or reason code.
- Confirmation outside owning session.
- Weekly data incomplete when WW gate is required.
- Invalid spread snapshot for SELL.
- Unset quota consumption in live profile.
- Ledger or identity collision.

## Authority Classification

| Classification | Meaning |
|---|---|
| `OWNER_CONFIRMED` | Explicitly selected by the owner in the 15-question decision response. |
| `SOURCE_CONFIRMED` | Directly present in the original Faerie Protocol source package or owner narrative. |
| `ARCHITECTURAL_DERIVATION` | Required to make the confirmed behavior deterministic, modular, testable, or compatible with shared cores. |
| `LEGACY_OBSERVATION` | Behavior observed in `FP 101.mq5`; not automatically canonical. |
| `OPEN_DECISION` | Must not be silently hard-coded. |

Canonical priority is: `OWNER_CONFIRMED` > `SOURCE_CONFIRMED` > reviewed `ARCHITECTURAL_DERIVATION` > `LEGACY_OBSERVATION`.

## Navigation

- [[00_EXP0019_MOC|EXP0019 Master MOC]]
- [[38_OWNER_DECISION_FREEZE_V2|Owner Decision Freeze v2]]
- [[33_AMBIGUITY_AND_DECISION_REGISTER|Decision Register]]
- [[40_NORMATIVE_ALGORITHM_SPECIFICATION|Normative Algorithm Specification]]
- [[44_ACCEPTANCE_GATE_FOR_CODING|Acceptance Gate for Coding]]
