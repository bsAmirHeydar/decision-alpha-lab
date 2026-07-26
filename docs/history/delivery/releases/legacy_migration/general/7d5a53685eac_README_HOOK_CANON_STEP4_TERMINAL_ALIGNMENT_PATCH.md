# Hook Canon Step 4 — Terminal/Cycle Alignment Patch

## Purpose

Step 4 finalizes the split between:

1. **Structural terminal node** — used for Hook-after-Hook continuity.
2. **Raw terminal price/time** — used for the visible cycle arc endpoint.

The previous raw terminal promotion could extend the visual Hook cycle beyond the origin boundary because it scanned raw candle lows/highs after the crown without enforcing the user-defined living Hook terminal constraint.

## Canon implemented

Positive Hook:

```text
terminal = lowest raw low after crown while still above origin
```

Negative Hook:

```text
terminal = highest raw high after crown while still below origin
```

When the raw candle touches/crosses origin, terminal scanning stops. The cycle cannot extend past its own death boundary.

## Changed files

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh

docs/nds_hook_architecture/63_phase46_terminal_cycle_alignment_step4.md

docs/obsidian_hook/00_mocs/HOOK_CANON_STEP4_MOC.md
docs/obsidian_hook/02_policies/Hook Terminal Must Stay Inside Origin Boundary.md
docs/obsidian_hook/02_policies/Structural Terminal And Visual Terminal Are Separate.md
docs/obsidian_hook/03_architecture/Phase 46 Terminal Cycle Alignment.md
docs/obsidian_hook/04_debug/Terminal Cycle Alignment Debug Checklist.md
```

## Scope

Hook Phase 02 terminal/cycle alignment only.
No F-counting, Rally, Zone, execution, broker, risk, or live trading behavior is changed.
