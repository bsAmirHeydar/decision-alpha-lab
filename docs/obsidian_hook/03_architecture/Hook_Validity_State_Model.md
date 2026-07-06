---
type: architecture
title: Hook Validity State Model
status: canonical_draft
---
# Hook Validity State Model

```text
Raw Hook-Like Candidate
    ↓
Validity Gate
    ├── Hook After Hook?
    │       └── shared terminal-start node required
    ├── Hook After Opposing F3?
    │       └── opposing direction required
    └── otherwise invalid
    ↓
Valid Hook
    ↓
Hook Zone Candidate
    ↓
Zone Risk Contract Check
    ↓
Tradable Zone or Watch Zone
```

## States

- `raw_candidate`
- `valid_hook_after_hook`
- `valid_hook_after_opposing_f3`
- `invalid_fractal_hook`
- `hook_zone_candidate`
- `tradable_hook_zone`
- `watch_hook_zone`

## Design Goal

The state model prevents invalid hooks from contaminating the zone engine.
