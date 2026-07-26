---
id: EXP0018-P05-RUNTIME
title: "P05 Runtime Validation Guide"
project: EXP0018
phase: P05
status: implemented-awaiting-metaeditor-validation
---

# Runtime Validation

1. Compile with `0 errors, 0 warnings`.
2. Confirm embedded self-tests pass.
3. Confirm P04 has ready resolutions.
4. Inspect a known reference high and verify A/B states independently.
5. Verify exact equality counts as touch.
6. Verify missing second-symbol data becomes unavailable.
7. During an open period, verify a state can move from one-sided to both as new closed M1 bars arrive.
8. Confirm no chart objects or orders are created.
