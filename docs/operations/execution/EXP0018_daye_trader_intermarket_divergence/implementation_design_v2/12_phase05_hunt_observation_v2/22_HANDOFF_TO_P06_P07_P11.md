---
id: EXP0018-P05-HANDOFF
title: "P05 Handoff to P06 P07 P11"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# P06

Consumes P05 observations at each host-timeframe close and decides whether the final state is one-sided, double, none, or unavailable.

# P07

Consumes confirmed P06 events, not raw P05 candidates, to manage reference lifecycle and First Sweep policy.

# P11

Replays the same P05 classifier chronologically from historical snapshots. It must not invent a separate hunt formula.
