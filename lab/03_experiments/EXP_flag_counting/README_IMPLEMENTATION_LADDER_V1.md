# Flag Counting Implementation Ladder V1

The Phoenix implementation ladder lives under:

```text
docs/flag_counting/implementation_ladder_v1/
```

Use it together with the current canon:

```text
docs/flag_counting/FLAG_COUNTING_CURRENT_CANON.md
```

The experiment rule is:

```text
Do not patch Hook, F lifecycle, ownership, canonicalization, audit/export, and renderer in one pass.
```

Current implementation order:

```text
L00 governance/canon
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
L11 canonicalization/audit decisions
L11.5 raw audit export/report
L12 renderer
L13 validation
L14 release/rollback
L15 interface contracts
L16 acceptance matrix
L17 resolved decisions
```

A patch must declare the highest layer it touches and provide acceptance evidence for that layer.
