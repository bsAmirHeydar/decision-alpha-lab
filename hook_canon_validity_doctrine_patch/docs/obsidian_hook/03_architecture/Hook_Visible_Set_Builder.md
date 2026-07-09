# Hook Visible Set Builder

## Purpose

Build the final set of Hook groups that are allowed to appear on the chart.

## Pseudocode

```text
visible_hook_groups = {}

for hook in hook_groups:
    if hook.family == HOOK_AFTER_OPPOSING_F3:
        visible_hook_groups.add(hook)

    if hook.family == HOOK_AFTER_HOOK:
        visible_hook_groups.add(hook)
        visible_hook_groups.add(hook.parent)
        hook.parent.is_parent_companion = true
```

## Rule

All draw operations must check membership in `visible_hook_groups`.
