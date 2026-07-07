# Greedy Hook Sequence Partition

A Hook sequence is built from a raw same-side node list.

Positive Hook:

```text
raw list = valleys old-to-new
```

Negative Hook:

```text
raw list = peaks old-to-new
```

The first unused raw node becomes node `1`. The engine then scans forward to the end of the raw list and appends every stricter unused continuation node.

Positive continuation:

```text
next valley must be lower than the last accepted valley
```

Negative continuation:

```text
next peak must be higher than the last accepted peak
```

The sequence is maximal: it does not stop at `2` if `3` or `4` exists later.

Related:

- [[Consumed_Node_Cannot_Start_New_Hook_Sequence]]
- [[Phase_34_Hook_Sequence_Partition_Guard]]
