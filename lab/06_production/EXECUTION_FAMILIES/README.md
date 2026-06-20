# Execution Families

This document summarizes the current execution families implied by the research.

---

## Reversal execution family

Purpose: capture reaction from structural zones.

Expected members:

- E0001 — reversal touch/limit execution,
- E0002 — close-confirmed market reversal execution.

Core rules:

- entry after valid regime is known,
- zone touch or close confirmation,
- zone-edge or structural invalidation stop,
- fixed R or first opposite zone target,
- same-bar stop-first policy unless tick data proves ordering.

Main risk:

- full structural reversal targets can be too ambitious,
- same-bar target/stop ambiguity can be high,
- costs can destroy small reaction edges.

---

## Continuation execution family

Purpose: capture larger path after structural break in continuation regime.

Expected members:

- E0003 — continuation close-hunt / Donchian / ATR trailing,
- E0004 — Heikin Ashi continuation flip,
- E0005 — close-break fixed-R continuation.

Core rules:

- entry after continuation regime is known,
- break trigger must be explicit,
- risk must be explicit: ATR, structural, fixed, or trailing,
- path and trading performance must be reported separately.

Main risk:

- continuation may go adverse before favorable,
- tight stops can kill the path edge,
- regime-change exits must use known-time rules.

---

## Family-level reporting

Every execution report should print at least:

- family,
- entry model,
- risk model,
- exit model,
- trades,
- win rate,
- average win R,
- average loss R,
- profit factor,
- expectancy,
- MFE/MAE,
- random or baseline comparison.
