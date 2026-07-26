# Hook Sequence Debug Checklist

Use this checklist when the chart looks over-counted or under-counted.

## Numbering

- Positive Hook labels must be on valleys.
- Negative Hook labels must be on peaks.
- A sequence must not stop at 2 if later strict continuation nodes exist.
- A participated node must not become node 1 of another overlapping sequence.
- A participated node may still appear later as node 2/3/4.

## Visibility

- `InpHookPhase02ShowOnlyValidHooks=false` shows all render-eligible Hook sequences.
- `InpHookPhase02ShowOnlyValidHooks=true` shows only valid-family Hooks.

## Valid families

- Hook After Hook: previous terminal equals current origin.
- Hook After Opposing F3: opposite completed/locked F3 exists before Hook start.

## CSV audit

Turn on `InpHookPhase02ExportCsv=true` and inspect:

```text
hook_phase02_sequences.csv
hook_phase02_summary.csv
```

Important fields:

```text
x_count
resolve_node_id
valid_after_hook
valid_after_opposing_f3
valid_hook_family
hook_validity_family
seed_reuse_rejects
```
