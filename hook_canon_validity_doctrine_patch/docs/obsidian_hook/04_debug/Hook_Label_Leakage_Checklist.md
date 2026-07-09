# Hook Label Leakage Checklist

If invalid Hook labels still appear in valid-only mode, check these failure points.

## Possible leak sources

- label renderer loops over all sequences;
- node renderer loops over all Phase01 nodes;
- Phase03/04/05/06 overlays are still active;
- stale chart objects are not deleted;
- parent companion expansion accidentally includes all parents, not immediate required parent;
- structural fallback is still active.

## Required invariant

```text
label_hook_group_id in visible_hook_groups
```

If this is false, do not draw the label.
