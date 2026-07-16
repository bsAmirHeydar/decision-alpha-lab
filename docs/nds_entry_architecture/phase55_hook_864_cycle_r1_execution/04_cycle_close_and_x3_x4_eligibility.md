# 04 — Cycle Close and X3/X4 Eligibility

## Gate order

The profile evaluates two authoritative layers.

### Phase02 intrinsic layer

1. exact profile configuration;
2. canonical valid/nonfailed Hook family;
3. existing HH or F3H family authorization;
4. Phase02 terminal availability through `FP_HookP02SequenceCycleClosed(seq)`;
5. confirmed terminal;
6. valid Crown and Origin;
7. canonical `x_count` exactly 3 or 4;
8. `MATURE` or `CAPPED` state;
9. 86.4 projection inside Origin–Crown.

### Phase04 runtime layer

10. exact matching Phase04 evidence record;
11. valid Phase04 record and closure candidate;
12. canonical 50% `x_closed` lifecycle state;
13. no origin-return death;
14. matching x-count 3 or 4;
15. no closed-bar 86.4 touch at or after closure;
16. existing execution/broker/risk gates.

## Meaning of cycle closed

Phase02 and Phase04 answer different questions:

- Phase02 terminal availability proves the canonical sequence has reached a usable terminal state.
- Phase04 `x_closed` proves the X cycle has closed according to the existing Y-reference and 50% closure engine.

Phase 55 consumes both. It does not recalculate nodes, Y extremes, closure, or death.

## X3 and X4

- X3 may qualify after canonical Phase04 closure.
- X4 may qualify under the same rules.
- X2 is too early.
- X5 or later is outside the approved setup.
- Origin is structural boundary and is not counted as an X node.
- x3→x4 retains one Hook identity, one attempt and no automatic reprice.

## First-arrival interpretation

The first-arrival gate is based on actual closed price travel after Phase04 closure, not `seq.retracement_ratio`.

```text
Positive Hook: first low <= Entry
Negative Hook: first high >= Entry
scan starts at Phase04 closure candle
```

The closure candle is included. If closure and 86.4 happen in the same closed candle, a new limit would be temporally retrospective and is rejected.

## Selection behavior

The existing latest-eligible selector remains authoritative. Phase 55 does not rank Hooks by distance, score, or expected return. Existing family, identity, recency, one-exposure and broker semantics remain intact.
