# Phase 34 — Hook Sequence Partition Guard

## Code

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh
```

## Changed behavior

The Phase 02 builder now partitions raw nodes old-to-new instead of enumerating overlapping end-backward branches.

## Engine flow

```text
collect direction/scale nodes
initialize consumed[]
for each raw node old-to-new:
    if consumed: skip
    start sequence at this node as 1
    scan to end of raw list
    append stricter unused continuation nodes
    mark accepted nodes consumed
    emit one canonical sequence
```

## Purpose

The guard prevents:

- premature termination at node `2`;
- overlapping sequence starts;
- reused raw nodes becoming new `1` labels;
- branch explosion caused by fractal recutting of the same raw node list.
