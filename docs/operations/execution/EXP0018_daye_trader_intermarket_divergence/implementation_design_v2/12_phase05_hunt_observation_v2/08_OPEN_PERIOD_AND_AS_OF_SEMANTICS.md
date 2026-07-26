---
id: EXP0018-P05-ASOF
title: "P05 Open Period and As-Of Semantics"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# As-Of Semantics

For an open current period, P05 reports the state **as of the latest closed base bar available to P03**. A state can evolve from `NONE` to `A_ONLY`, then to `BOTH` before the host confirmation candle closes.

P05 therefore records observation transitions but does not freeze a divergence. P06 owns the final host-close decision.
