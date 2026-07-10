---
id: EXP0018-P11-25_RUNTIME_VALIDATION
title: "Runtime validation"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# Runtime validation

Compile with zero errors and warnings. Verify embedded tests pass. Confirm source pair count and zero unmatched timestamps. During replay, processed cursor count must increase monotonically. At completion, status must be COMPLETE, missed-close count should be zero, hashes must be nonempty, and CSV rows must reconcile with summary counts.
