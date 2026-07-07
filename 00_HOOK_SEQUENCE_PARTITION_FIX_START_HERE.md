# Hook Sequence Partition Fix — Start Here

This patch fixes the Hook Phase 02 sequence-numbering doctrine.

The previous implementation could enumerate overlapping branch candidates and allow a raw same-side node to appear as part of one sequence and then later seed another sequence as `1`. That made Hook labels look fractal, noisy, and non-canonical.

The corrected doctrine is:

```text
Raw same-side nodes are partitioned old-to-new into canonical Hook sequences.
A consumed node cannot become node 1 of a later sequence.
A sequence must be extended to its maximal valid continuation before a new sequence is started.
```

For a positive Hook, the raw list is the ordered valley list:

```text
valley[0], valley[1], valley[2], ...
```

The first unused valley becomes node `1`; the engine then scans forward to the end of the raw list and appends every strictly lower unused valley as `2`, `3`, `4`, ... .

For a negative Hook, the same logic is applied to ordered peaks, except every accepted continuation must be strictly higher.

Start reading:

```text
docs/nds_hook_architecture/46_phase34_hook_sequence_greedy_partition_ownership.md
docs/obsidian_hook/00_mocs/HOOK_LIFECYCLE_MOC.md
```
