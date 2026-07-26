---
id: EXP0018-P11-08_ONE_SIDED_TRANSITION_MEMORY
title: "One-sided transition memory"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# One-sided transition memory

Candidates open only when an observation transitions from non-one-sided to A_ONLY or B_ONLY. Repeated callbacks with unchanged evidence do not open another candidate. Observation identity, availability time, and pair-state transitions are retained between cursors.
