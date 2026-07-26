# Article — Reversal vs Continuation Execution

## Abstract

Reversal and continuation are not two names for the same edge. They describe different market behaviors and require different execution logic.

This article summarizes the execution lessons learned from H0005.

---

## Reversal is a reaction problem

A reversal setup asks whether a structural zone can create a reaction when price revisits it.

Important properties:

- entry is usually a zone touch,
- the edge may be short-lived,
- full structural targets can be too ambitious,
- same-bar target/stop ambiguity can be high on larger timeframes,
- costs and fill price matter heavily.

A reversal report must therefore include:

- touch-based entry,
- zone-edge or structural invalidation stop,
- fixed R or first-opposite-zone target,
- same-bar policy,
- spread-aware entry/stop.

A structural path report may show that zones react. It does not prove that a reversal EA is profitable.

---

## Continuation is a path problem

A continuation setup asks whether a broken structural state can produce a larger path.

Important properties:

- entry may require close-break, intrabar-break, Donchian break, or another trigger,
- price may first move against the trade before the larger path appears,
- tight stops may destroy the edge,
- trailing logic can be more natural than fixed close targets,
- regime-change exit is only valid after the change is knowable.

A continuation report must therefore include:

- explicit break trigger,
- explicit risk denominator,
- ATR/structural/trailing stop mode,
- optional fixed R target,
- separate MFE/MAE path analysis.

---

## Why old continuation PF was not enough

The old H5 continuation report used a structural distance as the R denominator but did not execute a real initial stop. The result was a useful path-normalized statistic, not a real trading PF.

The correct interpretation is:

- continuation showed large directional paths,
- but its tradable R must be recalculated with an executable stop.

---

## Recommended execution split

### Reversal family

- E0001: touch/limit reversal,
- E0002: close-confirmed market reversal,
- target: R1, R2, first opposite zone,
- key validation: stop-aware reaction edge.

### Continuation family

- E0003: continuation close-hunt / Donchian / trailing family,
- E0004: Heikin Ashi continuation flip,
- E0005: close-break fixed-R continuation,
- key validation: path quality under explicit risk.

---

## Final rule

Never combine reversal and continuation into one headline unless the report also prints the two families separately.

The two families answer different questions:

- Reversal: does the zone react?
- Continuation: does the market continue with enough path quality to survive real risk?
