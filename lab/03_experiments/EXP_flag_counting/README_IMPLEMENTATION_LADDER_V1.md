# Flag Counting Implementation Ladder V1

The Phoenix implementation ladder has been added under:

```text
docs/flag_counting/implementation_ladder_v1/
```

Use this ladder before any further Phoenix code patch.

The experiment rule is:

```text
Do not patch Hook, F lifecycle, ownership, canonicalization, and renderer in one pass.
```

Next work should proceed by layer:

```text
L01 candle/index foundation
L02 nodes
L03 identity
L04 Hook/ND context
L05 flag body
L06 internal count
L07 F1
L08 F2
L09 F3
L10 sequence ownership
L11 canonicalization/audit
L12 renderer
L13 validation
L14 release/rollback
```

A patch must declare the highest layer it touches and provide acceptance evidence for that layer.
