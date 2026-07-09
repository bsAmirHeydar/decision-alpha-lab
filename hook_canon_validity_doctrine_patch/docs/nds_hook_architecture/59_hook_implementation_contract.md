# 59 — Hook Implementation Contract

## Status

Implementation contract for the next MQL5 patch.

This document translates the Hook Canon into code-level requirements without prescribing exact function names.

---

# 1. Required data model

Each Hook origin-group / cycle should expose at least these fields:

```text
hook_group_id
kind                         // positive or negative
origin_node_id
origin_time
origin_price
crown_time
crown_price
structural_terminal_node_id
structural_terminal_time
structural_terminal_price
cycle_terminal_time
cycle_terminal_price
sequence_ids[]
member_node_ids[]
validity_family
parent_hook_group_id
is_parent_companion
is_visible_in_valid_only
```

## 1.1 Terminal separation

There must be a clear distinction between:

```text
structural_terminal_node_id
cycle_terminal_price/time
```

The structural terminal is used for Hook-after-Hook continuity.  
The cycle terminal price/time is used for drawing the arc to the observed terminal extreme.

---

# 2. Sequence builder requirements

The sequence builder must:

1. Build positive sequences from valleys old-to-new.
2. Build negative sequences from peaks old-to-new.
3. Select node `1` only from nodes that have not participated before.
4. Continue scanning forward to the end of the raw list.
5. Add strict lower valleys for positive sequences.
6. Add strict higher peaks for negative sequences.
7. Prevent used nodes from restarting as node `1`.
8. Allow used nodes as later continuation nodes if reached naturally.
9. Preserve true terminal information beyond the fourth displayed label.

---

# 3. Validity assignment requirements

Validity must be assigned after structural Hook groups are built.

## 3.1 Hook After Opposing F3

A Hook group is valid by F3 when:

```text
latest opposing F3 context exists
hook origin is born from the F3 terminal area
hook kind is opposite to F3 direction
```

The F3 may continue extending after it forms. The matching logic must not require the F3 to be permanently finished in a simplistic way.

## 3.2 Hook After Hook

A Hook group is valid by Hook-after-Hook when:

```text
hook.kind == parent.kind
hook.origin is born from parent terminal/death-near endpoint
parent cycle is closed/completed structurally
```

The parent Hook does not have to be independently valid. It must be a completed structural parent.

---

# 4. Visible set construction

Before drawing, build:

```text
visible_hook_groups = []
```

Pseudo-contract:

```text
for each hook_group:
    if hook_group.validity_family == HOOK_AFTER_OPPOSING_F3:
        mark_visible(hook_group)

    if hook_group.validity_family == HOOK_AFTER_HOOK:
        mark_visible(hook_group)
        mark_visible(hook_group.parent_hook_group)
        hook_group.parent_hook_group.is_parent_companion = true
```

If valid-only is enabled and `visible_hook_groups` is empty, draw nothing.

---

# 5. Renderer requirements

The renderer must never draw directly from the full sequence list in valid-only mode.

Every draw operation must pass this check:

```text
object_hook_group_id in visible_hook_groups
```

This applies to:

- cycle arcs;
- labels;
- nodes;
- branch text;
- origin markers;
- crown markers;
- terminal markers.

---

# 6. Inputs

Recommended input contract:

```text
InpHookPhase02ShowOnlyValidHooks = true/false
```

When true:

```text
production valid-only view is active
```

No implicit structural fallback should occur.

Optional debug input may be added later, but not as part of production valid-only behavior.

---

# 7. Regression tests

## 7.1 Valid-only no fallback

When no valid Hook exists:

```text
expected_drawn_hook_objects = 0
```

## 7.2 F3 Hook

Given:

```text
Bullish F3 terminal environment
Negative Hook born from terminal side
```

Expected:

```text
negative Hook drawn with F3H family
only its nodes/labels drawn
```

## 7.3 Hook after Hook

Given:

```text
positive Hook-1 completed
positive Hook-2 origin born from Hook-1 terminal/death-near endpoint
```

Expected:

```text
Hook-2 drawn as HH
Hook-1 drawn as PARENT
both with full details
all other Hooks hidden
```

## 7.4 Label leakage

If an invalid Hook sequence label appears while valid-only is true, the patch fails.

## 7.5 Stale object cleanup

After changing timeframe or reattaching the expert, old invalid Hook objects must not remain.

---

# 8. Out of scope

The following are out of scope for the next implementation patch:

- Hook zone generation;
- trade entry;
- risk sizing;
- profit management;
- order execution;
- F-counting canonical definitions;
- Rally logic.

This contract is only for Hook validity, Hook cycle rendering, Hook node labels, and Hook sequence labels.
