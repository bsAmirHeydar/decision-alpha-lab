# F2 Waist Limit — Performance Contract

## Execution-only path

```text
closed bars
→ per-scale Phoenix node/F1/F2 builders
→ latest newly observable F2
→ broker request
```

The runtime does not call `FP_DetectAllScales`. Consequently it skips:

- F3 locking;
- global ownership passes;
- duplicate visual merging;
- Hook seed visibility;
- Level-11 canonical rendering checks;
- result recounting.

## FAST profile

```text
420 closed bars
scales 2, 3, 5
900 event cap
0 Hook cap
```

## PARITY profile

```text
2500 closed bars
scales 2, 3, 5, 8, 13, 21
4000 event cap
0 Hook cap
```

## Additional reductions

- once per new bar;
- no detector while exposure exists;
- no Print/PrintFormat path;
- no timing statistics;
- in-memory one-attempt registry;
- no terminal-global lock.
