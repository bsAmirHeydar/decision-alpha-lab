# HOOK-CANON STEP 2 — Validity Determination Layer

This patch implements the second step of the canonical Hook rebuild.

Step 1 fixed the production visible set. Step 2 fixes the validity annotation layer that feeds that visible set.

The code now distinguishes between:

- structural Hook counting, which remains complete;
- valid Hook determination, which tags only canonical families;
- production rendering, which may show only those canonical families.

Canonical valid families:

1. Hook After Opposing F3
2. Hook After Hook

This patch changes code and documentation. It does not modify F-counting logic, Rally logic, execution logic, broker behavior, position management, order sending, or risk sizing.
