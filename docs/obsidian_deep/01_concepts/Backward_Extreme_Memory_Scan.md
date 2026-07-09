# Backward Extreme Memory Scan

The scan walks backward from the newest previous cycle toward older cycles.

While walking backward it keeps memory of:

```text
highest high already seen
lowest low already seen
```

Only levels that push that memory outward are valid frontier references.
