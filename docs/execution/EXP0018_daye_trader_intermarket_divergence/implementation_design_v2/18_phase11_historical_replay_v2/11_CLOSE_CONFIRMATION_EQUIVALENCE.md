---
id: EXP0018-P11-11_CLOSE_CONFIRMATION_EQUIVALENCE
title: "Close confirmation equivalence"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# Close confirmation equivalence

P11 calls `DAYE_InitializeConfirmationCandidate`, `DAYE_UpdateConfirmationCandidate`, and `DAYE_FinalizeCandidateAtClose`. The possible immutable outcomes are CONFIRMED, INVALIDATED_DOUBLE_HUNT, NO_SIGNAL_AT_CLOSE, UNAVAILABLE_AT_CLOSE, INVALIDATED_ROLE_CHANGED, and MISSED_CLOSE_REPLAY_REQUIRED. In a correct replay, closes are processed causally and missed-close outcomes should remain zero.
