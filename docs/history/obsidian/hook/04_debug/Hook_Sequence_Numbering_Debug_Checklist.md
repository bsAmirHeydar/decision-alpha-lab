# Hook Sequence Numbering Debug Checklist

Use this checklist when Hook numbers look wrong on the chart.

## Positive Hook

1. Extract the visible valley list old-to-new.
2. Start with the first unused valley.
3. It must be `1`.
4. Scan forward to the end.
5. Every lower unused valley must continue the same sequence as `2`, `3`, `4`, ... .
6. Those consumed valleys must not become `1` of another sequence.

## Negative Hook

1. Extract the visible peak list old-to-new.
2. Start with the first unused peak.
3. It must be `1`.
4. Scan forward to the end.
5. Every higher unused peak must continue the same sequence.
6. Those consumed peaks must not become `1` of another sequence.

## Failure signs

The builder is wrong if:

```text
A sequence stops at 2 while a valid 3 exists later.
A node used in one sequence appears as 1 in another sequence.
Multiple branches recut the same raw node list with different numbering.
```
