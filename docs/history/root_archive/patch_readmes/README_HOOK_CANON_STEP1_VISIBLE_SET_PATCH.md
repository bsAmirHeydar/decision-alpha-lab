# Hook Canon Step 1 Visible Set Patch

## Purpose

This patch fixes the first rendering-layer problem: `show only valid hooks` must not draw all structural Hook sequences.

Previous behavior could still leak structural Hook rows because a valid sequence could expand into all same-origin group members or fallback to structural candidates.

## Changed file

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Visual.mqh
```

## Core changes

- Add `FP_HookP02SequenceIsProductionValidHook(...)`.
- In valid-only mode, select only:
  - `valid_after_opposing_f3`
  - `valid_after_hook`
- Keep Hook-after-Hook parent companion expansion.
- Disable same-origin group expansion in valid-only production view.
- Disable structural fallback in production valid-only view.

## What this does not do

This step does not change how a Hook becomes valid. It only ensures the renderer obeys the existing valid flags.

Next steps should implement the canonical validity determination itself:

- Hook after opposing F3 from the F3 terminal side.
- Hook-after-Hook where Hook-2 starts from the near-death terminal of Hook-1.
- Positive terminal = lowest valley above origin.
- Negative terminal = highest peak below origin.
