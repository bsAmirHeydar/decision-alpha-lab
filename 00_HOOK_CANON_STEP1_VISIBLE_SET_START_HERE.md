# HOOK-CANON STEP 1 — Valid Visible Set

This patch is the first implementation step after the canonical Hook validity doctrine.

It does **not** redesign Hook counting and does **not** change F-counting, Rally logic, execution, risk, broker behavior, or Zone logic.

Step 1 scope:

- Build the production visible set only from valid Hook families.
- Keep Hook counting complete internally.
- Prevent structural/debug Hook siblings from leaking into valid-only view.
- Prevent structural fallback from drawing when production valid-only mode is active.
- Keep Hook-after-Hook parent companion display.

Canonical production-visible families:

1. Immediate Hook After Opposing F3
2. Hook-2 After Hook-1
3. Hook-1 only as parent companion of a visible Hook-2

In production valid-only mode, no other Hook cycles, node labels, or sequence labels should be drawn.
