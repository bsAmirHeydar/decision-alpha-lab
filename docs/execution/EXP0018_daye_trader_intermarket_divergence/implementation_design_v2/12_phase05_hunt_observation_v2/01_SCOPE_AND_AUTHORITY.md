---
id: EXP0018-P05-SCOPE
title: "P05 Scope and Authority"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# Scope

P05 owns only the current-state observation of whether each symbol has touched its own reference high or reference low inside a P04 relationship context.

## P05 may

- compare symbol A current high with symbol A reference high;
- compare symbol B current high with symbol B reference high;
- compare symbol-local lows in the same manner;
- classify one-sided and double-touch states;
- assign factual Hunter/Protected roles when exactly one side touched;
- emit deterministic observations and audit events.

## P05 may not

- map HIGH/LOW to BUY/SELL;
- confirm at the host-chart candle close;
- retire or consume a reference;
- choose an entry, stop, target, or risk;
- draw a chart object;
- infer missing data as no touch.
