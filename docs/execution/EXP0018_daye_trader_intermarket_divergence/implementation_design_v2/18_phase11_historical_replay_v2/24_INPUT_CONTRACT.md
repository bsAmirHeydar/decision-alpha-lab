---
id: EXP0018-P11-24_INPUT_CONTRACT
title: "Input contract"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# Input contract

Critical inputs are broker symbols, canonical symbols, New York replay boundaries, base timeframe, host timeframe, fixed broker offset, exact-alignment policy, lifecycle policy, capacities, chunk size, and output prefix. Weekly remains disabled. Confirmation and lifecycle checkpoints are disabled because replay owns its complete chronological state.
