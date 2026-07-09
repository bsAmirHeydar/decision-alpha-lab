# Used Node Cannot Restart As One

## Policy

A node that participated in an earlier Hook sequence cannot become node `1` of a later sequence.

```text
participated_before(node) => cannot_seed_as_1
```

## Continuation exception

The same node may still appear as node `2`, `3`, `4`, etc. in a later sequence if the forward scan naturally reaches it.

```text
used node cannot restart
used node may continue
```
