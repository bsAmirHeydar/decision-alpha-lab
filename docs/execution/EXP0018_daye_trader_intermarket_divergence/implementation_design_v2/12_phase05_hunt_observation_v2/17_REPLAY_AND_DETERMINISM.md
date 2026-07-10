---
id: EXP0018-P05-REPLAY
title: "P05 Replay and Determinism"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# Replay

The classifier is pure with respect to a P04 resolution snapshot. The same current/reference OHLC produces the same facts and IDs.

P05 does **not** claim the exact first intraperiod touch timestamp from aggregate OHLC. Exact chronological first-touch reconstruction belongs to the future replay pipeline that feeds snapshots incrementally. This limitation is explicit rather than guessed.
