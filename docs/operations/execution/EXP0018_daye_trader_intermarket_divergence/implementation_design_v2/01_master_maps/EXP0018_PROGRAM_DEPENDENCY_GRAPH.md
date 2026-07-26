  ---
  id: EXP0018-PROGRAM-DEPENDENCY-GRAPH-V2
  title: "EXP0018 Program Dependency Graph v2"
  type: architecture
  status: active
  project: EXP0018
  version: 2.0.0
  created: 2026-07-10
  updated: 2026-07-10
  tags:
    - exp0018
- daye-trader
- implementation-design
  ---

# گراف وابستگی برنامه

## قواعد

- P00 precedes all behavioral code.
- P01/P02/P03 sequential because time and data define period truth.
- P09 can branch after P03.
- P10 can branch after P01 but remains blocked by TWO decision.
- P14–P20 cannot be required by P00–P13.
- P20 is the only place where evidence may create a promotion candidate; even there human approval is mandatory.

## Critical path

```text
P00 → P01 → P02 → P03 → P04 → P05 → P06 → P07 → P08 → P11 → P12 → P13
```

## Parallel branches

```text
P03 → P09 → P11
P01 → P10 → P11
P13 → P14/P15/P16/P17/P18/P19 → P20
```
