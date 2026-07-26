---
id: EXP0018-P11-15_CHUNKED_EXECUTION
title: "Chunked execution"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# Chunked execution

Replay runs from `OnTimer` in bounded cursor chunks. Chunk size changes latency only; it must not change identities, outcomes, hashes, or lifecycle state. Re-running from cursor zero is the canonical recovery policy. P11 v2 intentionally does not restore partial in-memory state from an incomplete run.
