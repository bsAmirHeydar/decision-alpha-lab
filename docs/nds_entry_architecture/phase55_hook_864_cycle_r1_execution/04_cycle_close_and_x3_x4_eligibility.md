# 04 — Cycle Close and X3/X4 Eligibility

## Gate order

The profile evaluates gates in a deterministic order:

1. validate exact profile configuration;
2. require canonical valid/nonfailed Hook family;
3. require existing HH or F3H family authorization;
4. require `FP_HookP02SequenceCycleClosed(seq)`;
5. require `seq.resolve_confirmed`;
6. require valid Crown;
7. require `seq.x_count` equal to 3 or 4;
8. require `MATURE` or `CAPPED` state;
9. require nonnegative canonical retracement;
10. compute 86.4 projection and verify it is inside Origin–Crown;
11. require the canonical Terminal not to have reached 86.4.

## Meaning of cycle closed

Phase 55 does not redefine cycle closure. It consumes the Hook Phase02 closure helper and adds the setup-specific confirmed-Terminal gate. This is intentionally stricter than merely observing three geometric turns.

## X3 and X4

- X3 may qualify when its confirmed Terminal exists and progress remains below 86.4.
- X4 may qualify under the same conditions.
- X2 is too early.
- X5 or later is outside the approved setup.
- Origin is structural boundary and not an X node.

## First-arrival interpretation

The intended phrase “when it is going to reach 86.4 and node count is three or four” is encoded as:

```text
canonical_terminal_retracement + epsilon < 0.864
```

If Terminal has already touched or crossed 86.4, placing a new limit at that price would be retrospective/late and is rejected.

## Selection behavior

The existing latest-eligible selector remains authoritative. Phase 55 does not rank Hooks by distance, score, or expected return. Existing family and recency semantics remain intact.
