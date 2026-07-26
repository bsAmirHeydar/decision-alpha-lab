# Hotfix007 Validation Plan

## Test 1 — repeated divergence allowed while protected survives

1. Find a reference high.
2. Let Symbol A hunt the high.
3. Let Symbol B remain below its high reference.
4. Confirm a SELL divergence.
5. Let Symbol A create another one-sided high-hunt condition while Symbol B remains protected.

Expected: repeated divergence may still draw.

## Test 2 — protected breach retires reference

1. Continue from Test 1.
2. Let Symbol B finally hunt its reference high.
3. Continue forward.

Expected: the same high reference side must no longer produce new SELL divergence drawings.

## Test 3 — low-side symmetry

Repeat Tests 1 and 2 with low references.

Expected: same behavior for BUY-side low references.

## Test 4 — side independence

Retire the high side of a reference cycle.

Expected: the low side of that same cycle is not retired automatically.

## Test 5 — day reset

Move to the next 18:00 New York trading day.

Expected: lifecycle memory resets and previous-day references are not considered live decision references.
