# Phase 44 — Canonical Validity Determination Step 2

## Intent

This phase converts the Hook Canon into executable validity annotation. Hook counting remains complete. Validity is not allowed to suppress structural counting. It only tags which Hook families are production-valid.

## Valid Family 1 — Hook After Opposing F3

A Hook is valid after F3 when it starts from the terminal side of the latest relevant opposing F3.

The implementation uses the following test:

1. The event must be F3.
2. The F3 must be completed or locked.
3. The Hook must be opposite in direction to the F3.
4. The Hook origin must match one of the F3 terminal endpoints.
5. The earliest structural Hook satisfying this terminal-start condition is selected for that F3.

The terminal endpoint test checks the F3 endpoints in terminal priority:

1. extension end
2. confirm node
3. leg2 node

The endpoint price must match the Hook origin price within a small platform-point tolerance. Time may lag due to confirmation mechanics, but the origin must not occur before the endpoint.

## Valid Family 2 — Hook After Hook

Hook-2 is valid after Hook-1 when:

1. Hook-1 has a closed structural cycle.
2. Hook-2 has the same Hook genus as Hook-1.
3. Hook-2 origin node id equals Hook-1 structural terminal node id.

Genus currently means same Hook direction.

Raw terminal price/time is used for cycle drawing. Structural terminal node id is used for Hook-after-Hook ownership and continuity.

## Parent Companion

Hook-1 is displayed only when required by a valid Hook-2. Hook-1 is not promoted into a valid Hook by itself. It is a parent companion.

## Inputs

The canonical direction requirement is enforced by code. `InpHookPhase02ValidF3RequireOppositeDirection` defaults to true to reflect the doctrine.

Scale matching remains configurable:

```text
InpHookPhase02ValidF3RequireSameScale = false
```

Scale is not part of genus. It is only a research strictness filter.

## Non-Goals

This phase does not change:

- sequence construction;
- raw terminal rendering;
- valid-only visible set selection;
- F-counting logic;
- zone generation;
- execution.
