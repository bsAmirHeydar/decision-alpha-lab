# Hook Validity Determination Pipeline

## Pipeline

```text
Phase01 nodes
→ structural Hook sequences
→ Hook origin-groups / cycles
→ terminal semantics
→ validity family assignment
→ visible_hook_groups
→ filtered renderer
```

## Required separation

The renderer must never draw directly from all sequences in valid-only mode.

It must draw only from `visible_hook_groups`.
