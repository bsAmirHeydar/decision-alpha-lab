---
type: strategy-factory-reference
status: canonical
title: "Setup, Entry, Stop, Exit, and Management Library Reference"
tags:
  - strategy-factory
  - setups
  - entry
  - exit
  - reference
---

# Setup, Entry, Stop, Exit, and Management Library Reference

## Library purpose

The setup library separates reusable execution hypotheses from market anatomy. An anatomy says what happened and where/when it matters. A setup says how exposure is initiated, invalidated, managed, and closed. The same setup can be tested across several anatomies through the canonical candidate interface.

## Entry families

### Immediate confirmation market

Enter at the first eligible quote/bar after confirmation. Highest fill and simplest causal baseline. Vulnerable to spread, slippage, and late confirmation. Required fields: confirmation time/price, side, expiry.

### Anatomy reference limit

Place at a canonical reference, zone edge, hook level, or reference open. Tests location-based optionality. Must specify touch/fill, gap, queue assumptions, and expiry. Report low fill and adverse selection.

### Fractional pullback

Entry at a predeclared fraction of a causal impulse. Define impulse start/end at decision time and fraction. Avoid scanning many fractions without trial accounting.

### Breakout stop

Enter beyond a known level plus tick/ATR offset. Tests continuation after acceptance. Requires gap behavior and stop-entry price semantics.

### First pullback after displacement

State machine: causal displacement confirmation → wait for first registered return to a declared area → fill/expire. “First” requires deterministic ownership and duplicate handling.

### Multi-stage scale-in

Several child intents share one event risk budget. Predeclare price levels and volume fractions. Aggregate risk cannot exceed the parent thesis cap.

## Stop families

### Exact anatomy invalidation

Preferred when the anatomy has a real failure boundary. It creates interpretable R and clean doctrine linkage.

### Reference extreme

Beyond a hunted high/low, structural node, zone boundary, or opposing hook. Include spread side and tick buffer.

### Volatility-buffered invalidation

`stop = invalidation -/+ ATR * buffer`. ATR window and known time are fixed. Test neighborhood stability.

### Time invalidation

Close when the event's informational horizon expires even if price stop is not hit. This may coexist with a hard disaster stop.

### Regime/state invalidation

Close when a causal state transition is confirmed. The transition known time must be explicit; no exit at the earlier price where the eventual transition began.

## Exit families

### Fixed R

Use 1R, 1.5R, 2R, or a bounded coarse set. This isolates entry/stop edge and forms the baseline.

### Structural target

Opposing node, liquidity reference, parent-zone boundary, cycle reference, or declared free-path objective. Target must be known at entry or updated through a causal policy.

### Time/cycle end

Close at current cycle end, session boundary, maximum holding time, or news cutoff. Timezone/DST is part of the policy.

### Trailing state

Trail behind confirmed nodes, hooks, ATR, channel, or state transitions. Every stop update is logged and tested on path replay.

### Partial plus runner

Close a fixed portion at a base target and manage the remainder with a declared runner policy. Report core and runner separately and include extra costs.

### Break-even

Move stop to entry or cost-adjusted entry only after a causal trigger. Treat as a distinct exit policy. It may increase win rate while reducing expectancy.

## Setup composites

A setup composite links an entry, stop, exit, expiry, and compatibility rules. It has its own version and tests. Example:

```json
{
  "setup_id": "first_pullback_structural_2r",
  "entry": "first_pullback_after_displacement",
  "stop": "anatomy_invalidation_atr_buffered",
  "exit": "fixed_2r",
  "expiry": "current_session",
  "required_features": ["displacement_end", "invalidation_price", "atr"]
}
```

## Candidate search discipline

Start with orthogonal families rather than dense parameters. First answer:

- Does immediate or pullback entry work better?
- Does structural or buffered risk survive?
- Is fixed, time, or structural exit the source of value?

Then refine only inside training and count every variant. Use multi-objective ranking, not highest mean alone.

## Setup-level metrics

- eligible event count
- fill rate and latency
- net expectancy and lower bound
- MFE/MAE and path quality
- cost share
- drawdown and tail share
- parameter-neighbor stability
- cross-anatomy transfer
- operational complexity and failure rate
- capacity

## Setup registry lifecycle

`DRAFT → FIXTURE_TESTED → RESEARCH_APPROVED → PAPER_APPROVED → LIVE_APPROVED → RETIRED`

A setup may be live-approved for one strategy and research-only for another because anatomy interaction matters. Global retirement occurs when fill assumptions or operational semantics are invalid.
