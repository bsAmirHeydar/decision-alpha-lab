# 58 — Valid Hook Rendering and Label Policy

## Status

Canonical production-view policy.

This document defines exactly what must be drawn when valid-only Hook mode is enabled.

---

# 1. Core policy

When valid-only Hook mode is enabled, the chart must show only valid Hook cycles.

```text
Valid-only view = valid Hook cycles only
```

A valid Hook cycle belongs to one of these families:

1. Hook After Opposing F3
2. Hook After Hook

If the valid Hook is Hook-2 in a Hook-after-Hook pair, Hook-1 must also be displayed as the parent companion.

---

# 2. Visible object set

The renderer must compute a final visible set before drawing anything.

```text
visible_hook_groups = valid_hooks + required_parent_companions
```

Only objects belonging to `visible_hook_groups` may be drawn.

This applies to all Hook-related object types:

- cycle arcs / semi-cycles;
- Hook envelopes;
- sequence labels;
- node labels;
- branch labels;
- origin/crown/terminal markers;
- any semantic Hook text;
- any debug-looking labels that could appear on the production chart.

---

# 3. Hook After Opposing F3 rendering

A Hook valid by the F3 rule should be drawn with full detail:

- cycle arc;
- sequence labels;
- node labels;
- origin/crown/terminal representation;
- family label.

Recommended label prefix:

```text
F3H
```

Example:

```text
F3H H123 B1:1
F3H H123 B1:2
F3H H123 B1:3
```

---

# 4. Hook After Hook rendering

When Hook-2 is valid by Hook-after-Hook:

```text
Render Hook-2 with full detail.
Render Hook-1 with full detail as parent companion.
```

Recommended label prefixes:

```text
HH     = valid Hook-after-Hook child
PARENT = required parent companion
```

Example:

```text
PARENT H122 B1:1
PARENT H122 B1:2
PARENT H122 B1:3

HH H123 B1:1
HH H123 B1:2
HH H123 B1:3
```

Hook-1 is shown because it explains Hook-2. It is not independently promoted into a valid production Hook unless it also satisfies one of the two validity families by itself.

---

# 5. What must be hidden

In valid-only mode, the renderer must not draw:

- structural Hook candidates that are not valid;
- raw Hook candidates;
- all-Hook sequence labels;
- Phase01 raw node labels unrelated to visible Hooks;
- Phase03/04/05/06 diagnostic overlays unless explicitly scoped to visible Hook groups;
- stale objects from previous runs;
- fallback structural Hooks;
- labels belonging to invalid Hook groups;
- cycle arcs belonging to invalid Hook groups.

If any invalid Hook label appears in valid-only mode, the renderer is leaking from a non-filtered path.

---

# 6. No fallback in production

If no valid Hook exists, valid-only production view draws nothing.

```text
valid_hooks.empty => no Hook objects on chart
```

This is correct behavior.

Debug fallback must not be enabled implicitly. If a developer needs to inspect structural Hooks, they must turn off valid-only mode or enable a separate debug view.

---

# 7. Color policy

Valid Hook families should be visually distinct.

Recommended distinction:

```text
Hook After Opposing F3  => F3H color family
Hook After Hook child   => HH color family
Parent companion        => muted companion color family
```

The precise RGB values are implementation details. The semantic requirement is that a user can distinguish:

- F3-origin valid Hooks;
- Hook-after-Hook valid child Hooks;
- parent companion Hooks.

---

# 8. Rendering pipeline

The correct renderer pipeline is:

```text
1. Clear stale Hook objects.
2. Build all structural Hook sequences internally.
3. Build origin-groups / cycles.
4. Assign validity family.
5. Build visible_hook_groups.
6. Draw only cycle arcs belonging to visible_hook_groups.
7. Draw only node labels belonging to visible_hook_groups.
8. Draw only sequence labels belonging to visible_hook_groups.
9. Draw nothing else.
```

Any path that draws labels directly from the full sequence array is incorrect in valid-only production mode.

---

# 9. Acceptance test

With valid-only enabled:

```text
InpHookPhase02ShowOnlyValidHooks = true
```

Expected behavior:

- If Hook after F3 exists: draw that Hook and its labels.
- If Hook after Hook exists: draw Hook-2 and Hook-1 parent companion with labels.
- If neither exists: draw nothing.
- No unrelated Hook labels should appear.
- No raw structural Hook grid should appear.
- No old labels should remain after timeframe changes or reattach.
