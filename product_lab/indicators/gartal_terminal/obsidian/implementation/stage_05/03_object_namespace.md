# Object Namespace

Stage 05 uses the existing prefix model:

```text
GT_DASH_       dashboard
GT_TL_         chart timeline
GT_TIMELINE_   bottom tape
GT_SHELL_      boot shell
GT_FATAL_      fatal init surface
```

## Cleanup Rule

`GT_ClearObjects(config.object_prefix)` remains the full cleanup authority. Dashboard objects should be overwritten by stable IDs, not duplicated each timer tick.
