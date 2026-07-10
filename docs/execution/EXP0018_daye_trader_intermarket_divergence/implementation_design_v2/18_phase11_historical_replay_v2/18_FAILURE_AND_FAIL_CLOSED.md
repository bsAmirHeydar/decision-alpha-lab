---
id: EXP0018-P11-18_FAILURE_AND_FAIL_CLOSED
title: "Failure and fail-closed behavior"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# Failure and fail-closed behavior

Invalid time ranges, auto broker offsets, insufficient history, unmatched timestamps, invalid OHLC, non-monotonic bars, registry corruption, host source gaps, duplicate identities, and I/O failures are explicit terminal or typed outcomes. The engine never converts unavailable evidence into clean/protected/no-hunt truth.
