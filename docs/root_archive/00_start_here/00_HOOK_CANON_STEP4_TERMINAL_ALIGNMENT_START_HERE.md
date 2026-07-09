# HOOK CANON STEP 4 — Terminal and Cycle Alignment

This patch implements the fourth step of the canonical Hook doctrine.

It does **not** change Hook sequence construction, Hook family validity, F-counting, order execution, position management, or risk sizing.

It aligns the raw terminal used for Hook cycle drawing with the canonical terminal rule:

- Positive Hook terminal = the lowest raw price reached after the crown while still above the Hook origin.
- Negative Hook terminal = the highest raw price reached after the crown while still below the Hook origin.
- If raw price touches/crosses the origin boundary, terminal scanning stops there.

The structural terminal node remains the continuity anchor for Hook-after-Hook.
Raw terminal price/time remain the visual endpoint for the cycle arc.

Start reading:

- `docs/nds_hook_architecture/63_phase46_terminal_cycle_alignment_step4.md`
- `docs/obsidian_hook/00_mocs/HOOK_CANON_STEP4_MOC.md`
