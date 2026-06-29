# Flag Counting Level 19 — Phase 7 Left-Upper Panel and Section Toggles

## Purpose

Phase 7 keeps the Level 19 State Gate read-only and improves usability.

The objective is not to add entry logic. The objective is to make the State Gate visible, readable, and debuggable while preserving the locked Node / Hook / ND / F-counting engines.

## What changed

Phase 7 introduces four usability changes:

1. The panel defaults to the **left-upper** chart corner instead of the right-upper corner.
2. The panel still supports a **master minimize / restore** button.
3. Each timeframe block supports its own **section minimize / restore** button.
4. Inside every expanded timeframe block, the **Rally** subsection and the **Hook** subsection each have their own minimize / restore toggle.

This means the State Gate can be inspected progressively:

- whole dashboard collapsed or expanded
- M1 / M10 / H1 blocks collapsed or expanded independently
- Rally lines collapsed or expanded independently
- Hook lines collapsed or expanded independently

## Locked boundaries

Phase 7 must not modify any of these engines:

- Node Engine
- Hook / ND Engine
- Flag Body Engine
- Internal Count Engine
- F1 Lifecycle Engine
- F2 Lifecycle Engine
- F3 Lifecycle Engine
- Ownership / Canonicalization
- Renderer
- Validation
- Release
- License

The panel only renders existing State Gate snapshot data.

## Inputs

The Phase 7 defaults are:

```text
InpStateGatePanelCorner          = CORNER_LEFT_UPPER
InpStateGatePanelX               = 16
InpStateGatePanelY               = 24
InpStateGatePanelForceRightUpper = false
```

If the user still wants the panel on the right side, they can set:

```text
InpStateGatePanelCorner          = CORNER_RIGHT_UPPER
```

or force it with:

```text
InpStateGatePanelForceRightUpper = true
```

## Chart interactions

### Master panel button

The title bar keeps a `+` / `-` button that collapses or expands the entire dashboard.

### Timeframe buttons

Each timeframe block has its own main toggle:

- `+` means the timeframe block is collapsed
- `-` means the timeframe block is expanded

### Subsection buttons

Each expanded timeframe block shows:

- `R+` / `R-` for the Rally subsection
- `H+` / `H-` for the Hook subsection

## Rendering rules

- A collapsed timeframe block still shows its header line.
- An expanded timeframe block shows tracker, optional counts, optional contract key, Rally header, Rally preview rows, Hook header, and Hook preview rows.
- If preview limits are smaller than the stored rows, the panel shows a `more rows in CSV` line.

## Why this matters

The State Gate is supposed to become a bridge from anatomy to future entry logic.

That bridge cannot be designed well if the dashboard is hidden, off-screen, or too dense to inspect. Phase 7 solves the visibility problem without changing the market-anatomy engines.

## Files touched

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
mql5/Include/FlagCountingPhoenix/FP_StateGatePanel.mqh
docs/flag_counting/FLAG_COUNTING_LEVEL_19_PHASE7_LEFT_PANEL_SECTION_TOGGLES.md
```

## Status

Phase 7 remains **context-only**.

It improves human inspection and debugging, but it does not produce entry permission, entry geometry, or trade decisions.
