---
id: EXP0018-P04-HANDOFF
title: "P04 Handoff to P05, P06, and P11"
type: handoff-contract
status: active
project: EXP0018
phase: P04
---
# Handoff

P05 receives only READY relationship resolutions and reads symbol-local current/reference OHLC to build hunt facts. P06 receives P05 facts and confirmation-bar boundaries. P11 reuses the same registry and resolver in chronological replay.

P05 must not reconstruct the 22 relationships independently. P11 must not use a separate historical mapping table.
