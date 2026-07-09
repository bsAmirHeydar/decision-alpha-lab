# README — Hook Canon Step 6: Post-F3 Hook Recognition Doctrine

## Purpose

The MT5 chart review showed that F3 detection is acceptable, but the selected `F3H` Hook is not always the Hook that the doctrine intends.

The missing distinction is that **F3H is not one single shape**.

A post-F3 Hook can be:

- a direct Hook starting from the F3 terminal endpoint
- a delayed/rebound Hook formed after price reaches the F3 terminal side and then builds a Hook slightly away from it
- a fully structural Hook with confirmed Hook nodes and sequence labels
- a geometric 80% cycle Hook when a visible near-death semicircle exists but the structural sequence does not complete

## Files

- `docs/nds_hook_architecture/65_phase48_post_f3_hook_recognition_doctrine.md`
- `docs/obsidian_hook/00_mocs/HOOK_CANON_STEP6_POST_F3_MOC.md`
- `docs/obsidian_hook/01_concepts/*`
- `docs/obsidian_hook/02_policies/*`
- `docs/obsidian_hook/03_architecture/*`
- `docs/obsidian_hook/04_debug/*`
- `docs/obsidian_hook/06_examples/*`

## Scope

Documentation and Obsidian only.

No code, rendering, validity, F-counting, Rally logic, Zone logic, broker behavior, order sending, risk sizing, or live execution is changed.
