# Level 06 STC SMT Candidate Engine

This document indexes the Level 06 implementation for EXEC001 STC SMT Cycles.

Level 06 converts raw touch-only previous-W hunts into audit-only SMT candidate rows.

It adds:

- high-side SMT candidate detection,
- low-side SMT candidate detection,
- clean-symbol trade mapping,
- same-check buy/sell forgetting,
- largest-stop reference selection using the clean symbol check close as the provisional entry proxy,
- candidate audit CSV output.

It still does not confirm, consume, trade, simulate, draw, partially close, or hard-close positions.

Primary detailed document:

`docs/operations/evidence/level_06_smt_candidate_engine/97fffdd7f422_27_level_06_smt_candidate_engine.md`
