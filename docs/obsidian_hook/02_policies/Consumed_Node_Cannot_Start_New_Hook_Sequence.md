# Consumed Node Cannot Start New Hook Sequence

A raw same-side node that already participated in a canonical Hook sequence cannot later become node `1` of another overlapping sequence.

This is a hard policy.

Allowed:

```text
unused raw node -> node 1 of new sequence
```

Not allowed:

```text
node used as 2/3/4 in prior sequence -> node 1 of later sequence
```

Hook-after-Hook exception:

```text
previous terminal = next Hook origin
```

The shared node may become the next Hook origin, but not node `1` of the next internal sequence.
