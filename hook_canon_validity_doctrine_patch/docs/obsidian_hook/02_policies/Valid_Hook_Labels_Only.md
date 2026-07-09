# Valid Hook Labels Only

## Policy

In valid-only mode, labels must be drawn only for visible Hook groups.

```text
label_hook_group_id must be in visible_hook_groups
```

This includes:

- sequence labels;
- node labels;
- branch labels;
- Hook ID labels;
- origin/crown/terminal labels.

## Failure condition

If a label belonging to an invalid Hook appears in valid-only mode, the renderer is leaking from an unfiltered draw path.
