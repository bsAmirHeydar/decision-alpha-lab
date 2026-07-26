# Valid Hook View Debug Checklist

Use this checklist when validating the production Hook view.

## Inputs

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02PrintSummary = true
InpHookPhase02ExportCsv = true
```

## CSV Fields

Check:

```text
valid_after_hook
valid_after_opposing_f3
valid_hook_family
hook_validity_family
previous_hook_sequence_id
previous_hook_terminal_node_id
```

## Expected Cases

### Hook After Opposing F3

- Hook is shown.
- No parent Hook is required.

### Hook After Hook

- Second Hook is shown.
- First Hook is shown only if it is referenced by `previous_hook_sequence_id`.

### Unqualified Hook

- Hidden in valid-only mode.
- Still available in CSV/audit when export is enabled.

## Common Failure

If only the second Hook is shown and the first Hook is missing, check whether:

```text
previous_hook_sequence_id >= 0
previous_hook_terminal_node_id == child.origin_node_id
parent.valid == true
parent.render_eligible == true
```
