---
id: EXP0018-P11-04_CHRONOLOGICAL_CURSOR
title: "Chronological cursor"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# Chronological cursor

The replay cursor advances one closed base-bar pair at a time. For cursor `i`, only source pairs `0..i` are visible. Every downstream snapshot is rebuilt as-of that cursor availability time. Future highs, lows, bars, host closes, reference breaches, and relationship states are inaccessible.
