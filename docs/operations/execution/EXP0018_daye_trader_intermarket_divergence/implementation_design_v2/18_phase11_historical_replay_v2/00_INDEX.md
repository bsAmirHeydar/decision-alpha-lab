---
id: EXP0018-P11-00_INDEX
title: "EXP0018 Phase 11 — Deterministic Historical Replay v2"
project: EXP0018
phase: P11
status: implemented
tags: [exp0018, daye, phase11, replay]
---

# EXP0018 Phase 11 — Deterministic Historical Replay v2

This package reconstructs P01–P07 causally from closed historical bars. It uses exact UTC alignment, as-of period aggregation, the canonical 22-relationship registry, touch-only hunt classification, the same P06 confirmation reducers, and the same P07 lifecycle reducers. It exports immutable replay ledgers and deterministic hashes. No chart, trade, risk, network, or model authority exists.

## Reading order
1. Scope and authority
2. Replay clock and source range
3. Chronological reducer
4. Pipeline reuse
5. Confirmation and lifecycle equivalence
6. Determinism, outputs, tests, and handoff
