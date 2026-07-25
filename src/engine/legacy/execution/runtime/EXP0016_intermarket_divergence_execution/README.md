# EXP0016 Intermarket Divergence Execution

This experiment group contains execution models built on intermarket divergence.

The first execution model is:

- `EXEC001_STC_SMT_Cycles`

EXEC001 is now documented as a locked, layered, English specification. It is ready for research/paper implementation.

## Strategy folders

- `EXEC001_STC_SMT_Cycles/` - STC SMT cycle strategy from the provided SRS and owner clarifications.

## Common principles

Although the current implementation target is EXEC001 only, the folder is organized so future divergence execution strategies can reuse the same architectural ideas:

- Source SRS extraction.
- Normalized specification.
- Cycle calendar.
- Divergence rules.
- Execution and risk rules.
- Architecture plan.
- Test plan.
- Data model and journals.
- Visualization contract.
- Implementation checklist.

## Current build order

1. Finish documentation.
2. Build research/paper engine for EXEC001.
3. Validate deterministic test cases.
4. Add drawing/audit overlays.
5. Add paper live runtime.
6. Add auto-trade runtime only after validation.
