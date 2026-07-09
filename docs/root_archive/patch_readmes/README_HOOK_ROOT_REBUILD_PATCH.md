# Hook Root Rebuild Patch

## What this fixes

- Removes premature Hook sequence termination at node 2.
- Prevents internal participant nodes from restarting as node 1.
- Keeps participant nodes eligible as continuation nodes.
- Adds Hook validity-family annotations.
- Adds `InpHookPhase02ShowOnlyValidHooks`.
- Updates Hook docs and Obsidian notes.

## Main input

```text
InpHookPhase02ShowOnlyValidHooks = false
```

Set it to `true` to hide unqualified Hook-like structures from the Phase 02 semantic view.
