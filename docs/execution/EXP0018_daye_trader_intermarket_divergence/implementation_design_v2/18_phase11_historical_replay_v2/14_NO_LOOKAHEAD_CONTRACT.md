---
id: EXP0018-P11-14_NO_LOOKAHEAD_CONTRACT
title: "No-lookahead contract"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# No-lookahead contract

No stage receives bars after the cursor. Confirmation uses only observation states whose availability is at or before the host close. Lifecycle retirement uses only observations already published by the current cursor. The output includes event time, availability time, and processing time so causal violations can be audited.
