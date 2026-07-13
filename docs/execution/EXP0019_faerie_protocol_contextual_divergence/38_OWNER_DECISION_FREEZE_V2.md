---
title: "38 - Owner Decision Freeze v2"
tags: [exp0019, faerie-protocol, contextual-divergence, obsidian]
status: normative
experiment: EXP0019
context_id: FP-CONTEXT-001
context_version: 2.0.0-doc-freeze
doc_version: 2.0.0
last_updated: 2026-07-13
language: en
---
# 38 - Owner Decision Freeze v2


## Decision-Set Identity

- **Decision set:** `FP-OWNER-DECISIONS-2026-07-13-V2`
- **Context:** `FP-CONTEXT-001`
- **Canonical documentation version:** `2.0.0-doc-freeze`
- **Owner response source:** fifteen option answers supplied in Persian on 2026-07-13
- **Frozen decisions:** 14
- **Open decisions:** 1 (`FP-DEC-012`)

## Exact Decision Mapping

| ID | Question | Owner Answer | Canonical Policy | Authority | Coding Consequence |
|---|---|---:|---|---|---|
| `FP-DEC-001` | N lookback counting | `A` | `CALENDAR_DAY_DEPTH` | `OWNER_CONFIRMED` | Count exact calendar-day offsets; weekends and missing-data days occupy offsets and are not replaced by older valid sessions. |
| `FP-DEC-002` | Reference reuse across later stages | `B` | `ALLOW_UNTIL_PROTECTED_TOUCH` | `OWNER_CONFIRMED` | A reference side remains eligible across later check windows until the protected symbol touches that same side; hunter touch alone does not globally consume it. |
| `FP-DEC-003` | Confirmation crossing session boundary | `B` | `STRICT_SAME_SESSION_CLOSE` | `OWNER_CONFIRMED` | The confirmation candle must close inside the owning check session; otherwise the candidate expires and is never transferred to the next session. |
| `FP-DEC-004` | First-sweep time authority | `A` | `M1_ONLY` | `OWNER_CONFIRMED` | Historical and live first-sweep ordering use M1 only; ticks do not change the canonical winner. |
| `FP-DEC-005` | Confirmation timeframe | `A` | `HOST_CHART_TIMEFRAME_RESOLVED_AT_INIT` | `OWNER_CONFIRMED` | Use the current chart timeframe, resolve it at initialization, and include the resolved timeframe in configuration and signal identity. |
| `FP-DEC-006` | Weekly window boundary | `B` | `NY_TRADING_WEEK_SUN_1800_TO_FRI_1700` | `OWNER_CONFIRMED` | Build weekly windows in America/New_York time from Sunday 18:00 inclusive to Friday 17:00 exclusive, DST-aware and broker-independent. |
| `FP-DEC-007` | WW lifecycle neutralization | `C` | `NEUTRALIZE_ON_SECOND_SYMBOL_TOUCH` | `OWNER_CONFIRMED` | A previously asymmetric weekly context becomes neutralized when the second symbol touches the corresponding weekly side; historical evidence is retained. |
| `FP-DEC-008` | WW tradeability | `B` | `WW_GATE_AND_TRADEABLE_SETUP` | `OWNER_CONFIRMED` | WW is both a directional gate for lower relations and an independently executable setup, subject to the same risk, quota, and geometry controls. |
| `FP-DEC-009` | No active WW behavior | `A` | `ALLOW_BOTH_DIRECTIONS_WHEN_NO_ACTIVE_WW` | `OWNER_CONFIRMED` | When weekly data is valid but no active WW exists, both directions are permitted. Missing weekly data remains a distinct fail-closed data state. |
| `FP-DEC-010` | Opposing WW conflict | `B` | `NEWEST_ACTIVE_CONFIRMED_WW_WINS` | `OWNER_CONFIRMED` | The most recently confirmed, still-active WW controls direction. Older opposite WW events remain in the ledger but are not the active gate. |
| `FP-DEC-011` | Session quota scope | `A` | `PAIR_GLOBAL_FIRST_ENTRY_PER_SESSION` | `OWNER_CONFIRMED` | Across the two symbols and all relations, only the first eligible entry in each A/L/N session may proceed. |
| `FP-DEC-012` | Quota consumption moment | `UNANSWERED` | `OPEN_QUOTA_CONSUMPTION_MOMENT` | `OPEN_DECISION` | Owner requested clarification. Detection, drawing, arbitration, and reservation can be implemented; permanent quota consumption for live execution must remain configurable or disabled until frozen. |
| `FP-DEC-013` | Simultaneous signal priority | `A` | `EARLIEST_HUNT_M1_TIME_WINS` | `OWNER_CONFIRMED` | The primary winner is the candidate with the earliest canonical M1 hunt time. Stable technical tie-breaks apply only when hunt timestamps are equal. |
| `FP-DEC-014` | SELL stop spread adjustment | `B` | `SELL_STOP_PLUS_ONE_SPREAD` | `OWNER_CONFIRMED` | For SELL trades, protective stop equals the raw structural stop plus one contemporaneous spread snapshot; risk sizing uses the adjusted stop distance. |
| `FP-DEC-015` | Suppressed signal drawing | `B` | `ALWAYS_DRAW_WITH_DISTINCT_STYLE` | `OWNER_CONFIRMED` | Signals suppressed by WW, quota, data state, or execution eligibility remain visible with distinct color/opacity/style and explicit reason codes. |


## Interpretation Notes

### Q7 - WW lifecycle

The selected answer `C` explicitly freezes **neutralization by second-symbol touch**. It does not independently specify whether activation is immediate or requires closed-candle confirmation. The architecture therefore applies the already-canonical candidate lifecycle:

```text
WW_RAW_ASYMMETRY
  -> WW_CONFIRMED on a closed host-chart candle while asymmetry persists
  -> WW_NEUTRALIZED when the second symbol touches the corresponding side
```

The neutralization rule is `OWNER_CONFIRMED`; use of the shared confirmation lifecycle is an `ARCHITECTURAL_DERIVATION` required for consistency with all other divergence relations.

### Q9 - no active WW

`ALLOW_BOTH_DIRECTIONS_WHEN_NO_ACTIVE_WW` applies only after the weekly data contract reports a complete, evaluable previous/current weekly pair. `WW_DATA_INCOMPLETE` is not equivalent to no WW and remains fail-closed for execution.

### Q10 - newest WW wins

"Newest" means the most recent **confirmed, active, non-neutralized** WW by `confirmation_close_time`. Ties are resolved by `first_hunt_m1_time`, relation-side enum, then signal ID. Older WW events remain visible and ledgered.

### Q11 and Q13 - first pair-global entry

The quota covers both symbols and every relation, including direct WW setups, within one A/L/N session. Primary ownership belongs to the earliest canonical M1 hunt. Technical tie-breaks do not express strategy preference; they exist only to guarantee deterministic arbitration.

### Q14 - SELL stop plus spread

One spread means exactly `ask - bid` in price units at the execution validation snapshot. The adjusted stop is included before risk sizing. Backtests require historical bid/ask or a versioned spread model.

## Open Decision

Only `FP-DEC-012` remains open. See [[39_QUOTA_CONSUMPTION_EXPLAINER_AND_OPEN_DECISION]]. Until it is frozen, the canonical live profile must reject initialization or disable order submission. Detection, drawing, paper plans, and quota reservation remain implementation-ready.

## Change Control

Any owner change to a frozen item creates:

1. a new decision-set version,
2. a new context configuration hash,
3. an impact report listing affected modules/tests,
4. a migration or namespace policy for historical signals,
5. a new patch manifest and commit.

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
